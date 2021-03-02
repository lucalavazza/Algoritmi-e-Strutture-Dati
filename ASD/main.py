import tkinter as tk

def CreaRete():
    print("Faccio qualcos'altro")



def CaricaRete():
    print("Faccio qualcosa")
    finestraCaricamento = tk.Toplevel(finestraPrincipale)
    finestraCaricamento.resizable(False, False)
    finestraCaricamento.title("Carica rete esistente")
    finestraCaricamento.configure(background = "white")

    spazioTotaleFinestra = tk.Canvas(finestraCaricamento, width=400, height=300)
    inputNomeFile = tk.Entry(finestraCaricamento)
    spazioTotaleFinestra.create_window(200, 140, window=inputNomeFile)
    # valoreImmesso = inputNomeFile.get()
    # labelValore = tk.Label(finestraCaricamento, text = valoreImmesso)
    # spazioTotaleFinestra.create_window(200, 230, window = labelValore)
    confermaCaricamentoReteButton = tk.Button(finestraCaricamento, text="Conferma nome rete")
    spazioTotaleFinestra.create_window(200, 180, window = confermaCaricamentoReteButton)

    indietroButton = tk.Button(finestraCaricamento, text = "Chiudi", command = finestraCaricamento.destroy)
    spazioTotaleFinestra.create_window(200, 180, window = indietroButton)


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

