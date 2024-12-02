import random
import math
import time
import numpy as np
import matplotlib.pyplot as plt

# Generowanie miast
def generate_cities(num_cities, max_coord=5000):
    cities = set()
    while len(cities) < num_cities:
        x = random.randint(0, max_coord)
        y = random.randint(0, max_coord)
        cities.add((x, y))
    return list(cities)

# Zapis miast do pliku
def save_cities_to_file(cities, file_path):
    with open(file_path, "w") as writer:
        writer.write(f"{len(cities)}\n")
        for number, (x, y) in enumerate(cities, start=1):
            writer.write(f"{number} {x} {y}\n")

# Obliczanie odległości
def calculate_distance_matrix(cities):
    num_cities = len(cities)
    distance_matrix = [[0] * num_cities for _ in range(num_cities)]
    for i in range(num_cities):
        for j in range(i + 1, num_cities):
            distance = math.sqrt((cities[i][0] - cities[j][0]) ** 2 + (cities[i][1] - cities[j][1]) ** 2)
            distance_matrix[i][j] = distance
            distance_matrix[j][i] = distance
    return distance_matrix

# Inicjalizacja populacji
def initialize_population(size, num_cities):
    population = []
    for _ in range(size):
        individual = list(range(num_cities))
        random.shuffle(individual)
        population.append(individual)
    return population

# Funkcja oceny
def calculate_distance(route, distance_matrix):
    return sum(distance_matrix[route[i - 1]][route[i]] for i in range(len(route)))

def evaluate_population(population, distance_matrix):
    return [calculate_distance(individual, distance_matrix) for individual in population]

# Operator krzyżowania DPX
def dpx(parent1, parent2):
    size = len(parent1)
    common_subpaths = []
    i = 0
    while i < size:
        if parent1[i] == parent2[i]:
            start = i
            while i < size and parent1[i] == parent2[i]:
                i += 1
            common_subpaths.append((start, i))
        i += 1

    child = [-1] * size
    for start, end in common_subpaths:
        for i in range(start, end):
            child[i] = parent1[i]

    def find_next_node(remaining_nodes, current_node):
        for node in remaining_nodes:
            if node != -1:
                return node
        return -1

    remaining_nodes1 = [-1 if node in child else node for node in parent1]
    remaining_nodes2 = [-1 if node in child else node for node in parent2]
    current_node = find_next_node(remaining_nodes1, -1)
    for i in range(size):
        if child[i] == -1:
            if current_node in remaining_nodes1:
                child[i] = current_node
                remaining_nodes1[remaining_nodes1.index(current_node)] = -1
                current_node = find_next_node(remaining_nodes1, current_node)
            else:
                child[i] = current_node
                remaining_nodes2[remaining_nodes2.index(current_node)] = -1
                current_node = find_next_node(remaining_nodes2, current_node)

    return child

# Mutacja
def mutate(individual):
    a, b = random.sample(range(len(individual)), 2)
    individual[a], individual[b] = individual[b], individual[a]

# Algorytm Genetyczny
def genetic_algorithm(cities, population_size=100, generations=500, mutation_rate=0.01):
    num_cities = len(cities)
    distance_matrix = calculate_distance_matrix(cities)
    population = initialize_population(population_size, num_cities)
    for _ in range(generations):
        new_population = []
        evaluated_population = evaluate_population(population, distance_matrix)
        for __ in range(population_size // 2):
            parents = random.choices(population, k=2, weights=[1 / d for d in evaluated_population])
            child1 = dpx(parents[0], parents[1])
            child2 = dpx(parents[1], parents[0])
            if random.random() < mutation_rate:
                mutate(child1)
            if random.random() < mutation_rate:
                mutate(child2)
            new_population.extend([child1, child2])
        population = new_population

    best_individual = min(population, key=lambda ind: calculate_distance(ind, distance_matrix))
    return best_individual, calculate_distance(best_individual, distance_matrix)

def load_cities_from_file(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()
        num_cities = int(lines[0].strip())
        cities = []
        for line in lines[1:]:
            _, x, y = map(int, line.strip().split())
            cities.append((x, y))
    return cities

def rysujSciezke(miasta, sciezka, najlepszaOdleglosc, instancja):
    fig = plt.figure(figsize=(10, 8))
    startoweMiasto = sciezka[0]

    for i in range(len(sciezka) - 1):
        xValues = [miasta[sciezka[i]][0], miasta[sciezka[i + 1]][0]]
        yValues = [miasta[sciezka[i]][1], miasta[sciezka[i + 1]][1]]

        kolor = np.random.rand(3, )

        plt.plot(xValues, yValues, marker='o', color=kolor)

        plt.annotate('', xy=(miasta[sciezka[i + 1]][0], miasta[sciezka[i + 1]][1]),
                     xytext=(miasta[sciezka[i]][0], miasta[sciezka[i]][1]),
                     arrowprops=dict(arrowstyle='->', color=kolor, lw=1.5))

    for miasto in range(1, len(miasta)):
        if miasto == startoweMiasto:
            plt.plot(miasta[miasto][0], miasta[miasto][1], 'ro', markersize=6)
            plt.text(
                miasta[startoweMiasto][0], miasta[startoweMiasto][1],
                f'{startoweMiasto}', fontsize=6, ha='left',
                bbox=dict(facecolor='red', alpha=0.9, edgecolor='black', boxstyle='round,pad=0.3')
            )
        else:
            plt.text(
                miasta[miasto][0], miasta[miasto][1], str(miasto),
                fontsize=6,
                bbox=dict(facecolor='white', alpha=0.75, edgecolor='black', boxstyle='round,pad=0.3')
            )

    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid()

    fig.canvas.manager.set_window_title(f"{instancja}")
    plt.show()

# Główna część programu
file_path = "instancje/berlin52.txt"

# Wczytywanie miast z pliku
cities = load_cities_from_file(file_path)

# Uruchamianie algorytmu genetycznego
best_route, best_distance = genetic_algorithm(cities)
print("Najlepsza trasa:", best_route)
print("Najkrótsza odległość:", best_distance)
rysujSciezke(cities, best_route, "najlepszaOdleglosc", "instancja")