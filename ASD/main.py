import SpazioComportamentale
import Automa
import Link
import Transizione


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
    automi.append(Automa.Automa(nome_automa, stati, lati, stati_finali))

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
    links.append(Link.Link(componente_iniziale, componente_finale, nome_link, content))

# Chiamo il metodo per disegnare la topologia. Gli passo l'oggetto Link (chiamato links) che ha tutti i collegamenti tra i vari componenti
Link.Link.disegnaTopologia(links);

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
    lista_transizioni.append(Transizione.Transizione(componente, lato, inpuuttrans, outputtrans, obs, rel))

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
stato_comportamentale.append(SpazioComportamentale.StatoComportamentale(lista_stati, lista_link, finale))

iterazione = 0
statoCambiato = True
while statoCambiato:
    i = SpazioComportamentale.StatoComportamentale.getPosStatoComportamentale(stato_comportamentale, lista_stati, lista_link)
    print("Stato attuale: ", lista_stati, lista_link)
    statoCambiato = False
    print("Iterazione: ", iterazione)
    iterazione += 1
    for transizione in lista_transizioni:  # ciclo le transizioni e per ciascuna identifico componente e lato (es: C2, t2a)
        print("Transizione in esame: ", transizione.component, " ", transizione.input, " ", transizione.output, " ", transizione.edge)
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

                            uscite = (transizione.output).split(';') # faccio la lista delle uscite
                            for uscita in uscite:
                                count = 0
                                for link in links:
                                    if uscita.split(':')[0] == link.name:
                                        nuova_lista_link[count] = uscita.split(':')[1]
                                    count += 1

                            # Verifico che il nuovo stato dello spazio comportamentale non esista già
                            doppione = SpazioComportamentale.StatoComportamentale.isDuplicate(stato_comportamentale, nuova_lista_stati, nuova_lista_link)
                            print("Il nodo è un doppione? ", doppione)

                            if doppione:  # il nodo a cui posso muovermi esiste già
                                print(lista_stati + lista_link, " == ", nuova_lista_stati + nuova_lista_link, "; ", transizione.edge)
                                arcoDoppione = SpazioComportamentale.ArcoComportamentale.isDuplicate(arco_comportamentale, lista_stati + lista_link, nuova_lista_stati + nuova_lista_link, transizione.edge)
                                print("L'arco è un doppione? ", arcoDoppione)
                                if arcoDoppione:
                                    break
                                else:
                                    # procedo a costruire l'arco che collegherà il nodo attuale a quello "doppione"
                                    print("Costruzione di solo arco in corso verso: ", nuova_lista_stati, nuova_lista_link)
                                    # devo trovare in che posto è lo stato doppione
                                    posizione_doppione = SpazioComportamentale.StatoComportamentale.getPosStatoComportamentale(stato_comportamentale, nuova_lista_stati, nuova_lista_link)
                                    print("Posizione doppione: ", posizione_doppione)
                                    arco_comportamentale.append(SpazioComportamentale.ArcoComportamentale(stato_comportamentale[i], stato_comportamentale[posizione_doppione], transizione.edge))
                                    i = posizione_doppione
                                    # lista_stati = nuova_lista_stati.copy()
                                    # lista_link = nuova_lista_link.copy()
                                    statoCambiato = True
                                    break
                            else:  # faccio il nuovo stato
                                statoCambiato = True
                                # verifico se lo stato è o meno finale
                                finale = SpazioComportamentale.StatoComportamentale.verificaSeStatoFinale(stato_comportamentale, nuova_lista_link)
                                print("Nessun doppione trovato")
                                print("Sto costruendo un nuovo stato: ", nuova_lista_stati, nuova_lista_link, finale)
                                stato_comportamentale.append(SpazioComportamentale.StatoComportamentale(nuova_lista_stati, nuova_lista_link, finale))
                                # Costruisco l'arco tra i due stati dello spazio comportamentale
                                arco_comportamentale.append(SpazioComportamentale.ArcoComportamentale(stato_comportamentale[i], stato_comportamentale[len(stato_comportamentale) - 1], transizione.edge))
                                lista_stati = nuova_lista_stati.copy()
                                lista_link = nuova_lista_link.copy()
                                i = SpazioComportamentale.StatoComportamentale.getPosStatoComportamentale(stato_comportamentale, lista_stati, lista_link)
                                break
                    if not soddisfa:
                        break

                if not soddisfa:
                    break
            if not soddisfa:
                break
            pos_automa += 1


        transizioneAttuale = transizione.component + "," + transizione.edge + "," + transizione.input + "," + transizione.output + "," + transizione.relevance + "," + transizione.observability
        # prendo i dati della radice
        statiRadice, linkRadice = SpazioComportamentale.StatoComportamentale.getStatiLinkComportamentali(stato_comportamentale, 0)


        # Nessun cambio di stato ed ho esaurito le transizioni disponibili, cioè sono bloccato in un terminale
        if not statoCambiato and transizioneAttuale == transizioni[len(transizioni) - 1]:
            print("Nessun cambiamento apportato, torno indietro")
            i -= 1
            lista_temp_stati, lista_temp_link = SpazioComportamentale.StatoComportamentale.getStatiLinkComportamentali(stato_comportamentale, i)
            print("Torno allo stato: ", lista_temp_stati, lista_temp_link)
            lista_stati = lista_temp_stati.copy()
            lista_link = lista_temp_link.copy()
            statoCambiato = True
            if statiRadice == lista_stati and linkRadice == lista_link:
                print("Sono tornato alla radice")
                statoCambiato = False

        if statoCambiato:
            break

            # Disegno lo spazio comportamentale
            print("È stato aggiunto un nuovo stato allo spazio comportamentale, ricomincio da capo con le transizioni")


SpazioComportamentale.ArcoComportamentale.disegnaSpazioComportamentale(arco_comportamentale, 'SpazioComportamentale')

lista_link_vuota = ['\u03B5', '\u03B5']

# Poto lo spazio comportamentale
nodoRimosso = True
while nodoRimosso:
    if nodoRimosso:
        nodoRimosso = False
    for nodo in stato_comportamentale:
        # Se il nodo ha i link vuoti è terminale e procedo oltre
        if nodo.listaLink == lista_link_vuota:
            continue
        rimuovi = True
        for arco in arco_comportamentale:
            # print(getattr(arco.statoPartenza, 'listaStati') + getattr(arco.statoPartenza, 'listaLink'), " == ", (nodo.listaStati + nodo.listaLink))
            if (getattr(arco.statoPartenza, 'listaStati') + getattr(arco.statoPartenza, 'listaLink')) == (nodo.listaStati + nodo.listaLink):
                print("Non rimuovere")
                rimuovi = False
                break
        if rimuovi:
            for arco in arco_comportamentale:
                if (getattr(arco.statoDestinazione, 'listaStati') + getattr(arco.statoDestinazione, 'listaLink')) == (nodo.listaStati + nodo.listaLink) or\
                        (getattr(arco.statoPartenza, 'listaStati') + getattr(arco.statoPartenza, 'listaLink')) == (nodo.listaStati + nodo.listaLink):
                    arco_comportamentale.remove(arco)
            print("Poto un nodo")
            stato_comportamentale.remove(nodo)
            nodoRimosso = True


SpazioComportamentale.ArcoComportamentale.disegnaSpazioComportamentale(arco_comportamentale, 'SpazioComportamentalePotato')

#faccio una copia di stato_comportamentale, a cui aggiungo un nome univoco per ciascuno stato
stato_comportamentale_ridenominato =[]
i=0
for s in stato_comportamentale:
    stato_comportamentale_ridenominato.append(SpazioComportamentale.StatoComportamentaleConNome(s.listaStati, s.listaLink, i, finale))
    i +=1

#faccio una copia di arco_comportamentale, in cui metto gli elementi di stato_comportamentale_ridenominato
arco_comportamentale_ridenominato = arco_comportamentale.copy()
for arco in arco_comportamentale_ridenominato:
    for stato in stato_comportamentale_ridenominato:
        if getattr(arco.statoPartenza, 'listaStati') == stato.listaStati and getattr(arco.statoPartenza, 'listaLink') == stato.listaLink:
            arco.statoPartenza = stato
        elif getattr(arco.statoDestinazione, 'listaStati') == stato.listaStati and getattr(arco.statoDestinazione, 'listaLink') == stato.listaLink:
            arco.statoDestinazione = stato
        else:
            continue

SpazioComportamentale.ArcoComportamentale.disegnaSpazioComportamentaleRidenominato(arco_comportamentale_ridenominato, lista_transizioni, 'SpazioComportamentalePotatoRidenominato')