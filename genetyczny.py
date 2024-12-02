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
    for _ in range(wielkoscPopulacji//2):
        startoweMiasto = random.randint(1, liczbaMiast)
        _, sciezka = najblizszySasiad(miasta, startoweMiasto)
        populacja.append(sciezka)

    for _ in range(wielkoscPopulacji // 2):
        sciezka = list(range(1, liczbaMiast + 1))
        random.shuffle(sciezka)
        sciezka.append(sciezka[0])
        populacja.append(sciezka)

    print("Wygenerowano populację")
    return populacja

def mutacja(sciezka, wspolczynnikMutacji):
    for swapped in range(2, len(sciezka) - 2):
        if random.random() < wspolczynnikMutacji:
            swapWith = random.randint(1, len(sciezka) - 2)
            sciezka[swapped], sciezka[swapWith] = sciezka[swapWith], sciezka[swapped]
    return sciezka

def krzyzowanieRodzicow(rodzic1, rodzic2):
    dlugosc = len(rodzic1)
    start = random.randint(1, len(rodzic1) - 3)
    end = random.randint(start + 1, len(rodzic1) - 2)
    dziecko = [None] * (dlugosc - 1)

    for i in range(start, end + 1):
        dziecko[i] = rodzic1[i]

    j = 0
    for m in rodzic2:
        if m not in dziecko:
            while dziecko[j] is not None:
                j += 1
            dziecko[j] = m

    dziecko.append(dziecko[0])
    return dziecko

def selekcjaTurniejowa(populacja, miasta, wielkoscTurnieju):
    turniej = random.sample(populacja, wielkoscTurnieju)
    najlepszyRodzic = min(turniej, key=lambda sciezka: obliczCalkowitaOdleglosc(miasta, sciezka))
    return najlepszyRodzic

def znajdzNajlepszaSciezke(miasta, populacja):
    najlepszaSciezka = None
    minimalnaOdleglosc = float('inf')

    for sciezka in populacja:
        odleglosc = obliczCalkowitaOdleglosc(miasta, sciezka)
        if odleglosc < minimalnaOdleglosc:
            minimalnaOdleglosc = odleglosc
            najlepszaSciezka = sciezka

    return najlepszaSciezka


def printPokolenie(pokolenie, miasta, populacja):
    najlepszaSciezka = znajdzNajlepszaSciezke(miasta, populacja)
    print(f"\n### Pokolenie {pokolenie} ###")
    print(f"Najlepsza ścieżka:  {obliczCalkowitaOdleglosc(miasta, najlepszaSciezka):.2f}")
    suma_dlugosci = 0
    for sciezka in populacja:
        suma_dlugosci += obliczCalkowitaOdleglosc(miasta, sciezka)

    srednia_dlugosc = suma_dlugosci / len(populacja)
    print(f"Średnio ścieżka:    {srednia_dlugosc:.2f}")


def algorytmGenetyczny(miasta, wielkoscPopulacji=100, liczbaPokolen=1000, wspolczynnikMutacji=0.013,wielkoscTurnieju=5):
    liczbaMiast = len(miasta) - 1
    populacja = wygenerujPopulacje(miasta, liczbaMiast, wielkoscPopulacji)
    #wielkoscTurnieju = int(wielkoscPopulacji * wspolczynnikTurnieju)

    for pokolenie in range(liczbaPokolen):
        nowaPopulacja = []
        for dziecko in range(wielkoscPopulacji // 2):
            '''if dziecko == 1:
                dziecko1  = znajdzNajlepszaSciezke(miasta, populacja)
                nowaPopulacja.append(dziecko1)
                nowaPopulacja.append(dziecko1)
                continue'''

            rodzic1 = selekcjaTurniejowa(populacja, miasta, wielkoscTurnieju)
            rodzic2 = selekcjaTurniejowa(populacja, miasta, wielkoscTurnieju)

            dziecko1 = krzyzowanieRodzicow(rodzic1, rodzic2)
            dziecko1 = mutacja(dziecko1, wspolczynnikMutacji)
            nowaPopulacja.append(dziecko1)

            dziecko2 = krzyzowanieRodzicow(rodzic1, rodzic2)
            dziecko2 = mutacja(dziecko2, wspolczynnikMutacji)
            nowaPopulacja.append(dziecko2)


        populacja = nowaPopulacja
        if pokolenie%100==0:
            printPokolenie(pokolenie, miasta, populacja)

    najlepszaSciezka = znajdzNajlepszaSciezke(miasta, populacja)
    najlepszaOdleglosc = obliczCalkowitaOdleglosc(miasta, najlepszaSciezka)

    return najlepszaOdleglosc, najlepszaSciezka


