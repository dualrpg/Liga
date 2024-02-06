from random import choices, shuffle, randint
from collections import Counter

def matchup(matchUp):
    team1 = matchUp[0]
    team2 = matchUp[1]
    results = choices([team1[0], team2[0], "Fallos"], [team1[1]*10, team2[1]*10, 10000], k=15)
    counted_results = Counter(results)
    return counted_results

def createSchedule(listado):
    """ Create a schedule for the teams in the list and return it"""
    s = []
    shuffle(listado)
    if len(listado) % 2 == 1: listado = listado + ["BYE"]

    for i in range(len(listado)-1):

        mid = int(len(listado) / 2)
        l1 = listado[:mid]
        l2 = listado[mid:]
        l2.reverse()    

        # Switch sides after each round
        if(i % 2 == 1):
            s = s + [ zip(l1, l2) ]
        else:
            s = s + [ zip(l2, l1) ]

        listado.insert(1, listado.pop())

    return s


def schedule(division):
    matches = []
    for round in createSchedule(division):
        for match in round:
            matches.append(match)
    return matches


# def faltas(agresividad:str):
#     match agresividad:
#         case "blando":
#             intensidad = [,]
#     faltas = choices([True, False], [intensidad], k=1)
#     if faltas[0]:
#         nfaltas = randint(1,6)
#         return nfaltas
        
