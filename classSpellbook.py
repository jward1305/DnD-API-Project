import requests
import pickle
from classClasses import non_caster, prepared_caster
from classSpells import display_spell_details, cantrip_exists, spell_exists
from API import api_2024_request, name_to_index

def spellbook_details(spellbook, character_name): #Displays general details on a spellbook.
    print(f"\n{character_name}'s {spellbook['class'].capitalize()} Spellbook:")
    print(f"Level: {spellbook['level']}")
    print(f"Spellcasting Ability Modifier: {spellbook['modifier']}")
    print(f"Cantrips Known: {spellbook['cantripsknown']}")
    print(f"Spells Known: {spellbook['spellsknown']}")
    print(f"Spells Prepared: {spellbook['spellsprepared']}")
    print(f"Spell Slots: {spellbook['spellslots']}")
    input("Press Enter to continue")
    
def view_cantrips(spellbook, character_name): #Displays any cantrips in a spellbook
    if spellbook['cantrips'] == []:
        print(f"\n{character_name}'s {spellbook['class'].capitalize()} Spellbook has no cantrips.")
    else:
        print(f"\n{character_name}'s {spellbook['class'].capitalize()} Cantrips:")
        for cantrip in spellbook['cantrips']:
            cantrip_index = cantrip.replace(" ", "-").lower()
            cantrip_data = api_2024_request(f"spells/{cantrip_index}")
            display_spell_details(cantrip_data)
    input("Press Enter to continue")

def view_spells(spellbook, character_name): #Displays any spells in a spellbook by level
    if spellbook['spells'] == {}:
        print(f"\n{character_name}'s {spellbook['class'].capitalize()} Spellbook has no spells.")
    else:
        print(f"\n{character_name}'s {spellbook['class'].capitalize()} Spells:")
        for level, spells in spellbook['spells'].items():
            if spells != []:
                print(f"\nLevel {level} Spells:")
                for spell in spells:
                    spell_index = spell.replace(" ", "-").lower()
                    spell_data = api_2024_request(f"spells/{spell_index}")
                    display_spell_details(spell_data)
    input("Press Enter to continue")

def view_prepared_spells(spellbook, character_name): #Displays any prepared spells in a spellbook by level if the class is a prepared caster.
    isprepared = spellbook["isprepared"]
    if isprepared:
        if spellbook['preppedspells'] == []:
            print(f"\n{character_name}'s {spellbook['class'].capitalize()} Spellbook has no spells.")
        else:
            print(f"\n{character_name}'s {spellbook['class'].capitalize()} Prepared Spells:")
            for spell in spellbook['preppedspells']:
                spell_index = spell.replace(" ", "-").lower()
                spell_data = api_2024_request(f"spells/{spell_index}")
                display_spell_details(spell_data)
    else:
        print(f"{spellbook['class'].capitalize()} is not a prepared caster class.")
    input("Press Enter to continue")

def add_cantrip(spellbook): #Attempts to add a cantrip to a spellbook
    cantrip_name = input("Enter the name of the cantrip to add:\n").capitalize()
    if cantrip_exists(cantrip_name):
        if cantrip_name in spellbook['cantrips']:
            print(f"{cantrip_name} is already in the spellbook.")
            
        elif len(spellbook['cantrips']) >= spellbook['cantripsknown']:
            print(f"You have already added the maximum number of cantrips ({spellbook['cantripsknown']}).")
            
        else:
            spellbook['cantrips'].append(cantrip_name)
            input(f"{cantrip_name.capitalize()} added! Press Enter to continue.")
    else:
        print(f"{cantrip_name} is not a valid cantrip name.")
    return spellbook

def learn_spell(spellbook, spell_data): #Adding spells for non-prepared casters.
    spell_name = spell_data['name']
    spell_level = spell_data['level']
    if spell_name in [spell for spells in spellbook['spells'].values() for spell in spells]:
        print(f"{spell_name} is already in the spellbook.")
        
    elif len([spell for spells in spellbook['spells'].values() for spell in spells]) >= spellbook['spellsknown']:
        print(f"You have already added the maximum number of spells ({spellbook['spellsknown']}).")
        
    else:
        if spell_level > spellbook['highest_spell_level']:
            print(f"{spell_name} is a level {spell_level} spell, which exceeds the current highest spell slot level ({spellbook['highest_spell_level']}) for this class.")
        else:
            spellbook['spells'][spell_level].append(spell_name)
            input(f"{spell_name.capitalize()} added! Press Enter to continue.")
    return spellbook

def prepare_spell(spellbook, spell_data): #Adding spells for prepared casters.
    spell_name = spell_data['name']
    spell_level = spell_data['level']
    if spell_name in spellbook['preppedspells']:
        print(f"{spell_name} is already prepared.")  
    elif len(spellbook['preppedspells']) >= spellbook['spellsprepared']:
        print(f"You have already prepared the maximum number of spells ({spellbook['spellsprepared']}).")    
    else:
        if spell_level > spellbook['highest_spell_level']:
            print(f"{spell_name} is a level {spell_level} spell, which exceeds the current highest spell slot level ({spellbook['highest_spell_level']}) for this class.")
        else:
            spellbook['preppedspells'].append(spell_name)
            input(f"{spell_name.capitalize()} prepared! Press Enter to continue.")
    return spellbook

def add_spell(spellbook): #Attempts to add a spell to a spellbook. If the class is a prepared caster, it will attempt to prepare the spell instead.
    spell_name = input("Enter the name of the spell to add:\n").capitalize()
    if spell_exists(spell_name):
        spell_index = name_to_index(spell_name)
        spell_data = api_2024_request(f"spells/{spell_index}")
        if spellbook["isprepared"]:
            spellbook = prepare_spell(spellbook, spell_data)
        else:
            spellbook = learn_spell(spellbook, spell_data)
    return spellbook

def remove_cantrip(spellbook): #Attempts to remove a cantrip from a spellbook
    cantrip_name = input("Enter the name of the cantrip to remove:\n").capitalize()
    if cantrip_exists(cantrip_name):
        if cantrip_name in spellbook['cantrips']:
            spellbook['cantrips'].remove(cantrip_name)
            input(f"{cantrip_name.capitalize()} removed! Press Enter to continue.")
        else:
            print(f"{cantrip_name} is not in the spellbook.")
    return spellbook

def unlearn_spell(spellbook, spell_data): #Removing spells for non-prepared casters.
    spell_name = spell_data['name']
    spell_level = spell_data['level']
    if spell_name in spellbook['spells'][spell_level]:
        spellbook['spells'][spell_level].remove(spell_name)
        input(f"{spell_name.capitalize()} removed! Press Enter to continue.")
    else:
        print(f"{spell_name} is not in the spellbook.")
    return spellbook

def unprepare_spell(spellbook,  spell_data): #Removing spells for prepared casters.
    spell_name = spell_data['name']
    if spell_name in spellbook['preppedspells']:
        spellbook['preppedspells'].remove(spell_name)
        input(f"{spell_name.capitalize()} unprepared! Press Enter to continue.")
    else:
        print(f"{spell_name} is not prepared.")
    return spellbook

def remove_spell(spellbook): #Attempts to remove a spell from a spellbook. If the class is a prepared caster, it will attempt to unprepare the spell instead.
    spell_name = input("Enter the name of the spell to remove:\n").capitalize()
    if spell_exists(spell_name):
        spell_index = name_to_index(spell_name)
        spell_data = api_2024_request(f"spells/{spell_index}")
        if spellbook["isprepared"]:
            spellbook = unprepare_spell(spellbook, spell_data)
        else:
            spellbook = unlearn_spell(spellbook, spell_data)
    return spellbook

def create_character_spellbook(chosen_classes, character_name): #Creates a spellbook for a character based on the classes they have chosen.
    quit = "n"                                                  #If a non-caster, it will not create a spellbook.
    while True:                                                
        if quit == "y":
                    break
        print(f"\n{character_name}'s Classes:")
        i = 0
        for c in chosen_classes:
            i += 1
            print(f"{i}- {c.name.capitalize()}")
        selected_class_idx = int(input("Select a class to create a spellbook for:\n"))
        selected_class = chosen_classes[selected_class_idx - 1]
        if selected_class.name in non_caster:
            print(f"{selected_class.name.capitalize()} is a non-caster class and has no spells.")
            quit = input("Exit? (y/n): ").lower()
            continue
        elif selected_class.name in prepared_caster:
            book_spells = {}
            for i in range(1, selected_class.highest_spell_level + 1):
                spells = api_2024_request(f"classes/{selected_class.name}/levels/{i}/spells")['results']
                spell_list = [spell['name'] for spell in spells]
                book_spells[i] = spell_list
                    
            spellbook = { 
            "class": selected_class.name,
            "level": selected_class.level,
            "isprepared": True,
            "modifier": selected_class.modifier,
            "cantripsknown": selected_class.cantrip_count,
            "spellsknown": selected_class.known_spells_count,
            "spellsprepared": selected_class.prepared_spells_count,
            "spellslots": selected_class.spell_slots,
            "cantrips": [],
            "spells": book_spells,
            "preppedspells": [],
            "highest_spell_level": selected_class.highest_spell_level
            }
            pickle.dump(spellbook, open(f"spellbooks/{character_name.capitalize()}_{selected_class.name.capitalize()}Spellbook.pkl", "wb"))
        else: 
            spellbook = {
            "class": selected_class.name,
            "level": selected_class.level,
            "isprepared": False,
            "modifier": selected_class.modifier,
            "cantripsknown": selected_class.cantrip_count,
            "spellsknown": selected_class.known_spells_count,
            "spellsprepared": selected_class.prepared_spells_count,
            "spellslots": selected_class.spell_slots,
            "cantrips": [],
            "spells": {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: []},
            "preppedspells": [],
            "highest_spell_level": selected_class.highest_spell_level
            }
            pickle.dump(spellbook, open(f"spellbooks/{character_name.capitalize()}_{selected_class.name.capitalize()}Spellbook.pkl", "wb"))
        print(f"\n{character_name}'s {selected_class.name.capitalize()} Spellbook created!")
        quit = input("Exit? (y/n): ").lower()
