from stats_util import s_mean_confidence_interval
from parser import parse_repetition
import json

REPETITIONS = 35

def parse_scenario(scenario):

    scenario_results = {}
    scenario_ci = {}
    outcomes = {}

    for i in range(0, REPETITIONS):
        results = parse_repetition(scenario + "-#" + str(i))
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

    with open(f"analysis/{scenario.split('/')[-1]}.json", "a") as file:
        file.write(json.dumps(scenario_ci, indent=4))
