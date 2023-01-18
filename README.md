**PokemonBot-with-Trie-AVL-Tree-Dijkstra-and-DFS**
# PokemonBotv3

![](Readme%20Screendshots/pokemonbot.png)

I love playing **Pokemon Go**. So, I developed this Bot to help me playing the game on the outside.


# Search Command

The **Search Command** works as a search engine of the system. **!seach [arg]** will bring all the searched Pokemon infomation on the discord output interface. If the argument does match with any name of the Pokemons that are stored in the data structure, the bot starts to match prefix of name of Pokemons with the gives argument. Later it shows the names of the Pokemons that matched with the prefix. If even the prefix does not match, the Bot simply shows **No Result Found** message.

![](Readme%20Screendshots/search_charizard.png)
_Image: The result of searching Charizard_

![](Readme%20Screendshots/search_groudon.png)
_Image: The result of searching Groudon_

![](Readme%20Screendshots/search_yveltal.png)
_Image: The result of searching Yveltal_

![](Readme%20Screendshots/search_giratina.png)
_Image: The result of searching Giratina Altered_

![](Readme%20Screendshots/search_ch.png)
_Image: "ch" matches the prefix of charizard and some other poekmons_

![](Readme%20Screendshots/search_no_result.png)
_Image: Simon pokemon does not exit xD_

# How It Is Happening?

When the program starts running, at first the **Pokemon JSON** data gets fetched by program and stored in both **Trie** (only name) and **AVL Tree**. When an arguments is sent to the Bot, it firstly searchs whether the word exits inside **Trie** or not. If exists, it fetched all the data related to argument from **AVL Tree** and later the bot interface shows the information. If the arguments does not exist inside trie, the bot searches whether the arguments matches any of the prefix with the **Trie data** or not.

# Shortest Path Command

The **!shortest_path [arg1] [arg2]** commands shows the shortest path between two loactions. The location information also gets stored in **Trie**. Just like **search** command, **Shortest Path** command also checks the existence of the location information.

![](Readme%20Screendshots/shortest_path_dhor_bapt.png)
_Image: Shortest Path between Dhoratana and Baptist Church_

![](Readme%20Screendshots/shortest_path_one_correct_one_wrong.png)
_Image: Dhoratana exists in the program but "bapt" does not_

![](Readme%20Screendshots/shortest_path_neither_exits.png)
_Image: Neither "dhor" or "bapt" exists in the program_

# Path Command

**!path [arg]** command shows all location information relative to given argument.

![](Readme%20Screendshots/path_baptist_church.png)
_Image: Path information relative to Baptist Church_

![](Readme%20Screendshots/wrong_path.png)
_Image: No location named "ba" exists in the program_

# How It Is Happening?

After verifying the existence on Point A and Point B. The bot send data to the **Dijkstra Algorithm**. The Algorithm sends the shortest path result to that bot. In the programm the **Priority Queue** is used to increase the speed of the algorithm.

# Areas Command

**!areas** command shows all the names of the location that ares stored in the program.

![](Readme%20Screendshots/areas.png)
_Image: All area names_

# Calling

**!calling** command is used to mention some of my fellow Pokemon Trainers.

![](Readme%20Screendshots/calling.png)
_Image: Use of calling command_

# Earthquake Command

**!eq** command uses **https://www.usgs.gov/** api to fetch previous 24 hours Earth Quake data. Then the bot uses python's folium library to create a world map and points out all the locations where **Earthquakes** occured in past 24 hours with **Tectnoic Plates** locations. Later, the bot sends output as a HTML File.

![](Readme%20Screendshots/eq.png)
_Image: The HTML file that contains the map and Earthquake Data_

![](Readme%20Screendshots/map.png)
_Image: The HTML file opened from a browser_

#Help Command:

It basically works as help center of the Bot.

![](Readme%20Screendshots/help.png)
_Image: The help command_










