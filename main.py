import time
import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, List, Tuple
from genetyczny import algorytmGenetyczny


def wczytajMiasta(sciezkaPliku: str) -> Tuple[Dict[int, Tuple[float, float]], int]:
    with open(sciezkaPliku, "r") as plik:
        linie = plik.readlines()
        liczbaMiast = int(linie[0])
        miasta = {}

        for i in range(1, liczbaMiast + 1):
            dane = linie[i].split()
            x = float(dane[1])
            y = float(dane[2])
            miasta[i] = (x, y)

    return miasta, liczbaMiast


def rysujTrase(miasta: Dict[int, Tuple[float, float]],
               trasa: List[int],
               najlepszaOdleglosc: float,
               nazwaInstancji: str) -> None:
    plt.figure(figsize=(12, 8))

    # krawędzie
    for i in range(len(trasa) - 1):
        xWartosci = [miasta[trasa[i]][0], miasta[trasa[i + 1]][0]]
        yWartosci = [miasta[trasa[i]][1], miasta[trasa[i + 1]][1]]
        plt.plot(xWartosci, yWartosci, 'b-', alpha=0.6)

    # punkty
    for miastoId, koordynaty in miasta.items():
        if miastoId == trasa[0]:  # Miasto startowe
            plt.plot(koordynaty[0], koordynaty[1], 'ro', markersize=10)
            plt.text(koordynaty[0], koordynaty[1], f'Start ({miastoId})',
                     fontsize=8, ha='right')
        else:
            plt.plot(koordynaty[0], koordynaty[1], 'ko', markersize=6)
            plt.text(koordynaty[0], koordynaty[1], str(miastoId),
                     fontsize=8, ha='right')

    plt.title(f"Problem TSP - {nazwaInstancji}\nDługość trasy: {najlepszaOdleglosc:.2f}")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True, alpha=0.3)
    plt.show()


def testujInstancje(nazwaInstancji: str, miasta: Dict, parametry: Dict) -> Tuple[float, List[int]]:
    print(f"\nTestowanie instancji: {nazwaInstancji}")
    najlepszaOdleglosc = np.inf
    najlepszaTrasa = None
    for test in range(parametry['liczbaTestow']):
        odleglosc, trasa = algorytmGenetyczny(
            miasta,
            rozmiarPopulacji=parametry['rozmiarPopulacji'],
            liczbaPokolen=parametry['liczbaPokolen'],
            wspolczynnikMutacji=parametry['wspolczynnikMutacji'],
            rozmiarTurnieju=parametry['rozmiarTurnieju']
        )
        if odleglosc<najlepszaOdleglosc:
            najlepszaOdleglosc=odleglosc
            najlepszaTrasa = trasa

    return najlepszaOdleglosc, najlepszaTrasa


def main():
    # Parametry algorytmu
    parametry = {
        'rozmiarPopulacji': 100,
        'liczbaPokolen': -1,
        #-1 - automatyczna, zalezna od ilosci miast
        # berlin52 - 180000
        # bier127 - 45000
        # tsp250 - 8000
        # tsp500 - 1500
        # tsp1000 - 300
        'wspolczynnikMutacji': 0.02,
        'rozmiarTurnieju': 5,
        'liczbaTestow': 3,
    }

    # Lista instancji do przetestowania
    instancje = ['berlin52', 'a280', 'tsp225', 'rat575', 'burma14',
                 'bier127', 'pr76', 'gr229', 'ali535', 'ts225']
    wyniki = {}

    for instancja in instancje:
        # Wczytaj dane
        sciezkaPliku = f"instancje/{instancja}.txt"
        miasta, liczbaMiast = wczytajMiasta(sciezkaPliku)

        # Mierz czas wykonania
        czasStart = time.perf_counter()
        najlepszaOdleglosc, najlepszaTrasa = testujInstancje(instancja, miasta, parametry)
        czasWykonania = time.perf_counter() - czasStart

        wyniki[instancja] = {
            'liczbaMiast': liczbaMiast,
            'najlepszaOdleglosc': najlepszaOdleglosc,
            'czas': czasWykonania
        }


        #print("\n----- RAPORT -----")
        print(f"Instancja: {instancja}")
        print(f"Najlepsza znaleziona odległość: {najlepszaOdleglosc:.2f}")
        # print(f"Czas wykonania: {czasWykonania:.2f} sekund")
        # print(f"Najlepsza trasa: {' -> '.join(map(str, najlepszaTrasa))}")

        # Wizualizuj wyniki
        # rysujTrase(miasta, najlepszaTrasa, najlepszaOdleglosc, instancja)


if __name__ == "__main__":
    main()