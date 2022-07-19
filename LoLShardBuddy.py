import numpy as np
import pandas as pd
champs = []
not_included = []
main_dict = {}

def update():
    # Load list of champions.
    with open('..\Documents\LoLShardBuddy\champion_list.txt') as f:
        champ = f.readlines() 
    champs = []
    for i in champ:
        champs = champs + (i.split(','))
        champs = ['Ahri']

    # Load list of skins not included in counts of skins obtainable by reroll.
    with open('..\Documents\LoLShardBuddy\listnot_included.txt') as f:
        not_included1 = f.readlines()
    for i in not_included1:
        not_included = not_included + (i.split(',').lower())

    main_dict = {}
    # Takes champion list, iterates through pulling JSON file from ddragon for champion, \
    # creates list of names of all skins for champion, creates dict with single key (champion name) \
    # with a nested dict containing all skin names as keys and whether the skin is to be included in \
    # calculations, the value of the skin, and whether the skin is owned by the player. This nested dict \
    # is then appended to a main nested dict with all champions.
    for i in champs:
        try:
            df = pd.read_json("https://ddragon.leagueoflegends.com/cdn/12.7.1/data/en_US/champion/"+str(i)+".json")
            temp_list = []
            temp_dict = {}
            for j in df['data'][i]['skins']:
                temp_list.append(j['name'])
            del temp_list[0]
            for j in temp_list:
                if j.lower() in not_included:
                    temp_dict[j] = {'incl_in_calc':False, 'value':0, 'owned':True}
                else:
                    temp_dict[j] = {'incl_in_calc':True, 'value':0, 'owned':True}
        except:
            pass
        main_dict[i] = temp_dict
    return champs,main_dict

def add_to_owned():
    while True:
        temp_champ = input('Enter the name of the champion (Q to quit): ')
        if str(temp_champ).upper() == 'Q':
            break
        elif temp_champ in champs:
            temp_skin = input('Enter the name of the skin (Q to quit): ')
            if temp_skin.upper() == 'Q':
                break
            else:
                if temp_skin in main_dict[temp_champ]:
                    print(temp_skin)
                else:
                    print("Skin not found.")
        else:
            print('Champion not found.')

champs,main_dict = update()
print(main_dict)
print(champs)
add_to_owned()