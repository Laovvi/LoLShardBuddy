import numpy as np
import pandas as pd

def update():
    # Load list of champions.
    with open('..\Documents\LoLShardBuddy\champion_list.txt') as f:
        champ = f.readlines() 
    champs = []
    for i in champ:
        champs = champs + (i.split(','))

    # Load list of skins not included in counts of skins obtainable by reroll.
    with open('..\Documents\LoLShardBuddy\listnot_included.txt') as f:
        not_included1 = f.readlines()
    not_included = []
    for i in not_included1:
        not_included = not_included + (i.split(','))

    main_dict = {}
    # Takes champion list, iterates through pulling JSON file from ddragon for champion, \
    # creates list of names of all skins for champion, creates dict with single key (champion name) \
    # with a nested dict containing all skin names as keys and whether the skin is to be included in \
    # calculations, the value of the skin, and whether the skin is owned by the player. This nested dict \
    # is then appended to a main nested dict with all champions.
    for i in champs:
        df = pd.read_json("https://ddragon.leagueoflegends.com/cdn/12.7.1/data/en_US/champion/"+i+".json")
        temp_list = []
        temp_dict = {}
        for j in df['data'][i]['skins']:
            temp_list.append(j['name'])
        del temp_list[0]
        for j in temp_list:
            if j in not_included:
                temp_dict[j] = {'incl_in_calc':False, 'value':350, 'owned':True}
            else:
                temp_dict[j] = {'incl_in_calc':True, 'value':350, 'owned':True}
        main_dict[i] = temp_dict
    update.main_dict = main_dict
update()
main_dict = update.main_dict    
print(main_dict)