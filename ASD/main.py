import tkinter as tk

def CreaRete():
    print("Faccio qualcos'altro")


def CaricaRete():

    def StampaFile():
        if inputNomeFile.get():
            fileDaCaricare = inputNomeFile.get()
        else:
            fileDaCaricare = "Nessun valore inserito!"
        fileDaCaricare = fileDaCaricare + ".txt"
        try:
            with open(fileDaCaricare) as f:
                print(f.read())
        except Exception:
            print("File non trovato")


    finestraCaricamento = tk.Toplevel(finestraPrincipale)
    finestraCaricamento.resizable(False, False)
    finestraCaricamento.geometry("400x400")
    finestraCaricamento.title("Carica rete esistente")
    finestraCaricamento.configure(background = "white")

    inputNomeFile = tk.Entry(finestraCaricamento)
    inputNomeFile.grid(row = 0, column = 0)
    confermaCaricamentoReteButton = tk.Button(finestraCaricamento, text="Conferma nome rete", command = StampaFile)
    confermaCaricamentoReteButton.grid(row = 0, column = 1, padx = 10, pady = 10)

    indietroButton = tk.Button(finestraCaricamento, text = "Chiudi", command = finestraCaricamento.destroy)
    indietroButton.grid(row = 2, pady = 10)


    finestraCaricamento.mainloop()


finestraPrincipale = tk.Tk()
finestraPrincipale.geometry("800x600")
finestraPrincipale.resizable(False, False)
finestraPrincipale.title("Pagina Principale - Algoritmi e Strutture Dati")
finestraPrincipale.configure(background ="white")

istruzioniBase = "Questo programma aiuta nella creazione e visualizzazione di reti di automi finiti.\n" \
                 "Sarà possibile caricare automi già esistenti o caricare una rete di automi.\n In questo" \
                 "caso si ricorda che è necessario anche avere la struttura dei link e le specifiche delle" \
                 "transsizioni."


etichettaAvvio = tk.Label(finestraPrincipale, text = istruzioniBase, bg ="white", font = ("Helvetica", 10))
etichettaAvvio.pack()

creaReteButton = tk.Button(finestraPrincipale, text = "Crea una rete", command = CreaRete)
creaReteButton.pack()
caricaReteButton = tk.Button(finestraPrincipale, text = "Carica una rete", command = CaricaRete)
caricaReteButton.pack()

chiudiButton = tk.Button(finestraPrincipale, text = "Esci", command = finestraPrincipale.destroy).pack()


finestraPrincipale.mainloop()

