import mysql.connector
import requests
import json

link = "https://raw.githubusercontent.com/DetainedDeveloper/Pokedex/master/pokedex_raw/pokedex_raw_array.json"
r = requests.get(link)
all_pokemon_info_json = r.json()

db = mysql.connector.connect(host="localhost", user="root", password="pwroot", database="pokemon_official_database")
mycursor = db.cursor()

pokemon_data_in_json = []
pokemon_name_and_id_json = {}
# number = len(all_pokemon_info_json) - (len(all_pokemon_info_json) - 10)
for i in range(len(all_pokemon_info_json)):
    id = all_pokemon_info_json[i]['id']
    n = all_pokemon_info_json[i]['name']

    print(f"Pokemon Name: {n}")

    h = all_pokemon_info_json[i]['height']
    w = all_pokemon_info_json[i]['weight']
    xp = all_pokemon_info_json[i]['xp']
    img = all_pokemon_info_json[i]['image_url']
    pk_url = all_pokemon_info_json[i]['pokemon_url']

    abilities_name, abilities_bool = [None] * 3, [None] * 3
    for j in range(len(all_pokemon_info_json[i]['abilities'])):
        abilities_name[j], abilities_bool[j] = all_pokemon_info_json[i]['abilities'][j]['name'], all_pokemon_info_json[i]['abilities'][j]['is_hidden']

    hp = all_pokemon_info_json[i]['stats'][0]['base_stat']
    a = all_pokemon_info_json[i]['stats'][1]['base_stat']
    d = all_pokemon_info_json[i]['stats'][2]['base_stat']
    sa = all_pokemon_info_json[i]['stats'][3]['base_stat']
    sd = all_pokemon_info_json[i]['stats'][4]['base_stat']
    sp = all_pokemon_info_json[i]['stats'][5]['base_stat']

    types = [None] * 2
    for j in range(len(all_pokemon_info_json[i]['types'])):
        types[j] = all_pokemon_info_json[i]['types'][j]['name']

    mycursor.execute("INSERT INTO pokemon_official (id, name, height, weight, xp, image_url, pokemon_url, abilities_1_name, abilities_1_bool, abilities_2_name, abilities_2_bool, abilities_3_name, abilities_3_bool, hp, attack, defence, special_attack, special_defence, speed, type_1, type_2) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                     (id, n, h, w, xp, img, pk_url, abilities_name[0], abilities_bool[0], abilities_name[1], abilities_bool[1], abilities_name[2], abilities_bool[2], hp, a, d, sa, sd, sp, types[0], types[1]))
    db.commit()

    pokemon_data_in_json.append({'id': id, 'name': n, 'pk_height': h, 'pk_weight': w, 'xp': xp, 'image_url': img, 'pokemon_url': pk_url, 'abilities_1_name': abilities_name[0], 'abilities_1_bool': abilities_bool[0], 'abilities_2_name': abilities_name[1], 'abilities_2_bool': abilities_bool[1], 'abilities_3_name': abilities_name[2], 'abilities_3_bool': abilities_bool[2], 'hp': hp, 'attack': a, 'defence': d, 'special_attack': sa, 'special_defence': sd, 'speed': sp, 'type_1': types[0], 'type_2': types[1]})
    pokemon_name_and_id_json[n] = id

with open('pokemon_official_data.json', 'w') as file:
    json.dump(pokemon_data_in_json, file, indent=2)

with open('pokemon_name_id_data.json', 'w') as file:
    json.dump(pokemon_name_and_id_json, file, indent=2)

print("Insert Completed")



