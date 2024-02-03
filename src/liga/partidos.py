from random import choices
from collections import Counter

def matchup(team1, team2):
    results = choices([team1["name"], team2["name"], "Fallos"], [team1["average"], team2["average"], 100], k=10)
    counted_results = Counter(results)
    return counted_results

print(matchup)