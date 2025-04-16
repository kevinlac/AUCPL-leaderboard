import glob
import csv
from time_utils import time_to_secs, secs_to_time
from functools import cmp_to_key

def read_csv(name):
    with open(name) as fp:
        reader = csv.reader(fp, delimiter=",")
        data_read = [row for row in reader]
    return data_read

def compare(item1, item2): # prioritize higher points then lower time
    if item1[0] != item2[0]:
        return -(item1[0] - item2[0])
    return item1[1] - item2[1]

def best_6_results(list_of_results):
    list_of_results.sort(key=cmp_to_key(compare))
    while (len(list_of_results) > 6): list_of_results.pop()
    total_score = 0
    total_penalty = 0
    for item in list_of_results:
        total_score += item[0]
        total_penalty += item[1]
    return [total_score, total_penalty]

def get_parsed_data():
    PENALTY_MULT = 4
    all_results = {} # team name: [[pts1, penalty1], [pts2, penalty2], ...]
    for scores_file in glob.glob("contests/*.csv"): # per event
        event_results = {} # team name: [score, penalty]
        csv_parsed = read_csv(scores_file)
        for line in range(2, len(read_csv(scores_file)), 2):
            team = csv_parsed[line][1]
            points = int(csv_parsed[line][-1])
            penalty = time_to_secs(csv_parsed[line + 1][-1])
            submitted = False
            for time in csv_parsed[line + 1][:-1]:
                if time != "":
                    submitted = True
            
            if team != "" and submitted:
                if team not in event_results:
                    event_results[team] = [points, penalty]
                else:
                    # if two submissions or more, then apply time penalty
                    event_results[team][1] *= PENALTY_MULT
            
        for team in event_results:
            if team not in all_results:
                all_results[team] = []
            all_results[team].append(event_results[team])

    parsed_leaderboard_results = []
    for team in all_results:
        team_curr_result = best_6_results(all_results[team])
        team_curr_result.append(team)
        parsed_leaderboard_results.append(team_curr_result)

    parsed_leaderboard_results.sort(key=cmp_to_key(compare))

    for team in parsed_leaderboard_results:
        team[1] = secs_to_time(team[1])
    
    return parsed_leaderboard_results
