import glob
import csv
from functools import cmp_to_key

def readcsv(name):
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


def time_to_secs(time_string):
    times = time_string.split(":")
    return int(times[0]) * 3600 + int(times[1]) * 60 + int(times[2])

def secs_to_time(time_int):
    hours = str(time_int // 3600)
    time_int %= 3600
    minutes = str(time_int // 60)
    time_int %= 60
    seconds = str(time_int)
    final_string = ""
    if (len(hours) == 1): final_string += "0"
    final_string += hours + ":"
    if (len(minutes) == 1): final_string += "0"
    final_string += minutes + ":"
    if (len(seconds) == 1): final_string += "0"
    final_string += seconds
    return final_string

def table_position(pos):
    if pos == 1:
        return "<td style='color: rgb(255, 215, 0); font-size: 30px; font-weight: 700;'>" + str(pos) + "</td>"
    elif pos == 2:
        return "<td style='color: rgb(192, 192, 192); font-size: 27px; font-weight: 600;'>" + str(pos) + "</td>"
    elif pos == 3:
        return "<td style='color: rgb(205,127,50); font-size: 24px; font-weight: 500;'>" + str(pos) + "</td>"
    return "<td>" + str(pos) + "</td>"

team_results = {} # team name: [[pts1, penalty1], [pts2, penalty2], ...]

# read files
for scores_file in glob.glob("contests/*.csv"):
    for line in readcsv(scores_file)[1:]:
        if line[0] not in team_results:
            team_results[line[0]] = []
        team_results[line[0]].append([int(line[1]), time_to_secs(line[2])])

# create sorted leaderboard
curr_leaderboard_results = [] # [[pts1, penalty1, team name]]

for team in team_results:
    team_curr_result = best_6_results(team_results[team])
    team_curr_result.append(team)
    curr_leaderboard_results.append(team_curr_result)

curr_leaderboard_results.sort(key=cmp_to_key(compare))

for team in curr_leaderboard_results:
    team[1] = secs_to_time(team[1])
  
# create table
tableTeams = [
    "<table style='width:85%; margin-left: auto; margin-right: auto;'>",
    '''
    <tr class='main-table'>
        <th>Position</th>
        <th>Team Name</th>
        <th style='background-color: rgb(65, 105, 225); color: white; font-weight: 600'>Problems Solved</th>
        <th>Total Penalty (HH:MM:SS)</th>
    </tr>
    '''    
]

pos = 0
prev_score = 0
prev_time = ""

for result in curr_leaderboard_results:
    if (result[0] != prev_score or result[1] != prev_time): pos += 1
    prev_score = result[0]
    prev_time = result[1]
    tableTeams.append("<tr class='main-table table-data'>"
                      + table_position(pos)
                      + "<td>" + result[2] + "</td>"
                      + "<td>" + str(result[0]) + "</td>"
                      + "<td>" + result[1] + "</td>"
                      + "</tr>")

tableTeams.append("</table>")

# create doc
lines = [
    '''
    <!DOCTYPE html>
    <html>
      <link rel="preconnect" href="https://fonts.googleapis.com">
      <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
      <link href="https://fonts.googleapis.com/css2?family=Inter:ital,opsz,wght@0,14..32,100..900;1,14..32,100..900&display=swap" rel="stylesheet">
      <style>
          table {
              border-spacing:0;
          }
          .main-table {
              height:50px;
          }
          .second-table {
              height:35px;
          }
          tr.table-data:hover {
              filter: brightness(0.9);
              transition: 0.15s;
          }
          tr:nth-child(odd) {
              background-color: rgb(247, 247, 247);
              transition: 0.15s;
          }
          tr:nth-child(even) {
              background-color: rgb(253, 253, 253);
              transition: 0.15s;
          }
          th {
              padding: 5px;
              text-align:center;
              color: rgb(64,64,64);
              background-color: rgb(230, 240, 255);
              font-family: Inter;
              font-size: 20px;
              font-weight: 500;
          }
          td {
              text-align:center;
              font-family: Inter;
              font-size: 15px;
              color: black;
          }
      </style>
      <head>
          <title>2025 AUCPL Standings</title>
      </head>
      <body>
      <h1 style='font-family: Inter; font-weight: 800'>2025 AUCPL Standings</h1>
      ''']

for line in tableTeams:
    lines.append(line)

lines.append("</body></html>")

f = open("test.html", "w", encoding="utf-8")

for line in lines:
    f.write(line)

f.close()

