functions = {}
# with open("./[P3][EUR] - PAC Instruction Dump new.txt", "r") as infile:
# with open("./p2_eur_functions_dump.txt", "r") as infile:
# with open("./p1_eur_functions_dump.txt", "r") as infile:
with open("./p2_usa_functions_dump.txt", "r") as infile:
    for line in infile.readlines():
        _, _, func_address, func_name = line.rstrip("\n").split(", ")
        func_address = int(func_address[2:], 16)
        if func_address == 0 and func_name == "null":
            continue
        functions[func_address] = func_name
        # print(f"{func_address:08X}, {func_name}")


# outfile = open("./ppsspp_p3_eur_913_func_names.sym", "w")
# outfile = open("./ppsspp_p2_eur_732_func_names.sym", "w")
# outfile = open("./ppsspp_p1_eur_566_func_names.sym", "w")
outfile = open("./ppsspp_p2_usa_732_func_names.sym", "w")
# with open("./p3_eur.sym", "r") as infile:
# with open("./p2_eur.sym", "r") as infile:
# with open("./p1_eur.sym", "r") as infile:
with open("./p2_usa.sym", "r") as infile:
    for line in infile.readlines():
        func, func_size = line.rstrip("\n").split(",")
        func_size = int(func_size, 16)
        # print(func)
        func_address, func_name = func.split(" ", maxsplit=1)
        func_address = int(func_address, 16)
        try:
            func_name = functions[func_address]
            functions.pop(func_address)
        except KeyError:
            continue
            # pass
        outfile.write(f"{func_address:08X} {func_name},{func_size:04X}\n")

for func_address, func_name in functions.items():
    if func_name == "dummy":
        continue
    outfile.write(f"{func_address:08X} {func_name},0004\n")
