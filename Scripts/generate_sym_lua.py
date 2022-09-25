import re

from rich import print

functions = {}
for file_path in [
    "./UCUS98732_features.lua",
    "./UCUS98732_patches.lua",
    "./UCUS98732_trophies.lua",
    # "UCES01177_features.lua",
    # "UCES01177_patches.lua",
    # "UCES01177_trophies.lua",
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


# p2 usa - addresses obtained manually, thanks to owocek
p2_usa_functions = """08828A00 sgxResFindSeq
0884600C PSP::Gfx::PrimitiveContext::setVertex2f
088687B4 Labo::GameSystem::callbackFunc_MemoryObject
08877104 convertLowerString::21@unnamed@BNDFile_cpp@Fv
08877304 System::Util::BNDFile::doNameCallback
088A95B8 Labo::Bases::Camp::Controller::reawakeDeathUnit
088B9044 Labo::Game::Talk::CommandGame::setStringVariable
088BF34C Labo::Talk::CommandMessage::getPadStand
088D5894 Labo::Bases::Talk::CommandCamp::setMissionNameFromVar
088D8ED0 Bases::Talk::CommandCamp::showDialog
088DC4DC Bases::Camp::Person::Behavior::Idle::update::4LaboFv
088E7E30 Utility::SaveDataUtility::setDataParamsfoString
088E94FC Labo::Bases::Camp::Scene::updateTips
088EF8E8 Labo::Game::Result::Controller::applyGlobalData
08901B84 Labo::Talk::CommandEffect::generateCapEffect
0890E984 Labo::Game::Gimmick::WindowAttacher::update
089183FC Labo::GameSystem::Item::Operator::addItem
089211A4 Labo::Sound::BeatCommander::sendCommand
089220F8 Sound::BeatCommander::endSubGame::4LaboFv
089528F0 Labo::Bases::Camp::SoundGame::Trent::Game::updatePlay
0895B1AC Labo::Bases::Camp::SelectItem::Behavior::UnitBirthParamTable::addBattleUnit
08977700 Localize::Manager::getLanguageName
089778E0 Font::Localize::getStringFromIndex
0897CEBC Bases::Item::ExplanationWindow::setItemId
0898BCDC Sound::SubGame::Blacksmith::Command::start::4LaboFv
0898EBF8 Labo::Bases::Camp::SoundGame::Bean::Game::updatePlayShineup
089910F0 Labo::Bases::Camp::SoundGame::Blacksmith::Game::notifyResult
08996024 Labo::Bases::Camp::SoundGame::Cook::Game::updatePlay
08998774 Labo::Bases::Camp::SoundGame::Rock::Game::updateDropTears
0899CF0C GameSystem::SaveDataController::update::4LaboFv
0899E458 GameSystem::SaveDataController::setStateMessage
08A03344 Labo::Bases::Camp::SoundGame::Alchemy::Game::requestEndGame
08A04A6C Labo::Bases::Camp::SoundGame::Bell::Game::selectAxel
08A15BBC Labo::Bases::Camp::EvolutionMap::PhyleticIcon::execLevelUpEffectWait
08A19E80 Labo::Game::Result::Single::Controller::updateMessage
08A2215C Bases::Organization::Managed::OrganizationManager::initSquadParam
08A39440 Bases::Organization::Managed::ItemSelectWindow::onSlotChange
08A6A1BC Labo::GameSystem::MovieModule::render
08A734DC GameSystem::Tips::Viewer::setup::4LaboFv"""
for line in p2_usa_functions.splitlines():
    address, func_name = line.split(" ")
    address = int(address, 16)
    functions[address] = func_name.replace("__", "::")


p2_eur_functions = """08828A00 sgxResFindSeq
0884600C PSP::Gfx::PrimitiveContext::setVertex2f
088687D0 Labo::GameSystem::callbackFunc_MemoryObject
08877120 convertLowerString::21@unnamed@BNDFile_cpp@Fv
08877320 System::Util::BNDFile::doNameCallback
088A95B4 Labo::Bases::Camp::Controller::reawakeDeathUnit
088B9040 Labo::Game::Talk::CommandGame::setStringVariable
088BF348 Labo::Talk::CommandMessage::getPadStand
088D5890 Labo::Bases::Talk::CommandCamp::setMissionNameFromVar
088D8ECC Bases::Talk::CommandCamp::showDialog
088DC4D8 Bases::Camp::Person::Behavior::Idle::update::4LaboFv
088E7E2C Utility::SaveDataUtility::setDataParamsfoString
088E94F8 Labo::Bases::Camp::Scene::updateTips
088EF998 Labo::Game::Result::Controller::applyGlobalData
08901C34 Labo::Talk::CommandEffect::generateCapEffect
0890EA34 Labo::Game::Gimmick::WindowAttacher::update
089119FC PSP::MoviePlayer::play
089148F4 MainGame::Mission::MissionScene::initialize::4LaboFv
089184AC Labo::GameSystem::Item::Operator::addItem
08921254 Labo::Sound::BeatCommander::sendCommand
089221A8 Sound::BeatCommander::endSubGame::4LaboFv
089529A0 Labo::Bases::Camp::SoundGame::Trent::Game::updatePlay
0895B25C Labo::Bases::Camp::SelectItem::Behavior::UnitBirthParamTable::addBattleUnit
089778E8 Localize::Manager::getLanguageName
08977B60 Font::Localize::getStringFromIndex
0897BA58 Labo::Game::Miracle::Quake::start
0897BBBC Labo::Game::Miracle::Storm::start
0897BE20 Labo::Game::Miracle::Wind::start
0897C004 Labo::Game::Miracle::Rain::start
0897D13C Bases::Item::ExplanationWindow::setItemId
08982838 Labo::Game::Map::ThunderLayer::generateThunder
0898BF5C Sound::SubGame::Blacksmith::Command::start::4LaboFv
0898EE78 Labo::Bases::Camp::SoundGame::Bean::Game::updatePlayShineup
08991370 Labo::Bases::Camp::SoundGame::Blacksmith::Game::notifyResult
089962A4 Labo::Bases::Camp::SoundGame::Cook::Game::updatePlay
089989F4 Labo::Bases::Camp::SoundGame::Rock::Game::updateDropTears
0899D18C GameSystem::SaveDataController::update::4LaboFv
0899E6D8 GameSystem::SaveDataController::setStateMessage
08A035C4 Labo::Bases::Camp::SoundGame::Alchemy::Game::requestEndGame
08A04CEC Labo::Bases::Camp::SoundGame::Bell::Game::selectAxel
08A0653C Labo::Game::Miracle::SnowStorm::start
08A0B50C Labo::Game::Miracle::Offense::start
08A0B648 Labo::Game::Miracle::Defense::start
08A15E3C Labo::Bases::Camp::EvolutionMap::PhyleticIcon::execLevelUpEffectWait
08A1A100 Labo::Game::Result::Single::Controller::updateMessage
08A223DC Bases::Organization::Managed::OrganizationManager::initSquadParam
08A396C0 Bases::Organization::Managed::ItemSelectWindow::onSlotChange
08A6A574 Labo::GameSystem::MovieModule::render
08A73894 GameSystem::Tips::Viewer::setup::4LaboFv"""
# for line in p2_eur_functions.splitlines():
#     address, func_name = line.split(" ")
#     address = int(address, 16)
#     functions[address] = func_name.replace("__", "::")


# p2 usa - function names obtained based on ghidra decompiled code, thanks to owocek
p2_usa_custom_functions = """0883E498 retrieveApplicationAddress
088438C8 packSeek
08843B14 packSeekLoggerFlag
088440C0 Script::Talk::Controller::getAddressFromPacPointer
0884430C Script::Talk::Controller::debugPacLogger
08844504 Script::Talk::Controller::getStringFromPacArgument
0889B4B0 setWindState
0889B818 setRainState
0889BA1C setSnowState
0889BB90 setFogState
0889BD04 setSandState
0889BE88 setCloudState
0889BFFC setThunderState
088F4ED8 set_v0_to_0x20
088F4EE0 playSoundEffect
088F5034 stopSoundEffect
089184d8 Labo::GameSystem::Item::Operator::subItem
0898C3F4 funcLeadingToVprintf"""
for line in p2_usa_custom_functions.splitlines():
    address, func_name = line.split(" ")
    address = int(address, 16)
    functions[address] = "custom__" + func_name.replace("__", "::")


print(functions)
print(len(functions))
# exit()


outfile = open("./ppsspp_p2_usa_732_(pac)_72_(lua)_and_custom_func_names.sym", "w")
with open("./ppsspp_p2_usa_732_func_names.sym", "r") as infile:
    # outfile = open("./ppsspp_p2_eur_732_(pac)_73_(lua).sym", "w")
    # with open("./ppsspp_p2_eur_732_func_names.sym", "r") as infile:
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
