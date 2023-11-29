import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation

import random
from typing import List

population = []
table = {
    "F"  : 50,
    "G"  : 67,
    "Mo" : 33,
    "Mix": (0.5, 0.5) # Pr(Mo), Pr(G)
}
# Create a figure and axis object
fig, ax = plt.subplots()
# Plot the data points
ax.set_xlabel('Generations')
ax.set_ylabel('Population Proportion')
ax.set_title('Something about sharing cake...')


def createPlayer(strategy : str, fitness : int = 0) -> list:
    return [strategy, fitness]

def m(f : float, tup : tuple) -> tuple:
    return tuple(f * i for i in tup)

def a(tup1 : float, tup2 : tuple) -> tuple:
    return tuple([tup1[i] + tup2[i] for i in range(len(tup1))])

def checkValue(player1 : list, player2 : list) -> tuple:
    s1 = player1[0]
    s2 = player2[0]
    p1 = table["Mix"][0]
    p2 = table["Mix"][1]
    if (s1 == "Mix" and s2 == "Mix"):
        return a(a(m(p1*p1, checkValuePure("Mo", "Mo")),\
                   m(p1*p2, checkValuePure("Mo", "G"))), \
                 a(m(p2*p1, checkValuePure("G", "Mo")),\
                   m(p2*p2, checkValuePure("G", "G"))))
    if (s1 == "Mix"):
        return a(m(p1, checkValuePure("Mo", s2)), m(p2, checkValuePure("G", s2)))
    elif (s2 == "Mix"):
        return a(m(p1,checkValuePure(s1, "Mo")), m(p2, checkValuePure(s1, "G")))
        
    return checkValuePure(player1[0], player2[0])

def checkValuePure(s1 : str, s2 : str) -> tuple:
    if table[s1] + table[s2] > 100:
        return (0, 0)
    return (table[s1], table[s2])

def updateFitness(player1 : list, player2 : list):
    val = checkValue(player1, player2)
    player1[1] += val[0]
    player2[1] += val[1]

def initPopulation(size : int, p1 : float, p2 : float, p3 : float, p4 : float):
    for i in range(0, round(size*p1)):
        population.append(createPlayer("F", 0))
    for i in range(0, round(size*p2)):
        population.append(createPlayer("G", 0))
    for i in range(0, round(size*p3)):
        population.append(createPlayer("Mo", 0))
    for i in range(0, round(size*p4)):
        population.append(createPlayer("Mix", 0))

def populationUpdate():
    for player1 in population:
        player2 = random.choice(population)
        updateFitness(player1, player2)
        # print(player1)
    
def prunePopulation(pruneVal : int):
    population.sort(key=lambda x: -x[1])
    for i in range(pruneVal):
        population.pop()
    for i in range(0, pruneVal):
        population.append(createPlayer(population[i][0], 0))

def cleanPopulation():
    for player in population:
        player[1] = 0

def calcProps():
    p1 = 0.0;
    p2 = 0.0;
    p3 = 0.0;
    p4 = 0.0;
    for player in population:
        if   (player[0] == "F"): p1 += 1 
        elif (player[0] == "G"): p2 += 1
        elif (player[0] == "Mo"): p3 += 1
        elif (player[0] == "Mix"): p4 += 1
    return (p1 / len(population), p2 / len(population), p3 / len(population), p4 / len(population))

def main():

    size = 2000
    generations = 2500
    fair = []
    greedy = [] 
    modest = [] 
    mixed  = []
    x = []

    initPopulation(size, 0.25, 0.25, 0.25, 0.25)
    for i in range(0, generations):
        populationUpdate()
        prunePopulation(1)
        cleanPopulation()
        props = calcProps()
        # print(props)
        x.append(i)
        fair.append(props[0])
        greedy.append(props[1])
        modest.append(props[2])
        mixed.append(props[3])
        # ax.scatter(i, props[0], color='red',    label='Fair')
        # ax.scatter(i, props[1], color='blue',   label='Greedy')
        # ax.scatter(i, props[2], color='green',  label='Modest')
        # ax.scatter(i, props[3], color='orange', label='Mixed')

    ax.plot(x, fair, color='red',    label='Fair')
    ax.plot(x, greedy, color='blue',   label='Greedy')
    ax.plot(x, modest, color='green',  label='Modest')
    ax.plot(x, mixed, color='orange', label='Mixed')
    ax.legend()
    plt.show()
    
if __name__ == "__main__":
    main()