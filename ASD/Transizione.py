class Transizione:
    def __init__(self, component, edge, input, output, observability, relevance):
        self.component = component
        self.edge = edge
        self.input = input
        self.output = output
        self.observability = observability
        self.relevance = relevance


def importaTransizioniDaFile(lista_transizioni, transizioni, transizioniFile):
    transizioni_file = open(transizioniFile, "r+")
    contenuto = transizioni_file.read()
    split_transizioni = contenuto.split("\n")
    transizioni.extend(split_transizioni)
    for transizione in transizioni:
        componente = transizione.split(",")[0]
        lato = transizione.split(",")[1]
        inpuuttrans = transizione.split(",")[2]
        outputtrans = transizione.split(",")[3]
        obs = transizione.split(",")[5]
        rel = transizione.split(",")[4]
        lista_transizioni.append(Transizione(componente, lato, inpuuttrans, outputtrans, obs, rel))
