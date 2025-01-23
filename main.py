import time
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple
from genetyczny import algorytmGenetyczny


def wczytajMiasta(sciezkaPliku: str) -> Tuple[Dict[int, Tuple[float, float]], int]:
    """
    Wczytuj dane miast z pliku.
    Zwraca słownik miast oraz ich liczbę.
    """
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
    """
    Wizualizuj znalezioną trasę.
    """
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

    plt.title(f"Problem TSP - {nazwaInstancji}\n"
              f"Długość trasy: {najlepszaOdleglosc:.2f}")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True, alpha=0.3)
    plt.show()


def main():
    # Parametry algorytmu
    ROZMIAR_POPULACJI = 100
    LICZBA_POKOLEN = 1500
    #berlin52 - 180000
    #bier127 - 45000
    #tsp250 - 8000
    #tsp500 - 1500
    #tsp1000 - 300
    WSPOLCZYNNIK_MUTACJI = 0.02
    ROZMIAR_TURNIEJU = 5

    instancje = ["berlin52"]
    wyniki = {}
    #,,"tsp1000","tsp1000","tsp1000","tsp1000","tsp1000","tsp1000","tsp1000","tsp1000","tsp1000","tsp1000"
    for instancja in instancje:

        # Wczytaj dane
        sciezkaPliku = f"instancje/{instancja}.txt"
        miasta, liczbaMiast = wczytajMiasta(sciezkaPliku)

        # Mierz czas wykonania
        czasStart = time.perf_counter()

        # Uruchom algorytm genetyczny
        najlepszaOdleglosc, najlepszaTrasa = algorytmGenetyczny(
            miasta,
            rozmiarPopulacji=ROZMIAR_POPULACJI,
            liczbaPokolen=LICZBA_POKOLEN,
            wspolczynnikMutacji=WSPOLCZYNNIK_MUTACJI,
            rozmiarTurnieju=ROZMIAR_TURNIEJU
        )

        czasWykonania = time.perf_counter() - czasStart


        wyniki[instancja] = {
            'liczbaMiast': liczbaMiast,
            'najlepszaOdleglosc': najlepszaOdleglosc,
            'czas': czasWykonania
        }

        # Wyświetl raport
        #print("\n----- RAPORT -----")
        print(f"Instancja: {instancja}")
        print(f"Najlepsza znaleziona odległość: {najlepszaOdleglosc:.2f}")
        #print(f"Czas wykonania: {czasWykonania:.2f} sekund")
        #print(f"Najlepsza trasa: {' -> '.join(map(str, najlepszaTrasa))}")

        # Wizualizuj wyniki
        rysujTrase(miasta, najlepszaTrasa, najlepszaOdleglosc, instancja)


if __name__ == "__main__":
    main()