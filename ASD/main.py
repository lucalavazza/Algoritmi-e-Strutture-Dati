import tkinter as tk
from datetime import datetime

def CreaRete():
    """
    Quello che dobbiamo fare:
        - consentire la creazione dei tre tipi di file
            -- effettuare dei crontrolli sulla formattazione degli stessi
        - nel caso nella cartella del programma ce ne siano già almeno uno per tipo, dare la possibilità di spostarsi
          in CaricaRete per effettuare le operazioni necessarie
    """
    def CreaAutoma():
        automa = open("./Automa_" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".txt", "w")
        """
        E poi? 
        L'interazione con l'utente la facciamo in una finestra grafica, oppure nella console (tipo la primissima versione ancora su Colab)?
        """

    def CreaLink():
        print("Creo link...")

    def CreaTransizioni():
        print("Creo transizioni...")

    finestraCreazione = tk.Toplevel(finestraPrincipale)
    finestraCreazione.resizable(False, False)
    finestraCreazione.title("Crea una nuova rete")
    finestraCreazione.configure(background="white")

    indicazioniCreazione = "Sceglere cosa creare"
    etichettaAvvioCreazione = tk.Label(finestraCreazione, text=indicazioniCreazione, bg="white", font=("Helvetica", 10))
    etichettaAvvioCreazione.grid(row=0, column=1)

    creaAutomaButton = tk.Button(finestraCreazione, text="Crea un nuovo automa", command=CreaAutoma)
    creaAutomaButton.grid(row = 2, column = 0, padx = 10, pady = 10)
    # Non so ancora come/se si può fare, ma sarebbe il caso di disabilitarlo nel caso non esista almeno un automa
    creaLinkButton = tk.Button(finestraCreazione, text="Crea link tra automi", command=CreaLink)
    creaLinkButton.grid(row = 2, column = 1, padx = 10, pady = 10)
    # Le transizioni sono particolarmente delicate... devono effettivamente esistere negli automi. E come sopra, abilitazione.
    # Sempre che abbia senso crearle a mano... Forse è meglio leggerle e far inserire all'utente solo gli eventi e le etichette di osservabilità e rilevanza.
    creaTransizioniButton = tk.Button(finestraCreazione, text="Crea delle transizioni", command=CreaTransizioni)
    creaTransizioniButton.grid(row=2, column=3, padx=10, pady=10)

    indietroButton = tk.Button(finestraCreazione, text="Chiudi", command=finestraCreazione.destroy)
    indietroButton.grid(row = 4, column=1, padx = 10, pady = 10)

    finestraCreazione.mainloop()

def CaricaRete():
    """
    Quello che dobbiamo fare:
      - far scegliere i 3 file giusti (quello degli Automi, quello dei Link e quello delle Transizioni)
          -- problema: come controlliamo che la scelta sia giusta? E se l'utente seleziona un file contenente i link, per esempio?
                      Dobbiamo fare in modo che non si rompa tutto.
      - una volta scelti e aperti i file, chiedere cosa si vuol fare:
          -- stampare automi, topologia, spazio comportamentale, ecc
      - permettere di tornare indietro per fare qualcosa di diverso e/o cambiare file
    """
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
    #finestraCaricamento.geometry("400x400")
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
                 "caso si ricorda che è necessario anche avere la struttura dei link e le specifiche delle " \
                 "transizioni."


etichettaAvvio = tk.Label(finestraPrincipale, text = istruzioniBase, bg ="white", font = ("Helvetica", 12))
etichettaAvvio.pack()

creaReteButton = tk.Button(finestraPrincipale, text = "Crea una rete", command = CreaRete)
creaReteButton.pack()
caricaReteButton = tk.Button(finestraPrincipale, text = "Carica una rete", command = CaricaRete)
caricaReteButton.pack()

chiudiButton = tk.Button(finestraPrincipale, text = "Esci", command = finestraPrincipale.destroy).pack()


finestraPrincipale.mainloop()

