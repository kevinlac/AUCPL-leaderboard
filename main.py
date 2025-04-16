from parse_leaderboard import get_parsed_data

def table_position(pos):
    if pos == 1:
        return "<td style='color: rgb(255, 215, 0); font-size: 30px; font-weight: 700;'>" + str(pos) + "</td>"
    elif pos == 2:
        return "<td style='color: rgb(192, 192, 192); font-size: 27px; font-weight: 600;'>" + str(pos) + "</td>"
    elif pos == 3:
        return "<td style='color: rgb(205,127,50); font-size: 24px; font-weight: 500;'>" + str(pos) + "</td>"
    return "<td>" + str(pos) + "</td>"

team_results = {} # team name: [[pts1, penalty1], [pts2, penalty2], ...]

# get leaderboard data
curr_leaderboard_results = get_parsed_data()

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

f = open("leaderboard.html", "w", encoding="utf-8")

for line in lines:
    f.write(line)

f.close()
