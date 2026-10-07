import requests
import pickle
from classSpells import view_available_spells, search_spell, view_spell_details
from classClasses import classSelection, class_details, display_class_details
from classSpellbook import create_character_spellbook, spellbook_details, view_cantrips, view_spells, view_prepared_spells, add_cantrip, add_spell, remove_cantrip, remove_spell

def view_character_spellbook(spellbook, character_name):
    while True:
        print("\nCommands:") #add option to add spells to Wizard spellbook
        print("1 - View spellbook details")
        print("2 - View cantrips")
        print("3 - View spells")
        print("4 - View prepared spells")
        print("5 - Add a cantrip") #add class filtering
        print("6 - Add a spell") #add class filtering
        print("7 - Remove a cantrip")
        print("8 - Remove a spell")
        print("9 - Exit")
        selected_option = input("Enter your choice:\n")
        if selected_option == '1':
            spellbook_details(spellbook, character_name)
        elif selected_option == '2':
            view_cantrips(spellbook, character_name)
        elif selected_option == '3':
            view_spells(spellbook, character_name)
        elif selected_option == '4':
            view_prepared_spells(spellbook, character_name)
        elif selected_option == '5':
            spellbook = add_cantrip(spellbook)
            pickle.dump(spellbook, open(f"spellbooks/{character_name.capitalize()}_{spellbook['class'].capitalize()}Spellbook.pkl", "wb"))
        elif selected_option == '6':
            spellbook = add_spell(spellbook)
            pickle.dump(spellbook, open(f"spellbooks/{character_name.capitalize()}_{spellbook['class'].capitalize()}Spellbook.pkl", "wb"))
        elif selected_option == '7':
            spellbook = remove_cantrip(spellbook)
            pickle.dump(spellbook, open(f"spellbooks/{character_name.capitalize()}_{spellbook['class'].capitalize()}Spellbook.pkl", "wb"))
        elif selected_option == '8':
            spellbook = remove_spell(spellbook)
            pickle.dump(spellbook, open(f"spellbooks/{character_name.capitalize()}_{spellbook['class'].capitalize()}Spellbook.pkl", "wb"))
        elif selected_option == '9':
            print("Exiting spellbook view.")
            break
           
def character_menu(chosen_classes, character_name):
    while True:
        print("\nCommands:")
        print("1 - View available spells for a class")
        print("2 - Search for a spell by name")
        print("3 - View details of a spell")
        print("4 - Create character spellbook")
        print("5 - View character spellbook")
        print("6 - Exit")
        selected_option = input("Enter your choice:\n")
        if selected_option == '1':
            print(f"\n{character_name}'s Classes:")
            i = 0
            for c in chosen_classes:
                i += 1
                print(f"{i}- {c.name.capitalize()}")
            try:
                selected_class = int(input("Select a class to view spell details:\n"))
                view_available_spells(chosen_classes[selected_class - 1])
            except:
                print("Invalid input.")
        elif selected_option == '2':
            search_spell()
        elif selected_option == '3':
            view_spell_details()
        elif selected_option == '4':
            create_character_spellbook(chosen_classes, character_name)
        elif selected_option == '5':
            print(f"\n{character_name}'s Classes:")
            i = 0
            for c in chosen_classes:
                i += 1
                print(f"{i}- {c.name.capitalize()}")
            print(f"{i+1}- Exit")
            selected_class_idx = int(input("Select a class to view the spellbook of:\n"))
            if selected_class_idx == i + 1:
                print("Exiting spellbook view.")
                continue
            else:
                selected_class = chosen_classes[selected_class_idx - 1]
            try:
                loaded = pickle.load(open(f"spellbooks/{character_name.capitalize()}_{selected_class.name.capitalize()}Spellbook.pkl", "rb"))
                view_character_spellbook(loaded, character_name)
            except FileNotFoundError:
                print(f"No spellbook found for {character_name.capitalize()} as a {selected_class.name.capitalize()}.")
                continue
        elif selected_option == '6':
            print("Goodbye!")
            break

def main():
    print("Welcome to the D&D spellbook.")
    while True:
        print("\n1 - Create a new character") #add multiclass requirements
        print("2 - Load a character from file")
        print("3 - Exit")
        choice = input("What would you like to do?\n")
        if choice == '1':
            character_name = input("What is the character's name?\n").capitalize()
            chosen_classes = []
            chosen_classes, spell_level = classSelection(chosen_classes)
            chosen_classes = class_details(chosen_classes, spell_level)
            save_data = {"name": character_name, "classes": chosen_classes}
            pickle.dump(save_data, open(f"characters/{character_name}.pkl", "wb"))
            input(f"Character {character_name} saved. Press Enter to continue.")
            character_menu(chosen_classes, character_name)
        elif choice == '2':
            character_name = input("What is the character's name?\n").capitalize()
            try:
                loaded = pickle.load(open(f"characters/{character_name}.pkl", "rb"))
                chosen_classes = loaded["classes"]
                display_class_details(chosen_classes)
                input(f"Character {character_name} loaded. Press Enter to continue.")
                character_menu(chosen_classes, character_name)
            except FileNotFoundError:
                print(f"No saved character with the name {character_name} found.")
        elif choice == '3':
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()