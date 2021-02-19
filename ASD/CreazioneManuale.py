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