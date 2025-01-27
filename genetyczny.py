import random
import numpy as np
from numba import jit
from typing import Dict, List, Tuple


@jit(nopython=True)
def obliczOdleglosc(miasto1: np.ndarray, miasto2: np.ndarray) -> float:
    return np.sqrt(((miasto2 - miasto1) ** 2).sum())


@jit(nopython=True)
def utworzMacierzOdleglosci(tablicaMiast: np.ndarray) -> np.ndarray:
    liczbaMiast = len(tablicaMiast)
    odleglosci = np.zeros((liczbaMiast, liczbaMiast))
    for i in range(liczbaMiast):
        for j in range(liczbaMiast):
            if i != j:
                odleglosci[i][j] = obliczOdleglosc(tablicaMiast[i], tablicaMiast[j])
    return odleglosci


@jit(nopython=True)
def obliczKosztTrasy(trasa: np.ndarray, macierzOdleglosci: np.ndarray) -> float:
    calkowityKoszt = 0.0
    for i in range(len(trasa) - 1):
        calkowityKoszt += macierzOdleglosci[trasa[i] - 1][trasa[i + 1] - 1]
    return calkowityKoszt


@jit(nopython=True)
def poprawa2opt(trasa: np.ndarray, macierzOdleglosci: np.ndarray) -> np.ndarray:
    poprawiono = True
    najlepszaOdleglosc = obliczKosztTrasy(trasa, macierzOdleglosci)
    trasa = trasa.copy()

    while poprawiono:
        poprawiono = False
        for i in range(1, len(trasa) - 2):
            if poprawiono:
                break
            for j in range(i + 1, len(trasa) - 1):
                if (macierzOdleglosci[trasa[i - 1] - 1][trasa[j] - 1] +
                    macierzOdleglosci[trasa[i] - 1][trasa[j + 1] - 1]) < (
                        macierzOdleglosci[trasa[i - 1] - 1][trasa[i] - 1] +
                        macierzOdleglosci[trasa[j] - 1][trasa[j + 1] - 1]):
                    trasa[i:j + 1] = trasa[i:j + 1][::-1]
                    nowaOdleglosc = obliczKosztTrasy(trasa, macierzOdleglosci)
                    if nowaOdleglosc < najlepszaOdleglosc:
                        najlepszaOdleglosc = nowaOdleglosc
                        poprawiono = True
                        break
    return trasa


@jit(nopython=True)
def trasaNajblizzegoSasiada(macierzOdleglosci: np.ndarray, miastoStartowe: int) -> np.ndarray:
    liczbaMiast = len(macierzOdleglosci)
    nieodwiedzone = np.ones(liczbaMiast, dtype=np.bool_)
    trasa = np.zeros(liczbaMiast + 1, dtype=np.int64)

    aktualneMiasto = miastoStartowe
    trasa[0] = aktualneMiasto
    nieodwiedzone[aktualneMiasto - 1] = False

    for i in range(1, liczbaMiast):
        nastepneMiasto = -1
        minOdleglosc = np.inf

        for j in range(liczbaMiast):
            if nieodwiedzone[j] and macierzOdleglosci[aktualneMiasto - 1][j] < minOdleglosc:
                minOdleglosc = macierzOdleglosci[aktualneMiasto - 1][j]
                nastepneMiasto = j + 1

        trasa[i] = nastepneMiasto
        nieodwiedzone[nastepneMiasto - 1] = False
        aktualneMiasto = nastepneMiasto

    trasa[liczbaMiast] = trasa[0]
    return trasa


def konwertujDoNumpy(miasta: Dict) -> np.ndarray:
    """Konwertuje słownik miast na format NumPy. """
    liczbaMiast = len(miasta)
    tablicaMiast = np.zeros((liczbaMiast, 2))
    for idMiasta, wspolrzedne in miasta.items():
        tablicaMiast[idMiasta - 1] = np.array(wspolrzedne)
    return tablicaMiast


def generujPopulacjePoczatkowa(tablicaMiast: np.ndarray,
                               macierzOdleglosci: np.ndarray,
                               rozmiarPopulacji: int) -> List[np.ndarray]:
    """Generuje początkową populację."""
    populacja = []
    liczbaMiast = len(tablicaMiast)

    # Metoda najbliższego sąsiada - 40% populacji
    for _ in range(int(rozmiarPopulacji * 0.4)):
        miastoStart = random.randint(1, liczbaMiast)
        trasa = trasaNajblizzegoSasiada(macierzOdleglosci, miastoStart)
        populacja.append(trasa)

    # Losowo z 2-opt - 60% populacji
    for _ in range(rozmiarPopulacji - len(populacja)):
        trasa = np.arange(1, liczbaMiast + 1)
        np.random.shuffle(trasa)
        trasa = np.append(trasa, trasa[0])
        trasa = poprawa2opt(trasa, macierzOdleglosci)
        populacja.append(trasa)

    return populacja


@jit(nopython=True)
def krzyzeowanieEAX(rodzic1: np.ndarray, rodzic2: np.ndarray,
                    macierzOdleglosci: np.ndarray) -> np.ndarray:
    liczbaMiast = len(rodzic1) - 1
    dziecko = np.zeros(liczbaMiast + 1, dtype=np.int64)
    nieodwiedzone = np.ones(liczbaMiast, dtype=np.bool_)

    aktualnaPoz = np.random.randint(0, liczbaMiast)
    aktualneMiasto = rodzic1[aktualnaPoz]
    dziecko[0] = aktualneMiasto
    nieodwiedzone[aktualneMiasto - 1] = False

    for i in range(1, liczbaMiast):
        minOdleglosc = np.inf
        nastepneMiasto = -1

        for rodzic in (rodzic1, rodzic2):
            idx = np.where(rodzic == aktualneMiasto)[0][0]
            if idx < liczbaMiast:
                kandydat = rodzic[idx + 1]
                if nieodwiedzone[kandydat - 1]:
                    odleglosc = macierzOdleglosci[aktualneMiasto - 1][kandydat - 1]
                    if odleglosc < minOdleglosc:
                        minOdleglosc = odleglosc
                        nastepneMiasto = kandydat

        if nastepneMiasto == -1:
            for miasto in range(1, liczbaMiast + 1):
                if nieodwiedzone[miasto - 1]:
                    odleglosc = macierzOdleglosci[aktualneMiasto - 1][miasto - 1]
                    if odleglosc < minOdleglosc:
                        minOdleglosc = odleglosc
                        nastepneMiasto = miasto

        dziecko[i] = nastepneMiasto
        nieodwiedzone[nastepneMiasto - 1] = False
        aktualneMiasto = nastepneMiasto

    dziecko[liczbaMiast] = dziecko[0]
    return dziecko


def algorytmGenetyczny(miasta: Dict,
                       rozmiarPopulacji: int = 100,
                       liczbaPokolen: int = 1000,
                       wspolczynnikMutacji: float = 0.02,
                       rozmiarTurnieju: int = 5) -> Tuple[float, List[int]]:
    """Główna funkcja algorytmu genetycznego."""
    tablicaMiast = konwertujDoNumpy(miasta)
    macierzOdleglosci = utworzMacierzOdleglosci(tablicaMiast)

    if liczbaPokolen == -1:
        liczbaPokolen = int(1469261436.98 * (len(miasta)**(-2.21)))
        #print("liczba pokoleń: "+str(liczbaPokolen))

    populacja = generujPopulacjePoczatkowa(tablicaMiast, macierzOdleglosci, rozmiarPopulacji)
    najlepszaOdleglosc = np.inf
    najlepszaTrasa = None
    licznikStagnacji = 0

    for pokolenie in range(liczbaPokolen):
        nowaPopulacja = []

        # Elityzm
        elita = min(populacja, key=lambda x: obliczKosztTrasy(x, macierzOdleglosci))
        nowaPopulacja.append(elita)

        while len(nowaPopulacja) < rozmiarPopulacji:
            turniej = random.sample(populacja, rozmiarTurnieju)
            rodzic1 = min(turniej, key=lambda x: obliczKosztTrasy(x, macierzOdleglosci))
            rodzic2 = min(turniej, key=lambda x: obliczKosztTrasy(x, macierzOdleglosci))

            dziecko = krzyzeowanieEAX(rodzic1, rodzic2, macierzOdleglosci)

            if random.random() < wspolczynnikMutacji:
                dziecko = poprawa2opt(dziecko, macierzOdleglosci)

            nowaPopulacja.append(dziecko)

        populacja = nowaPopulacja

        aktualnieNajlepszy = min(populacja, key=lambda x: obliczKosztTrasy(x, macierzOdleglosci))
        aktualnaOdleglosc = obliczKosztTrasy(aktualnieNajlepszy, macierzOdleglosci)

        if aktualnaOdleglosc < najlepszaOdleglosc:
            najlepszaOdleglosc = aktualnaOdleglosc
            najlepszaTrasa = aktualnieNajlepszy.tolist()
            licznikStagnacji = 0
        else:
            licznikStagnacji += 1

        if licznikStagnacji > 50:
            polowaRozmiaru = rozmiarPopulacji // 2
            populacja = populacja[:polowaRozmiaru]
            populacja.extend(generujPopulacjePoczatkowa(
                tablicaMiast, macierzOdleglosci, rozmiarPopulacji - polowaRozmiaru))
            licznikStagnacji = 0

        #if pokolenie % 100 == 0:
            #print(f"Pokolenie {pokolenie}: {najlepszaOdleglosc:.2f}")

    return najlepszaOdleglosc, najlepszaTrasa