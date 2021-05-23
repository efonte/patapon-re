import subprocess
import os
from pathlib import Path
import zlib
import gzinfo
from concurrent.futures import ThreadPoolExecutor
from struct import unpack
from rich import print
from rich.progress import track

FNULL = open(os.devnull, "w")


def bndrepacker_call(
    file_path: Path,
    bndrepacker_path: Path = Path("./BNDRePacker1_1-beta4.4/BNDRePackerCMD.exe"),
) -> int:
    return_code = subprocess.call(
        f'"{bndrepacker_path.absolute()}" "{file_path.absolute()}"',
        stdout=FNULL,
        stderr=FNULL,
        shell=False,
    )
    return return_code


def extract_bnd(file_path: Path):
    # print(f'Extracting "{file_path}"')
    return_code = bndrepacker_call(file_path)
    if return_code == 0:
        for j, sub_file in enumerate(
            file_path.parent.joinpath(f"@{file_path.stem}").glob("unknown_*")
        ):
            with open(sub_file, "rb") as infile:
                data = infile.read()
            if data[0:4] == b"BND\x00":
                extension = ".bnd"
            elif data[0:4].startswith(b"TWS"):
                extension = ".tws"
            elif data[0:11] == b"XXG.01.0OMG":
                extension = ".gxx"
            elif data[0:11] == b"XXG.01.0MIG":
                extension = ".gxt"
            else:
                # print(data[0:11])
                # exit()
                extension = ".dat"
            sub_file.rename(
                sub_file.with_stem(f"{file_path.stem}_{j}").with_suffix(extension)
            )
        file_path.unlink()  # remove
    else:
        print(f'Error extracting "{file_path}"')
        exit()


def extract_helper(folder_path: Path):
    executor = ThreadPoolExecutor(max_workers=6)

    for file_path in track(list(folder_path.glob("**/*")), description="Processing..."):
        if file_path.is_dir():
            continue
        if file_path.name == "datams.hed":
            continue
        if file_path.parent.joinpath(f"@{file_path.stem}").is_dir():
            file_path.unlink()  # remove
            continue
        # print(file_path)
        with open(file_path, "rb") as infile:
            data = infile.read()
        if data[0:4].startswith(b"\x1F\x8B"):
            data = zlib.decompress(data, 16 + zlib.MAX_WBITS)
            info = gzinfo.read_gz_info(file_path)
            if info.fname == str(file_path):
                file_path_new = file_path
            else:
                file_path_new = file_path.with_name(info.fname.lower())
            if file_path.parent.joinpath(f"@{file_path_new.stem}").exists():
                print(f'Error. "{file_path_new}" already exists')
                exit()
            if file_path_new.name == "default.bnd":
                file_path_new = file_path
            with open(file_path_new, "wb") as outfile:
                outfile.write(data)
            if file_path != file_path_new:
                file_path.unlink()  # remove
            file_path = file_path_new

        if data[0:4] == b"BND\x00":
            # extract_bnd(file_path)
            executor.submit(extract_bnd, file_path)


# rename gxt extensions
def change_gxt_extensions(folder_path: Path):
    for i, file_path in enumerate(folder_path.glob("**/*")):
        if file_path.is_dir():
            continue
        # print(file_path)
        with open(file_path, "rb") as infile:
            data = infile.read()
        if data[0:11] == b"XXG.01.0MIG" and file_path.suffix != ".gxt":
            file_path_new = file_path.with_suffix(".gxt")
            print(f"{file_path.name} -> {file_path_new.name}")
            file_path.rename(file_path_new)
            # exit()


# rename gxt files using the real name
def change_gxt_names(folder_path: Path):
    for i, file_path in enumerate(folder_path.glob("**/*.gxt")):
        # print(file_path)
        with open(file_path, "rb") as infile:
            infile.seek(-0x7C, os.SEEK_END)
            name_offset = unpack("I", infile.read(4))[0]
            infile.seek(name_offset)
            name_bytes = infile.read()
            name = (
                unpack(f"{len(name_bytes)}s", name_bytes)[0]
                .decode("utf-8")
                .rstrip("\x00")
            )
            # print(name)
        file_path_new = file_path.with_stem(name)
        if file_path != file_path_new:
            if file_path_new.is_file():
                print(f'Error. File "{file_path_new}" already exists')
                exit()
            elif file_path.with_suffix(".gxx").is_file():
                print(f'Error. Model "{file_path.with_suffix(".gxx")}" exists')
                # rename model too
                exit()
            else:
                print(f"{file_path.name} -> {file_path_new.name}")
                file_path.rename(file_path_new)
                # exit()


# TODO remove empty folders



# file_path = Path("./p1_UCES00995_DATA_CMN.BND")
# file_path = Path("./p1_UCJP00125_DATA_CMN.BND")
# file_path = Path("./p1_UCJP00133_DATA_CMN.BND")
# file_path = Path("./p1_UCJP00135_DATA_CMN.BND")
# file_path = Path("./p2_UCES01177_DATA_CMN.BND")
# file_path = Path("./p3_UCES01421_DATA_CMN.BND")
# file_path = Path("./p3_UCJX90031_DATA_CMN.BND")
file_path = Path("./p3_NPJG90088_DATA_CMN.BND")
# file_path = Path("./p3_NPJG90088_DATAMS.BND")
# bndrepacker_call(file_path)
# exit()

# folder_path = Path("./@p1_UCES00995_DATA_CMN")
# folder_path = Path("./@p1_UCJP00125_DATA_CMN")
# folder_path = Path("./@p1_UCJP00133_DATA_CMN")
# folder_path = Path("./@p1_UCJP00135_DATA_CMN")
# folder_path = Path("./@p2_UCES01177_DATA_CMN")
# folder_path = Path("./@p3_UCES01421_DATA_CMN")
# folder_path = Path("./@p3_UCES01421_DATAMS")
# folder_path = Path("./@p3_UCJX90031_DATA_CMN")
# folder_path = Path("./@p3_UCJX90031_DATAMS")
# folder_path = Path("./@p3_NPJG90088_DATA_CMN")
folder_path = Path("./@p3_NPJG90088_DATAMS")

# extract_helper(folder_path)
# exit()

# change_gxt_extensions(folder_path)
# exit()

# change_gxt_names(folder_path)
# exit()
