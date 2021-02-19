# IMPORT VARI
from graphviz import Digraph


# DEFINIZIONE DELLE CLASSI E DEI RELATIVI METODI
class Automa:
    def __init__(self, name, states, edges, final_states):
        self.name = name
        self.states = states
        self.edges = edges
        self.final_states = final_states
        # questo metodo è da sistemare, ma devo cercare di capire come. Perchè considera ogni carattere della stringa come elemento.
        # quindi, dato "20,21,t2a", considera x[1]=2, x[2]=0, x[3]=, e poi di nuovo per 21,
        # RISOLTO

    def disegnaAutoma(self, lati):
        fa = Digraph(self.name, filename="" + self.name + ".gv")
        fa.attr(rankdir="LR", size="8.5")
        i = 0
        for x in self.edges:
            nodo_partenza = lati[i].split(',')[0]
            nodo_destinazione = lati[i].split(',')[1]
            etichetta = lati[i].split(',')[2]
            fa.edge(nodo_partenza, nodo_destinazione, label=etichetta)
            i = i + 1
        fa.view()   # Funziona, ma è necessario installare dei componenti aggiuntivi che siano in grado di mostrare l'output.
                    # In particolare, nel caso (spero) tu abbia sotto Anaconda/Miniconda, basta digitare nella shell 'conda install python-graphviz'.
                    # In questo modo installa quello che serve e poi i grafi si vedono senza problemi.
                    # Ho trovato la soluzione qui: https://stackoverflow.com/questions/53347010/graphviz-throws-errors-calling-view-function
                    # ATTENZIONE: su Windows graphviz va installato direttamente e non solo con pip install graphviz (o conda)

class Link:
    def __init__(self, initial, final, name, content):
        self.initial = initial
        self.final = final
        self.name = name
        self.content = content

    def disegnaTopologia(self, initial, final, name):
        link = Digraph("Topologia", filename="Topologia.gv")
        link.attr(rankdir="LR", size="8.5")
        i = 0
        for x in self.link:
            componente_iniziale = initial[i].split(',')[0]
            componente_finale = final[i].split(',')[1]
            name = name[i].split(',')[2]
            link.edge(initial, final, label=name)
            i += 1
        link.view()



class Transizione:
    def __init__(self, component, edge, input, output, observability, relevance):
        self.component = component
        self.edge = edge
        self.input = input
        self.output = output
        self.observability = observability
        self.relevance = relevance


# STRUMENTI DI IMPORT DEGLI ELEMENTI DA FILE TXT


# Automi
automa_file = open(".\Automa.txt", "r+")
contenuto = automa_file.read()
singolo_automa = contenuto.split(" &\n")
automi = {}
i = 0
for x in singolo_automa:
    # Spezzo i dati del singolo automa
    contenuto_automa = singolo_automa[i].split("\n")
    nome_automa = contenuto_automa[0]
    stati = contenuto_automa[1].split(",")
    stati_finali = contenuto_automa[2].split(",")  # possono non esserci
    # ogni lato è dato da: sorgente, destinazione, nome
    lati = contenuto_automa[3].split("|")
    # creazione oggetto Automa
    automi[i] = Automa(nome_automa, stati, lati, stati_finali)
    i = i + 1

i = 1
for x in automi:
    print("\nAutoma " + str(i) + ': \n', "   Nome: ", automi[x].name, "\n    Stati: ",  automi[x].states, "\n    Lati: ", automi[x].edges, "\n    Stati terminali: ", automi[x].final_states)
    automi[x].disegnaAutoma(automi[x].edges) # Attenzione, qui c'era scritto solo "lati", ma ormai abbiamo l'oggetto, quindi meglio chiamare l'oggetto i-esimo e la variabile che ci interessa
    i = i + 1


# Link
#formato: comp_iniziale, comp_finale, link, contenuto
link_file = open("Link.txt", "r+")
contenuto = link_file.read()
contenuto_link = contenuto.split("\n")

links = {}
i = 0
for x in contenuto_link:
    componente_iniziale = contenuto_link[i].split(",")[0]
    componente_finale = contenuto_link[i].split(",")[1]
    nome_link = contenuto_link[i].split(",")[2]
    content = contenuto_link[i].split(",")[3]
    # Viene creato l'oggetto LINK
    links[i] = Link(componente_iniziale, componente_finale, nome_link, content)
    i = i + 1

i = 1
for x in links:
    print("\nLink " + str(i) + ': ', links[x].initial,  links[x].final,  links[x].name,  links[x].content)
    links[x].disegnaTopologia(Link[x].initial, Link[x].final, Link[x].name)
    i = i + 1



# Transizioni
#Formato: Automa, nome, input, output, rilevanza, osservabilità
transizioni_file = open("Transizioni.txt", "r+")
contenuto = transizioni_file.read()
transizioni = contenuto.split("\n")

transs = {}
i = 0
for x in transizioni:
    componente = transizioni[i].split(",")[0]
    lato = transizioni[i].split(",")[1]
    inpuuttrans = transizioni[i].split(",")[2]
    outputtrans = transizioni[i].split(",")[3]
    obs = transizioni[i].split(",")[5]
    rel = transizioni[i].split(",")[4]
    transs[i] = Transizione(componente, lato, inpuuttrans, outputtrans, obs, rel)
    i = i + 1

i = 1
for x in links:
    print("\nTransizione " + str(i) + ': ', transs[x].component,  transs[x].edge,  transs[x].input,  transs[x].output, transs[x].observability, transs[x].relevance)
    i = i + 1

