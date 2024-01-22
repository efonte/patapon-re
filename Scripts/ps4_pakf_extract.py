# Script by efonte, thanks to mrmemmo_ for the lz4 information

import concurrent.futures
from pathlib import Path
from struct import unpack

import lz4.block
import numpy as np
from PIL import Image

PAKF_PATH = Path("./texreplace.pak")


class DecompressionError(Exception):
    def __init__(self, message, img_name):
        self.message = message
        self.img_name = img_name
        super().__init__(message)


def decompress_lz4_img(
    data: bytes, img_name: str, width: int, height: int, decompress_size: int
):
    try:
        decompressed_data = lz4.block.decompress(
            data, uncompressed_size=decompress_size
        )
        numpy_array = np.frombuffer(decompressed_data, dtype=np.uint8).reshape(
            (height, width, 4)
        )
    except Exception as e:
        raise DecompressionError(str(e), img_name)
    img = Image.fromarray(numpy_array)
    output_path = PAKF_PATH.parent.joinpath(PAKF_PATH.stem).joinpath(
        img_name.replace(".lz4", ".png")
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(output_path)


def extract_pakf():
    infile = open(PAKF_PATH, "rb")

    magic = unpack("8s", infile.read(8))[0].decode("ansi").rstrip("\x00")
    if magic != "PAKF":
        raise Exception(f"Expected PAKF header. Found {magic}")

    num_entries = unpack("I", infile.read(4))[0]
    print(f"{num_entries=}")

    padding1 = infile.read(4)
    if padding1 != b"\x00" * 4:
        raise Exception(f"Expected padding. Found {padding1!r}")

    entries = []

    for i in range(num_entries):
        name = unpack("64s", infile.read(64))[0].decode("ansi").rstrip("\x00")
        width, height, size, decompress_size = unpack("4I", infile.read(16))
        entries.append((name, size, width, height, decompress_size))

    out_path = Path("./").joinpath(PAKF_PATH.stem)
    out_path.mkdir(parents=True, exist_ok=True)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for name, size, width, height, decompress_size in entries:
            compressed_data = infile.read(size)
            future = executor.submit(
                decompress_lz4_img,
                compressed_data,
                name,
                width,
                height,
                decompress_size,
            )
            futures.append(future)

        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except DecompressionError as e:
                print(
                    f"An error occurred during image decompression for file {e.img_name}: {e.message}"
                )


extract_pakf()
