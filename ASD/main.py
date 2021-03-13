import tkinter as tk
import tkinter.messagebox as tkMsg
import sys
import json
from datetime import datetime

import Automa
import Link
import Transizione
import SpazioComportamentale

def CreaRete():

    # Questo metodo cambia lo stato del bottone crea. Serve che i campi siano pieni per renderlo attivo
    def cambiaStatoBottone(*_):
        if inputAutoma.var.get() and inputLink.var.get() and inputTransizioni.var.get() and inputNomeRete.var.get():
            creaReteButton['state'] = 'normal'
        else:
            creaReteButton['state'] = 'disabled'

    # Questo metodo fa dei controlli sui file per vedere se esistono
    # Per ora se un file non esiste il programma viene chiuso, poi magari sistemiamo diversamente
    def confermaCreazione():
        #Caricamento Automa
        AutomaDaCaricare = inputAutoma.get()
        AutomaDaCaricare = AutomaDaCaricare + ".txt"
        error = False
        try:
            with open(AutomaDaCaricare) as f:
                print(f.read())
        except Exception:
            tkMsg.showerror(title="Errore", message="Il file degli automi inserito non è stato trovato")
            error = True
            sys.exit(1)
        #Caricamento Link
        LinkDaCaricare = inputLink.get()
        LinkDaCaricare = LinkDaCaricare + ".txt"
        try:
            with open(LinkDaCaricare) as f:
                print(f.read())
        except Exception:
            tkMsg.showerror(title="Errore", message="Il file dei link inserito non è stato trovato")
            error = True
            sys.exit(1)
        #Caricamento Transizioni
        TransizioniDaCaricare = inputTransizioni.get()
        TransizioniDaCaricare = TransizioniDaCaricare + ".txt"
        try:
            with open(TransizioniDaCaricare) as f:
                print(f.read())
        except Exception:
            tkMsg.showerror(title="Errore", message="Il file delle transizioni inserito non è stato trovato")
            error = True
            sys.exit(1)
        try:
            with open(inputNomeRete.get()) as f:
                print(f.read())
            tkMsg.showerror(title="Errore", message="Il nome inserito esiste già, inserirne un altro")
            error = True
        except Exception:
            print("Il file non esiste ancora, ottimo!")

        if error:
            error = False
            tkMsg.showinfo(title="Suggerimento", message="Riprova ad inserire i nomi")
        else:
            importaFile(AutomaDaCaricare, LinkDaCaricare, TransizioniDaCaricare)


    def importaFile(AutomaDaCaricare, LinkDaCaricare, TransizioniDaCaricare):
        automi = []
        Automa.importaAutomiDaFile(automi, AutomaDaCaricare)
        # Disegno degli automi
        for automa in automi:
            automa.disegnaAutoma(automa.edges, automa.final_states)
        # Importazione dei link
        links = []
        Link.importaLinkDaFile(links, LinkDaCaricare)
        # Disegno della topologia
        Link.Link.disegnaTopologia(links);
        # Importazione delle transizioni
        lista_transizioni = []
        transizioni = []
        Transizione.importaTransizioniDaFile(lista_transizioni, transizioni, TransizioniDaCaricare)

        # Creazione dello spazio comportamentale
        lista_stati = []
        lista_link = []
        stato_comportamentale = []
        arco_comportamentale = []
        SpazioComportamentale.creaSpazioComportamentale(automi, transizioni, links, lista_stati, lista_link,
                                                        lista_transizioni, stato_comportamentale, arco_comportamentale)

        # Disegno dello spazio comportamentale
        SpazioComportamentale.ArcoComportamentale.disegnaSpazioComportamentale(arco_comportamentale,
                                                                               inputNomeRete.get())
        # Potatura
        SpazioComportamentale.Potatura(stato_comportamentale, arco_comportamentale)
        # Salvataggio su txt dello spazio comportamentale
        num = SpazioComportamentale.ArcoComportamentale.salvaSpazioComportamentale(arco_comportamentale, inputNomeRete.get(),
                                                                                   inputAutoma.get(), inputLink.get(),
                                                                                   inputTransizioni.get())
        if num == 0:
            # Disegno dello spazio comportamentale potato
            nomeRetePotata = inputNomeRete.get() + "Potato"
            SpazioComportamentale.ArcoComportamentale.disegnaSpazioComportamentale(arco_comportamentale,
                                                                                   nomeRetePotata)
        else:
            tkMsg.showerror(title="Errore", message="Il nome del file che hai inserito esiste già")

    finestraCreazione = tk.Toplevel(finestraPrincipale)
    finestraCreazione.resizable(False, False)
    finestraCreazione.title("Crea una nuova rete")
    finestraCreazione.configure(background="white")

    indicazioniCreazione = "Menu creazione rete - Inserire i nomi dei file txt per importarli"
    etichettaAvvioCreazione = tk.Label(finestraCreazione, text=indicazioniCreazione, bg="white", font=("Helvetica", 10))
    etichettaAvvioCreazione.grid(row=0, column=1)

    labelAutoma = tk.Label(finestraCreazione, text="Automa")
    labelAutoma.grid(row=1, column=0)
    inputAutoma = tk.Entry(finestraCreazione)
    inputAutoma.grid(row=2, column=0)
    inputAutoma.var = tk.StringVar()
    inputAutoma['textvariable'] = inputAutoma.var
    inputAutoma.var.trace_add('write', cambiaStatoBottone)

    labelLink = tk.Label(finestraCreazione, text="Link")
    labelLink.grid(row=1, column=1)
    inputLink = tk.Entry(finestraCreazione)
    inputLink.grid(row=2, column=1)
    inputLink.var = tk.StringVar()
    inputLink['textvariable'] = inputLink.var
    inputLink.var.trace_add('write', cambiaStatoBottone)

    labelTransizioni = tk.Label(finestraCreazione, text="Transizioni")
    labelTransizioni.grid(row=1, column=2)
    inputTransizioni = tk.Entry(finestraCreazione)
    inputTransizioni.grid(row=2, column=2)
    inputTransizioni.var = tk.StringVar()
    inputTransizioni['textvariable'] = inputTransizioni.var
    inputTransizioni.var.trace_add('write', cambiaStatoBottone)

    labelNomeRete = tk.Label(finestraCreazione, text="Nome Rete")
    labelNomeRete.grid(row=3, column=0)
    inputNomeRete = tk.Entry(finestraCreazione)
    inputNomeRete.grid(row=3, column=1)
    inputNomeRete.var = tk.StringVar()
    inputNomeRete['textvariable'] = inputNomeRete.var
    inputNomeRete.var.trace_add('write', cambiaStatoBottone)

    creaReteButton = tk.Button(finestraCreazione, text="Crea", command = confermaCreazione, stat='disabled')
    creaReteButton.grid(row=4, column=1, padx=10, pady=10)

    indietroButton = tk.Button(finestraCreazione, text="Chiudi", command = finestraCreazione.destroy)
    indietroButton.grid(row = 5, column=1, padx = 10, pady = 10)

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
    def importaFile(AutomaDaCaricare, LinkDaCaricare, TransizioniDaCaricare):
        automi = []
        Automa.importaAutomiDaFile(automi, AutomaDaCaricare)
        # Disegno degli automi
        for automa in automi:
            automa.disegnaAutoma(automa.edges, automa.final_states)
        # Importazione dei link
        links = []
        Link.importaLinkDaFile(links, LinkDaCaricare)
        # Disegno della topologia
        Link.Link.disegnaTopologia(links);
        # Importazione delle transizioni
        lista_transizioni = []
        transizioni = []
        Transizione.importaTransizioniDaFile(lista_transizioni, transizioni, TransizioniDaCaricare)

    def CaricaFile():
        if inputNomeFile.get():
            fileDaCaricare = inputNomeFile.get()
        else:
            fileDaCaricare = "Nessun valore inserito!"
        fileDaCaricare = fileDaCaricare + ".txt"
        try:
            with open(fileDaCaricare) as f:
                contenuto = f.readline().split(";")
                # aggiungo l'estensione txt al nome del file
                AutomaDaCaricare = contenuto[0] + ".txt"
                try:
                    with open(AutomaDaCaricare) as f:
                        pass
                except Exception:
                    tkMsg.showerror(title="Errore",
                                    message="Il file degli automi di questo spazio comportamentale non è stato trovato")
                LinkDaCaricare = contenuto[1] + ".txt"
                try:
                    with open(LinkDaCaricare) as f:
                        pass
                except Exception:
                    tkMsg.showerror(title="Errore",
                                    message="Il file dei link di questo spazio comportamentale non è stato trovato")
                TransizioniDaCaricare = contenuto[2] + ".txt"
                try:
                    with open(TransizioniDaCaricare) as f:
                        pass
                except Exception:
                    tkMsg.showerror(title="Errore",
                                    message="Il file delle transizioni di questo spazio comportamentale non è stato trovato")
                importaFile(AutomaDaCaricare, LinkDaCaricare, TransizioniDaCaricare)
                # leggo tutte le righe del file degli spazi comportamentali
                contenuto = f.read().split("\n")
        except Exception:
            print("File non trovato")

    finestraCaricamento = tk.Toplevel(finestraPrincipale)
    finestraCaricamento.resizable(False, False)
    finestraCaricamento.title("Carica rete esistente")
    finestraCaricamento.configure(background = "white")

    inputNomeFile = tk.Entry(finestraCaricamento)
    inputNomeFile.grid(row = 0, column = 0)
    confermaCaricamentoReteButton = tk.Button(finestraCaricamento, text="Conferma nome rete", command = CaricaFile)
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

