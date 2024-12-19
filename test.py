import csv

def readcsv(name):
    with open(name) as fp:
        reader = csv.reader(fp, delimiter=",", quotechar='"')
        data_read = [row for row in reader]
    return data_read

results = readcsv("results.csv")
scoring = readcsv("scoring.csv")

# all of these store something in the form (123, TeamName) or TeamName: someValue
prevTeamPoints = []
currTeamPoints = []
currTeamPlayed = {}
teamBestResult = {} 
currTeamResult = {}
pointsByPos = {}

tablePoints = [
    "<table>",
    """<tr>
        <th>Position</th>
        <th>Points Awarded</th>
    </tr>""",
    "</table>"
]


for i in range(1, len(scoring)):
    tablePoints.insert(1 + i, "<tr><td>" + str(i) + "</td><td>" + scoring[i][1] + "</td></tr>")
    pointsByPos[scoring[i][0]] = int(scoring[i][1])

for i in range(1, len(results)): # score and previous week score for each team
    teamScore = [0 if results[i][1] == "-1" else int(results[i][1])]
    teamPlayed = 0
    bestResult = 9999
    latestResult = "No Participation" if results[i][-1] == "-1" else results[i][-1]
    for j in range(1, len(results[0])):
        if results[i][j] in pointsByPos: 
            teamScore.append(teamScore[-1] + pointsByPos[results[i][j]]) 
        else:
            teamScore.append(teamScore[-1])
        if results[i][j] != "-1":
            teamPlayed += 1
            if int(results[i][j]) < bestResult: bestResult = int(results[i][j])

    teamName = results[i][0]
    prevTeamPoints.append((teamScore[-2], teamName)) 
    currTeamPoints.append((teamScore[-1], teamName))
    bestResult = "No Participation" if bestResult == 9999 else str(bestResult)
    
    currTeamPlayed[teamName] = teamPlayed
    currTeamResult[teamName] = latestResult
    teamBestResult[teamName] = bestResult

prevTeamPoints.sort(reverse=True)
currTeamPoints.sort(reverse=True)

f = open("test.html", "w")

tableTeams = [
    "<table>",
    """<tr>
        <th>Position</th>
        <th>Team</th>
        <th>Score</th>
        <th>Prev Score</th>
        <th>Change in Position</th>
        <th>Number Played</th>
        <th>Best Result</th>
        <th>Latest Result</th>
    </tr>""",
    "</table>"
]

for i in range(0, len(currTeamPoints)):
    teamName = currTeamPoints[i][1]
    tableTeams.insert(i + 2, "<tr><td>" + str(i + 1) # Position
                      + "</td><td>" + teamName # team name
                      + "</td><td>" + str(currTeamPoints[i][0]) # team curr points
                      + "</td><td>" + str([item for item in prevTeamPoints if teamName in item][0][0]) # prev week points
                      + "</td><td>" + str(prevTeamPoints.index([item for item in prevTeamPoints if teamName in item][0]) - i) # change in pos
                      + "</td><td>" + str(currTeamPlayed[teamName]) # played in
                      + "</td><td>" + teamBestResult[teamName] # best
                      + "</td><td>" + currTeamResult[teamName] # latest
                      + "</td></tr>")

# print(table)

lines = ["<html>",
            "<body>", 
            "<h2>Stuff</h2>", 
            "</body>",
            "</html>"]

for index, value in enumerate(tablePoints, start=3):
    lines.insert(index, value)

for index, value in enumerate(tableTeams, start=3):
    lines.insert(index, value)

for i in lines:
    f.write(i + "\n")

f.close() 