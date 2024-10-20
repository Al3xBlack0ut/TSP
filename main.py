import random
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import scrolledtext
import time


def wczytajGraf(sciezkaPliku):
    miasta = {}
    with open(sciezkaPliku, "r") as reader:
        linie = reader.readlines()
        liczbaMiast = int(linie[0])

        for i in range(1, liczbaMiast + 1):
            dane = linie[i].split()
            numerMiasta = int(dane[0])
            x = int(dane[1])
            y = int(dane[2])
            miasta[numerMiasta] = (x, y)

    return miasta, liczbaMiast


def obliczOdleglosc(miasto1, miasto2):
    return np.sqrt((miasto2[0] - miasto1[0]) ** 2 + (miasto2[1] - miasto1[1]) ** 2)


def najblizszySasiad(miasta, startoweMiasto):
    liczbaMiast = len(miasta)
    odwiedzone = [False] * (liczbaMiast + 1)
    sciezka = []
    aktualneMiasto = startoweMiasto
    calkowitaOdleglosc = 0

    odwiedzone[aktualneMiasto] = True
    sciezka.append(aktualneMiasto)

    for _ in range(liczbaMiast - 1):
        najblizszeMiasto = -1
        najkrotszaOdleglosc = float('inf')

        for miasto in miasta.keys():
            if not odwiedzone[miasto]:
                odleglosc = obliczOdleglosc(miasta[aktualneMiasto], miasta[miasto])
                if odleglosc < najkrotszaOdleglosc:
                    najkrotszaOdleglosc = odleglosc
                    najblizszeMiasto = miasto

        if najblizszeMiasto != -1:
            odwiedzone[najblizszeMiasto] = True
            sciezka.append(najblizszeMiasto)
            calkowitaOdleglosc += najkrotszaOdleglosc
            aktualneMiasto = najblizszeMiasto

    #Powrót do miasta startowego
    calkowitaOdleglosc += obliczOdleglosc(miasta[aktualneMiasto], miasta[startoweMiasto])
    sciezka.append(startoweMiasto)

    return calkowitaOdleglosc, sciezka


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


    for miasto in miasta:
        if miasto == startoweMiasto:
            plt.plot(miasta[miasto][0], miasta[miasto][1], 'ro', markersize=6)
            plt.text(
                miasta[startoweMiasto][0], miasta[startoweMiasto][1],
                f'{startoweMiasto}', fontsize=6, ha='left',
                bbox=dict(facecolor='red', alpha=0.5, edgecolor='black', boxstyle='round,pad=0.3')
            )
        else:
            plt.text(
                miasta[miasto][0], miasta[miasto][1], str(miasto),
                fontsize=6,
                bbox=dict(facecolor='white', alpha=0.5, edgecolor='black', boxstyle='round,pad=0.3')
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
    miasta, liczbaMiast = wczytajGraf("graf.txt")

    print(f"Miasta: {miasta}")

    startoweMiasto = 3

    najlepszaOdleglosc, sciezka = najblizszySasiad(miasta, startoweMiasto)

    print(f"Liczba miast: {liczbaMiast}")
    print("Miasta:")
    for numer, (x, y) in miasta.items():
        print(f"{numer}: (X: {x}, Y: {y})")

    wyniki = (f"Liczba miast: {liczbaMiast}\n"
              f"Najkrótsza znaleziona odległość: {najlepszaOdleglosc:.2f}\n"
              f"Najlepsza trasa: {' > '.join(map(str, sciezka))}")

    print(wyniki)

    czas = time.perf_counter()  - startTime
    print(f"Czas wykonywania: {czas:.4f} sekundy")

    #pokazWyniki(wyniki)
    rysujSciezke(miasta, sciezka, startoweMiasto, najlepszaOdleglosc)


if __name__ == "__main__":
    main()
