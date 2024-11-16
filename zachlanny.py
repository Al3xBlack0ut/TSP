import numpy as np
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
