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
    "<table style='width:30%; margin-left: auto; margin-right: auto;'>",
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
    teamScore = [0 if results[i][1] == "-1" else pointsByPos[results[i][1]]]
    teamPlayed = 0 if results[i][1] == "-1" else 1
    bestResult = 9999 if results[i][1] == "-1" else int(results[i][1])
    latestResult = "No Participation" if results[i][-1] == "-1" else results[i][-1]
    for j in range(2, len(results[0])):
        if results[i][j] in pointsByPos: 
            teamScore.append(teamScore[-1] + pointsByPos[results[i][j]]) 
        else:
            teamScore.append(teamScore[-1])
        if results[i][j] != "-1":
            teamPlayed += 1
            if int(results[i][j]) < bestResult: bestResult = int(results[i][j])

    teamName = results[i][0]
    if len(teamScore) > 1: prevTeamPoints.append((teamScore[-2], teamName)) 
    currTeamPoints.append((teamScore[-1], teamName))
    bestResult = "No Participation" if bestResult == 9999 else str(bestResult)
    
    currTeamPlayed[teamName] = teamPlayed
    currTeamResult[teamName] = latestResult
    teamBestResult[teamName] = bestResult

prevTeamPoints.sort(reverse=True)
currTeamPoints.sort(reverse=True)

f = open("test.html", "w", encoding="utf-8")

tableTeams = [
    "<table style='width:50%; margin-left: auto; margin-right: auto;'>",
    """<tr>
        <th>Position</th>
        <th>   </th>
        <th>Team Name</th>
        <th>Score</th>
        <th>Contests Attended</th>
        <th>Best Result</th>
        <th>Latest Result</th>
    </tr>""",
    "</table>"
]

for i in range(0, len(currTeamPoints)):
    teamName = currTeamPoints[i][1]
    
    changeInPos = prevTeamPoints.index([item for item in prevTeamPoints if teamName in item][0]) - i if len(prevTeamPoints) > 0 else 0
    if changeInPos > 0:
        changeInPos = "<span style='color: green'>▲ </span>" + str(changeInPos)
    elif changeInPos < 0:
        changeInPos = "<span style='color: red'>▼ </span>" + str(-changeInPos)
    else:
        changeInPos = "▬"

    pos = i + 1
    if pos == 1:
        pos = "<td style='color: rgb(255, 215, 0); font-size: 30px';>" + str(pos)
    elif pos == 2:
        pos = "<td style='color: rgb(192, 192, 192); font-size: 27px';'>" + str(pos)
    elif pos == 3:
        pos = "<td style='color: rgb(140, 120, 83); font-size: 24px';'>" + str(pos)
    else:
        pos = "<td>" + str(pos)
    tableTeams.insert(i + 2, "<tr style='height:50px;'>"
                      + pos # Position
                      + "</td><td style='text-align:left;'>" + changeInPos # change in pos
                      + "</td><td>" + teamName # team name
                      + "</td><td>" + str(currTeamPoints[i][0]) # team curr points
                      + "</td><td>" + str(currTeamPlayed[teamName]) # played in
                      + "</td><td>" + teamBestResult[teamName] # best
                      + "</td><td>" + currTeamResult[teamName] # latest
                      + "</td></tr>")

# print(table)
# border: 1px solid;
lines = ["<html>",
            '''
            <style>
                table {
                    border-spacing:0;
                }
                th {
                    text-align:center;
                    background-color: rgb(170, 170, 170);
                    font-family: Monospace;
                    font-size: 20px;
                }
                td {
                    text-align:center;
                    background-color: rgb(245, 245, 245);
                    font-family: Monospace;
                    font-size: 15px;
                }
            </style>
            '''
            "<body>", 
            "<h1 style='font-family: Monospace;'>2025 AUCPL Standings</h1>", 
            "</body>",
            "</html>"]

for index, value in enumerate(tablePoints, start=4):
    lines.insert(index, value)

lines.insert(4, "<br>")

for index, value in enumerate(tableTeams, start=4):
    lines.insert(index, value)

for i in lines:
    f.write(i + "\n")

f.close() 