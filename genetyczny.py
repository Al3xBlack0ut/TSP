import numpy as np
import random
from numba import jit
from zachlanny import najblizszySasiad, obliczOdleglosc


def obliczCalkowitaOdleglosc(miasta, sciezka):
    calkowitaOdleglosc = 0.0
    for i in range(len(sciezka) - 1):
        calkowitaOdleglosc += obliczOdleglosc(miasta[sciezka[i]], miasta[sciezka[i + 1]])
    calkowitaOdleglosc += obliczOdleglosc(miasta[sciezka[len(sciezka) - 1]], miasta[sciezka[0]])
    return calkowitaOdleglosc


def wygenerujPopulacje(miasta, liczbaMiast, wielkoscPopulacji):
    populacja = []
    for _ in range(wielkoscPopulacji // 2):
        startoweMiasto = random.randint(1, liczbaMiast)
        _, sciezka = najblizszySasiad(miasta, startoweMiasto)
        populacja.append(sciezka)

    for _ in range(wielkoscPopulacji // 2):
        sciezka = np.random.permutation(liczbaMiast) + 1
        sciezka = np.append(sciezka, sciezka[0])
        populacja.append(sciezka)

    return populacja


def mutacja(sciezka, wspolczynnikMutacji):
    for swapped in range(len(sciezka)):
        if random.random() < wspolczynnikMutacji:
            swapWith = random.randint(1, len(sciezka) - 1)
            sciezka[swapped], sciezka[swapWith] = sciezka[swapWith], sciezka[swapped]
    return sciezka


def krzyzowanieRodzicow(rodzic1, rodzic2):
    dlugosc = len(rodzic1)
    start = random.randint(1, len(rodzic1) - 3)
    end = random.randint(start + 1, len(rodzic1) - 1)
    dziecko = [None] * dlugosc

    for i in range(end-start+1):
        dziecko[i] = rodzic1[start+i]

    j = dziecko.index(None)
    for m in rodzic2:
        if m not in dziecko:
            dziecko[j]=m
            j+=1

    dziecko[dlugosc-1] = dziecko[0]
    return dziecko


def selekcjaTurniejowa(populacja, miasta, wielkoscTurnieju):
    turniej = random.sample(populacja, wielkoscTurnieju)
    najlepszyRodzic = min(turniej, key=lambda sciezka: obliczCalkowitaOdleglosc(miasta, sciezka))
    return najlepszyRodzic


def algorytmGenetyczny(miasta, wielkoscPopulacji=200, liczbaPokolen = 10, wspolczynnikMutacji = 0.013):
    liczbaMiast = len(miasta) - 1
    populacja = wygenerujPopulacje(miasta, liczbaMiast, wielkoscPopulacji)
    wielkoscTurnieju = wielkoscPopulacji // 4
    #print(populacja)

    for pokolenie in range(liczbaPokolen):
        nowaPopulacja = []
        for _ in range(wielkoscPopulacji):
            rodzic1 = selekcjaTurniejowa(populacja, miasta, wielkoscTurnieju)
            rodzic2 = selekcjaTurniejowa(populacja, miasta, wielkoscTurnieju)

            dziecko1 = krzyzowanieRodzicow(rodzic1, rodzic2)
            dziecko1 = mutacja(dziecko1, wspolczynnikMutacji)
            nowaPopulacja.append(dziecko1)

            dziecko2 = krzyzowanieRodzicow(rodzic1, rodzic2)
            dziecko2 = mutacja(dziecko2, wspolczynnikMutacji)
            nowaPopulacja.append(dziecko2)

        populacja = nowaPopulacja


    najlepszaSciezka = min(populacja, key=lambda sciezka: obliczCalkowitaOdleglosc(miasta, sciezka))
    najlepszaOdleglosc = obliczCalkowitaOdleglosc(miasta, najlepszaSciezka)
    return najlepszaOdleglosc, najlepszaSciezka