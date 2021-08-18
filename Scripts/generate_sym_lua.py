import re
from rich import print

functions = {}
for file_path in ["./UCUS98732_features.lua", "./UCUS98732_patches.lua"]:
    with open(file_path, "r", encoding="utf-8") as infile:
        for line in infile.readlines():
            if m := re.match(
                r".*AddHook\(0x(?P<address>.{7}), 0x.{8}, H\d+\)\s+-- (?P<func_name>.+)",
                line,
            ):
                functions[int(m.group("address"), 16)] = m.group("func_name")
            elif m := re.match(
                r".*axFuncReplace\(0x(?P<address>.{7}), \"(?P<func_name>.+)\"(, 0x.{7})?\)",
                line,
            ):
                functions[int(m.group("address"), 16)] = "ps4__" + m.group("func_name")


print(functions)
print(len(functions))
# exit()


outfile = open("./ppsspp_p2_usa_732_(pac)_and_30_(lua)_func_names.sym", "w")
with open("./ppsspp_p2_usa_732_func_names.sym", "r") as infile:
    for line in infile.readlines():
        func, func_size = line.rstrip("\n").split(",")
        func_size = int(func_size, 16)
        # print(func)
        func_address, func_name = func.split(" ", maxsplit=1)
        func_address = int(func_address, 16)
        func_name_ori = func_name
        try:
            func_name = functions[func_address]
            functions.pop(func_address)
        except KeyError:
            # continue
            pass
        # outfile.write(f"{func_address:08X} {func_name},{func_size:04X}\n")
        if func_name_ori.startswith("z_un"):
            outfile.write(f"{func_address:08X} {func_name},{func_size:04X}\n")
        else:
            outfile.write(f"{func_address:08X} {func_name_ori},{func_size:04X}\n")

# for func_address, func_name in functions.items():
#     if func_name == "dummy":
#         continue
#     outfile.write(f"{func_address:08X} {func_name},0004\n")
