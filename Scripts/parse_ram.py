from typing import Dict, List, Tuple
from rich import print
from pathlib import Path


def get_functions(sym_path: str) -> Dict[int, Tuple[str, int]]:
    functions = {}
    with open(sym_path, "r") as infile:
        for line in infile.readlines():
            func, func_size = line.rstrip("\n").split(",")
            func_size = int(func_size, 16)
            func_address, func_name = func.split(" ", maxsplit=1)
            func_address = int(func_address, 16)
            # if not func_name.startswith("z_un_") and not func_name.startswith("zz_"):
            functions[func_address] = (func_name, func_size)
            # print(func_address)
            # print(func_name)
            # print(func_size)
            # exit()
    return functions


def get_function_bytes(
    ram_path: str, functions: Dict[int, Tuple[str, int]]
) -> Dict[int, bytes]:
    function_bytes = {}
    with open(ram_path, "rb") as infile:
        for address, (func_name, func_size) in functions.items():
            infile.seek(address - 0x08800000)
            function_bytes[address] = infile.read(func_size)
            # print(function_bytes)
            # exit()
    return function_bytes


def get_same_functions(
    ram_path: str,
    functions_destination: Dict[int, Tuple[str, int]],
    functions: Dict[int, Tuple[str, int]],
    function_bytes: Dict[int, bytes],
) -> Dict[int, Tuple[str, int]]:
    # functions_ported_names = functions_destination.copy()
    functions_ported_names = {}
    with open(ram_path, "rb") as infile:
        ram_bytes = infile.read()
    for address, (function_bytes) in function_bytes.items():
        # print(functions[address][0])
        # exit()
        if functions[address][0].startswith("z_un_") or functions[address][
            0
        ].startswith("zz_"):
            continue
        num_results = 0
        last_offset = 0
        while (offset := ram_bytes.find(function_bytes, last_offset + 1)) != -1:
            last_offset = offset
            num_results += 1
        if num_results == 1:
            last_offset += 0x08800000
            # print(functions_ported_names[last_offset])
            try:
                functions_ported_names[last_offset] = functions[last_offset]
                # print(functions_ported_names[last_offset])
            except KeyError:
                continue
            # print(functions_ported_names[last_offset])
        # exit()
        # infile.seek(address - 0x08800000)
        # if function_bytes[address] == infile.read(func_size):
        #     # print(address)
        #     # print(func_name)
        #     # print(func_size)
        #     # exit()
        #     if not func_name.startswith("z_un_") and not func_name.startswith(
        #         "zz_"
        #     ):
        #         # print(func_name)
        #         functions_ported_names[address] = (func_name, func_size)
        # exit()
    return functions_ported_names


def write_functions(sym_path: str, functions: Dict[int, Tuple[str, int]]):
    outfile = open(
        Path(sym_path).parent.joinpath(f"{Path(sym_path).stem}_ported.sym"), "w"
    )
    with open(sym_path, "r") as infile:
        for line in infile.readlines():
            func, func_size = line.rstrip("\n").split(",")
            ori_func_size = int(func_size, 16)
            ori_func_address, ori_func_name = func.split(" ", maxsplit=1)
            ori_func_address = int(ori_func_address, 16)
            # if not func_name.startswith("z_un_") and not func_name.startswith("zz_"):
            # functions[func_address] = (func_name, func_size)
            try:
                func_name, func_size = functions[ori_func_address]
                if func_name != ori_func_name and func_size == ori_func_size:
                # if func_name != ori_func_name:
                    # print(ori_func_address)
                    # print(functions[ori_func_address])
                    print(
                        # f"{func_name=} {ori_func_name=} {func_size=} {ori_func_size=}"
                        f"{func_name=} {ori_func_name=}"
                    )
                    ori_func_name = func_name
            except KeyError:
                pass
            outfile.write(
                f"{ori_func_address:08X} {ori_func_name},{ori_func_size:04X}\n"
            )


p1_UCUS98711_functions = get_functions(
    # "../PPSSPP sym/ppsspp_p1_UCUS98711_566_(pac)_39_(lua)_and_custom_func_names.sym"
    "../PPSSPP sym/ppsspp_p2_UCUS98732_732_(pac)_68_(lua)_and_custom_func_names.sym"
)
# print (p1_UCUS98711_functions[0x08816BDC])
# print(p1_UCUS98711_functions)

p1_UCES00995_functions = get_functions(
    # "../PPSSPP sym/ppsspp_p1_UCES00995_566_func_names.sym"
    "../PPSSPP sym/ppsspp_p2_UCES01177_732_func_names.sym"
    # "../PPSSPP sym/ppsspp_p3_UCES01421_913_func_names.sym"
)
# print(p1_UCES00995_functions)

p1_UCUS98711_function_bytes = get_function_bytes(
    # "./RAM/RAMp1_UCUS98711.dump",
    "./RAM/RAMp2_UCUS98732.dump",
    p1_UCUS98711_functions,
)

p1_UCES00995_functions_ported_names = get_same_functions(
    # "./RAM/RAMp1_UCES00995.dump",
    "./RAM/RAMp2_UCES01177.dump",
    # "./RAM/RAMp3_UCES01421.dump",
    p1_UCES00995_functions,
    p1_UCUS98711_functions,
    p1_UCUS98711_function_bytes,
)
# print(p1_UCES00995_functions_ported_names)

write_functions(
    # "../PPSSPP sym/ppsspp_p1_UCES00995_566_func_names.sym",
    "../PPSSPP sym/ppsspp_p2_UCES01177_732_func_names.sym",
    # "../PPSSPP sym/ppsspp_p3_UCES01421_913_func_names.sym",
    p1_UCES00995_functions_ported_names,
)
