import javalang

class Mytree:
    privacy_key = ["public", "private", "protected"]
    useless_key = ["static", "final","abstract"]
    def __init__(self, father, tokens):
        self.father = father
        self.nodes = []
        self.value = "tree"
        flag_begin = -1
        flag_depth = 0
        for index, token in enumerate(tokens):
            if token.value == "(" or token.value == "{":
                
                if flag_depth == 0:
                    self.nodes.append(token)
                    flag_begin = index + 1
                flag_depth += 1
            if token.value == ")" or token.value == "}":
                flag_depth -= 1
                if flag_depth == 0:
                    pass
                    self.nodes.append(Mytree(self, tokens[flag_begin: index]))
            if flag_depth == 0:
                self.nodes.append(token)
    
    def display(self, offset):
        for item in self.nodes:
            if type(item) != Mytree:
                print(offset,item.value, end=" ")
            else:
                item.display(offset + 1)
    
    def to_string(self):
        result = ""
        for item in self.nodes:
            if type(item) != Mytree:
                result += item.value + " "
            else:
                result += item.to_string() + " "
        return result

    def to_list(self):
        result = []
        for item in self.nodes:
            if type(item) != Mytree:
                result.append(item.value)
            else:
                result += item.to_list()
        return result
    
    def to_tokens(self):
        result = []
        for item in self.nodes:
            if type(item) != Mytree:
                result.append(item)
            else:
                result += item.to_tokens()
        return result
    
    def to_masked_list(self):
        tokens = self.to_tokens()
        dictionary = {}
        counter = 0
        for token in tokens:
            name = str(type(token)).split(".")[-1].split("'")[0]
            if name == "Identifier":
                dictionary.setdefault(token.value, name + str(len(dictionary)))
        result = []
        for token in tokens:
            name = str(type(token)).split(".")[-1].split("'")[0]
            if name == "Identifier":
                result.append(dictionary[token.value])
            else:
                result.append(token.value)
        return result


    def get_subtree(self):
        result = []
        for index, item in enumerate(self.nodes):
            if type(item) != Mytree:
                if item.value in Mytree.privacy_key:
                    for i in range(index, len(self.nodes)):
                        if type(self.nodes[i]) != Mytree and (self.nodes[i].value == "}" or self.nodes[i].value == ";"):
                            temp_tree = Mytree(None, self.nodes[index:i + 1])
                            result.append(temp_tree)
                            break
            else:
                result += item.get_subtree()
        return result
    
    def get_classified_subtree(self):
        result = self.get_subtree()
        result_class = []
        result_interface = []
        result_assign = []
        result_rest = []
        for r in result:
            nodes = r.nodes.copy()
            for index, n in enumerate(nodes):
                if n.value in Mytree.useless_key:
                    del nodes[index]
            if nodes[1].value == "class":
                result_class.append(r)
            elif nodes[1].value == "interface":
                result_interface.append(r)
            elif nodes[-1].value == ";":
                result_assign.append(r)
            else:
                result_rest.append(r)
        return result_class,result_interface,result_rest

data = open("data/107733.txt").read()
tokens = javalang.tokenizer.tokenize(data)
l = list(tokens)
mytree = Mytree(None, l)
# mytree.display(0)
# print(mytree.to_string())
rs = mytree.get_classified_subtree()[2]
for r in rs:
    print(r.to_string())
pass

path = "data"

import os

dirs = os.listdir(path)

data = []
methods_list = []
for file in dirs:
    f = open(os.path.join(path,file))
    data = f.read()
    try:
        tokens = javalang.tokenizer.tokenize(data)
        tokens = list(tokens)
        tree = Mytree(None, tokens)
        methods_list += tree.get_classified_subtree()[2]
    except :
        print("Error at",os.path.join(path,file))

methods_list = [m.to_masked_list() for m in methods_list]
import json
f = open("all_methods.txt", "w")
for m in methods_list:
    json_str = json.dumps(m) + '\n'
    f.write(json_str)
