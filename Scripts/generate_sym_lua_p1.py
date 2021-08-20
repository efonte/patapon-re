import re
from rich import print

functions = {}
for file_path in [
    "./Patapon_Remastered_v1.00_CUSA06171_UCUS98711_features.lua",
    "./Patapon_Remastered_v1.00_CUSA06171_UCUS98711_patches.lua",
    "./Patapon_Remastered_v1.00_CUSA06171_UCUS98711_trophies.lua",
]:
    with open(file_path, "r", encoding="utf-8") as infile:
        for line in infile.readlines():
            if m := re.match(
                r".*AddHook\(0x(?P<address>.{7}), 0x.{8}, H\d+\)\s+-- (?P<func_name>.+)",
                line,
            ):
                func_name = m.group("func_name")
                if func_name[0] == "(" and func_name[-1] == ")":
                    # (Labo::Bases__Camp__SoundGame__Bean__Game__updatePlayShineup - Fah Zakpon's)
                    func_name = func_name[1:-1]
                func_name = func_name.split("\t", maxsplit=1)[0].strip()
                func_name = func_name.split(" ", maxsplit=1)[0].strip()
                functions[int(m.group("address"), 16)] = func_name.replace("__", "::")
            elif m := re.match(
                r".*axFuncReplace\(0x(?P<address>.{7}), \"(?P<func_name>.+)\"(, 0x.{7})?\)",
                line,
            ):
                functions[int(m.group("address"), 16)] = "ps4__" + m.group(
                    "func_name"
                ).replace("__", "::")


# p1 usa - addresses obtained manually, thanks to owocek
p1_usa_functions = """"""
for line in p1_usa_functions.splitlines():
    address, func_name = line.split(" ")
    address = int(address, 16)
    functions[address] = func_name.replace("__", "::")

# p1 usa - function names obtained based on ghidra decompiled code, thanks to owocek
p1_usa_custom_functions = """"""
for line in p1_usa_custom_functions.splitlines():
    address, func_name = line.split(" ")
    address = int(address, 16)
    functions[address] = "custom__" + func_name.replace("__", "::")


print(functions)
print(len(functions))
# exit()


outfile = open(
    "./ppsspp_p1_UCUS98711_566_(pac)_39_(lua)_and_custom_func_names.sym", "w"
)
with open("./ppsspp_p1_UCUS98711_566_func_names.sym", "r") as infile:
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
        if not func_name_ori.startswith("z_un") and func_name.startswith("ps4__"):
            outfile.write(f"{func_address:08X} {func_name_ori},{func_size:04X}\n")
        else:
            outfile.write(f"{func_address:08X} {func_name},{func_size:04X}\n")
        # if func_name_ori.startswith("z_un"):
        #     outfile.write(f"{func_address:08X} {func_name},{func_size:04X}\n")
        # else:
        #     outfile.write(f"{func_address:08X} {func_name_ori},{func_size:04X}\n")

# for func_address, func_name in functions.items():
#     if func_name == "dummy":
#         continue
#     outfile.write(f"{func_address:08X} {func_name},0004\n")
