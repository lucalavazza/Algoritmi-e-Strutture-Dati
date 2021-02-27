from graphviz import Digraph


class StatoComportamentale:
    def __init__(self, listaStati, listaLink, finale):
        self.listaStati = listaStati
        self.listaLink = listaLink

    # Questo metodo restituisce la posizione dello stato dello spazio comportamentale nella lista
    def getPosStatoComportamentale(self, nuovaListaStati, nuovaListaLink):
        count = 0
        for v in self:
            if v.listaStati == nuovaListaStati and v.listaLink == nuovaListaLink:
                return count
            count += 1
        return -1

    # Questo metodo restituisce i dati di un nodo dello spazio comportamentale dato l'indice
    def getStatiLinkComportamentali(self, i):
        lista_stati = self[i].listaStati
        lista_link = self[i].listaLink
        return lista_stati, lista_link

    # mi dice se uno stato comportamentale è una copia di un altro
    def isDuplicate(self, nuovaListaStati, nuovaListaLink):
        for v in self:
            if v.listaStati == nuovaListaStati and v.listaLink == nuovaListaLink:
                return True
        return False

    # autoesplicativo
    def verificaSeStatoFinale(self, nuovaListaLink):
        for link in nuovaListaLink:
            if link != '\u03B5':
                return False
        return True


class StatoComportamentaleConNome:
    def __init__(self, listaStati, listaLink, nome, finale):
        self.listaStati = listaStati
        self.listaLink = listaLink
        self.nome = nome


class ArcoComportamentale:
    def __init__(self, statoPartenza, statoDestinazione, etichetta, observability, relevance):
        self.statoPartenza = statoPartenza
        self.statoDestinazione = statoDestinazione
        self.etichetta = etichetta
        self.observability = observability
        self.relevance = relevance

    def isDuplicate(self, statoPartenza, statoDestinazione, etichetta):
        for v in self:
            partenza = getattr(v.statoPartenza, 'listaStati') + getattr(v.statoPartenza, 'listaLink')
            arrivo = getattr(v.statoDestinazione, 'listaStati') + getattr(v.statoDestinazione, 'listaLink')
            if partenza == statoPartenza and arrivo == statoDestinazione and v.etichetta == etichetta:
                return True
        return False

    def disegnaSpazioComportamentale(self, titolo):
        spazio_comportamentale = Digraph(titolo, filename=""+titolo+".gv")
        spazio_comportamentale.attr(rankdir="LR", size="8.5")
        spazio_comportamentale.attr("node", shape="circle")
        for arco in self:
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

    # molto simile alla versione normale, ma al posto di stampare gli stati completi, ne stampa solo l'etichetta
    def disegnaSpazioComportamentaleRidenominato(self, titolo):
        spazio_comportamentale = Digraph(titolo, filename="" + titolo + ".gv")
        spazio_comportamentale.attr(rankdir="LR", size="8.5")
        spazio_comportamentale.attr("node", shape="circle")
        for arco in self:
            finale = True
            nodo_partenza = getattr(arco.statoPartenza, 'listaStati') + getattr(arco.statoPartenza,'listaLink')  # dello stato recupero prima gli stati e poi i link
            mylabelPartenzaString = str(getattr(arco.statoPartenza, 'nome'))
            listaCollegamenti = getattr(arco.statoPartenza, 'listaLink')

            for collegamento in listaCollegamenti:
                if collegamento != '\u03B5':
                    finale = False
                    break
            if finale:
                spazio_comportamentale.attr('node', shape='doublecircle')
                spazio_comportamentale.node(mylabelPartenzaString)

            finale = True
            nodo_destinazione = getattr(arco.statoDestinazione, 'listaStati') + getattr(arco.statoDestinazione, 'listaLink')
            mylabelDestinazioneString = str(getattr(arco.statoDestinazione, 'nome'))
            listaCollegamenti = getattr(arco.statoDestinazione, 'listaLink')
            etichetta = arco.etichetta
            if arco.observability != 'Îµ' and arco.relevance == 'Îµ':
                etichetta = etichetta + " " + arco.observability
            elif arco.observability == 'Îµ' and arco.relevance != 'Îµ':
                etichetta = etichetta + " " + arco.relevance
            elif arco.observability == 'Îµ' and arco.relevance == 'Îµ':
                etichetta = etichetta + " " + '\u03B5'
            else:
                etichetta = etichetta + " " + arco.observability + " " + arco.relevance

            for collegamento in listaCollegamenti:
                if collegamento != '\u03B5':
                    finale = False
                    break
            if finale:
                spazio_comportamentale.attr('node', shape='doublecircle')
                spazio_comportamentale.node(mylabelDestinazioneString)

            spazio_comportamentale.attr('node', shape='circle')

            spazio_comportamentale.edge(mylabelPartenzaString, mylabelDestinazioneString, label=etichetta)
        spazio_comportamentale.view()


def creaSpazioComportamentale(automi, transizioni, links, lista_stati, lista_link, lista_transizioni, stato_comportamentale, arco_comportamentale):
    # faccio la lista di stati di partenza per il primo elemento dello spazio comportamentale
    for x in automi:
        statoPartenza = x.states[0]
        lista_stati.append(statoPartenza)

    for x in links:
        lista_link.append('\u03B5')

    finale = True

    stato_comportamentale.append(StatoComportamentale(lista_stati, lista_link, finale))

    iterazione = 0
    statoCambiato = True

    # Servono davvero i print?

    while statoCambiato:
        i = StatoComportamentale.getPosStatoComportamentale(stato_comportamentale, lista_stati,
                                                                                  lista_link)
        print("Stato attuale: ", lista_stati, lista_link)
        statoCambiato = False
        print("Iterazione: ", iterazione)
        iterazione += 1
        for transizione in lista_transizioni:  # ciclo le transizioni e per ciascuna identifico componente e lato (es: C2, t2a)
            print("Transizione in esame: ", transizione.component, " ", transizione.input, " ", transizione.output, " ",
                  transizione.edge)
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
                                if ingressi[0] != '':  # se il primo elemento è vuoto, la lista è vuota
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
                                doppione = StatoComportamentale.isDuplicate(stato_comportamentale,
                                                                                                  nuova_lista_stati,
                                                                                                  nuova_lista_link)
                                print("Il nodo è un doppione? ", doppione)

                                if doppione:  # il nodo a cui posso muovermi esiste già
                                    print(lista_stati + lista_link, " == ", nuova_lista_stati + nuova_lista_link, "; ",
                                          transizione.edge)
                                    arcoDoppione = ArcoComportamentale.isDuplicate(
                                        arco_comportamentale, lista_stati + lista_link,
                                        nuova_lista_stati + nuova_lista_link, transizione.edge)
                                    print("L'arco è un doppione? ", arcoDoppione)
                                    if arcoDoppione:
                                        break
                                    else:
                                        # procedo a costruire l'arco che collegherà il nodo attuale a quello "doppione"
                                        print("Costruzione di solo arco in corso verso: ", nuova_lista_stati,
                                              nuova_lista_link)
                                        # devo trovare in che posto è lo stato doppione
                                        posizione_doppione = StatoComportamentale.getPosStatoComportamentale(
                                            stato_comportamentale, nuova_lista_stati, nuova_lista_link)
                                        print("Posizione doppione: ", posizione_doppione)
                                        arco_comportamentale.append(
                                            ArcoComportamentale(stato_comportamentale[i],
                                                                                      stato_comportamentale[
                                                                                          posizione_doppione],
                                                                                      transizione.edge,
                                                                                      transizione.observability,
                                                                                      transizione.relevance))
                                        i = posizione_doppione
                                        # lista_stati = nuova_lista_stati.copy()
                                        # lista_link = nuova_lista_link.copy()
                                        statoCambiato = True
                                        break
                                else:  # faccio il nuovo stato
                                    statoCambiato = True
                                    # verifico se lo stato è o meno finale
                                    finale = StatoComportamentale.verificaSeStatoFinale(
                                        stato_comportamentale, nuova_lista_link)
                                    print("Nessun doppione trovato")
                                    print("Sto costruendo un nuovo stato: ", nuova_lista_stati, nuova_lista_link,
                                          finale)
                                    stato_comportamentale.append(
                                        StatoComportamentale(nuova_lista_stati, nuova_lista_link,
                                                                                   finale))
                                    # Costruisco l'arco tra i due stati dello spazio comportamentale
                                    arco_comportamentale.append(
                                        ArcoComportamentale(stato_comportamentale[i],
                                                                                  stato_comportamentale[
                                                                                      len(stato_comportamentale) - 1],
                                                                                  transizione.edge,
                                                                                  transizione.observability,
                                                                                  transizione.relevance))
                                    lista_stati = nuova_lista_stati.copy()
                                    lista_link = nuova_lista_link.copy()
                                    i = StatoComportamentale.getPosStatoComportamentale(
                                        stato_comportamentale, lista_stati, lista_link)
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
            statiRadice, linkRadice = StatoComportamentale.getStatiLinkComportamentali(
                stato_comportamentale, 0)

            # Nessun cambio di stato ed ho esaurito le transizioni disponibili, cioè sono bloccato in un terminale
            if not statoCambiato and transizioneAttuale == transizioni[len(transizioni) - 1]:
                print("Nessun cambiamento apportato, torno indietro")
                i -= 1
                lista_temp_stati, lista_temp_link = StatoComportamentale.getStatiLinkComportamentali(
                    stato_comportamentale, i)
                print("Torno allo stato: ", lista_temp_stati, lista_temp_link)
                lista_stati = lista_temp_stati.copy()
                lista_link = lista_temp_link.copy()
                statoCambiato = True
                if statiRadice == lista_stati and linkRadice == lista_link:
                    print("Sono tornato alla radice")
                    statoCambiato = False

            if statoCambiato:
                break


def Potatura(stato_comportamentale, arco_comportamentale):
    lista_link_vuota = ['\u03B5', '\u03B5']
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
                if (getattr(arco.statoPartenza, 'listaStati') + getattr(arco.statoPartenza, 'listaLink')) == (
                        nodo.listaStati + nodo.listaLink):
                    print("Non rimuovere")
                    rimuovi = False
                    break
            if rimuovi:
                for arco in arco_comportamentale:
                    if (getattr(arco.statoDestinazione, 'listaStati') + getattr(arco.statoDestinazione,
                                                                                'listaLink')) == (
                            nodo.listaStati + nodo.listaLink) or \
                            (getattr(arco.statoPartenza, 'listaStati') + getattr(arco.statoPartenza, 'listaLink')) == (
                            nodo.listaStati + nodo.listaLink):
                        arco_comportamentale.remove(arco)
                print("Poto un nodo")
                stato_comportamentale.remove(nodo)
                nodoRimosso = True


def Ridenomina(stato_comportamentale, stato_comportamentale_ridenominato, arco_comportamentale_ridenominato, finale):
    i = 0
    for s in stato_comportamentale:
        stato_comportamentale_ridenominato.append(
            StatoComportamentaleConNome(s.listaStati, s.listaLink, i, finale))
        i += 1

    # faccio una copia di arco_comportamentale, in cui metto gli elementi di stato_comportamentale_ridenominato

    for arco in arco_comportamentale_ridenominato:
        for stato in stato_comportamentale_ridenominato:
            if getattr(arco.statoPartenza, 'listaStati') == stato.listaStati and getattr(arco.statoPartenza,
                                                                                         'listaLink') == stato.listaLink:
                arco.statoPartenza = stato
            elif getattr(arco.statoDestinazione, 'listaStati') == stato.listaStati and getattr(arco.statoDestinazione,
                                                                                               'listaLink') == stato.listaLink:
                arco.statoDestinazione = stato
            else:
                continue