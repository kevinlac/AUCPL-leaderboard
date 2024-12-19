import csv

def readcsv(name):
    with open(name) as fp:
        reader = csv.reader(fp, delimiter=",", quotechar='"')
        data_read = [row for row in reader]
    return data_read

results = readcsv("results.csv")
scoring = readcsv("scoring.csv")

prevTeamPoints = []
currTeamPoints = []
currTeamPlayed = {}
teamBestResult = {}
currTeamResult = {}

tablePoints = [
    "<table>",
    "<tr>",
    "<th>Position</th>",
    "<th>Points Awarded</th>",
    "</tr>",
    "</table>"
]

pointsByPos = {} # dict of points for given position
for i in range(1, len(scoring)):
    tablePoints.insert(4 + i, "<tr><td>" + str(i) + "</td><td>" + scoring[i][1] + "</td></tr>")
    pointsByPos[scoring[i][0]] = int(scoring[i][1])

for i in range(1, len(results)): # score and previous week score for each team
    teamScore = 0
    teamPlayed = 0
    bestResult = 9999
    latestResult = "No Participation" if results[i][len(results[i]) - 1] == "-1" else results[i][len(results[i]) - 1]
    for j in range(1, len(results[i]) - 1):
        if (results[i][j] in pointsByPos): teamScore += pointsByPos[results[i][j]]
        if (results[i][j] != "-1"): teamPlayed += 1
        if (int(results[i][j]) != -1 and int(results[i][j]) < bestResult): bestResult = int(results[i][j])
    prevTeamPoints.append((teamScore, results[i][0])) # (score, name of team) of previous week
    if (results[i][len(results[i]) - 1] in pointsByPos): teamScore += pointsByPos[results[i][len(results[i]) - 1]]
    if (results[i][len(results[i]) - 1] != "-1"): teamPlayed += 1
    if (int(results[i][len(results[i]) - 1]) != -1 and int(results[i][len(results[i]) - 1]) < bestResult): bestResult = int(results[i][len(results[i]) - 1])
    bestResult = "No Participation" if bestResult == 9999 else str(bestResult)
    currTeamPoints.append((teamScore, results[i][0]))
    currTeamPlayed[results[i][0]] = teamPlayed
    currTeamResult[results[i][0]] = latestResult
    teamBestResult[results[i][0]] = bestResult

prevTeamPoints.sort(reverse=True)
currTeamPoints.sort(reverse=True)

f = open("test.html", "w")

tableTeams = [
    "<table>",
    "<tr>",
    "<th>Position</th>",
    "<th>Team</th>",
    "<th>Score</th>",
    "<th>Prev Score</th>",
    "<th>Change in Position</th>",
    "<th>Number Played</th>",
    "<th>Best Result</th>",
    "<th>Latest Result</th>",
    "</tr>",
    "</table>"
]

# for i in teams:
#     table.insert(3, "<td>" + i + "</td>")
for i in range(0, len(currTeamPoints)):

    tableTeams.insert(i + 10, "<tr><td>" + str(i + 1) # Position
                      + "</td><td>" + currTeamPoints[i][1] # team name
                      + "</td><td>" + str(currTeamPoints[i][0]) # team curr points
                      + "</td><td>" + str([item for item in prevTeamPoints if currTeamPoints[i][1] in item][0][0]) # prev week points
                      + "</td><td>" + str(prevTeamPoints.index([item for item in prevTeamPoints if currTeamPoints[i][1] in item][0]) - i) # change in pos
                      + "</td><td>" + str(currTeamPlayed[currTeamPoints[i][1]]) # played in
                      + "</td><td>" + teamBestResult[currTeamPoints[i][1]] # best
                      + "</td><td>" + currTeamResult[currTeamPoints[i][1]] # latest
                      + "</td></tr>")

# print(table)

lines = ["<html>",
          "<head>",
            "<title>Title</title> ", 
            "</head>" , 
            "<body>", 
            "<h2>Stuff</h2>", 
            "</body>",
            "</html>"]

for index, value in enumerate(tablePoints, start=6):
    lines.insert(index, value)

for index, value in enumerate(tableTeams, start=6):
    lines.insert(index, value)

for i in lines:
    f.write(i + "\n")

f.close() 