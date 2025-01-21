# genetyczny.py

from typing import List, Tuple, Dict
import random
import math


def calculate_distance(city1: Tuple[float, float], city2: Tuple[float, float]) -> float:
    """Oblicza odległość euklidesową między dwoma miastami."""
    return math.sqrt((city2[0] - city1[0]) ** 2 + (city2[1] - city1[1]) ** 2)


def create_distance_matrix(cities: Dict[int, Tuple[float, float]]) -> Dict[Tuple[int, int], float]:
    """Tworzy macierz odległości między wszystkimi miastami dla szybszego dostępu."""
    distances = {}
    for i in cities:
        for j in cities:
            if i != j:
                distances[(i, j)] = calculate_distance(cities[i], cities[j])
    return distances


def calculate_path_cost(path: List[int], distance_matrix: Dict[Tuple[int, int], float]) -> float:
    """Oblicza całkowitą długość ścieżki."""
    total_cost = 0
    for i in range(len(path) - 1):
        total_cost += distance_matrix.get((path[i], path[i + 1]), float('inf'))
    return total_cost


def two_opt_improvement(path: List[int], distance_matrix: Dict[Tuple[int, int], float]) -> List[int]:
    """Implementacja lokalnego przeszukiwania 2-opt."""
    improved = True
    best_distance = calculate_path_cost(path, distance_matrix)

    while improved:
        improved = False
        for i in range(1, len(path) - 2):
            for j in range(i + 1, len(path) - 1):
                if (distance_matrix.get((path[i - 1], path[j]), float('inf')) +
                    distance_matrix.get((path[i], path[j + 1]), float('inf'))) < (
                        distance_matrix.get((path[i - 1], path[i]), float('inf')) +
                        distance_matrix.get((path[j], path[j + 1]), float('inf'))):
                    # Wykonaj 2-opt zamianę
                    path[i:j + 1] = reversed(path[i:j + 1])
                    new_distance = calculate_path_cost(path, distance_matrix)
                    if new_distance < best_distance:
                        best_distance = new_distance
                        improved = True
                    else:
                        # Cofnij zmianę jeśli nie było poprawy
                        path[i:j + 1] = reversed(path[i:j + 1])

    return path


def generate_initial_population(cities: Dict[int, Tuple[float, float]],
                                pop_size: int,
                                distance_matrix: Dict[Tuple[int, int], float]) -> List[List[int]]:
    """
    Generuje początkową populację używając różnych metod:
    - 40% populacji metodą najbliższego sąsiada z różnych punktów startowych
    - 30% populacji metodą insertion z lokalną optymalizacją
    - 30% populacji losowo z 2-opt
    """
    population = []
    city_count = len(cities)

    # Nearest Neighbor - 40% populacji
    for _ in range(int(pop_size * 0.4)):
        path = [random.randint(1, city_count)]
        unvisited = set(range(1, city_count + 1)) - {path[0]}

        while unvisited:
            current = path[-1]
            next_city = min(unvisited,
                            key=lambda x: distance_matrix.get((current, x), float('inf')))
            path.append(next_city)
            unvisited.remove(next_city)
        path.append(path[0])
        path = two_opt_improvement(path, distance_matrix)  # Dodatkowa optymalizacja
        population.append(path)

    # Insertion method z lokalną optymalizacją - 30% populacji
    for _ in range(int(pop_size * 0.3)):
        path = [random.randint(1, city_count)]
        unvisited = list(range(1, city_count + 1))
        unvisited.remove(path[0])

        while unvisited:
            # Wybierz losowe miasto do wstawienia
            city = unvisited.pop(random.randint(0, len(unvisited) - 1))

            # Znajdź najlepszą pozycję do wstawienia
            best_pos = 0
            best_increase = float('inf')

            for i in range(len(path)):
                prev_city = path[i - 1] if i > 0 else path[-1]
                next_city = path[i] if i < len(path) else path[0]

                increase = (distance_matrix.get((prev_city, city), float('inf')) +
                            distance_matrix.get((city, next_city), float('inf')) -
                            distance_matrix.get((prev_city, next_city), float('inf')))

                if increase < best_increase:
                    best_increase = increase
                    best_pos = i

            path.insert(best_pos, city)

        path.append(path[0])
        path = two_opt_improvement(path, distance_matrix)
        population.append(path)

    # Random with 2-opt - 30% populacji
    for _ in range(pop_size - len(population)):
        path = list(range(1, city_count + 1))
        random.shuffle(path)
        path.append(path[0])
        path = two_opt_improvement(path, distance_matrix)
        population.append(path)

    return population


def edge_assembly_crossover(parent1: List[int], parent2: List[int],
                            distance_matrix: Dict[Tuple[int, int], float]) -> List[int]:
    """
    Implementacja Edge Assembly Crossover (EAX).
    """

    def create_edge_map(path: List[int]) -> Dict[int, List[int]]:
        edge_map = {}
        for i in range(len(path) - 1):
            if path[i] not in edge_map:
                edge_map[path[i]] = []
            if path[i + 1] not in edge_map:
                edge_map[path[i + 1]] = []
            edge_map[path[i]].append(path[i + 1])
            edge_map[path[i + 1]].append(path[i])
        return edge_map

    # Tworzenie map krawędzi dla obu rodziców
    edge_map1 = create_edge_map(parent1)
    edge_map2 = create_edge_map(parent2)

    # Inicjalizacja potomka
    unvisited = set(parent1[:-1])
    child = []

    # Wybierz losowe miasto startowe
    current = random.choice(list(unvisited))
    child.append(current)
    unvisited.remove(current)

    while unvisited:
        # Znajdź wszystkich kandydatów
        candidates = []
        if current in edge_map1:
            candidates.extend(c for c in edge_map1[current] if c in unvisited)
        if current in edge_map2:
            candidates.extend(c for c in edge_map2[current] if c in unvisited)

        if candidates:
            # Wybierz następne miasto bazując na odległości i częstości występowania
            next_city = min(candidates,
                            key=lambda x: distance_matrix.get((current, x), float('inf')) *
                                          (1.0 / (candidates.count(x) + 1)))
        else:
            # Jeśli brak kandydatów, wybierz najbliższe nieodwiedzone miasto
            next_city = min(unvisited,
                            key=lambda x: distance_matrix.get((current, x), float('inf')))

        child.append(next_city)
        unvisited.remove(next_city)
        current = next_city

    # Zamknij cykl
    child.append(child[0])
    return child


def adaptive_mutation(path: List[int], distance_matrix: Dict[Tuple[int, int], float],
                      mutation_rate: float, generation: int, max_generations: int) -> List[int]:
    """
    Adaptacyjny operator mutacji z różnymi strategiami.
    """
    if len(path) <= 3:
        return path

    # Adaptacja współczynnika mutacji
    current_rate = mutation_rate * (1 + math.cos(math.pi * generation / max_generations))

    # Kopia ścieżki do mutacji
    mutated = path[:-1]  # Usuń ostatni element (powrót do początku)

    # 2-opt mutacja
    if random.random() < current_rate:
        for _ in range(2):  # Maksymalnie 2 zamiany
            if len(mutated) >= 4:  # Sprawdzamy czy trasa jest wystarczająco długa
                i = random.randint(1, len(mutated) - 3)  # Zmniejszamy zakres o 1
                j = random.randint(i + 1, len(mutated) - 2)  # Zmniejszamy zakres o 1
                if (distance_matrix.get((mutated[i - 1], mutated[j]), float('inf')) +
                    distance_matrix.get((mutated[i], mutated[j + 1]), float('inf'))) < (
                        distance_matrix.get((mutated[i - 1], mutated[i]), float('inf')) +
                        distance_matrix.get((mutated[j], mutated[j + 1]), float('inf'))):
                    mutated[i:j + 1] = reversed(mutated[i:j + 1])

    # Insert mutation
    if random.random() < current_rate / 2:
        idx1 = random.randint(1, len(mutated) - 1)
        idx2 = random.randint(1, len(mutated) - 1)
        city = mutated.pop(idx1)
        mutated.insert(idx2, city)

    # Reverse mutation
    if random.random() < current_rate / 3:
        i = random.randint(1, len(mutated) - 2)
        j = random.randint(i + 1, len(mutated) - 1)
        mutated[i:j + 1] = reversed(mutated[i:j + 1])

    # Zamknij cykl
    mutated.append(mutated[0])
    return mutated


def tournament_selection(population: List[List[int]], distance_matrix: Dict[Tuple[int, int], float],
                         tournament_size: int) -> List[int]:
    """Selekcja turniejowa z adaptacyjną wielkością turnieju."""
    tournament = random.sample(population, tournament_size)
    return min(tournament, key=lambda x: calculate_path_cost(x, distance_matrix))


def genetic_algorithm(cities: Dict[int, Tuple[float, float]],
                      pop_size: int = 100,
                      generations: int = 1000,
                      mutation_rate: float = 0.02,
                      tournament_size: int = 5) -> Tuple[float, List[int]]:
    """
    Główna funkcja algorytmu genetycznego z mechanizmami przeciwdziałającymi
    utknięciu w minimum lokalnym.
    """
    # Utworzenie macierzy odległości
    distance_matrix = create_distance_matrix(cities)

    # Inicjalizacja populacji
    population = generate_initial_population(cities, pop_size, distance_matrix)
    best_distance = float('inf')
    best_path = None
    stagnation_counter = 0

    # Parametry adaptacyjne
    min_tournament_size = 3
    max_tournament_size = 7
    current_tournament_size = tournament_size

    for generation in range(generations):
        new_population = []

        # Elityzm - zachowaj najlepszego osobnika
        elite = min(population, key=lambda x: calculate_path_cost(x, distance_matrix))
        new_population.append(elite)

        # Adaptacja parametrów w zależności od stagnacji
        if stagnation_counter > 20:
            current_tournament_size = max(min_tournament_size, current_tournament_size - 1)
            mutation_rate *= 1.05
        else:
            current_tournament_size = min(max_tournament_size, tournament_size)
            mutation_rate = max(0.01, mutation_rate * 0.95)

        # Tworzenie nowej populacji
        while len(new_population) < pop_size:
            parent1 = tournament_selection(population, distance_matrix, current_tournament_size)
            parent2 = tournament_selection(population, distance_matrix, current_tournament_size)

            # Krzyżowanie
            child = edge_assembly_crossover(parent1, parent2, distance_matrix)

            # Mutacja
            child = adaptive_mutation(child, distance_matrix, mutation_rate, generation, generations)

            new_population.append(child)

        # Aktualizacja populacji
        population = new_population

        # Sprawdzenie najlepszego rozwiązania
        current_best = min(population, key=lambda x: calculate_path_cost(x, distance_matrix))
        current_distance = calculate_path_cost(current_best, distance_matrix)

        if current_distance < best_distance:
            best_distance = current_distance
            best_path = current_best.copy()
            stagnation_counter = 0
        else:
            stagnation_counter += 1

        # Restart populacji przy długiej stagnacji
        if stagnation_counter > 50:
            half_size = pop_size // 2
            population = population[:half_size]
            population.extend(generate_initial_population(cities, pop_size - half_size, distance_matrix))
            stagnation_counter = 0

        if generation % 100 == 0:
            print(f"Generacja {generation}: {best_distance:.2f}")

    return best_distance, best_path