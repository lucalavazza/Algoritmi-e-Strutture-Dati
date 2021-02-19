#IMPORT VARI
from graphviz import Digraph

#DEFINIZIONE DELLE CLASSI E DEI RELATIVI METODI
class Automa:
    def __init__(self, name, states, edges, final_states):
        self.name = name
        self.states = states
        self.edges = edges
        self.final_states = final_states
    def disegnaAutoma(self):
        fa = Digraph(self.name, filename="" + self.name + ".gv")
        fa.attr(rankdir="LR", size="5,5")
        for x in self.edges:
            print(x)
            nodo_partenza = x[1]
            nodo_uscita = x[2]
            etichetta = x[3]
            fa.edge(nodo_partenza, nodo_uscita, label=etichetta)
        fa.view()  ##Perché non funziona brutto scemo!
# Funziona, ma è necessario installare dei componenti aggiuntivi che siano in grado di mostrare l'output.
# In particolare, nel caso (spero) tu abbia sotto Anaconda/Miniconda, basta digitare nella shell 'conda install python-graphviz'.
# In questo modo installa quello che serve e poi i grafi si vedono senza problemi.
# Ho trovato la soluzione qui: https://stackoverflow.com/questions/53347010/graphviz-throws-errors-calling-view-function

class Link:
    def __init__(self, initial, final, name, content):
        self.initial = initial
        self.final = final
        self.name = name
        self.content = content

class Transizione:
    def __init__(self, component, edge, input, output, observability, relevance):
        self.component = component
        self.edge = edge
        self. input = input
        self.output = output
        self.observability = observability
        self.relevance = relevance


#STRUMENTI DI IMPORT DEGLI ELEMENTI DA FILE TXT

#Automi
automa_file = open(".\Automa.txt", "r+")
contenuto = automa_file.read()

contenuto_automa = contenuto.split("\n")
nome_automa = contenuto_automa[0]
stati = contenuto_automa[1].split(",")
stati_finali = contenuto_automa[2].split(",") # possono non esserci
lati = contenuto_automa[3].split("|")

print('AUTOMA')
print(nome_automa)
print(stati)
print(lati)
print(stati_finali)

c2 = Automa(nome_automa,stati,lati,stati_finali)
c2.disegnaAutoma()

#Link
link_file = open("Link.txt", "r+")
contenuto = link_file.read()

contenuto_link1 = contenuto.split("\n")
componente_iniziale1 = contenuto_link1[0].split(",")[0]
componente_finale1 = contenuto_link1[0].split(",")[1]
nome_link1 = contenuto_link1[0].split(",")[2]
content1 = contenuto_link1[0].split(",")[3]

componente_iniziale2 = contenuto_link1[1].split(",")[0]
componente_finale2 = contenuto_link1[1].split(",")[1]
nome_link2 = contenuto_link1[1].split(",")[2]
content2 = contenuto_link1[1].split(",")[3]

print('\nLINK')
print(contenuto)
print('\nLink 1')
print(contenuto_link1[0])
print(componente_iniziale1)
print(componente_finale1)
print(nome_link1)
print(content1)
print('\nLink 2')
print(contenuto_link1[1])
print(componente_iniziale2)
print(componente_finale2)
print(nome_link2)
print(content2)

l2=Link(componente_iniziale1,componente_finale1,nome_link1,content1)
l3=Link(componente_iniziale2,componente_finale2,nome_link2,content2)

#Transizioni
transizioni_file = open("Transizioni.txt", "r+")
contenuto = transizioni_file.read()

transizioni = contenuto.split("\n")
print('\nTRANSIZIONI')
print(transizioni)