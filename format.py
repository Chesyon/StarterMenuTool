from dataclasses import dataclass


@dataclass
class Pokemon:
    name: str
    species: int
    gender: int


def gen_starter_option(species_name: str, species_id: int, gender: int, is_partner: int, starter_setter_sp: int,
                       set_frame_color_sp: int, choose_gender: bool, gender_list: int, confirm_species: bool,
                       confirmation_string: str) -> str:
    confirmation_string = confirmation_string.replace("[SPECIESNAME]", "[CS:K]" + species_name + "[CR]")
    indent_if_confirm = ""
    if confirm_species:
        indent_if_confirm += "     "
    output = '''     case menu("'''
    if gender == 0:
        output += "♂"
    elif gender == 1:
        output += "♀"
    elif gender == 2:
        output += "-"
    output += " [CS:K]" + species_name + '''[CR]"):\n          message_Close();\n'''
    if confirm_species:
        output += "          message_Monologue('" + confirmation_string + "');\n          switch ( message_SwitchMenu(2, 1) ) {\n               case menu('Yes'):\n                    message_Close();\n"
    output += "               " + indent_if_confirm + "ProcessSpecial(" + str(starter_setter_sp) + "," + str(
        is_partner) + "," + str(species_id) + ");\n"
    if not choose_gender and not is_partner:
        output += "               " + indent_if_confirm + "ProcessSpecial(" + str(set_frame_color_sp) + "," + str(
            gender) + ",0);\n"
    output += "               " + indent_if_confirm + "jump @label_end_choice" + str(is_partner) + ";\n"
    if confirm_species:
        output += '''               case menu('No'):\n                    message_Close();\n                    jump @label_start_choice''' + str(
            is_partner)
        if choose_gender:
            output += "_" + str(gender_list)
        output += ";\n               }\n"
    return output


def gen_gender_prompt(is_partner: int, gender_prompt: str, set_frame_color_sp: int):
    output = "message_Monologue('" + gender_prompt + "');\nswitch ( message_SwitchMenu(0, 1) ) {\n     case menu('Male'):\n"
    if is_partner == 0:
        output += "          ProcessSpecial(" + str(set_frame_color_sp) + ",0,0);\n"
    output += "          jump @label_start_choice" + str(is_partner) + "_0;\n     case menu('Female'):\n"
    if is_partner == 0:
        output += "          ProcessSpecial(" + str(set_frame_color_sp) + ",1,0);\n"
    output += "          jump @label_start_choice" + str(is_partner) + "_1;\n}\n"
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
             choose_gender: bool, is_partner: int, mons: list, female_mons: list, starter_setter_sp: int, set_frame_color_sp: int):
    output = ""
    if choose_gender:
        output += gen_gender_prompt(is_partner, gender_prompt, set_frame_color_sp)
    output += gen_menu_header(is_partner, choose_gender, 0, species_prompt)
    i = 0
    while i != len(mons):
        output += gen_starter_option(mons[i].name, mons[i].species, mons[i].gender, is_partner, starter_setter_sp,
                                     set_frame_color_sp, choose_gender, 0, confirm_species, species_confirmation)
        i += 1
    output += gen_menu_footer(choose_gender, 0, is_partner)
    if choose_gender:
        output += gen_menu_header(is_partner, choose_gender, 1, species_prompt)
        i = 0
        while i != len(female_mons):
            output += gen_starter_option(female_mons[i].name, female_mons[i].species, female_mons[i].gender, is_partner,
                                         starter_setter_sp, set_frame_color_sp, choose_gender, 1, confirm_species,
                                         species_confirmation)
            i += 1
        output += gen_menu_footer(choose_gender, 1, is_partner)
    return output


# PLAYER SETTINGS
player_pokemon = [Pokemon("Torchic", 283, 0), Pokemon("Charmander", 4, 0), Pokemon("Pikachu", 25, 0), Pokemon("Totodile", 158, 0), Pokemon("Piplup", 428, 0), Pokemon("Chimchar", 425, 0), Pokemon("Cyndaquil", 155, 0), Pokemon("Shinx", 438, 0), Pokemon("Riolu", 489, 0), Pokemon("Chikorita", 152, 0), Pokemon("Phanpy", 258, 0), Pokemon("Bulbasaur", 1, 0), Pokemon("Squirtle", 7, 0), Pokemon("Treecko", 280, 0), Pokemon("Mudkip", 286, 0), Pokemon("Turtwig", 422, 0)]
player_pokemon_female = [Pokemon("Treecko", 880, 1), Pokemon("Bulbasaur", 4, 601), Pokemon("Charmander", 25, 604), Pokemon("Eevee", 733, 1), Pokemon("Chimchar", 1025, 1), Pokemon("Skitty", 928, 1), Pokemon("Turtwig", 1022, 1), Pokemon("Pikachu", 625, 1), Pokemon("Totodile", 758, 1), Pokemon("Cyndaquil", 755, 1), Pokemon("Vulpix", 637, 1), Pokemon("Mudkip", 886, 1), Pokemon("Piplup", 1028, 1), Pokemon("Chikorita", 752, 1), Pokemon("Torchic", 883, 1), Pokemon("Squirtle", 607, 1)]

# PARTNER SETTINGS
partner_pokemon = [Pokemon("Bulbasaur", 1, 0), Pokemon("Charmander", 4, 0), Pokemon("Squirtle", 7, 0), Pokemon("Pikachu", 25, 0), Pokemon("Chikorita", 752, 1), Pokemon("Cyndaquil", 155, 0), Pokemon("Totodile", 158, 0), Pokemon("Treecko", 280, 0), Pokemon("Torchic", 883, 1), Pokemon("Mudkip", 286, 0), Pokemon("Turtwig", 422, 0),Pokemon("Chimchar", 425, 0), Pokemon("Piplup", 428, 0), Pokemon("Eevee", 733, 1), Pokemon("Shinx", 438, 0), Pokemon("Riolu", 489, 0), Pokemon("Phanpy", 258, 0), Pokemon("Vulpix", 637, 1), Pokemon("Skitty", 928, 1), Pokemon("Meowth", 52, 0), Pokemon("Munchlax", 488, 0)]
partner_pokemon_female = partner_pokemon

print(gen_menu("Are you male or female?", "Who would you like to be?", "Is [SPECIESNAME] who you want?", True, True, 0, player_pokemon, player_pokemon_female, 64, 65))
print(gen_menu("Are you male or female?", "Choose the Pokémon you want for a partner.", "Is [SPECIESNAME] who you want?", True, False, 1, partner_pokemon, partner_pokemon_female, 64, 65))
