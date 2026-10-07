import requests
import pickle
from API import api_2014_request

non_caster = {"barbarian", "fighter", "monk", "rogue"}
prepared_caster = {"cleric", "druid", "paladin", "wizard"}
multiclass_spell_prog ={
    1: {'1st': 2, '2nd': 0, '3rd': 0, '4th': 0, '5th': 0, '6th': 0, '7th': 0, '8th': 0, '9th': 0},
    2: {'1st': 3, '2nd': 0, '3rd': 0, '4th': 0, '5th': 0, '6th': 0, '7th': 0, '8th': 0, '9th': 0},
    3: {'1st': 4, '2nd': 2, '3rd': 0, '4th': 0, '5th': 0, '6th': 0, '7th': 0, '8th': 0, '9th': 0},
    4: {'1st': 4, '2nd': 3, '3rd': 0, '4th': 0, '5th': 0, '6th': 0, '7th': 0, '8th': 0, '9th': 0},
    5: {'1st': 4, '2nd': 3, '3rd': 2, '4th': 0, '5th': 0, '6th': 0, '7th': 0, '8th': 0, '9th': 0},
    6: {'1st': 4, '2nd': 3, '3rd': 3, '4th': 0, '5th': 0, '6th': 0, '7th': 0, '8th': 0, '9th': 0},
    7: {'1st': 4, '2nd': 3, '3rd': 3, '4th': 1, '5th': 0, '6th': 0, '7th': 0, '8th': 0, '9th': 0},
    8: {'1st': 4, '2nd': 3, '3rd': 3, '4th': 2, '5th': 0, '6th': 0, '7th': 0, '8th': 0, '9th': 0},
    9: {'1st': 4, '2nd': 3, '3rd': 3, '4th': 3, '5th': 1, '6th': 0, '7th': 0, '8th': 0, '9th': 0},
    10: {'1st': 4, '2nd': 3, '3rd': 3, '4th': 3, '5th': 2, '6th': 0, '7th': 0, '8th': 0, '9th': 0},
    11: {'1st': 4, '2nd': 3, '3rd': 3, '4th': 3, '5th': 2, '6th': 1, '7th': 0, '8th': 0, '9th': 0},
    12: {'1st': 4, '2nd': 3, '3rd': 3, '4th': 3, '5th': 2, '6th': 1, '7th': 0, '8th': 0, '9th': 0},
    13: {'1st': 4, '2nd': 3, '3rd': 3, '4th': 3, '5th': 2, '6th': 1, '7th': 1, '8th': 0, '9th': 0},
    14: {'1st': 4, '2nd': 3, '3rd': 3, '4th': 3, '5th': 2, '6th': 1, '7th': 1, '8th': 0, '9th': 0},
    15: {'1st': 4, '2nd': 3, '3rd': 3, '4th': 3, '5th': 2, '6th': 1, '7th': 1, '8th': 1, '9th': 0},
    16: {'1st': 4, '2nd': 3, '3rd': 3, '4th': 3, '5th': 2, '6th': 1, '7th': 1, '8th': 1, '9th': 0},
    17: {'1st': 4, '2nd': 3, '3rd': 3, '4th': 3, '5th': 2, '6th': 1, '7th': 1, '8th': 1, '9th': 1},
    18: {'1st': 4, '2nd': 3, '3rd': 3, '4th': 3, '5th': 3, '6th': 1, '7th': 1, '8th': 1, '9th': 1},
    19: {'1st': 4, '2nd': 3, '3rd': 3, '4th': 3, '5th': 3, '6th': 2, '7th': 1, '8th': 1, '9th': 1},
    20: {'1st': 4, '2nd': 3, '3rd': 3, '4th': 3, '5th': 3, '6th': 2, '7th': 2, '8th': 1, '9th': 1},
}

class PlayerClass:
    def __init__(self, level, modifier, cantrip_count = 0, known_spells_count = 0, prepared_spells_count = 0):
        self.level = level
        self.modifier = modifier
        self.cantrip_count = cantrip_count
        self.known_spells_count = known_spells_count
        self.prepared_spells_count = prepared_spells_count
        self.spell_slots = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0, '8': 0, '9': 0}
        self.highest_spell_level = 0
        self.classURL = f"classes/{self.name}/"
        
    def count_cantrips(self): #Counts the number of cantrips known for bard, cleric, druid, sorcerer, warlock, and wizard
        cantripURL = self.classURL + f"levels/{self.level}"
        response = api_2014_request(cantripURL)
        cantrips = int(response['spellcasting']['cantrips_known'])
        self.cantrip_count = cantrips

    
    def count_spells(self): #Counts the number of spells known for bard, ranger, sorcerer, and warlock
        spellURL = self.classURL + f"levels/{self.level}"
        response = api_2014_request(spellURL)
        spell_count = int(response['spellcasting']['spells_known'])
        self.known_spells_count = spell_count
        self.prepared_spells_count = spell_count

    
    def count_spell_slots(self): #Counts the number of spells slots for a class
        spellslotURL = self.classURL + f"levels/{self.level}"
        response = api_2014_request(spellslotURL)
        spellslots = response['spellcasting']
        for i in range(1, 10):
            self.spell_slots[f'{i}'] = int(spellslots[f'spell_slots_level_{i}'])
            if self.spell_slots[f'{i}'] > 0:
                self.highest_spell_level = i


class NonCaster(PlayerClass): #(barbarian, fighter, monk, rogue)
    def __init__(self, level, modifier, name, cantrip_count=0, known_spells_count=0, prepared_spells_count=0):
        self.name = name
        super().__init__(level, modifier, cantrip_count, known_spells_count, prepared_spells_count)
        
    def count_cantrips(self):
        self.cantrip_count = 0
        
    def count_spells(self):
        self.known_spells_count = 0
        self.prepared_spells_count = 0

class Bard(PlayerClass):
    def __init__(self, level, modifier, name = "bard", cantrip_count=0, known_spells_count=0, prepared_spells_count=0):
        self.name = name
        super().__init__(level, modifier, cantrip_count, known_spells_count, prepared_spells_count)
        self.count_spell_slots()

class Cleric(PlayerClass):
    def __init__(self, level, modifier, name = "cleric", cantrip_count=0, known_spells_count=0, prepared_spells_count=0):
        self.name = name
        super().__init__(level, modifier, cantrip_count, known_spells_count, prepared_spells_count)
        self.count_spell_slots()
        
    def count_spells(self): #Prepared casters (cleric, druid, paladin, wizard) can prepare a number of spells equal to their level + spellcasting ability modifier. 
        totalcount = 0      #This function counts the total number of spells available to prepare for these classes.
        for i in range(1,self.highest_spell_level + 1):
            spellURL = self.classURL + f"levels/{i}/spells"
            response = api_2014_request(spellURL)
            totalcount += response['count']
        self.known_spells_count = totalcount
        self.prepared_spells_count = max(1, (self.level + self.modifier))

            

class Druid(PlayerClass):
    def __init__(self, level, modifier, name = "druid", cantrip_count=0, known_spells_count=0, prepared_spells_count=0):
        self.name = name
        super().__init__(level, modifier, cantrip_count, known_spells_count, prepared_spells_count)
        self.count_spell_slots()
        
    def count_spells(self):
        totalcount = 0
        for i in range(1,self.highest_spell_level + 1):
            spellURL = self.classURL + f"levels/{i}/spells"
            response = api_2014_request(spellURL)
            totalcount += response['count']
        self.known_spells_count = totalcount
        self.prepared_spells_count = max(1, (self.level + self.modifier))


class Paladin(PlayerClass):
    def __init__(self, level, modifier, name = "paladin", cantrip_count=0, known_spells_count=0, prepared_spells_count=0):
        self.name = name
        super().__init__(level, modifier, cantrip_count, known_spells_count, prepared_spells_count)
        self.count_spell_slots()
        
    def count_cantrips(self): #Paladins have no cantrips
        self.cantrip_count = 0
        
    def count_spell_slots(self): #Paladins are half casters, so cannot have spells past 5th level
        spellslotURL = self.classURL + f"levels/{self.level}"
        response = api_2014_request(spellslotURL)
        spellslots = response['spellcasting']
        for i in range(1, 6):
            self.spell_slots[f'{i}'] = int(spellslots[f'spell_slots_level_{i}'])
            if self.spell_slots[f'{i}'] > 0:
                self.highest_spell_level = i


    def count_spells(self):
        totalcount = 0
        if self.level > 1:
            for i in range(1,self.highest_spell_level + 1):
                spellURL = self.classURL + f"levels/{i}/spells"
                response = api_2014_request(spellURL)
                totalcount += response['count']
        self.known_spells_count = totalcount
        self.prepared_spells_count = max(1, ((self.level//2) + self.modifier))

    

class Ranger(PlayerClass):
    def __init__(self, level, modifier, name = "ranger", cantrip_count=0, known_spells_count=0, prepared_spells_count=0):
        self.name = name
        super().__init__(level, modifier, cantrip_count, known_spells_count, prepared_spells_count)
        self.count_spell_slots()
        
    def count_cantrips(self): #Rangers have no cantrips
        self.cantrip_count = 0

    def count_spell_slots(self): #Rangers are half casters, so cannot have spells past 5th level
        spellslotURL = self.classURL + f"levels/{self.level}"
        response = api_2014_request(spellslotURL)
        spellslots = response['spellcasting']
        for i in range(1, 6):
            self.spell_slots[f'{i}'] = int(spellslots[f'spell_slots_level_{i}'])
            if self.spell_slots[f'{i}'] > 0:
                self.highest_spell_level = i


class Sorcerer(PlayerClass):
    def __init__(self, level, modifier, name = "sorcerer", cantrip_count=0, known_spells_count=0, prepared_spells_count=0):
        self.name = name
        super().__init__(level, modifier, cantrip_count, known_spells_count, prepared_spells_count)
        self.count_spell_slots()
        
class Warlock(PlayerClass):
    def __init__(self, level, modifier, name = "warlock", cantrip_count=0, known_spells_count=0, prepared_spells_count=0):
        self.name = name
        super().__init__(level, modifier, cantrip_count, known_spells_count, prepared_spells_count)
        self.count_spell_slots()

class Wizard(PlayerClass): #add function to scribe spells
    def __init__(self, level, modifier, name = "wizard", cantrip_count=0, known_spells_count=0, prepared_spells_count=0, addedSpells = 0):
        self.name = name
        super().__init__(level, modifier, cantrip_count, known_spells_count, prepared_spells_count)
        self.count_spell_slots()
        self.addedSpells = addedSpells
        
    def count_spells(self): #Wizards not only prepare spells, but also have a limited amount of spells they can know without adding new spells.
        totalcount = 6 + ((self.level - 1) * 2) + self.addedSpells
        self.known_spells_count = totalcount
        self.prepared_spells_count = max(1, (self.level + self.modifier))
        
def classSelection(chosen_classes): #Gathers the classes, levels, spell level, and spellcasting modifiers for a character. Makes sure it can't exceed level 20.
    spell_level = 0
    total_level = 0
    while total_level < 20:
        playerClass = input("Please choose a class (barbarian, bard, cleric, druid, fighter, monk, paladin, ranger, rogue, sorcerer, warlock, wizard): \n").lower()
        playerLevel = int(input("How many level do you have in this class?\n"))
        if total_level + playerLevel > 20:
            print("Characters cannot have more than 20 levels.")
            continue
        if not playerClass in non_caster:
            ability_score = (api_2014_request(f"classes/{playerClass}")['spellcasting']['spellcasting_ability']['name']).capitalize()
            ability_spell_mod = (int(input(f"What is your {ability_score} score?\n")) - 10)//2
        else:
            ability_spell_mod = 0
        match playerClass:
            case "bard":
                spell_level += playerLevel
                chosen_classes.append(Bard(playerLevel, ability_spell_mod))
            case "cleric":
                spell_level += playerLevel
                chosen_classes.append(Cleric(playerLevel,ability_spell_mod))
            case "druid":
                spell_level += playerLevel
                chosen_classes.append(Druid(playerLevel,ability_spell_mod))
            case "paladin":
                spell_level += (playerLevel//2)
                chosen_classes.append(Paladin(playerLevel, ability_spell_mod))
            case "ranger":
                spell_level += (playerLevel//2) 
                chosen_classes.append(Ranger(playerLevel,ability_spell_mod))
            case "sorcerer":
                spell_level += playerLevel
                chosen_classes.append(Sorcerer(playerLevel, ability_spell_mod))
            case "warlock":
                chosen_classes.append(Warlock(playerLevel, ability_spell_mod))
            case "wizard":
                spell_level += playerLevel
                chosen_classes.append(Wizard(playerLevel, ability_spell_mod))
            case "fighter":
                chosen_classes.append(NonCaster(playerLevel, ability_spell_mod, playerClass))
            case "barbarian":
                chosen_classes.append(NonCaster(playerLevel, ability_spell_mod, playerClass))
            case "monk":
                chosen_classes.append(NonCaster(playerLevel, ability_spell_mod, playerClass))
            case "rogue":
                chosen_classes.append(NonCaster(playerLevel, ability_spell_mod, playerClass))
            case _:
                print("Invalid class.")
                continue
        total_level += playerLevel
        if total_level == 20:
            print("You cannot multiclass due to being at level 20.")
        while True:
            multiclass = input("Do you have levels in another class? (y/n)\n").lower()
            if multiclass == "y":
                break
            elif multiclass == "n":
                print("Character complete.")
                total_level = 21
                break
            else:
                print("Invalid input. Please respond with y or n.")
    return chosen_classes, spell_level

def display_class_details(chosen_classes): #displays the details of each class such as levels, known spells and cantrips, and spell slots. Also notes if character has levels
    warlock = False                        #in warlock
    warlock_spell_slots = [0, "0"]
    non_caster_count = 0
    for c in chosen_classes:
            c.count_cantrips()
            c.count_spells()
            if c.name == "warlock":
                warlock = True
                warlock_spell_slots = [c.highest_spell_level, c.spell_slots[f'{c.highest_spell_level}']]
            if c.name in prepared_caster:
                print(f"Level {c.level} {c.name.capitalize()}. From this class, you know {c.cantrip_count} cantrips and can prepare {c.prepared_spells_count} out of {c.known_spells_count} spells.")
            elif c.name in non_caster:
                print(f"Level {c.level} {c.name.capitalize()}. You have no spells from this.")
                non_caster_count += 1
            else:
                print(f"Level {c.level} {c.name.capitalize()}. From this class, you know {c.cantrip_count} cantrips and {c.known_spells_count} spells.")
    return warlock, warlock_spell_slots, non_caster_count

def class_details(chosen_classes, spell_level): #Calculates how many spells slots a character has, as multiclassing spellcasters has a different spell slot progression
                                                #from single casters. Warlocks work seperately, so are unaffected.
    warlock, warlock_spell_slots, non_caster_count = display_class_details(chosen_classes)
    if len(chosen_classes) > 1:
        if warlock:
            print(f"\nWarlocks have a seperate feature for determining spell slots. You have {warlock_spell_slots[1]} level {warlock_spell_slots[0]} spell slots from Warlock.\n")
            if ((len(chosen_classes) - non_caster_count)-1) == 1:
                for c in chosen_classes:
                    if not c.name in non_caster:
                        print(f"Your {c.name.capitalize()} spellslots are:")
                        for level, slots in c.spell_slots.items():
                            if slots > 0:
                                if level == '1':
                                    print(f"1st: {slots}")
                                elif level == '2':
                                    print(f"2nd: {slots}")
                                elif level == '3':
                                    print(f"3rd: {slots}")
                                else:
                                    print(f"{level}th: {slots}")
            elif ((len(chosen_classes) - non_caster_count)-1) >= 2:
                multiclass_spell_slots = multiclass_spell_prog[spell_level]
                print("Due to multiclassing into multiple spellcasters, your spellslots are:")
                for level, slots in multiclass_spell_slots.items():
                    if slots > 0:
                        print(f"{level}: {slots}")
                        if level == "9th":
                            highest_spell_level = 9
                    else:
                        highest_spell_level = int(level[0]) - 1
                        break
                for c in chosen_classes:
                    if not (c.name in non_caster) and not (c.name == "warlock"):
                        c.spell_slots = multiclass_spell_slots
                        c.highest_spell_level = highest_spell_level
        else:
            if (len(chosen_classes) - non_caster_count) == 1:
                for c in chosen_classes:
                    if not c.name in non_caster:
                        print(f"Your {c.name.capitalize()} spellslots are:")
                        for level, slots in c.spell_slots.items():
                            if slots > 0:
                                if level == '1':
                                    print(f"1st: {slots}")
                                elif level == '2':
                                    print(f"2nd: {slots}")
                                elif level == '3':
                                    print(f"3rd: {slots}")
                                else:
                                    print(f"{level}th: {slots}")
                            else:
                                break
            else:
                multiclass_spell_slots = multiclass_spell_prog[spell_level]
                highest_spell_level = 9
                for c in chosen_classes:
                    if not (c.name in non_caster):
                        c.spell_slots = multiclass_spell_slots
                print("Due to multiclassing into multiple spellcasters, your spellslots are:")
                for level, slots in multiclass_spell_slots.items():
                    if slots > 0:
                        print(f"{level}: {slots}")
                    else:
                        highest_spell_level = int(level[0]) - 1
                        break
                for c in chosen_classes:
                    if not (c.name in non_caster) and not (c.name == "warlock"):
                        c.spell_slots = multiclass_spell_slots
                        c.highest_spell_level = highest_spell_level
    return chosen_classes