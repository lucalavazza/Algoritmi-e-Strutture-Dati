import SpazioComportamentale
import Automa
import Link
import Transizione

# Importazione degli automi da file
automi = []
Automa.importaAutomiDaFile(automi)

# Disegno degli automi
for automa in automi:
    automa.disegnaAutoma(automa.edges, automa.final_states)

# Importazione dei link
links = []
Link.importaLinkDaFile(links)

# Disegno della topologia
Link.Link.disegnaTopologia(links);

# Importazione delle transizioni
lista_transizioni = []
transizioni = []
Transizione.importaTransizioniDaFile(lista_transizioni, transizioni)

# Creazione dello spazio comportamentale
lista_stati = []
lista_link = []
stato_comportamentale = []
arco_comportamentale = []
SpazioComportamentale.creaSpazioComportamentale(automi, transizioni, links, lista_stati, lista_link, lista_transizioni, stato_comportamentale, arco_comportamentale)

# Disegno dello spazio comportamentale
SpazioComportamentale.ArcoComportamentale.disegnaSpazioComportamentale(arco_comportamentale, 'SpazioComportamentale')

# Potatura
SpazioComportamentale.Potatura(stato_comportamentale, arco_comportamentale)

# Disegno dello spazio comportamentale potato
SpazioComportamentale.ArcoComportamentale.disegnaSpazioComportamentale(arco_comportamentale, 'SpazioComportamentalePotato')

# Ridenominazione
stato_comportamentale_ridenominato = []
arco_comportamentale_ridenominato = arco_comportamentale_ridenominato = arco_comportamentale.copy()
finale = True
SpazioComportamentale.Ridenomina(stato_comportamentale, stato_comportamentale_ridenominato, arco_comportamentale_ridenominato, finale)

# Disegno dello spazio comportamentale ridenominato
SpazioComportamentale.ArcoComportamentale.disegnaSpazioComportamentaleRidenominato(arco_comportamentale_ridenominato, 'SpazioComportamentalePotatoRidenominato')