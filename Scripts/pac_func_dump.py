import os
from pathlib import Path
from struct import unpack
from typing import Dict, List, Tuple
from rich import print


def read_string(infile) -> str:
    string = unpack("4s", infile.read(4))[0].decode()
    while string[-1] != "\x00":
        string += unpack("4s", infile.read(4))[0].decode()
    return string.rstrip("\x00")


def get_func_name(infile) -> Dict[str, Tuple]:
    func_names = {}
    padding = unpack("4B", infile.read(4))
    offset = infile.tell() - 4
    infile.seek(offset)
    while padding != (0, 0, 0, 0):
        try:
            func_name = read_string(infile)
        except UnicodeDecodeError:
            infile.seek(offset)
            break
        # func_names.append(func_name)
        func_names[func_name] = ()
        padding = unpack("4B", infile.read(4))
        offset = infile.tell() - 4
        infile.seek(offset)
    return func_names


with open("RAMp2_usa.dump", "rb") as infile:
    infile.seek(0, os.SEEK_END)
    last_offset = infile.tell()
    infile.seek(0)
    func_list = []
    # while infile.tell() < 0x7911BC:
    while infile.tell() < last_offset:
        # category = unpack("8s", infile.read(8))[0].decode().rstrip("\x00")
        category = unpack("4B", infile.read(4))

        if category == (0x6E, 0x75, 0x6C, 0x6C):
            padding = unpack("4B", infile.read(4))
            if padding == (0, 0, 0, 0):
                print(f"Category Offset: {infile.tell()-8:08X}")
                # print(read_string(infile))
                func_names = get_func_name(infile)
                # print(func_names)
                infile.seek(0x10, os.SEEK_CUR)
                # print(infile.tell())
                for func_name, value in func_names.items():
                    offset1, id, padding1, padding2, offset2 = unpack(
                        "5I", infile.read(20)
                    )
                    # print(
                    #     f"{func_name=} {offset1=:08X} {id=:04X} {padding1=:08X} {padding2=:08X} {offset2=:08X}"
                    # )
                    func_names[func_name] = (id, offset2)
                print(func_names)
                func_list.append(func_names)
                # exit()
    # print(len(func_list))


with open("p2_usa_functions_dump.txt", "w", encoding="utf-8") as outfile:
    category = 0
    for i, func_names in enumerate(func_list):
        if len(func_names) == 0:
            continue
        # outfile.write(f"{category:02X};0000;null\n")
        outfile.write(f"unk{category}, 0x0000, 0x0, null\n")
        for func_name, (id, offset) in func_names.items():
            # outfile.write(f"{category:02X};{id:04X};{offset:08X};{func_name}\n")
            # outfile.write(f"0x{category:02x}, 0x{id:04x}, 0x{offset:x}, {func_name}\n")
            outfile.write(f"unk{category}, 0x{id:04x}, 0x{offset:x}, {func_name}\n")
        category += 1
