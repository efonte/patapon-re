from pathlib import Path
import shutil


def cwcheat_to_psp(cheat: str) -> str:
    cheat_new = ""
    for c in cheat.splitlines():
        l, address, code = c.split(" ")
        address = int(address[3:], 16) + 0x8800000
        cheat_new += f"{l} 0x{address:X} {code}\n"
    return cheat_new


cheat = """_L 0x20222F70 0x3C020001
_L 0x201E0E00 0x34020000"""
cheat = cwcheat_to_psp(cheat)
print(cheat)