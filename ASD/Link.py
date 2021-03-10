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


def importaLinkDaFile(links, linkFile):
    link_file = open(linkFile, "r+")
    contenuto = link_file.read()
    lista_link_inseriti = contenuto.split("\n")
    for link in lista_link_inseriti:
        componente_iniziale = link.split(",")[0]
        componente_finale = link.split(",")[1]
        nome_link = link.split(",")[2]
        content = link.split(",")[3]
        links.append(Link(componente_iniziale, componente_finale, nome_link, content))
