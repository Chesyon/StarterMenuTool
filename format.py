from dataclasses import dataclass
import csv
import textwrap


@dataclass
class Pokemon:
    name: str
    species: int
    gender: int
    talk_kind: int


def gen_starter_option(species_name: str, species_id: int, gender: int, is_partner: int, starter_setter_sp: int,
                       set_frame_color_sp: int, choose_gender: bool, gender_list: int, confirm_species: bool,
                       confirmation_string: str, talk_kind: int) -> str:
    confirmation_string = confirmation_string.replace("[SPECIESNAME]", "[CS:K]" + species_name + "[CR]")
    indent_if_confirm = ""
    if confirm_species:
        indent_if_confirm += "    "
    output = '''    case menu("'''
    if gender == 0:
        output += "♂"
    elif gender == 1:
        output += "♀"
    elif gender == 2:
        output += "-"
    output += " [CS:K]" + species_name + '''[CR]"):\n        message_Close();\n'''
    if confirm_species:
        output += "        message_Monologue('" + confirmation_string + "');\n        switch ( message_SwitchMenu(2, 1) ) {\n            case menu('Yes'):\n                    message_Close();\n"
    output += "            " + indent_if_confirm + "ProcessSpecial(" + str(starter_setter_sp) + "," + str(
        is_partner) + "," + str(species_id) + ");\n" + "            " + indent_if_confirm + "$"
    if is_partner == 0:
        output += "HERO"
    else:
        output += "PARTNER"
    output += "_TALK_KIND = " + str(talk_kind) + ";\n"
    if not choose_gender and not is_partner:
        output += "            " + indent_if_confirm + "ProcessSpecial(" + str(set_frame_color_sp) + "," + str(
            gender) + ",0);\n"
    output += "            " + indent_if_confirm + "jump @label_end_choice" + str(is_partner) + ";\n"
    if confirm_species:
        output += '''            case menu('No'):\n                message_Close();\n                jump @label_start_choice''' + str(
            is_partner)
        if choose_gender:
            output += "_" + str(gender_list)
        output += ";\n            }\n"
    return output


def gen_gender_prompt(is_partner: int, gender_prompt: str, set_frame_color_sp: int):
    output = "message_Monologue('" + gender_prompt + "');\nswitch ( message_SwitchMenu(0, 1) ) {\n    case menu('Male'):\n"
    if is_partner == 0:
        output += "        ProcessSpecial(" + str(set_frame_color_sp) + ",0,0);\n"
    output += "        jump @label_start_choice" + str(is_partner) + "_0;\n    case menu('Female'):\n"
    if is_partner == 0:
        output += "        ProcessSpecial(" + str(set_frame_color_sp) + ",1,0);\n"
    output += "        jump @label_start_choice" + str(is_partner) + "_1;\n}\n"
    return output


def gen_menu_header(is_partner: int, choose_gender: bool, gender_list: int, prompt: str):
    output = "§label_start_choice" + str(is_partner)
    if choose_gender:
        output += "_" + str(gender_list)
    output += ";\nmessage_Monologue('" + prompt + "');\nswitch ( message_SwitchMenu(0, 1) ) {\n"
    return output


def gen_menu_footer(choose_gender: bool, gender_list: int, is_partner: int):
    output = "}\n"
    if not (choose_gender and gender_list == 0):
        output += "§label_end_choice" + str(is_partner) + ";\n"
    return output


def gen_menu(gender_prompt: str, species_prompt: str, species_confirmation: str, confirm_species: bool,
             choose_gender: bool, is_partner: int, mons: list, female_mons: list, starter_setter_sp: int,
             set_frame_color_sp: int):
    output = ""
    if choose_gender:
        output += gen_gender_prompt(is_partner, gender_prompt, set_frame_color_sp)
    output += gen_menu_header(is_partner, choose_gender, 0, species_prompt)
    i = 0
    while i != len(mons):
        output += gen_starter_option(mons[i].name, mons[i].species, mons[i].gender, is_partner, starter_setter_sp,
                                     set_frame_color_sp, choose_gender, 0, confirm_species, species_confirmation,
                                     mons[i].talk_kind)
        i += 1
    output += gen_menu_footer(choose_gender, 0, is_partner)
    if choose_gender:
        output += gen_menu_header(is_partner, choose_gender, 1, species_prompt)
        i = 0
        while i != len(female_mons):
            output += gen_starter_option(female_mons[i].name, female_mons[i].species, female_mons[i].gender, is_partner,
                                         starter_setter_sp, set_frame_color_sp, choose_gender, 1, confirm_species,
                                         species_confirmation, female_mons[i].talk_kind)
            i += 1
        output += gen_menu_footer(choose_gender, 1, is_partner)
    return output


def gen_post_menu():
    output = "    switch ( ProcessSpecial(PROCESS_SPECIAL_INIT_MAIN_TEAM_AFTER_QUIZ, 0, 0) ) { }\n"
    with open('settings.csv', 'r') as f:
        mycsv = csv.reader(f)
        mycsv = list(mycsv)
        if mycsv[7][1] == "Yes":
            output += "    switch ( message_Menu(MENU_PLAYER_NAME) ) { }\n"
        if mycsv[8][1] == "Yes":
            output += "    switch ( message_Menu(MENU_PARTNER_NAME) ) { }\n"
        if mycsv[9][1] == "Yes":
            output += "    switch ( message_Menu(MENU_TEAM_NAME) ) { }\n    $PERFORMANCE_PROGRESS_LIST[1] = 1;\n"
    return output


def parse_csv_settings(is_partner: int):
    # row_num 0 is 1
    # col_num 0 is A
    # accessing a cell can be done as mycsv[row_num][col_num]
    if is_partner != 0 and is_partner != 1:
        raise ValueError("is_partner must be 0 or 1!")
    with open('settings.csv', 'r') as f:
        mycsv = csv.reader(f)
        mycsv = list(mycsv)
        mycsv.append(['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''])
        if is_partner == 0:
            species_prompt = mycsv[1][1]
        else:
            species_prompt = mycsv[4][1]
        if species_prompt == '':
            raise ValueError("Species prompt cannot be empty!")
        if is_partner == 0:
            species_confirmation = mycsv[2][1]
        else:
            species_confirmation = mycsv[5][1]
        if species_confirmation == '':
            confirm_species = False
        else:
            confirm_species = True
        if is_partner == 0:
            gender_prompt = mycsv[0][1]
        else:
            gender_prompt = mycsv[3][1]
        if gender_prompt == '':
            choose_gender = False
        else:
            choose_gender = True
        if is_partner == 0:
            first_col = 3
        else:
            first_col = 13
        cur_row = 2
        mons = []
        while is_mon_valid(mycsv[cur_row][first_col], mycsv[cur_row][first_col + 1], mycsv[cur_row][first_col + 2],
                           mycsv[cur_row][first_col + 3]):
            mons.append(Pokemon(mycsv[cur_row][first_col], int(mycsv[cur_row][first_col + 1]),
                                int(mycsv[cur_row][first_col + 2]), int(mycsv[cur_row][first_col + 3])))
            cur_row += 1
        if choose_gender == 1:
            if is_partner == 0:
                first_col = 8
            else:
                first_col = 18
            cur_row = 2
            female_mons = []
            while is_mon_valid(mycsv[cur_row][first_col], mycsv[cur_row][first_col + 1], mycsv[cur_row][first_col + 2],
                               mycsv[cur_row][first_col + 3]):
                female_mons.append(Pokemon(mycsv[cur_row][first_col], int(mycsv[cur_row][first_col + 1]),
                                           int(mycsv[cur_row][first_col + 2]), int(mycsv[cur_row][first_col + 3])))
                cur_row += 1
        else:
            female_mons = []
        starter_setter_sp = int(mycsv[11][1])
        set_frame_color_sp = int(mycsv[12][1])
    return [gender_prompt, species_prompt, species_confirmation, confirm_species, choose_gender, is_partner, mons,
            female_mons, starter_setter_sp, set_frame_color_sp]


def is_mon_valid(name: str, species: str, gender: str, talk_kind: str):
    if name == '' or species == '' or gender == '' or talk_kind == '':
        return False
    else:
        try:
            int(species)
            int(gender)
            int(talk_kind)
        except ValueError:
            return False
    return True


def gen_script():
    output = ""
    with open('script_header.txt', 'r', encoding="utf8") as f:
        output += f.read()
    hero_settings = parse_csv_settings(0)
    output += textwrap.indent(
        gen_menu(*hero_settings), '    ')
    partner_settings = parse_csv_settings(1)
    output += textwrap.indent(
        gen_menu(*partner_settings), '    ')
    output += gen_post_menu()
    with open('script_footer.txt', 'r') as f:
        output += f.read()
    return output


with open("output.txt", "w", encoding="utf8") as file:
    file.write(gen_script())
    print("Done!")
