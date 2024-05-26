# StarterMenuTool

StarterMenuTool is a tool written in Python that generates an [ExplorerScript](https://github.com/SkyTemple/ExplorerScript) menu for starter selection in Pokémon Mystery Dungeon: Explorers of Sky. It is compatible with the US and EU versions of the game. It is designed to be used alongside SkyTemple, and is a completely custom implementation of the game's starter selection. It was created by Chesyon, and credit would be appreciated if you use this! Please also credit Adex, HeckaBad, and Irdkwia for the ASM code that makes StarterMenuTool work! Thanks! <3
## Why use StarterMenuTool?
* A custom implementation of starter selection removes any hardcoded restrictions from EoS' vanilla Personality Test.
* This implementation *can* be done by hand in SkyTemple, but this tool automates the repetitive menu code.
# Usage guide
You will need a copy of Explorers of Sky (obviously), and [SkyTemple](https://download.skytemple.org/skytemple/latest/), to follow this guide. You will need Python 3 as well, which may come pre-installed on your computer. You can check this by opening your terminal, and running `python3`. If no error is given, it's installed! Otherwise, it can be downloaded [here](https://www.python.org/downloads/). All other necessary files are included in this repository.
## ROM Setup
1. Open your ROM in SkyTemple, and navigate to Patches > ASM. Go to the Utility tab, and apply ExtraSpace, if it has not been applied already. SkyTemple will reload your ROM after this. Go back to the Utility tab, and apply ExtractSPCode, if it has not been applied already.
2. In your file manager of choice, go to the location of your ROM (the .nds file.) There should be a folder called rom.nds.skytemple, with `rom.nds` being the name of your .nds file. Open it, and go to the Patches folder inside.
3. Place FixPartnerNameMenu.skypatch (from this repo's skypatches folder) inside the Patches folder. Return to SkyTemple, and go to Patches > ASM once more. SkyTemple should give a warning about malicious code. Click "Yes" to load the Skypatch.
4. Go to the Others tab, and apply FixPartnerNameMenu.
5. Go to Patches > ASM > Special Process Effects. Click "Add Special Process" twice, and then scroll down to the bottom. The last two numbers in the "Effect" column should be zeros. Replace them with the lowest numbers that aren't already in use. If you haven't added any special processes before, this should be 61 and 62.
	* If you've already added special processes to this ROM, write down the last two numbers in the ID column. You'll need these later.
6. Go to the Effects Code tab, and press the plus button. Click "Import Code", and then select starter_setter.asm from the folder in this repo that matches your ROM's region.
	* If you do not know your ROM's region, click the dropdown arrow by "Text Strings" on the left bar. If the only option that shows up is English, your ROM is US. If multiple languages are shown, your ROM is EU.
7. Repeat the prior step, using set_frame_color.asm.

**Note:** These next steps use S02P01A as their level, as this is the same one the personality test uses. You don't have to use this level, but make sure to replace S02P01A with whatever level you *are* using in the following steps.

8. Search for S02P01A in the searchbar. Two options should show up, one under Script Scenes, and the other under Map Backgrounds. Select the one under Script Scenes.
9. Select "Add Acting Scene", and name the new scene "smt". Double click "smt" in the left bar to open it, and save your ROM. Open smt.ssb on the right. A new window will open, and this is where you'll paste StarterMenuTool's output later. But for now, we have two more scripts to edit.

**Note:** These following steps assume you haven't already edited unionall.ssb or m00a01a.ssb. If you have, just make sure that smt.ssb is called in unionall before the hero/partner actors/names are used for the first time, and before `switch ( ProcessSpecial(PROCESS_SPECIAL_INIT_MAIN_TEAM_AFTER_QUIZ, 0, 0) ) { }` is called. `PROCESS_SPECIAL_INIT_MAIN_TEAM_AFTER_QUIZ` really shouldn't appear *anywhere* outside of smt.ssb, but StarterMenuTool is *guaranteed* not to work if it's used before smt.ssb. Also, any code related to the Personality Test should be removed.

10. Staying in the script engine debugger (the window that was opened when you opened smt.ssb), search for m00a01a.ssb, and open it. Replace the contents of this file with the contents of [m00a01a.exps](https://github.com/Chesyon/StarterMenuTool/blob/main/m00a01a.exps) from the repository. Save.
11. Search for unionall.ssb, and open it. Use Ctrl+F to find `coro EVENT_M00A_01`. Add a new line after `supervision_ExecuteActingSub(LEVEL_S02P01A, 'M00A01A', 0);`. In this newline, paste (or type) `supervision_ExecuteActingSub(LEVEL_S02P01A, 'SMT', 0);`. Save!

That's all for ROM setup! The personality test has been removed, and smt.ssb will be loaded upon starting a new game. You can now use StarterMenuTool to generate the code that will go in smt.ssb!

## settings.csv customization
settings.csv is the file that determines how your menu will work. It is a spreadsheet, and can be edited in programs such as Microsoft Excel, LibreOffice Calc, or even Google Sheets (not sure why you'd want to do that, but the option's there!) By default, it is configured to produce a menu that is near-identical to that of the vanilla one in Explorers of Sky, but it is fully customizable! This section will go over what each option does.
### The left side options
* **Hero gender prompt** (B1): What the game will display when asking your gender. If this is left blank, gender selection for the hero will be disabled. In this case, the Hero Pokemon (Female) list will be unused, and only the Male/Default list will be used.
* **Hero species prompt** (B2): The text shown when selecting your player's species. This should not be left blank, and it will look very weird in-game if you do.
* **Hero confirmation prompt** (B3): What the game will ask when you select a species for your player. [SPECIESNAME] will be converted to the name of the species for each option. (For example, if my text here is "Is [SPECIESNAME] who you want?", and I select Totodile in-game, the game will then ask "Is Totodile who you want?") Leaving this field blank will skip confirming the hero.

Partner gender prompt (B4), Partner species prompt (B5), and Partner confirmation prompt (B6) function the same as their hero counterparts, just used for the Partner menu instead of the Hero menu.

* **Set hero name?** (B8): Can be set to either "Yes" or "No". If enabled, the game will ask for the hero's name after the hero/partner are selected. Disabled by default, as the game will already ask for the players name in a later cutscene.
* **Set partner name?** (B9): Can be set to either "Yes" or "No". If enabled, the game will ask for the partner's name after the hero/partner are selected. Enabled by default, as the game does not ask for the partner's name outside of the personality test.
* **Set team name?** (B10): Can be set to either "Yes" or "No". If enabled, the game will ask for the team name after the hero/partner are selected. Disabled by default, as the game will already ask for the team name in a later cutscene. Enabling this will also set the flag to show the team name in dungeons.

* **starter_setter SP ID** (B12): The ID of the starter_setter special process that was imported during the ROM Setup section. If you did not import any special process before following this guide, you should leave this at its default value (64). If you *did* import special processes before following this guide, change this to the first of the two numbers you wrote down during step 5 of ROM setup. **Using the wrong number for this will cause the game to crash!**
* **set_frame_color SP ID** (B13): The ID of the set_frame_color special process that was imported during the ROM Setup section. If you did not import any special process before following this guide, you should leave this at its default value (65). If you *did* import special processes before following this guide, change this to the second of the two numbers you wrote down during step 5 of ROM setup. **Using the wrong number for this will cause the game to crash!**
### The Pokémon options
There are four lists of Pokémon here. Two for the hero, and two for the partner. If the gender prompt is disabled, you should only use the first one instead of both. Each Pokémon option has 4 parameters that need to be configured. The species ID is the only one that really matters, and you *could* input wrong information for the other ones if you really wanted to. If you were evil. StarterMenuTool won't stop you. If you're *not* evil, make sure you input the right information for all of these!
* **Name**: The name of the Pokémon species. Pretty self explanatory.
* **Species ID**: The internal ID for the species. Do not assume that this is just the Pokédex number! You can find the species ID by searching the Pokémon's name in SkyTemple. Do note that male/female use different IDs, with female almost always being the higher one.
* **Gender**: The gender icon that will be shown next to the Pokémon's name. 0 is male, 1 is female, and 2 is neutral/unknown. You should try to use the correct one for the species ID you entered, but again, StarterMenuTool won't stop you.
* **Talk Group**: This is an interesting one. Did you know that Explorers of Sky has slightly varying hero/partner dialogue, depending on the species you picked? This is handled by their Talk Group. This also handles pronouns. You're welcome to set this to whatever you want, but here's what the vanilla game uses:
	* **Hero**:
		* **4** if the Pokémon is male, or genderless.
		* **5** (or anything other than 4) if the Pokémon is female.
	* **Partner**:
		* **1** if the Pokémon is Squirtle, Totodile, Chimchar, Meowth or Munchlax (which are all male). Why is this separate from 2? Who knows! Which one you use is up to you.
		* **2** for all other male Pokémon not stated above.
		* **3** (or anything other than 1 or 2) for all female Pokémon (Chikorita, Torchic, Eevee, Vulpix, Skitty)

Play around with these settings as much as you want, and then move onto the next step!
## script_header.txt and script_footer.txt
These two text files will be added to the beginning and end, respectively, of the output. The idea here is to build one complete cutscene that you can paste in! By default, it's my recreation of the text from the Personality Test. You're welcome to customize this as much as you want, or, if you want the menu code by itself, you can delete the contents of both files.
## Using StarterMenuTool to generate a new smt.ssb
Once you've configured all your files, you can now run `format.py`. This is where StarterMenuTool does its magic to generate menu code. If double clicking it doesn't run it, you can run `linux-run.sh` on Linux, or open up the terminal in that folder, and run `python3 format.py`. If `output.txt` is generated in that folder, it worked! If not... wuh-oh. Make sure the file actually ran, and if you're sure it did and it still isn't working, please contact Chesyon (the creator of this tool). StarterMenuTool will create `output.txt` if it doesn't exist, or overwrite its current contents if it does. Once the file is generated, you can open it up, and copy its contents. You can then return to the SkyTemple Script Engine debugger (make sure you're on smt.ssb!), and paste in the code! And of course, don't forget to save your ROM. At this point, you should be done, and your starter menu should be working! Have fun!
