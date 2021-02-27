from graphviz import Digraph


class Automa:
    def __init__(self, name, states, edges, final_states):
        self.name = name
        self.states = states
        self.edges = edges
        self.final_states = final_states

    def disegnaAutoma(self, lati, final_states):
        fa = Digraph(self.name, filename="" + self.name + ".gv")
        fa.attr(rankdir="LR", size="8.5")
        fa.attr('node', shape='circle')
        i = 0
        for x in self.edges:
            nodo_partenza = lati[i].split(',')[0]
            nodo_destinazione = lati[i].split(',')[1]

            if nodo_partenza in final_states:
                fa.attr('node', shape='doublecircle')
                fa.node(nodo_partenza)
            if nodo_destinazione in final_states:
                fa.attr('node', shape='doublecircle')
                fa.node(nodo_destinazione)

            etichetta = lati[i].split(',')[2]
            fa.attr('node', shape='circle')
            fa.edge(nodo_partenza, nodo_destinazione, label=etichetta)
            i = i + 1
        fa.view()


def importaAutomiDaFile(automi):
    automa_file = open(".\Automa.txt", "r+")
    contenuto = automa_file.read()
    lista_automi = contenuto.split(" &\n")
    for automa in lista_automi:
        contenuto_automa = automa.split("\n")
        nome_automa = contenuto_automa[0]
        stati = contenuto_automa[1].split(",")
        stati_finali = contenuto_automa[2].split(",")  # Possono non esserci
        lati = contenuto_automa[3].split("|")
        automi.append(Automa(nome_automa, stati, lati, stati_finali))
