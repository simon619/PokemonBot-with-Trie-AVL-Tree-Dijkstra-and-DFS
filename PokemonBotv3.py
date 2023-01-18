import discord
import json
import csv
import folium
import os
import socket
import requests
from discord.ext import commands
from datetime import date, timedelta


class RSACrypto:

    def __init__(self, public_key, private_key, p, q):
        self.e = public_key
        self.d = private_key
        self.p = p
        self.q = q
        self.n = self.p * self.q
        self.phi = (self.p - 1) * (self.q - 1)
        self.alpha_dic = {}
        self.forbidder = [91, 92, 93, 40, 39, 41, 123, 125]

    def __build_dic_table__(self):
        i = 0
        pointer = 0
        while (i < 95):
            if i + 32 not in self.forbidder:
                self.alpha_dic[chr(i + 32)] = pointer
                pointer += 1
            i += 1

    def __conversion__(self, st):
        main_string_list = [0] * len(st)
        main_string_list = [self.alpha_dic[st[i]] for i in range(len(st))]
        return main_string_list

    def __euler_extend__(self, phi1, phi2, e, d):
        if e == 1:
            return d
        else:
            div = phi1 // e
            a, b = e * div, d * div
            x, y = phi1 - a, phi2 - b
            if x < 0:
                x = x % self.phi
            if y < 0:
                y = y % self.phi
            return self.__euler_extend__(e, d, x, y)

    def __decryption__(self, st):
        st_to_num_conv = self.__conversion__(st)
        de_string_list = [0] * len(st_to_num_conv)
        self.d = self.__euler_extend__(self.phi, self.phi, self.e, 1)
        de_string_list = [(st_to_num_conv[i] ** self.d) % self.n for i in range(len(st_to_num_conv))]
        de_num, de_st = self.__list_to_string__(de_string_list)
        return de_num, de_st

    def __list_to_string__(self, list):
        num, st = '', ''
        for i in list:
            num += str(i)
            st += [j for j in self.alpha_dic if self.alpha_dic[j] == i][0]
        return num, st


class TrieNode:

    def __init__(self):
        self.children = {}
        self.is_end = False


class Trie:

    def __init__(self):
        pass

    def __insertion__(self, root, word):
        if not root:
            root = TrieNode()

        current_node = root
        for i in range(len(word)):
            if word[i] not in current_node.children:
                current_node.children[word[i]] = TrieNode()
            current_node = current_node.children[word[i]]

        current_node.is_end = True
        return root

    def __search__(self, root, word):
        current_node = root
        for i in range(len(word)):
            if word[i] not in current_node.children:
                return False
            current_node = current_node.children[word[i]]
        return current_node.is_end

    def __start_with__(self, root, word):
        current_node = root
        for i in range(len(word)):
            if word[i] not in current_node.children:
                return [current_node, False]
            current_node = current_node.children[word[i]]
        return [current_node, True] if not current_node.is_end else [current_node, False]

    def __dfs_search__(self, current_node, c):

        if current_node.is_end:  # use not.current_node.children for bigger
            return [c]

        list, short_list = [], []
        for i in current_node.children.keys():
            list.append(self.__dfs_search__(current_node.children[i], i))
        for j in range(len(list)):
            for k in range(len(list[j])):
                short_list.append(c + list[j][k])

        return short_list


class AVL:

    def __init__(self, id, name, pk_height, pk_weight, xp, image_url, pokemon_url, abilities_1_name, abilities_1_bool,
                 abilities_2_name, abilities_2_bool, abilities_3_name, abilities_3_bool, hp, attack, defence,
                 special_attack, special_defence, speed, type_1, type_2):
        self.id = id
        self.name = name
        self.pk_height = pk_height
        self.pk_weight = pk_weight
        self.xp = xp
        self.image_url = image_url
        self.pokemon_url = pokemon_url
        self.abilities_1_name = abilities_1_name
        self.abilities_1_bool = abilities_1_bool
        self.abilities_2_name = abilities_2_name
        self.abilities_2_bool = abilities_2_bool
        self.abilities_3_name = abilities_3_name
        self.abilities_3_bool = abilities_3_bool
        self.hp = hp
        self.attack = attack
        self.defence = defence
        self.special_attack = special_attack
        self.special_defence = special_defence
        self.speed = speed
        self.type_1 = type_1
        self.type_2 = type_2
        self.left = None
        self.right = None
        self.height = 1


class AVLTree:
    def __init__(self):
        pass

    def __insertion__(self, node, data):
        if node is None:
            return AVL(data['id'], data['name'], data['pk_height'], data['pk_weight'], data['xp'], data['image_url'],
                       data['pokemon_url'], data['abilities_1_name'], data['abilities_1_bool'],
                       data['abilities_2_name'], data['abilities_2_bool'], data['abilities_3_name'],
                       data['abilities_3_bool'], data['hp'], data['attack'], data['defence'], data['special_attack'],
                       data['special_defence'], data['speed'], data['type_1'], data['type_2'])
        elif node.id > int(data['id']):
            node.left = self.__insertion__(node.left, data)
        elif node.id < int(data['id']):
            node.right = self.__insertion__(node.right, data)

        node.height = self.__height__(node)
        balance = self.__height__(node.left) - self.__height__(node.right)

        if balance > 1:
            if node.left.id > int(data['id']):
                return self.__right_rotation__(node)
            else:
                node.left = self.__left_rotation__(node.left)
                return self.__right_rotation__(node)
        if balance < -1:
            if node.right.id < int(data['id']):
                return self.__left_rotation__(node)
            else:
                node.right = self.__right_rotation__(node.right)
                return self.__left_rotation__(node)

        return node

    def __height__(self, node):
        if node is None:
            return 0
        else:
            left = self.__height__(node.left)
            right = self.__height__(node.right)
            return 1 + max(left, right)

    def __right_rotation__(self, node):
        lefty = node.left
        temp = lefty.right
        lefty.right = node
        node.left = temp
        node.height = self.__height__(node)
        lefty.height = self.__height__(lefty)
        return lefty

    def __left_rotation__(self, node):
        righty = node.right
        temp = righty.left
        righty.left = node
        node.right = temp
        node.height = self.__height__(node)
        righty.height = self.__height__(righty)
        return righty

    def __minimum_value__(self, node):
        if node.left is None or node is None:
            return node
        else:
            return self.__minimum_value__(node.left)

    def __noorder_traversal__(self, node):
        current_node = node
        q = [current_node]

        def __traversal__(q, traversal):
            if q:
                info = q.pop(0)
                traversal += str(info.name) + '->'
                if info.left:
                    q.append(info.left)
                if info.right:
                    q.append(info.right)
                traversal = __traversal__(q, traversal)
            return traversal

        result = __traversal__(q, '')
        return result

    def __search__(self, node, id):
        if not node:
            return None
        elif node.id == id:
            return node
        elif node.id < id:
            return self.__search__(node.right, id)
        else:
            return self.__search__(node.left, id)


class Vertex:

    def __init__(self, vertex, weight=0):
        self.vertex = vertex
        self.weight = weight


class Dijkstra:

    def __init__(self, graph, n, area_id_dic):
        self.number_of_areas = n
        self.adj_list = [[] for i in range(n)]
        self.priority_que = []
        self.area_id_dic = area_id_dic
        for (source, destination, weight) in graph:
            self.adj_list[source].append((destination, weight))

    def __dijkstra__(self, source, final_destination):

        def __heapify__(priority_que, n, pointer):
            minimum = pointer
            left, right = 2 * pointer + 1, 2 * pointer + 2

            if left < n and priority_que[left].weight < priority_que[minimum].weight:
                minimum = left

            if right < n and priority_que[right].weight < priority_que[minimum].weight:
                minimum = right

            if minimum != pointer:
                priority_que[minimum], priority_que[pointer] = priority_que[pointer], priority_que[minimum]
                __heapify__(priority_que, n, minimum)

        def __insert__(node):
            if not self.priority_que:
                self.priority_que.append(node)

            else:
                self.priority_que.append(node)
                for i in range(len(self.priority_que) // 2 - 1, -1, -1):
                    __heapify__(self.priority_que, len(self.priority_que), i)

        def __delete__():
            if not self.priority_que:
                print("Not Possible")
                return None

            else:
                self.priority_que[0], self.priority_que[len(self.priority_que) - 1] = self.priority_que[
                                                                                          len(self.priority_que) - 1], \
                                                                                      self.priority_que[0]
                temp = self.priority_que[len(self.priority_que) - 1]
                del self.priority_que[-1]
                for i in range(len(self.priority_que) // 2 - 1, -1, -1):
                    __heapify__(self.priority_que, len(self.priority_que), i)
                return temp

        __insert__(Vertex(source))
        distance = [999999] * len(self.adj_list)
        distance[source] = 0
        visited = [False] * len(self.adj_list)
        visited[source] = True
        previous_vertex = [-1] * len(self.adj_list)

        while self.priority_que:
            current_vertex = __delete__()
            current_vertex = current_vertex.vertex
            for (neighbor, weight) in self.adj_list[current_vertex]:
                if not visited[neighbor] and (distance[current_vertex] + weight) < distance[neighbor]:
                    distance[neighbor] = distance[current_vertex] + weight
                    previous_vertex[neighbor] = current_vertex
                    __insert__(Vertex(neighbor, weight))
            visited[current_vertex] = True

        def __traversal__(prev, i, n):
            if i >= 0:
                __traversal__(prev, prev[i], n)
                path_list.append(i)

        if final_destination == "path":
            path_list, final_result, counter = [], [''] * (self.number_of_areas - 1), 0
            for neighbor in range(len(self.adj_list)):
                if neighbor != source and distance[neighbor] != 999999:
                    __traversal__(previous_vertex, neighbor, len(self.adj_list))
                    path_string = ''
                    for i in path_list:
                        path_string += self.area_id_dic[str(i)] + '->'
                    final_result[
                        counter] = f'Source: {self.area_id_dic[str(source)]} -> Destination: {self.area_id_dic[str(neighbor)]}, Cost: {distance[neighbor]} meter, Route: {path_string} \n'
                    counter += 1
                    path_list.clear()
            return final_result

        else:
            path_list = []
            if final_destination != source and distance[final_destination] != 999999:
                __traversal__(previous_vertex, final_destination, len(self.adj_list))
                path_string = ''
                for i in path_list:
                    path_string += self.area_id_dic[str(i)] + '>'
            return f'Source: {self.area_id_dic[str(source)]} -> Destination: {self.area_id_dic[str(final_destination)]}, Cost: {distance[final_destination]} meter, Route: {path_string}'


class BotCommand:

    def __init__(self, com, nameList, Graph, numberOfAreas, raw_area_id_data, pokemonOfficialData, pokemonNameIdData):
        self.com = com
        self.Graph = Graph
        self.numberOfAreas = numberOfAreas
        self.raw_area_id_data = raw_area_id_data
        self.nameList = nameList
        self.tanzim_id = '598189420717277204'
        self.uzumaki_id = '760506256049307690'
        self.chief_id = '517727081090646048'
        self.general_id_BotTesting = 764925464153423886
        self.dk_obj = Dijkstra(self.Graph, self.numberOfAreas, self.raw_area_id_data[0])
        self.avl_obj = AVLTree()
        self.pk_root = None
        self.pokemonOfficialData = pokemonOfficialData
        self.pokemonNameIdData = pokemonNameIdData
        self.trie_root = None
        self.trie_obj = Trie()
        self.insert_pokemon_data()

    def insert_pokemon_data(self):
        for i in range(len(self.pokemonOfficialData)):
            self.pk_root = self.avl_obj.__insertion__(self.pk_root, self.pokemonOfficialData[i])
            self.trie_root = self.trie_obj.__insertion__(self.trie_root, self.pokemonOfficialData[i]['name'])
        for area in self.raw_area_id_data[1].keys():
            self.trie_root = self.trie_obj.__insertion__(self.trie_root, str(area))

    def network_detail(self):
        hostname = socket.gethostname()
        device_ip = socket.gethostbyname(hostname)
        print('')
        print("Hosting By:")
        print(f"Device Name: {hostname}")
        print(f"Device IPv4 Address: {device_ip}")
        print("Bot Version PokemonBotv3")
        print("Gotta Catch 'em All")
        print("Press [ctrl + c] to Close The Server")
        print('')

    def discord_commands(self):
        @self.com.event
        async def on_ready():
            self.network_detail()

        @self.com.command()
        async def shortest_path(ctx, arg1, arg2):
            temp1, temp2 = str(arg1), str(arg2)
            src, des = temp1.lower(), temp2.lower()
            bool1, bool2 = self.trie_obj.__search__(self.trie_root, src), self.trie_obj.__search__(self.trie_root,
                                                                                                   des)
            if bool1 and bool2:
                result = self.dk_obj.__dijkstra__(self.raw_area_id_data[1][src], self.raw_area_id_data[1][des])
                await ctx.send(f'Shortest Path: [{result}]')

            if not bool1:
                res1 = self.trie_obj.__start_with__(self.trie_root, src)
                if res1[1]:
                    found = self.trie_obj.__dfs_search__(res1[0], src)
                    st = ''
                    for result in found:
                        st += result + ', '
                    await ctx.send(f"Found Results for [{src}]: {st}")
                else:
                    await ctx.send(f"No Result Found \U0001FE0F")

            if not bool2:
                res2 = self.trie_obj.__start_with__(self.trie_root, des)
                if res2[1]:
                    found = self.trie_obj.__dfs_search__(res2[0], des)
                    st = ''
                    for result in found:
                        st += result + ', '
                    await ctx.send(f"Found Results for [{des}]: {st}")
                else:
                    await ctx.send(f"No Result Found \U0001FE0F")

            print(f"{ctx.author} Has Used Shorted Path Command")
            self.network_detail()

        @self.com.command()
        async def path(ctx, arg):
            temp = str(arg)
            src = temp.lower()
            if self.trie_obj.__search__(self.trie_root, src):
                result_list = self.dk_obj.__dijkstra__(self.raw_area_id_data[1][src], "path")

                with open("path.txt", "w") as file:
                    file.writelines(result_list)

                with open("path.txt", "rb") as file:
                    await ctx.send("This Text Contains Your Result:", file=discord.File(file, "path.txt"))

            else:
                res = self.trie_obj.__start_with__(self.trie_root, src)
                if res[1]:
                    found = self.trie_obj.__dfs_search__(res[0], src)
                    st = ''
                    for result in found:
                        st += result + ', '
                    await ctx.send(f"Found Results for [{src}]: {st}")
                else:
                    await ctx.send(f"No Result Found \U0001FE0F")

            print(f"{ctx.author} Has Used Path Command")
            self.network_detail()

        @self.com.command()
        async def info(ctx):
            await ctx.send(ctx.guild)
            await ctx.send(ctx.author)
            await ctx.send(ctx.message.id)

            print(f"{ctx.author} Has Used Info Command")
            self.network_detail()

        @self.com.command()
        async def areas(ctx):
            st = ''
            for areas in self.raw_area_id_data[0].keys():
                st += str(self.raw_area_id_data[0][areas]) + ', '
            await ctx.send(f"Areas in My Database: {st}")

            print(f"{ctx.author} Has Used Path Command")
            self.network_detail()

        @self.com.command()
        async def search(ctx, arg):
            temp = str(arg)
            lower_case_pk_arg = temp.lower()
            if self.trie_obj.__search__(self.trie_root, lower_case_pk_arg):
                poke_info_node = self.avl_obj.__search__(self.pk_root, int(self.pokemonNameIdData[lower_case_pk_arg]))
                in_kg = poke_info_node.pk_weight / 10
                pk_img_url = f"Pokemon Images//{poke_info_node.id}.png"
                file_name = f"{poke_info_node.id}.png"
                thumbnail_img = f"attachment://{file_name}"
                file = discord.File(pk_img_url, filename=file_name)
                embed = discord.Embed(
                    title='Searched Pokemon Information',
                    description=f'The Searched Pokemon {poke_info_node.name} Has Been Found in Our Database',
                    colour=discord.Colour.red()
                )
                embed.set_thumbnail(url=thumbnail_img)
                embed.add_field(
                    name='Name: ',
                    value=f'{poke_info_node.name.capitalize()}',
                    inline=True
                )
                embed.add_field(
                    name='Pokemon ID: ',
                    value=f'{poke_info_node.id}',
                    inline=True
                )
                embed.add_field(
                    name='Height: ',
                    value=f'{poke_info_node.pk_height}cm',
                    inline=True
                )
                embed.add_field(
                    name='Weight: ',
                    value=f'{in_kg}kg',
                    inline=True
                )
                embed.add_field(
                    name='XP: ',
                    value=f'{poke_info_node.xp}',
                    inline=True
                )
                embed.add_field(
                    name='Pokemon URL: ',
                    value=f'{poke_info_node.pokemon_url}',
                    inline=False
                )
                embed.add_field(
                    name='Ability 1: ',
                    value=f'{poke_info_node.abilities_1_name}',
                    inline=True
                )
                embed.add_field(
                    name='Ability 2: ',
                    value=f'{poke_info_node.abilities_2_name}',
                    inline=True
                )
                embed.add_field(
                    name='Ability 3: ',
                    value=f'{poke_info_node.abilities_3_name}',
                    inline=True
                )
                embed.add_field(
                    name='HP: ',
                    value=f'{poke_info_node.hp}',
                    inline=True
                )
                embed.add_field(
                    name='Attack: ',
                    value=f'{poke_info_node.attack}',
                    inline=True
                )
                embed.add_field(
                    name='Defence: ',
                    value=f'{poke_info_node.defence}',
                    inline=True
                )
                embed.add_field(
                    name='Special Attack: ',
                    value=f'{poke_info_node.special_attack}',
                    inline=True
                )
                embed.add_field(
                    name='Special Defence: ',
                    value=f'{poke_info_node.special_defence}',
                    inline=True
                )
                embed.add_field(
                    name='Type 1: ',
                    value=f'{poke_info_node.type_1}',
                    inline=False
                )
                embed.add_field(
                    name='Type 2: ',
                    value=f'{poke_info_node.type_2}',
                    inline=True
                )

                await ctx.send(file=file, embed=embed)

            else:
                res = self.trie_obj.__start_with__(self.trie_root, lower_case_pk_arg)
                if res[1]:
                    found = self.trie_obj.__dfs_search__(res[0], lower_case_pk_arg)
                    st = ''
                    for result in found:
                        st += result + ', '
                    await ctx.send(f"Found Results for [{lower_case_pk_arg}]: {st}")
                else:
                    await ctx.send(f"No Result Found \U0001FE0F")

            print(f"{ctx.author} Has Used Search Command")
            self.network_detail()

        @self.com.command()
        async def calling(ctx):
            if str(ctx.author) in self.nameList:
                await ctx.send(f'Calling <@{self.chief_id}>, <@{self.tanzim_id}> and <@{self.uzumaki_id}>')

                print(f"{ctx.author} Has Used Calling Command")
                self.network_detail()

        @self.com.command()
        async def help(ctx):
            help_img_url = "Pokemon Images//pokeball.png"
            file = discord.File(help_img_url, filename='pokeball.png')
            embed = discord.Embed(
                title='PokemonBot Commands',
                description=f"Welcome to PokemonBot Customer Service xD. Bot Version: PokemonBotv3",
                colour=discord.Colour.red()
            )
            embed.set_thumbnail(url="attachment://pokeball.png")
            embed.add_field(
                name='!help',
                value='List of All Commands',
                inline=False
            )
            embed.add_field(
                name='!shortest_path',
                value='Format: !shortest_path [arg1] [arg2]. This Gives the Shortest Path Between Two Locations',
                inline=False
            )
            embed.add_field(
                name='!path',
                value='Format: !shortest_path [arg]. This Gives the Path Between Given Location and Other Locations',
                inline=False
            )
            embed.add_field(
                name='!info',
                value='Format: !info. This Shows Basic Information',
                inline=False
            )
            embed.add_field(
                name='!search',
                value='Format: !search [arg]. This Shows Search Results',
                inline=False
            )
            embed.add_field(
                name='!calling',
                value='Format: !calling. This Mentions Certain People',
                inline=False
            )
            embed.add_field(
                name='!areas',
                value='Format: !areas. This Shows the Name of Areas',
                inline=False
            )
            embed.add_field(
                name='!eq',
                value='Format: !eq. This Shows All The Earthquake Information Around The World That Occurred In Past 24hrs As A HTML File. Open It With You Browser. Source: https://earthquake.usgs.gov',
                inline=False
            )

            await ctx.send(file=file, embed=embed)

            print(f"{ctx.author} Has Used Help Commad")
            self.network_detail()

        @self.com.command()
        async def eq(ctx):
            earth_map = folium.Map(location=[0, 0], zoom_start=2)

            time_today = date.today()
            time_yesterday = date.today() - timedelta(days=1)
            csv_url = f"https://earthquake.usgs.gov/fdsnws/event/1/query?format=csv&starttime={time_yesterday}&endtime{time_today}"
            eq_list = list(csv.DictReader(requests.get(csv_url).text.splitlines()))

            for i in range(len(eq_list)):
                pop_up = f"Magnitude: {eq_list[i]['mag']}, Type: {eq_list[i]['magType']}, Depth: {eq_list[i]['depth']}, Time: {eq_list[i]['time']}"
                lat, lng = float(eq_list[i]['latitude']), float(eq_list[i]['longitude'])
                rad = 100000 * float(eq_list[i]['mag'])
                marker = folium.Circle(radius=rad, location=(lat, lng), color='red', fill=False, popup=pop_up)
                earth_map.add_child(marker)

            print("Earthquake Data Added")

            with open('EarthQuake Data//tectonicplates.csv', 'r') as csv_file:
                tectonic_plates_data = csv.reader(csv_file)

                for line in tectonic_plates_data:
                    plate, lat, lng = line[0], float(line[1]), float(line[2])
                    marker = folium.Circle(radius=0.1, location=(lat, lng), color='yellow', fill=True)
                    earth_map.add_child(marker)

            print("Tectonic Plate Data Added")

            eq_file_name = f"eq_data_{time_today}.html"
            eq_data_saved_link = f"EarthQuake Data//{eq_file_name}"

            if os.path.isfile(eq_data_saved_link):
                print("File Already Exists.....")
                os.remove(eq_data_saved_link)
                print("File Has Been Removed")
                earth_map.save(eq_data_saved_link)
            else:
                earth_map.save(eq_data_saved_link)

            with open(eq_data_saved_link, "rb") as file:
                await ctx.send("This HTML Contains Your Result. Download It Then Open It With A Browser:", file=discord.File(file, eq_file_name))

            print("File Has Been Created")
            print(f"{ctx.author} Has Used Eq Command")
            self.network_detail()

        @self.com.command()
        async def logo(ctx):
            logo_link = "My Logo//logo.txt"

            with open(logo_link, "rb") as file:
                await ctx.send("The Dark One", file=discord.File(file, "logo.txt"))



if __name__ == '__main__':
    intent = discord.Intents.default()
    intent.message_content = True
    intent.members = True

    name_list = ['MegaMagikarp69#1357', 'Uzumakii#1598', 'Chief#6121']

    area_id_link = 'Collect Jessore Data//area_id_data.json'
    area_distance_link = 'Collect Jessore Data//jessore_distance_data.json'
    pokemon_official_data_link = 'Collect Pokemon Data//pokemon_official_data.json'
    pokemon_name_id_data_link = 'Collect Pokemon Data//pokemon_name_id_data.json'

    with open(area_id_link) as f:
        area_id_data = json.load(f)

    with open(area_distance_link) as f:
        distance_data = json.load(f)

    with open(pokemon_official_data_link) as f:
        pokemon_official_data = json.load(f)

    with open(pokemon_name_id_data_link) as f:
        pokemon_name_id_data = json.load(f)

    number_of_areas = len(area_id_data[0])
    G = []
    for i in range(len(distance_data)):
        t1, t2 = distance_data[i]['source'], distance_data[i]['destination']
        temp = [area_id_data[1][t1], area_id_data[1][t2], int(distance_data[i]['distance'])]
        G.append(temp)

    com = commands.Bot(command_prefix='!', intents=intent)
    com.remove_command('help')
    obj_command = BotCommand(com, name_list, G, number_of_areas, area_id_data, pokemon_official_data,
                             pokemon_name_id_data)
    obj_command.discord_commands()

    encypted_result_string = '&xAJ&+n2&xtJj,"5&xQ565tYjQ1Pw%5up1M2w_Y$bP-dqjMUobx%|8X#aEYc.7a-A,5fBU5p'
    crypto_obj = RSACrypto(public_key=5, private_key=0, p=3, q=29)
    crypto_obj.__build_dic_table__()
    dencypted_result_num, decypted_result_string = crypto_obj.__decryption__(encypted_result_string)
    com.run(decypted_result_string)
