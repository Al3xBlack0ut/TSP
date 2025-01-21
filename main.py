import time
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple
from genetyczny import genetic_algorithm


def wczytaj_miasta(sciezka_pliku: str) -> Tuple[Dict[int, Tuple[float, float]], int]:
    """
    Wczytuje dane miast z pliku.
    Zwraca słownik miast oraz ich liczbę.
    """
    with open(sciezka_pliku, "r") as plik:
        linie = plik.readlines()
        liczba_miast = int(linie[0])
        miasta = {}

        for i in range(1, liczba_miast + 1):
            dane = linie[i].split()
            x = float(dane[1])
            y = float(dane[2])
            miasta[i] = (x, y)

    return miasta, liczba_miast


def rysuj_trase(miasta: Dict[int, Tuple[float, float]],
                trasa: List[int],
                najlepsza_odleglosc: float,
                nazwa_instancji: str) -> None:
    """
    Wizualizuje znalezioną trasę.
    """
    plt.figure(figsize=(12, 8))

    # Rysowanie połączeń między miastami
    for i in range(len(trasa) - 1):
        x_wartosci = [miasta[trasa[i]][0], miasta[trasa[i + 1]][0]]
        y_wartosci = [miasta[trasa[i]][1], miasta[trasa[i + 1]][1]]
        plt.plot(x_wartosci, y_wartosci, 'b-', alpha=0.6)

    # Rysowanie punktów miast
    for miasto_id, koordynaty in miasta.items():
        if miasto_id == trasa[0]:  # Miasto startowe
            plt.plot(koordynaty[0], koordynaty[1], 'ro', markersize=10)
            plt.text(koordynaty[0], koordynaty[1], f'Start ({miasto_id})',
                     fontsize=8, ha='right')
        else:
            plt.plot(koordynaty[0], koordynaty[1], 'ko', markersize=6)
            plt.text(koordynaty[0], koordynaty[1], str(miasto_id),
                     fontsize=8, ha='right')

    plt.title(f"Problem TSP - {nazwa_instancji}\n"
              f"Długość trasy: {najlepsza_odleglosc:.2f}")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True, alpha=0.3)
    plt.show()


def zapisz_wyniki(sciezka: str,
                  wyniki: dict) -> None:
    """
    Zapisuje wyniki do pliku w formacie CSV.
    """
    with open(sciezka, 'w') as f:
        f.write("Instancja,Liczba_miast,Najlepsza_odleglosc,Czas_wykonania\n")
        for instancja, dane in wyniki.items():
            f.write(f"{instancja},{dane['liczba_miast']},"
                    f"{dane['najlepsza_odleglosc']:.2f},{dane['czas']:.2f}\n")


def main():
    # Parametry algorytmu
    ROZMIAR_POPULACJI = 100
    LICZBA_GENERACJI = 5000
    WSPOLCZYNNIK_MUTACJI = 0.02
    ROZMIAR_TURNIEJU = 5

    # Lista instancji do przetestowania
    instancje = ["bier127"]  # Możesz dodać więcej instancji
    wyniki = {}

    for instancja in instancje:
        print(f"\nRozwiązywanie instancji: {instancja}")

        # Wczytaj dane
        sciezka_pliku = f"instancje/{instancja}.txt"
        miasta, liczba_miast = wczytaj_miasta(sciezka_pliku)

        # Mierz czas wykonania
        czas_start = time.perf_counter()

        # Uruchom algorytm genetyczny
        najlepsza_odleglosc, najlepsza_trasa = genetic_algorithm(
            miasta,
            pop_size=ROZMIAR_POPULACJI,
            generations=LICZBA_GENERACJI,
            mutation_rate=WSPOLCZYNNIK_MUTACJI,
            tournament_size=ROZMIAR_TURNIEJU
        )

        czas_wykonania = time.perf_counter() - czas_start

        # Zapisz wyniki
        wyniki[instancja] = {
            'liczba_miast': liczba_miast,
            'najlepsza_odleglosc': najlepsza_odleglosc,
            'czas': czas_wykonania
        }

        # Wyświetl raport
        print("\n----- RAPORT -----")
        print(f"Instancja: {instancja}")
        print(f"Liczba miast: {liczba_miast}")
        print(f"Najlepsza znaleziona odległość: {najlepsza_odleglosc:.2f}")
        print(f"Czas wykonania: {czas_wykonania:.2f} sekund")
        print(f"Najlepsza trasa: {' -> '.join(map(str, najlepsza_trasa))}")

        # Wizualizuj wyniki
        rysuj_trase(miasta, najlepsza_trasa, najlepsza_odleglosc, instancja)



if __name__ == "__main__":
    main()