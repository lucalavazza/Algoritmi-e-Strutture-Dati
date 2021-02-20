# IMPORT VARI
from graphviz import Digraph
import collections


# DEFINIZIONE DELLE CLASSI E DEI RELATIVI METODI
class Automa:
    def __init__(self, name, states, edges, final_states):
        self.name = name
        self.states = states
        self.edges = edges
        self.final_states = final_states

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
        fa.view()


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

        for link in links:
            topologia.edge(link.initial, link.final, label=link.name)
        topologia.view()


class Transizione:
    def __init__(self, component, edge, input, output, observability, relevance):
        self.component = component
        self.edge = edge
        self.input = input
        self.output = output
        self.observability = observability
        self.relevance = relevance


class SpazioComportamentale:
    def __init__(self, listaStati, listaLink):
        self.listaStati = listaStati
        self.listaLink = listaLink

    def cercaDoppioni(self, nuovaListaStati, nuovaListaLink):
        for v in statoComportamentale:
            print("Nodo in verifica: ", v.listaStati, v.listaLink)
            if v.listaStati == nuovaListaStati:
                if v.listaLink == nuovaListaLink:
                    print("Nodo già esistente: ", v.listaStati, v.listaLink)
                    return True
        return False


# STRUMENTI DI IMPORT DEGLI ELEMENTI DA FILE TXT

# Automi
automa_file = open(".\Automa.txt", "r+")
contenuto = automa_file.read()
lista_automi = contenuto.split(" &\n")
automi = []
for automa in lista_automi:
    # Spezzo i dati del singolo automa
    contenuto_automa = automa.split("\n")
    nome_automa = contenuto_automa[0]
    stati = contenuto_automa[1].split(",")
    stati_finali = contenuto_automa[2].split(",")  # possono non esserci
    # ogni lato è dato da: sorgente, destinazione, nome
    lati = contenuto_automa[3].split("|")
    # creazione oggetto Automa
    automi.append(Automa(nome_automa, stati, lati, stati_finali))

# Richiamo della funzione per disegnare gli automi uno per volta
for automa in automi:
    automa.disegnaAutoma(automa.edges)

# Link
# Formato: comp_iniziale, comp_finale, link, contenuto
link_file = open("Link.txt", "r+")
contenuto = link_file.read()
lista_link_inseriti = contenuto.split("\n")
print(lista_link_inseriti)
links = []
for link in lista_link_inseriti:
    componente_iniziale = link.split(",")[0]
    componente_finale = link.split(",")[1]
    nome_link = link.split(",")[2]
    content = link.split(",")[3]
    # Viene creato l'oggetto LINK
    links.append(Link(componente_iniziale, componente_finale, nome_link, content))

# Chiamo il metodo per disegnare la topologia. Gli passo l'oggetto Link (chiamato links) che ha tutti i collegamenti tra i vari componenti
Link.disegnaTopologia(links);

# Transizioni
# Formato: Automa, nome, input, output, rilevanza, osservabilità
transizioni_file = open("Transizioni.txt", "r+")
contenuto = transizioni_file.read()
transizioni = contenuto.split("\n")

lista_transizioni = []
for transizione in transizioni:
    componente = transizione.split(",")[0]
    lato = transizione.split(",")[1]
    inpuuttrans = transizione.split(",")[2]
    outputtrans = transizione.split(",")[3]
    obs = transizione.split(",")[5]
    rel = transizione.split(",")[4]
    lista_transizioni.append(Transizione(componente, lato, inpuuttrans, outputtrans, obs, rel))

# Stampo le transizioni
for transizione in lista_transizioni:
    print("\nTransizione", transizione.component, transizione.edge, transizione.input, transizione.output,
          transizione.observability, transizione.relevance)

# Ogni stato dello spazio comportamentale è definito da: stati dei componenti + contenuto link
# Creo il primo stato dello spazio comportamentale, che sarà dato dai primi stati dei componenti e dai link vuoti (CONTROLLARE SE SPECIFICATO DIVERSO NELLA RICHIESTA)
lista_stati = []
lista_link = []  # ricordarsi che qui ci sono i CONTENUTI dei link
statoComportamentale = []
# faccio la lista di stati di partenza per il primo elemento dello spazio comportamentale
for x in automi:
    statoPartenza = x.states[0]
    lista_stati.append(statoPartenza)

for x in links:
    ##ATTENZIONE, vanno messi i contenuti del file link non sempre vuoti
    lista_link.append('\u03B5')  # metto la epsilon per indicare che sono vuoti

# A questo punto posso creare l'oggetto stato_comportamentale come la lista degli stati ed i contenuti dei link che lo definiscono
statoComportamentale.append(SpazioComportamentale(lista_stati, lista_link))
i = 0
# fine = True;
# while fine: #serve una funzione che confronti lo statoAttuale con il comportamentale
for transizione in lista_transizioni:  # ciclo le transizioni
    componente = transizione.component
    lato = transizione.edge
    soddisfa = True
    pos_automa = 0
    for automa in automi:  # cerco l'automa giusto
        if componente == automa.name:  # trovo l'automa giusto
            for l in automa.edges:  # cerco il lato giusto
                if lato == l.split(',')[2]:  # trovo il lato giusto
                    stato = statoComportamentale[i].listaStati[pos_automa]  # prendo lo stato dell'automa n-esimo nello stato comportamentale
                    if stato == l.split(',')[0]:  # verifico che stato di partenza sia quello contenuto nel stato comportamentale attuale
                        ingressi = (transizione.input).split(';')  # faccio la lista di tutti gli eventi; formato: link:evento
                        for j in ingressi:  # ciclo tutti gli eventi in ingresso
                            count = 0  # contatore (i link sono ordinati in un modo unico negli spazi comportamentali, questo mi serve per andare a quello relativo all'evento da confrontare
                            for link in links:  # ciclo i link esistenti
                                if j.split(':')[0] == link.name:  # verifico che il link i-esimo sia uguale a quello della transizione
                                    if statoComportamentale[i].listaLink[count] != j.split(':')[1]:  # verifico che il contenuto del link in ingresso sia quello dello stato comportamentale
                                        #print("Esco")
                                        soddisfa = False
                                        break
                                count += 1
                            # se tutto è stato soddisfatto non ho interrotto prima e quindi posso procedere
                        if not soddisfa:
                            break
                        # costruisco un nuovo stato dello spazio comportamentale
                        # faccio prima un backup delle liste
                        nuova_lista_stati = lista_stati.copy()
                        nuova_lista_link = lista_link.copy()

                        stato = l.split(',')[1] # stato di destinazione
                        nuova_lista_stati[pos_automa] = stato # Nella lista stati originaria sostituisco lo stato vecchio con quello nuovo

                        uscite = (transizione.output).split(';') # faccio la lista delle uscite
                        for uscita in uscite:
                            count = 0
                            for link in links:
                                if uscita.split(':')[0] == link.name:
                                    nuova_lista_link[count] = uscita.split(':')[1]
                                count += 1

                        # Verifico che il nuovo stato dello spazio comportamentale non esista già
                        doppione = SpazioComportamentale.cercaDoppioni(statoComportamentale, nuova_lista_stati, nuova_lista_link)
                        if doppione: # rimetto tutto a posto
                            nuova_lista_stati = lista_stati.copy()
                            nuova_lista_link = lista_link.copy()
                            break
                        else: # faccio il nuovo stato
                            print("Nessun doppione trovato")
                            i += 1
                            print("Sto costruendo un nuovo stato: ", nuova_lista_stati, nuova_lista_link)
                            statoComportamentale.append(SpazioComportamentale(nuova_lista_stati, nuova_lista_link))
                            #statoComportamentale[i] = SpazioComportamentale(nuova_lista_stati, nuova_lista_link)
                            break
                if not soddisfa:
                    break

            if not soddisfa:
                break
        if not soddisfa:
            break
        pos_automa += 1
    print(i+1) # numero stati comportamentali creati fino a quel momento (parte da zero)

    #break
# verifico che lo statoattuale esiste già
# se non esiste lo aggiungo
# se esiste esco
# fine = False
