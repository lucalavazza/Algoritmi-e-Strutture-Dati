import tkinter as tk


def CaricaRete():
    print("Faccio qualcosa")

def SalvaRete():
    print("Faccio qualcos'altro")

window = tk.Tk()
window.geometry("800x600")
window.resizable(False, False)
window.title("Pagina Principale - Algoritmi e Strutture Dati")
window.configure(background = "#c4f7ff")

istruzioniBase = "Questo programma aiuta nella creazione e visualizzazione di reti di automi finit.\n" \
                 "Sarà possibile caricare automi già esistenti o caricare una rete di automi.\n In questo" \
                 "caso si ricorda che è necessario anche avere la struttura dei link e le specifiche delle" \
                 "transizioni."


etichettaAvvio = tk.Label(window, text = istruzioniBase, bg = "#c4f7ff", font = ("Helvetica", 16))
etichettaAvvio.grid(row = 0, column = 1)

creaReteButton = tk.Button(text = "Crea una rete", command = CaricaRete)
creaReteButton.grid(row = 1, column = 0)
caricaReteButton = tk.Button(text = "Carica una rete", command = SalvaRete)
caricaReteButton.grid(row = 1, column = 1)


if __name__ == "__main__":
    window.mainloop()

