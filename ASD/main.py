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


class StatoComportamentale:
    def __init__(self, listaStati, listaLink, finale):
        self.listaStati = listaStati
        self.listaLink = listaLink

    # mi dice se uno stato comportamentale è una copia di un altro
    def isDuplicate(self, nuovaListaStati, nuovaListaLink):
        # print("Nodo in verifica: ", nuovaListaStati, nuovaListaLink)
        for v in stato_comportamentale:
            # print("Verificando: ", v.listaStati, v.listaLink)
            if v.listaStati == nuovaListaStati and v.listaLink == nuovaListaLink:
                # print("Nodo già esistente: ", v.listaStati, v.listaLink)
                return True
        return False

    # questo non ho capito (per ora).
    def cercaDoppione(self, nuovaListaStati, nuovaListaLink):
        count = 0
        for v in stato_comportamentale:
            if v.listaStati == nuovaListaStati and v.listaLink == nuovaListaLink:
                return count
        return -1

    # autoesplicativo
    def verificaSeStatoFinale(self, nuovaListaLink):
        for link in nuovaListaLink:
            if link != '\u03B5':
                return False
        return True


class ArcoComportamentale:
    def __init__(self, statoPartenza, statoDestinazione, etichetta):
        self.statoPartenza = statoPartenza
        self.statoDestinazione = statoDestinazione
        self.etichetta = etichetta

    def isDuplicate(self, statoPartenza, statoDestinazione, etichetta):
        for v in arco_comportamentale:
            if v.statoPartenza == statoPartenza and v.statoDestinazione == statoDestinazione and v.etichetta == etichetta:
                return True
        return False

    def disegnaSpazioComportamentale(self, archi):
        spazio_comportamentale = Digraph("Spazio Comportamentale", filename="SpazioComportamentale.gv")
        spazio_comportamentale.attr(rankdir="LR", size="8.5")
        spazio_comportamentale.attr("node", shape="circle")
        for arco in archi:
            finale = True
            nodo_partenza = getattr(arco.statoPartenza, 'listaStati') + getattr(arco.statoPartenza, 'listaLink') #dello stato recupero prima gli stati e poi i link
            listaCollegamenti = getattr(arco.statoPartenza, 'listaLink')

            for collegamento in listaCollegamenti:
                if collegamento != '\u03B5':
                    finale = False
                    break
            nodo_partenza = ' '.join(nodo_partenza)  # converto la lista in stringa
            if finale:
                spazio_comportamentale.attr('node', shape='doublecircle')
                spazio_comportamentale.node(nodo_partenza)

            finale = True
            nodo_destinazione = getattr(arco.statoDestinazione, 'listaStati') + getattr(arco.statoDestinazione, 'listaLink')
            listaCollegamenti = getattr(arco.statoDestinazione, 'listaLink')

            for collegamento in listaCollegamenti:
                if collegamento != '\u03B5':
                    finale = False
                    break
            nodo_destinazione = ' '.join(nodo_destinazione)  # converto la lista in stringa
            if finale:
                spazio_comportamentale.attr('node', shape='doublecircle')
                spazio_comportamentale.node(nodo_destinazione)

            spazio_comportamentale.attr('node', shape='circle')
            nomeEtichetta = arco.etichetta
            spazio_comportamentale.edge(nodo_partenza, nodo_destinazione, label=nomeEtichetta)
        spazio_comportamentale.view()


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
    automa.disegnaAutoma(automa.edges, automa.final_states)

# Link
# Formato: comp_iniziale, comp_finale, link, contenuto
link_file = open("Link.txt", "r+")
contenuto = link_file.read()
lista_link_inseriti = contenuto.split("\n")
# print(lista_link_inseriti)
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
lista_link = []  # ricordarsi che qui ci sono i CONTENUTI dei link, inoltre è un dictionary

stato_comportamentale = []
arco_comportamentale = []
# faccio la lista di stati di partenza per il primo elemento dello spazio comportamentale
for x in automi:
    statoPartenza = x.states[0]
    lista_stati.append(statoPartenza)

for x in links:
    ##ATTENZIONE, sono sempre vuoti alla prima iterazione???
    lista_link.append('\u03B5')  # metto la epsilon per indicare che sono vuoti

# Le slide dicono: "Lo stato iniziale della rete è quello in cui ciascun componente è nel suo stato iniziale e i link sono vuoti"
# Perciò dovrebbe essere corretto fatto così. Credo.

finale = True  # Bisogna capire se all'inizio è sempre così o no

# A questo punto posso creare l'oggetto stato_comportamentale come la lista degli stati ed i contenuti dei link che lo definiscono
stato_comportamentale.append(StatoComportamentale(lista_stati, lista_link, finale))

i = 0  # numero di stati comportamentali
iterazione = 0
statoCambiato = True
while statoCambiato:
    statoCambiato = False
    print("Iterazione: ", iterazione)
    iterazione += 1
    for transizione in lista_transizioni:  # ciclo le transizioni e per ciascuna identifico componente e lato (es: C2, t2a)
        componente = transizione.component
        lato = transizione.edge
        soddisfa = True
        pos_automa = 0

        for automa in automi:  # cerco l'automa giusto
            if componente == automa.name:  # trovo l'automa giusto
                for l in automa.edges:  # cerco il lato giusto
                    if lato == l.split(',')[2]:  # trovo il lato giusto
                        # prendo lo stato dell'automa n-esimo nello stato comportamentale
                        stato = stato_comportamentale[i].listaStati[pos_automa]
                        # verifico che stato di partenza sia quello contenuto nel stato comportamentale attuale
                        if stato == l.split(',')[0]:
                            # faccio la lista di tutti gli eventi; formato: link:evento
                            ingressi = (transizione.input).split(';')
                            for j in ingressi:  # ciclo tutti gli eventi in ingresso
                                count = 0  # contatore (i link sono ordinati in un modo unico negli spazi comportamentali, questo mi serve per andare a quello relativo all'evento da confrontare)
                                for link in links:  # ciclo i link esistenti
                                    # verifico che il link i-esimo sia uguale a quello della transizione
                                    if j.split(':')[0] == link.name:
                                        # verifico che il contenuto del link in ingresso sia quello dello stato comportamentale
                                        if stato_comportamentale[i].listaLink[count] != j.split(':')[1]:
                                            # print("Esco")
                                            soddisfa = False
                                            break
                                    count += 1
                                if not soddisfa:
                                    break
                            if soddisfa:
                                uscite = (transizione.output).split(';')
                                # verifica che i link su cui scrivere le uscite siano vuoti
                                for k in uscite:
                                    count = 0
                                    for link in links:
                                        if k.split(':')[0] == link.name:
                                            # verifico che il link dove scrivere sia vuoto
                                            if stato_comportamentale[i].listaLink[count] != '\u03B5':
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

                            stato = l.split(',')[1]  # stato di destinazione
                            # Nella lista stati originaria sostituisco lo stato vecchio con quello nuovo
                            nuova_lista_stati[pos_automa] = stato

                            # rimuovo gli eventi in ingresso dai link appositi
                            if ingressi[0] != '': # se il primo elemento è vuoto, la lista è vuota
                                for ingresso in ingressi:
                                    count = 0
                                    nomeLink = ingresso.split(':')[0]
                                    valoreLink = ingresso.split(':')[1]
                                    for link in links:
                                        # NON STA CONTROLLANDO GLI EVENTI IN INGRESSO...
                                        if nomeLink == link.name:
                                            if valoreLink == nuova_lista_link[count]:
                                                nuova_lista_link[count] = '\u03B5'
                                        count += 1

                            uscite = (transizione.output).split(';')  # faccio la lista delle uscite
                            for uscita in uscite:
                                count = 0
                                for link in links:
                                    if uscita.split(':')[0] == link.name:
                                        nuova_lista_link[count] = uscita.split(':')[1]
                                    count += 1

                            # Verifico che il nuovo stato dello spazio comportamentale non esista già
                            doppione = StatoComportamentale.isDuplicate(stato_comportamentale, nuova_lista_stati, nuova_lista_link)

                            if doppione:  # il nodo a cui posso muovermi esiste già
                                arcoDoppione = ArcoComportamentale.isDuplicate(arco_comportamentale, lista_stati + lista_link, nuova_lista_stati + nuova_lista_link, transizione.edge)
                                if arcoDoppione:
                                    # l'arco esiste già
                                    lista_stati = nuova_lista_stati.copy()
                                    lista_link = nuova_lista_link.copy()
                                    break
                                else:
                                    # procedo a costruire l'arco che collegherà il nodo attuale a quello "doppione"
                                    finale = StatoComportamentale.verificaSeStatoFinale(stato_comportamentale, nuova_lista_link)
                                    print("Costruzione di solo arco in corso verso: ", nuova_lista_stati, nuova_lista_link)
                                    # devo trovare in che posto è lo stato doppione
                                    posizione_doppione = StatoComportamentale.cercaDoppione(stato_comportamentale, nuova_lista_stati, nuova_lista_link)
                                    arco_comportamentale.append(ArcoComportamentale(stato_comportamentale[i], stato_comportamentale[posizione_doppione], transizione.edge))

                                    lista_stati = nuova_lista_stati.copy()
                                    lista_link = nuova_lista_link.copy()
                                    break
                            else:  # faccio il nuovo stato
                                statoCambiato = True
                                # verifico se lo stato è o meno finale
                                finale = StatoComportamentale.verificaSeStatoFinale(stato_comportamentale, nuova_lista_link)
                                print("Nessun doppione trovato")
                                i += 1
                                print("Sto costruendo un nuovo stato: ", nuova_lista_stati, nuova_lista_link, finale)
                                stato_comportamentale.append(StatoComportamentale(nuova_lista_stati, nuova_lista_link, finale))
                                # Costruisco l'arco tra i due stati dello spazio comportamentale
                                arco_comportamentale.append(ArcoComportamentale(stato_comportamentale[i - 1], stato_comportamentale[i], transizione.edge))
                                lista_stati = nuova_lista_stati.copy()
                                lista_link = nuova_lista_link.copy()
                                break
                    if not soddisfa:
                        break

                if not soddisfa:
                    break
            if not soddisfa:
                break
            pos_automa += 1
        print("Stati dello spazio comportamentale costruiti: ", i + 1)  # numero stati comportamentali creati fino a quel momento (parte da zero)
        if statoCambiato:
            break

# Disegno lo spazio comportamentale
            print("È stato aggiunto un nuovo stato allo spazio comportamentale, ricomincio da capo con le transizioni")
ArcoComportamentale.disegnaSpazioComportamentale(ArcoComportamentale, arco_comportamentale)