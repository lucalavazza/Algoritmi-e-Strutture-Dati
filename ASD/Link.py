from graphviz import Digraph

class Link:
    def __init__(self, initial, final, name, content):
        self.initial = initial
        self.final = final
        self.name = name
        self.content = content

    def disegnaTopologia(self):
        nome_topologia = "topologia"
        topologia = Digraph(nome_topologia, filename="" + nome_topologia + ".gv")
        topologia.attr(rankdir="LR", size="8,5")
        topologia.attr("node", shape="rectangle")

        for link in self:
            topologia.edge(link.initial, link.final, label=link.name)
        topologia.view()