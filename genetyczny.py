import numpy as np
import random
from zachlanny import najblizszySasiad, obliczOdleglosc

def obliczCalkowitaOdleglosc(miasta, sciezka):
    calkowitaOdleglosc = 0.0
    for i in range(len(sciezka) - 1):
        calkowitaOdleglosc += obliczOdleglosc(miasta[sciezka[i]], miasta[sciezka[i + 1]])
    calkowitaOdleglosc += obliczOdleglosc(miasta[sciezka[-1]], miasta[sciezka[0]])
    return calkowitaOdleglosc


def wygenerujPopulacje(miasta, liczbaMiast, wielkoscPopulacji):
    populacja = []
    for _ in range(wielkoscPopulacji // 2):
        startoweMiasto = random.randint(1, liczbaMiast)
        _, sciezka = najblizszySasiad(miasta, startoweMiasto)
        populacja.append(sciezka)

    for _ in range(wielkoscPopulacji // 2):
        sciezka = np.random.permutation(liczbaMiast) + 1
        populacja.append(sciezka)

    return populacja


def krzyzowanieRodzicow(rodzic1, rodzic2):
    start = random.randint(0, len(rodzic1) - 1)
    end = random.randint(start + 1, len(rodzic1))

    dziecko = [-1] * len(rodzic1)
    dziecko[start:end] = rodzic1[start:end]

    for i in range(len(rodzic2)):
        if rodzic2[i] not in dziecko:
            for j in range(len(dziecko)):
                if dziecko[j] == -1:
                    dziecko[j] = rodzic2[i]
                    break

    return dziecko


def selekcjaTurniejowa(populacja, miasta, wielkoscTurnieju):
    turniej = random.sample(populacja, wielkoscTurnieju)
    najlepszyRodzic = min(turniej, key=lambda sciezka: obliczCalkowitaOdleglosc(miasta, sciezka))
    return najlepszyRodzic


def mutacja(sciezka, wspolczynnikMutacji):
    for swapped in range(len(sciezka)):
        if random.random() < wspolczynnikMutacji:
            swapWith = random.randint(0, len(sciezka) - 1)
            sciezka[swapped], sciezka[swapWith] = sciezka[swapWith], sciezka[swapped]
    return sciezka


def algorytmGenetyczny(miasta, wielkoscPopulacji):
    liczbaMiast = len(miasta) - 1
    populacja = wygenerujPopulacje(miasta, liczbaMiast, wielkoscPopulacji)
    liczbaPokolen = 5
    wielkoscTurnieju = wielkoscPopulacji//4
    wspolczynnikMutacji = 0.13
    for pokolenie in range(liczbaPokolen):
        nowaPopulacja = []
        for _ in range(wielkoscPopulacji):
            rodzic1 = selekcjaTurniejowa(populacja, miasta, wielkoscTurnieju)
            rodzic2 = selekcjaTurniejowa(populacja, miasta, wielkoscTurnieju)
            dziecko = krzyzowanieRodzicow(rodzic1, rodzic2)
            dziecko = mutacja(dziecko, wspolczynnikMutacji)
            nowaPopulacja.append(dziecko)

        populacja = nowaPopulacja

    najlepszaSciezka = min(populacja, key=lambda sciezka: obliczCalkowitaOdleglosc(miasta, sciezka))
    najlepszaOdleglosc = obliczCalkowitaOdleglosc(miasta, najlepszaSciezka)
    return najlepszaOdleglosc, najlepszaSciezka

