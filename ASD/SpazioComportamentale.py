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
    def __init__(self, statoPartenza, statoDestinazione, etichetta):
        self.statoPartenza = statoPartenza
        self.statoDestinazione = statoDestinazione
        self.etichetta = etichetta

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
    def disegnaSpazioComportamentaleRidenominato(self, listaTransizioni, titolo):
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
            nodo_partenza = ' '.join(nodo_partenza)  # converto la lista in stringa
            if finale:
                spazio_comportamentale.attr('node', shape='doublecircle')
                spazio_comportamentale.node(mylabelPartenzaString)

            finale = True
            nodo_destinazione = getattr(arco.statoDestinazione, 'listaStati') + getattr(arco.statoDestinazione, 'listaLink')
            mylabelDestinazioneString = str(getattr(arco.statoDestinazione, 'nome'))
            listaCollegamenti = getattr(arco.statoDestinazione, 'listaLink')

            for collegamento in listaCollegamenti:
                if collegamento != '\u03B5':
                    finale = False
                    break
            nodo_destinazione = ' '.join(nodo_destinazione)  # converto la lista in stringa
            if finale:
                spazio_comportamentale.attr('node', shape='doublecircle')
                spazio_comportamentale.node(mylabelDestinazioneString)

            spazio_comportamentale.attr('node', shape='circle')
            nomeEtichetta = arco.etichetta

            # ovviamente non funziona
            for t in listaTransizioni:
                if nomeEtichetta == t.edge and t.input in getattr(arco.statoPartenza, 'listaLink'):
                    if t.observability != '\u03B5':
                        etichettatura = t.observability
                    elif t.relevance != '\u03B5':
                        etichettatura = t.relevance
                    else:
                        etichettatura = 'gino'
                else:
                    etichettatura = ' pippo'
            spazio_comportamentale.edge(mylabelPartenzaString, mylabelDestinazioneString, label=(nomeEtichetta + etichettatura))
        spazio_comportamentale.view()
