from stats_util import s_mean_confidence_interval
from parser import parse_repetition
import json
import sys

def parse_scenario(scenario, reps = 35):

    scenario_results = {}
    scenario_ci = {}
    outcomes = {}

    for i in range(0, reps):
        results = parse_repetition(scenario + "-#" + str(i))
        if results == None:
            continue
        for metric in results:
            if not metric in scenario_results:
                scenario_results[metric] = []
            scenario_results[metric].append(results[metric])

    
    for key in scenario_results:
        if "outcome" in key:
            if "count" in key:
                if not key in outcomes:
                    outcomes[key] = 0
                for i in range(0, len(scenario_results[key])):
                    outcomes[key] += scenario_results[key][i]
        else:
            low, high = s_mean_confidence_interval(scenario_results[key])
            scenario_ci[key] = [low, high]

    with open(f"./analysis/{scenario.split('/')[-1]}.json", "a") as file:
        file.write(json.dumps(scenario_ci, indent=4))
        
<<<<<<< HEAD
if __name__=="__main__":
    if len(sys.argv) > 2:
        parse_scenario(sys.argv[1], int(sys.argv[2]))
=======
if __name__ == "__main__":
    parse_scenario(sys.argv[1], int(sys.argv[2]))
>>>>>>> 290742baabb1430dabc8292b1fe5650c612c7518
