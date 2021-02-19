# Ho copiato tutto abbastanza brutalmente, non sapendo se possa servirci in futuro, o se restiamo solo sull'insertimento tramite txt.
# Al massimo riordinare è un attimo

from graphviz import Digraph

f = Digraph("Macchina Stati Finiti", filename="fsm.gv")
f.attr(rankdir="LR", size="8,5")
#Così creo i nodi terminali
f.attr("node", shape="doublecircle")
f.node("LR_0")
#Così creo i generici nodi
f.attr("node", shape="circle") #Non serve dichiarare i nodi restanti
#Se ci sono delle relazioni (archi o lati) che toccano nodi senza il doppio cerchio,
#allora gli altri nodi sono creati automaticamente con il cerchio in questo caso.
f.edge("LR_1", "LR_0", label="S(A)") #nodo_iniziale, nodo_finale, etichetta
f.view()

fa = []

while True:
  nome_fa = input("Inserisci il nome del FA comportamentale che vuoi inserire, altrimenti scrivi 'fine': ")
  if nome_fa == 'fine':
    break
  fa_comportamentale = Digraph(nome_fa, filename=""+ nome_fa +".gv")
  fa_comportamentale.attr(rankdir="LR", size="8,5")

  #Gli FA comportamentali non hanno al loro interno stati di accettazione, quindi
  #mi basta definire gli archi o lati

  #Definisco uno "stato" iniziale e lo chiamo /
  fa_comportamentale.attr("node", shape="circle")
  fa_comportamentale.node("/")

  while True:
    nodo_partenza = input("Inserisci nodo di partenza del lato, se non si vogliono inserire più nodi scrivi 'fine': ")
    if nodo_partenza=='fine':
      break
    nodo_uscita = input("Inserisci nodo di arrivo del lato: ")
    etichetta = input("Indicare l'etichetta del lato: ")
    fa_comportamentale.edge(nodo_partenza, nodo_uscita, label=etichetta)

  fa_comportamentale
  fa.append(fa_comportamentale)

rete_fa = Digraph("Rete FA", filename="rete_fa.gv")
rete_fa.attr(rankdir="LR", size="8,5")
rete_fa.attr("node", shape="box")

#Visualizzazione FA comportamentali immessi
for x in fa:
  print(x)
  x

fa_comportamentale

#Inserimento link

nome_topologia = "topologia"
topologia = Digraph(nome_topologia, filename=""+ nome_topologia +".gv")
topologia.attr(rankdir="LR", size="8,5")

topologia.attr("node", shape="rectangle")
while True:
  componente_partenza = input("Inserisci il componente di partenza del link, se non si vogliono inserire più componenti scrivi 'fine': ")
  if componente_partenza=='fine':
    break
  componente_uscita = input("Inserisci il componente di arrivo del link: ")
  etichetta = input("Indicare l'etichetta del link: ")
  topologia.edge(componente_partenza, componente_uscita, label=etichetta)

topologia