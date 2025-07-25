# Problem Komiwojażera (TSP) – Algorytm Genetyczny
Autor: **Aleks Czarnecki**
Ten projekt rozwiązuje problem komiwojażera (TSP) przy użyciu algorytmu genetycznego oraz metod zachłannych. Pozwala na testowanie różnych instancji problemu, wizualizację tras oraz generowanie nowych instancji.

---

## Struktura projektu

- `main.py` – główny plik uruchamiający algorytm, wizualizujący trasę i raportujący wyniki.
- `genetyczny.py` – implementacja algorytmu genetycznego, operatorów krzyżowania, mutacji (2-opt), selekcji turniejowej oraz generowania populacji.
- `zachlanny.py` – algorytm zachłanny najbliższego sąsiada
- `generator.py` – generator nowych instancji miast.
- `instancje/` – przykładowe pliki z instancjami problemu TSP.
- `pseudokod.txt` – pseudokod algorytmów.
- `sprawozdanie.pdf` – dokumentacja projektu.

---

## Wymagania

- Python 3.8+
- NumPy
- Numba
- Matplotlib

Możesz zainstalować wymagane biblioteki poleceniem:

```
pip install numpy numba matplotlib
```

---

## Uruchomienie

1. Wybierz instancje do testowania w pliku `main.py` (lista `instancje/`).
2. Uruchom program:

```
python main.py
```

3. Wyniki zostaną wyświetlone w konsoli oraz zwizualizowane w oknie matplotlib.

---

## Generowanie nowych instancji

Aby wygenerować nowy plik z miastami, uruchom `generator.py`:

```
python generator.py
```

---

## Najważniejsze funkcje

- `algorytmGenetyczny` (`genetyczny.py`) – główna funkcja algorytmu genetycznego.
- `generujPopulacjePoczatkowa` (`genetyczny.py`) – generowanie początkowej populacji tras.
- `krzyzeowanieEAX` (`genetyczny.py`) – operator krzyżowania tras.
- `poprawa2opt` (`genetyczny.py`) – lokalna optymalizacja tras (mutacja).
- `rysujTrase` (`main.py`) – wizualizacja najlepszej znalezionej trasy.

---

## Pliki instancji

Pliki w folderze `instancje/` zawierają współrzędne miast w formacie:

```
LiczbaMiast
ID X Y
ID X Y
...
```
