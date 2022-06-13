from random import random, seed

class Node:
    def __init__(self, id, args={}):
        self.id = id
        self.args = args

    def __str__(self):
        return self.id
        if self.args == {}:
            return self.id
        return self.id+"{"+",".join([str(k)+":"+str(v) for k,v in self.args.items()])+"}"
    
    def __eq__(self, __o):
        return self.id == __o

class Rule:
    def __init__(self, node, to1, to2=None, chance=1):
        self.node = node
        self.to1 = to1
        self.to2 = to2
        self.chance = chance
    
    def next(self):
        if random() < self.chance:
            return self.to1
        return self.to2

    def __str__(self):
        if self.to2 == None:
            return str(self.node) + " := "+ "".join([str(t) for t in self.to1]) 
        return str(self.node) + " ("+str(self.chance)+") := "+"".join([str(t) for t in self.to1])+" | "+"".join([str(t) for t in self.to2])

class CFG:
    rules = {}
    vocabulary = {}
    seed = None
    steps = None
    leaf_color = None
    trunk_color = None

    def __init__(self, start=None, vocabulary=None):
        if start:
            self._state = start
        if vocabulary:
            self.vocabulary = {node.id:node for node in vocabulary}

    def addRule(self, rule):
        self.rules[rule.node.id] = rule
    
    def translate(self, word):
        return [self.vocabulary[letter] for letter in word]
    
    def advance(self, n=None):
        if n == None:
            n = self.steps
        for _ in range(n):
            #print(self.state())
            self._advance()
    
    def _advance(self):
        new_state = []
        for node in self._state:
            if node.id in self.rules:
                nexts = self.rules[node.id].next()
                for next in nexts:
                    new_state.append(next)
            else:
                new_state.append(node)
        self._state = new_state
        
    def state(self):
        return "".join([str(node) for node in self._state])
    
    def readRule(self, line):
        line = line.strip()
        _from, to = line.split(":=")
        if len(_from.split()) > 1:
            _from, chance = _from.split()
            _from = self.vocabulary[_from] 
            chance = float(chance[1 :-1])
            to1, to2 = to.split("|")
            to1 = [self.vocabulary[next] for next in to1]
            to2 = [self.vocabulary[next] for next in to2]
            return Rule(_from, to1, to2, chance)

        to = [self.vocabulary[next] for next in to]
        _from = self.vocabulary[_from]

        return Rule(_from, to)

    def _loadRules(self, lines):
        for line in lines:
                self.addRule(self.readRule(line))

    def loadRules(self, filename):
        with open(filename, "r") as file:
            self._loadRules(file.readlines())
    
    def loadCFG(self,fileName):
        with open(fileName, "r") as file:
            for line in file.readlines():
                line.strip()
                try:
                    kind,rest = line.split(" ",1)
                except:
                    continue
                if kind == "NODE":
                    if len(rest.split()) > 1:
                        id, rest = rest.split(" ", 1)
                        args = {arg.split(":")[0].strip():float(arg.split(":")[1].strip()) for arg in rest.split()}
                        node = Node(id,args)
                    else:
                        node = Node(rest.strip())
                    self.vocabulary[node.id] = node 
                elif kind == "RULE":
                    self.addRule(self.readRule(rest.strip()))
                elif kind == "SEED":
                    self.seed = int(rest.strip())
                elif kind == "STEPS":
                    self.steps = int(rest.strip())
                elif kind == "START":
                    self._state = self.translate(rest.strip())
                elif kind == "LEAF_COLOR":
                    self.leaf_color = [float(c) for c in rest.split()]
                elif kind == "TRUNK_COLOR":
                    self.trunk_color = [float(c) for c in rest.split()]