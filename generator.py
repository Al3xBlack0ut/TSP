import random

liczbaMiast = 100000
sciezkaPliku = "graf.txt"
miasta = {}

while len(miasta) < liczbaMiast:
    x = random.randint(0, 3000)
    y = random.randint(0, 3000)
    numerMiasta = len(miasta) + 1

    if (x, y) not in miasta.values():
        miasta[numerMiasta] = (x, y)

with open(sciezkaPliku, "w") as writer:
    writer.write(f"{liczbaMiast}\n")
    for numer, (x, y) in miasta.items():
        writer.write(f"{numer} {x} {y}\n")

print(f"Wygenerowano {liczbaMiast} miast i zapisano do pliku {sciezkaPliku}.")

