import random

liczbaMiast = 100
sciezkaPliku = "instancje/graf.txt"
miasta = set()

while len(miasta) < liczbaMiast:
    x = random.randint(0, 5000)
    y = random.randint(0, 5000)
    miasta.add((x, y))

with open(sciezkaPliku, "w") as writer:
    writer.write(f"{liczbaMiast}\n")
    for numer, (x, y) in enumerate(miasta, start=1):
        writer.write(f"{numer} {x} {y}\n")

print(f"Wygenerowano {len(miasta)} miast i zapisano do pliku {sciezkaPliku}.")
