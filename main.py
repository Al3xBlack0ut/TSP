import random
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import scrolledtext
import time
from numba import jit


@jit(nopython=True)
def obliczOdleglosc(miasto1, miasto2):
    return np.sqrt((miasto2[0] - miasto1[0]) ** 2 + (miasto2[1] - miasto1[1]) ** 2)


@jit(nopython=True)
def najblizszySasiad(miasta, startoweMiasto):
    liczbaMiast = len(miasta) - 1
    odwiedzone = np.zeros(liczbaMiast + 1, dtype=np.bool_)
    sciezka = np.empty(liczbaMiast + 1, dtype=np.int32)
    aktualneMiasto = startoweMiasto
    calkowitaOdleglosc = 0.0

    odwiedzone[aktualneMiasto] = True
    sciezka[0] = aktualneMiasto

    for i in range(1, liczbaMiast):
        najblizszeMiasto = -1
        najkrotszaOdleglosc = float('inf')

        for miasto in range(1, liczbaMiast + 1):
            if not odwiedzone[miasto]:
                odleglosc = obliczOdleglosc(miasta[aktualneMiasto], miasta[miasto])
                if odleglosc < najkrotszaOdleglosc:
                    najkrotszaOdleglosc = odleglosc
                    najblizszeMiasto = miasto

        if najblizszeMiasto != -1:
            odwiedzone[najblizszeMiasto] = True
            sciezka[i] = najblizszeMiasto
            calkowitaOdleglosc += najkrotszaOdleglosc
            aktualneMiasto = najblizszeMiasto

    # Powrót do miasta startowego
    calkowitaOdleglosc += obliczOdleglosc(miasta[aktualneMiasto], miasta[startoweMiasto])
    sciezka[liczbaMiast] = startoweMiasto

    return calkowitaOdleglosc, sciezka


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


def rysujSciezke(miasta, sciezka, startoweMiasto, najlepszaOdleglosc):
    fig = plt.figure(figsize=(10, 8))

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

    plt.title("Ścieżka między miastami\n" f"Najkrótsza znaleziona odległość: {najlepszaOdleglosc:.2f}\n")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid()

    fig.canvas.manager.set_window_title("Problem Komiwojażera")
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
    miasta, liczbaMiast = wczytajGraf("instancje/graf.txt")
    startoweMiasto = 1

    najlepszaOdleglosc, sciezka = najblizszySasiad(miasta, startoweMiasto)

    wyniki = (f"Liczba miast: {liczbaMiast}\n"
              f"Najkrótsza znaleziona odległość: {najlepszaOdleglosc:.2f}\n"
              f"Najlepsza trasa: {' > '.join(map(str, sciezka))}")

    print(wyniki)

    czas = time.perf_counter() - startTime
    print(f"Czas wykonywania: {czas:.4f} s")

    # pokazWyniki(wyniki)
    rysujSciezke(miasta, sciezka, startoweMiasto, najlepszaOdleglosc)


if __name__ == "__main__":
    main()
