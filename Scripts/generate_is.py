functions = {}
outfile = open("./instruction_set.csv", "w")
with open("./[P3] - PAC Instruction Dump.txt", "r") as infile:
    for line in infile.readlines():
        func_id, func_subid, func_address, func_name = line.rstrip("\n").split(", ")
        if "unk" in func_id:
            continue
        func_id = int(func_id[2:], 16)
        func_subid = int(func_subid[2:], 16)
        func_address = int(func_address[2:], 16)
        if func_address == 0 and func_name == "null":
            continue
        functions[func_address] = func_name
        outfile.write(
            f"{func_id:02X};{func_subid:04X};{func_name};Unk;Unk;-1;\n"
            # f"{func_id:02X} {func_subid:02X};{func_name};Unk;Unk;-1;Unk1: str\n"
            # f"{func_id:02X} {func_subid:02X};{func_name};Unk;Unk;-1;Unk1: uint\n"
        )

# outfile.close()
# outfile = open("./instruction_set.csv", "w")
# with open("./instruction_set1.csv", "r") as infile:
#     for line in infile.readlines():
#         # 00 0E;00_0E;Unk;Unk;12;Unk1: uint, Unk2: uint, Unk3: uint
#         func_type, func_name, title, desc, size, types = line.rstrip("\n").split(";")
#         func_id, func_subid = func_type.split(" ")
#         func_id = int(func_id, 16)
#         func_subid = int(func_subid, 16)
#         outfile.write(
#             f"{func_id:02X};{func_subid:04X};{func_name};{title};{desc};{size};{types};\n"
#         )