import os
from struct import unpack

from rich import print


def read_string(infile) -> str:
    string = unpack("4s", infile.read(4))[0].decode()
    while string[-1] != "\x00":
        string += unpack("4s", infile.read(4))[0].decode()
    return string.rstrip("\x00")


# with open("RAMp1.dump", "rb") as infile:
# with open("RAMp3_UCJP00125.dump", "rb") as infile:
# with open("RAMp3_UCJP00133.dump", "rb") as infile:
with open("RAMp3_UCJP00135.dump", "rb") as infile:
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
                padding1, padding2, offset = unpack("3I", infile.read(12))
                infile.seek(-12, os.SEEK_CUR)
                func_names = {}
                while padding1 == 0 and padding2 == 0xFFFFFFFF:
                    padding1, padding2, offset = unpack("3I", infile.read(12))
                    func_name = read_string(infile)
                    func_names[func_name] = (-1, offset)
                    # print(f"{padding1=:04X} {padding2=:08X} {offset=:08X} {func_name=}")
                    padding1, padding2, offset = unpack("3I", infile.read(12))
                    infile.seek(-12, os.SEEK_CUR)

                # print(func_names)
                func_list.append(func_names)
                # exit()
    # print(len(func_list))


# with open("p1_eur_functions_dump.txt", "w", encoding="utf-8") as outfile:
# with open("p3_UCJP00125_functions_dump.txt", "w", encoding="utf-8") as outfile:
# with open("p3_UCJP00133_functions_dump.txt", "w", encoding="utf-8") as outfile:
with open("p3_UCJP00135_functions_dump.txt", "w", encoding="utf-8") as outfile:
    category = 0
    for i, func_names in enumerate(func_list):
        if len(func_names) == 0:
            continue
        # outfile.write(f"{category:02X};0000;null\n")
        # outfile.write(f"unk{category}, 0x0000, 0x0, null\n")
        id_count = 0
        outfile.write(f"unk{category}, unk{id_count}, 0x0, null\n")
        for func_name, (id, offset) in func_names.items():
            id_count += 1
            # outfile.write(f"{category:02X};{id:04X};{offset:08X};{func_name}\n")
            # outfile.write(f"0x{category:02x}, 0x{id:04x}, 0x{offset:x}, {func_name}\n")
            # outfile.write(f"unk{category}, 0x{id:04x}, 0x{offset:x}, {func_name}\n")
            outfile.write(f"unk{category}, unk{id_count}, 0x{offset:x}, {func_name}\n")
        category += 1
