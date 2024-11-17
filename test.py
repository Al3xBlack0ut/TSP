import random



def krzyzowanieRodzicow(rodzic1, rodzic2):
    dlugosc = len(rodzic1)
    start = random.randint(1, len(rodzic1) - 2)
    end = random.randint(start + 1, len(rodzic1) - 1)
    print(start,end)
    dziecko = [None] * dlugosc

    for i in range(end-start+1):
        dziecko[i] = rodzic1[start+i]

    j = dziecko.index(None)
    for m in rodzic2:
        if m not in dziecko:
            dziecko[j]=m
            j+=1


    dziecko[dlugosc-1] = dziecko[0]
    return dziecko







# Przykładowi rodzice
parent1 = [1, 2, 3, 4, 5, 6, 7, 1]
parent2 = [3, 7, 1, 6, 4, 5, 2, 3]

# Generowanie potomków
dziecko1 = krzyzowanieRodzicow(parent1, parent2)
dziecko2 = krzyzowanieRodzicow(parent1, parent2)

print("Rodzic 1:  ", parent1)
print("Rodzic 2:  ", parent2)
print("Potomek 1:", dziecko1)
print("Potomek 2:", dziecko2)
