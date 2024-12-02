import time
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import scrolledtext
from zachlanny import najblizszySasiad
from genetyczny import algorytmGenetyczny

def wczytajGraf(sciezkaPliku):
    with open(sciezkaPliku, "r") as reader:
        linie = reader.readlines()
        liczbaMiast = int(linie[0])

        miasta = np.empty((liczbaMiast + 1, 2))

        for i in range(1, liczbaMiast + 1):
            dane = linie[i].split()
            x = float(dane[1])
            y = float(dane[2])
            miasta[i] = (x, y)

    return miasta, liczbaMiast


def rysujSciezke(miasta, sciezka, najlepszaOdleglosc, instancja):
    fig = plt.figure(figsize=(10, 8))
    startoweMiasto = sciezka[0]

    for i in range(len(sciezka) - 1):
        xValues = [miasta[sciezka[i]][0], miasta[sciezka[i + 1]][0]]
        yValues = [miasta[sciezka[i]][1], miasta[sciezka[i + 1]][1]]

        kolor = np.random.rand(3, )

        plt.plot(xValues, yValues, marker='o', color=kolor)

        plt.annotate('', xy=(miasta[sciezka[i + 1]][0], miasta[sciezka[i + 1]][1]),
                     xytext=(miasta[sciezka[i]][0], miasta[sciezka[i]][1]),
                     arrowprops=dict(arrowstyle='->', color=kolor, lw=1.5))

    for miasto in range(1, len(miasta)):
        if miasto == startoweMiasto:
            plt.plot(miasta[miasto][0], miasta[miasto][1], 'ro', markersize=6)
            plt.text(
                miasta[startoweMiasto][0], miasta[startoweMiasto][1],
                f'{startoweMiasto}', fontsize=6, ha='left',
                bbox=dict(facecolor='red', alpha=0.9, edgecolor='black', boxstyle='round,pad=0.3')
            )
        else:
            plt.text(
                miasta[miasto][0], miasta[miasto][1], str(miasto),
                fontsize=6,
                bbox=dict(facecolor='white', alpha=0.75, edgecolor='black', boxstyle='round,pad=0.3')
            )

    plt.title(f"Instancja: {instancja}\n" "Ścieżka między miastami\n" f"Najkrótsza znaleziona odległość: {najlepszaOdleglosc:.2f}\n")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid()

    fig.canvas.manager.set_window_title(f"{instancja}")
    plt.show()


def pokazWyniki(wyniki):
    okno = tk.Tk()
    okno.title("Wyniki")

    poleTekstowe = scrolledtext.ScrolledText(okno, width=50, height=20, padx=10, pady=10)
    poleTekstowe.pack()

    poleTekstowe.insert(tk.END, wyniki)
    poleTekstowe.config(state=tk.DISABLED)
    button = tk.Button(okno, text="Wyświetl graf", command=okno.destroy)
    button.pack()

    okno.mainloop()


def main():
    startTime = time.perf_counter()
    instancja = "bier127"
    miasta, liczbaMiast = wczytajGraf(f"instancje/{instancja}.txt")
    startoweMiasto = 1


    #najlepszaOdleglosc, najlepszaSciezka = najblizszySasiad(miasta, startoweMiasto)
    #najlepszaOdleglosc, najlepszaSciezka = algorytmGenetyczny(miasta)
    najlepszaOdleglosc, najlepszaSciezka = algorytmGenetyczny(miasta, 100,1000,0.033, 10)


    endTime = time.perf_counter()
    czasWykonania = endTime - startTime

    wyniki = ("\n\n##### RAPORT #####\n"
            f"Liczba miast: {liczbaMiast}\n"
              f"Najkrótsza znaleziona odległość: {najlepszaOdleglosc:.2f}\n"
              f"czas: {czasWykonania}s\n"
              f"Najlepsza trasa: {' > '.join(map(str, najlepszaSciezka))}"
              )

    print(wyniki)

    #pokazWyniki(wyniki)
    rysujSciezke(miasta, najlepszaSciezka, najlepszaOdleglosc, instancja)

if __name__ == "__main__":
    main()
