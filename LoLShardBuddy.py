import numpy as np
import pandas as pd
import pathlib as Path

def initialize():
    champs = []
    not_included = []
    main_dict = {}
    # Initialize version, champ list, skin list
    # Load list of champions.
    with open(str(Path.Path(__file__).parent)+'\champion_list.txt') as f:
        champ = f.readlines() 
    champs = []
    for i in champ:
        champs = champs + (i.split(','))
        champs = ['Ahri'] #REMOVE after testing

    # Load list of skins not included in counts of skins obtainable by reroll.
    with open(str(Path.Path(__file__).parent)+'\listnot_included.txt') as f:
        not_included1 = f.readlines()
    for i in not_included1:
        not_included = []
        not_included = not_included + [(i.strip().lower())]

    main_dict = {}
    # Takes champion list, iterates through pulling JSON file from ddragon for champion, \
    # creates list of names of all skins for champion, creates dict with single key (champion name) \
    # with a nested dict containing all skin names as keys and whether the skin is to be included in \
    # calculations, the value of the skin, and whether the skin is owned by the player. This nested dict \
    # is then appended to a main nested dict with all champions.
    for i in champs:
        try:
            with open(str(Path.Path(__file__).parent)+'\gamever.txt') as f:
                version = f.readlines() 
            df = pd.read_json("https://ddragon.leagueoflegends.com/cdn/"+str(version[0])\
                +"/data/en_US/champion/"+str(i)+".json")
            temp_list = []
            temp_dict = {}
            for j in df['data'][i]['skins']:
                temp_list.append(j['name'])
            del temp_list[0]
            for j in temp_list:
                if j.lower() in not_included:
                    temp_dict[j] = {'incl_in_calc':False, 'value':0, 'owned':False}
                else:
                    temp_dict[j] = {'incl_in_calc':True, 'value':0, 'owned':False}
        except:
            pass
    main_dict[i] = temp_dict
    return champs, main_dict, temp_list

champs,main_dict,temp_list = initialize()

def add_to_owned():
    #Takes arguments to add to owned list.
    while True:
        temp_champ = input('Enter the name of the champion (Q to quit): ')
        if str(temp_champ).upper() == 'Q':
            break
        elif temp_champ in champs:
            temp_skin = input('Enter the name of the skin (Q to quit): ')
            if temp_skin.upper() == 'Q':
                break
            else:
                if temp_skin in temp_list:
                    main_dict[temp_champ][temp_skin]['owned'] = True
                else:
                    print("Skin not found.")
        else:
            print('Champion not found.')

def update():
    version1 = input('Enter version number (e.g. 12.4.1; Q to quit: ')
    if version1.upper() != 'Q':
        with open(str(Path.Path(__file__).parent)+'\gamever.txt', 'w') as f:
            f.write(version1)
        initialize()

initialize()
print('Welcome to LoLSkinBuddy!')

while True:
    print()
    print('I = Initialize requisite files')
    print('U = Update requisite files')
    print('A = Add Skins to Owned')
    print('G = Get Shard Use Recommendations')
    print('Q = Quit')
    print()
    command = input('What would you like to do?: ')
    if command.upper() == 'I':
        initialize()
    if command.upper() == 'U':
        update()
    if command.upper() == 'A':
        add_to_owned()
    if command.upper() == 'G':
        pass
    if command.upper() == 'Q':
        print('Goodbye :)')
        break

