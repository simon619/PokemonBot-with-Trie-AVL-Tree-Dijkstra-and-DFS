import json
class TrieNode:

    def __init__(self):
        self.children = {}
        self.is_end = False


class Trie:

    def __init__(self):
        pass

    def insert(self, root, word):
        if not root:
            root = TrieNode()

        current_node = root
        for i in range(len(word)):
            if word[i] not in current_node.children:
                current_node.children[word[i]] = TrieNode()
            current_node = current_node.children[word[i]]

        current_node.is_end = True
        return root

    def search(self, root, word):
        current_node = root
        for i in range(len(word)):
            if word[i] not in current_node.children:
                return False
            current_node = current_node.children[word[i]]
        return current_node.is_end

    def start_with(self, root, word):
        current_node = root
        for i in range(len(word)):
            if word[i] not in current_node.children:
                return False
            current_node = current_node.children[word[i]]
        return (current_node, True) if not current_node.is_end else (current_node, False)

    # def traverse(self, last_node):
    #
    #     def dfs(current_node, c):
    #         if current_node.is_end:
    #             return []
    #
    #         list = []
    #         for i in current_node.children.keys():
    #             list.append(dfs(current_node.children[i], i))
    #         for j in range(len(list)):
    #             for k in range(len(list[j])):
    #                 list[j][k] = c + list[j][k]
    #         return list
    #
    #     t_list = [] * len(last_node.children)
    #     counter = 0
    #     for k in last_node.children.keys():
    #         t_list[counter] = k + dfs(last_node.children[k], k)
    #     return t_list

    def dfs(self, current_node, c):

        if current_node.is_end:  # use not.current_node.children for bigger
            return [c]

        list, short_list = [], []
        for i in current_node.children.keys():
            print(i)
            list.append(self.dfs(current_node.children[i], i))
        print(list)
        counter = 0
        for j in range(len(list)):
            for k in range(len(list[j])):
                short_list.append(c + list[j][k])
                # print(short_list)

        return short_list


if __name__ == '__main__':
    obj = Trie()
    head = None
    with open('pokemon_official_data.json') as f:
        pk_data = json.load(f)
    print(type(pk_data))
    # print(obj.start_with(head, 'dino'))
    for i in range(len(pk_data)):
        head = obj.insert(head, str(pk_data[i]['name']))
    (last_node, bool) = obj.start_with(head, 'fuc')
    print(last_node.is_end)
    if bool:
        print(obj.dfs(last_node, 'fuc'))
