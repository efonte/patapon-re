import re
from rich import print

functions = {}
for file_path in [
    "./UCUS98732_features.lua",
    "./UCUS98732_patches.lua",
    "./UCUS98732_trophies.lua",
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
                functions[int(m.group("address"), 16)] = func_name
            elif m := re.match(
                r".*axFuncReplace\(0x(?P<address>.{7}), \"(?P<func_name>.+)\"(, 0x.{7})?\)",
                line,
            ):
                functions[int(m.group("address"), 16)] = "ps4__" + m.group("func_name")


# p2 usa - addresses obtained manually thanks to owocek
p2_usa_functions = """0884600C PSP::Gfx::PrimitiveContext::setVertex2f
088687B4 Labo::GameSystem__callbackFunc_MemoryObject
08877104 convertLowerString__21@unnamed@BNDFile_cpp@Fv
08877304 System::Util__BNDFile__doNameCallback
088A95B8 reawakeDeathUnit
088B9044 Labo::Game::Talk::CommandGame::setStringVariable
088D5894 Labo::Bases__Talk__CommandCamp__setMissionNameFromVar
088D8ED0 Bases__Talk__CommandCamp__showDialog
088DC4DC Bases__Camp__Person__Behavior__Idle__update__4LaboFv
088E7E30 Utility__SaveDataUtility__setDataParamsfoString
088E94FC Labo::Bases__Camp__Scene__updateTips
088EF8E8 Labo::Game__Result__Controller__applyGlobalData
08901B84 Labo::Talk__CommandEffect__generateCapEffect
0890E984 Labo::Game__Gimmick__WindowAttacher__update
089183FC Labo::GameSystem__Item__Operator__addItem
089211A4 Labo::Sound__BeatCommander__sendCommand
089220F8 Sound__BeatCommander__endSubGame__4LaboFv
089528F0 Labo::Bases__Camp__SoundGame__Trent__Game__updatePlay
08977700 Localize__Manager__getLanguageName
0897CEBC Bases__Item__ExplanationWindow__setItemId
0898BCDC Sound__SubGame__Blacksmith__Command__start__4LaboFv
0898EBF8 Labo::Bases__Camp__SoundGame__Bean__Game__updatePlayShineup
089910F0 Labo::Bases__Camp__SoundGame__Blacksmith__Game__notifyResult
08996024 Labo::Bases__Camp__SoundGame__Cook__Game__updatePlay
08998774 Labo::Bases__Camp__SoundGame__Rock__Game__updateDropTears
0899CF0C GameSystem__SaveDataController__update__4LaboFv
0899E458 GameSystem__SaveDataController__setStateMessage
08A03344 Labo::Bases__Camp__SoundGame__Alchemy__Game__requestEndGame
08A04A6C Labo::Bases__Camp__SoundGame__Bell__Game__selectAxel
08A15BBC Labo::Bases__Camp__EvolutionMap__PhyleticIcon__execLevelUpEffectWait
08A19E80 Labo::Game__Result__Single__Controller__updateMessage
08A39440 Bases__Organization__Managed__ItemSelectWindow__onSlotChange
08A6A1BC Labo::GameSystem__MovieModule__render
08A734DC GameSystem__Tips__Viewer__setup__4LaboFv"""
for line in p2_usa_functions.splitlines():
    address, func_name = line.split(" ")
    address = int(address, 16)
    functions[address] = func_name

print(functions)
print(len(functions))
# exit()


outfile = open("./ppsspp_p2_usa_732_(pac)_and_67_(lua)_func_names.sym", "w")
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
