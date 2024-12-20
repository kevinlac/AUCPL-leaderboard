import csv

def readcsv(name):
    with open(name) as fp:
        reader = csv.reader(fp, delimiter=",", quotechar='"')
        data_read = [row for row in reader]
    return data_read

results = readcsv("results 1 comp.csv")
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
    """<tr class='second-table'>
        <th>Position</th>
        <th>Points Awarded</th>
    </tr>""",
    "</table>"
]


for i in range(1, len(scoring)):
    tablePoints.insert(1 + i, "<tr class='second-table table-data'><td>" + str(i) + "</td><td>" + scoring[i][1] + "</td></tr>")
    pointsByPos[scoring[i][0]] = int(scoring[i][1])

for i in range(1, len(results)): # score and previous week score for each team
    teamScore = [0 if results[i][1] == "-1" else pointsByPos[results[i][1]]]
    teamPlayed = 0 if results[i][1] == "-1" else 1
    bestResult = 9999 if results[i][1] == "-1" else int(results[i][1])
    latestResult = "Did Not Compete" if results[i][-1] == "-1" else results[i][-1]
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
    bestResult = "Did Not Compete" if bestResult == 9999 else str(bestResult)
    
    currTeamPlayed[teamName] = teamPlayed
    currTeamResult[teamName] = latestResult
    teamBestResult[teamName] = bestResult

prevTeamPoints.sort(reverse=True)
currTeamPoints.sort(reverse=True)

f = open("test.html", "w", encoding="utf-8")

tableTeams = [
    "<table style='width:70%; margin-left: auto; margin-right: auto;'>",
    """<tr class='main-table'>
        <th>Position</th>
        <th>   </th>
        <th>Team Name</th>
        <th style='background-color: rgb(65, 105, 225); color: white; font-weight: 600'>Score</th>
        <th>Contests Attended</th>
        <th>Best Result</th>
        <th>Latest Result</th>
    </tr>""",
    "</table>"
]

def numText(number):
    if number == "Did Not Compete": return number
    number = int(number)
    if (number % 10 == 1 and number % 100 != 11): number = str(number) + "<sup>st</sup>"
    elif (number % 10 == 2 and number % 100 != 12): number = str(number) + "<sup>nd</sup>"
    elif (number % 10 ==3 and number % 100 != 13): number = str(number) + "<sup>rd</sup>"
    else: number = str(number) + "<sup>th</sup>"
    return number

for i in range(0, len(currTeamPoints)):
    teamName = currTeamPoints[i][1]
    
    changeInPos = prevTeamPoints.index([item for item in prevTeamPoints if teamName in item][0]) - i if len(prevTeamPoints) > 0 else 0
    if changeInPos > 0:
        changeInPos = "<span style='color: limegreen'>▲ </span>" + str(changeInPos)
    elif changeInPos < 0:
        changeInPos = "<span style='color: red'>▼ </span>" + str(-changeInPos)
    else:
        changeInPos = "<span style='color: lightgray'>▬</span>"

    pos = i + 1
    if pos == 1:
        pos = "<td style='color: rgb(255, 215, 0); font-size: 30px; font-weight: 700;'>" + str(pos)
    elif pos == 2:
        pos = "<td style='color: rgb(192, 192, 192); font-size: 27px; font-weight: 600;'>" + str(pos)
    elif pos == 3:
        pos = "<td style='color: rgb(140, 120, 83); font-size: 24px; font-weight: 500;'>" + str(pos)
    else:
        pos = "<td>" + str(pos)
    tableTeams.insert(i + 2, "<tr class='main-table table-data'>"
                      + pos # Position
                      + "</td><td style='text-align:left;'>" + changeInPos # change in pos
                      + "</td><td>" + teamName # team name
                      + "</td><td style='font-weight: 700; background-color: rgb(240, 240, 240)'>" + str(currTeamPoints[i][0]) # team curr points
                      + "</td><td>" + str(currTeamPlayed[teamName]) # played in
                      + "</td><td>" + numText(teamBestResult[teamName]) # best
                      + "</td><td>" + numText(currTeamResult[teamName]) # latest
                      + "</td></tr>")


lines = ["<!DOCTYPE html><html>",
            '''
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
                    background-color: rgb(240, 240, 240);
                }
                tr {
                    background-color: rgb(247, 247, 247);
                }
                th {
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
                }
            </style>
            <head>
                <title>2025 AUCPL Standings</title>
            </head>
            '''
            "<body>", 
            "<h1 style='font-family: Inter; font-weight: 800'>2025 AUCPL Standings</h1>", 
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