import requests
from API import api_2024_request, name_to_index

def view_available_spells(chosen_class): #Displays all available spells for a given class by level.
    for i in range(1, chosen_class.highest_spell_level + 1):
        spells = api_2024_request(f"classes/{chosen_class.name}/levels/{i}/spells")['results']
        print(f"\nLevel {i} Spells:")
        for spell in spells:
            print(f"- {spell['name']}")

def display_spell(spell_data): #Displays a simple overview of a spell.
    print()
    print(f"Name: {spell_data['name']}")
    print(f"Level: {spell_data['level']}")
    print(f"Index: {spell_data['index']}")
    print(f"URL: {spell_data['url']}")
    print()

def display_spell_details(spell_data): #Displays detailed information about a spell.
    print(f"Name: {spell_data['name']}")
    print(f"Level: {spell_data['level']}")
    print(f"School: {spell_data['school']['name']}")
    print(f"Casting Time: {spell_data['casting_time']}")
    print(f"Classes: {', '.join([c['name'] for c in spell_data['classes']])}")
    print(f"Duration: {spell_data['duration']}")
    print(f"Description: {spell_data['description']}")
    print(f"Higher Level: {spell_data['higher_level'] if 'higher_level' in spell_data else 'N/A'}")
    print(f"Index: {spell_data['index']}")
    print(f"URL: {spell_data['url']}")
    print()

def search_spell(): #Searches for a spell by name and displays matching results.
    spells_data = api_2024_request("spells")
    spells = spells_data['results']
    
    spell_name = input("Enter the spell name: \n").lower()
    matching_spells = [spell for spell in spells if spell_name in spell['name'].lower()]
    print("\nMatching Spells:")
    for spell in matching_spells:
        display_spell(spell)
        
def view_spell_details(): #Displays detailed information about a spell.
    spell_name = input("Enter the spell name: \n").lower()
    spell_index = name_to_index(spell_name)
    spell_data = api_2024_request(f"spells/{spell_index}")
    display_spell_details(spell_data)
    
def cantrip_exists(cantrip_name): #Checks if a cantrip exists in the API and returns True or False.
    cantrip_index = name_to_index(cantrip_name)
    cantrip_data = api_2024_request(f"spells/{cantrip_index}")
    if cantrip_data is None:
        print(f"{cantrip_name} is not a valid cantrip name.")
        return False
    if cantrip_data['level'] != 0:
        print(f"{cantrip_name} is a spell, not a cantrip.")
        return False
    return True

def spell_exists(spell_name): #Checks if a spell exists in the API and returns True or False.
    spell_index = name_to_index(spell_name)
    spell_data = api_2024_request(f"spells/{spell_index}")
    if spell_data is None:
        print(f"{spell_name} is not a valid spell name.")
        return False
    if spell_data['level'] == 0:
        print(f"{spell_name} is a cantrip, not a spell.")
        return False
    return True