from bs4 import BeautifulSoup
import requests
from csv import writer
import sqlite3

teams = {
    'Arsenal': '1',
    'Aston-Villa': '2',
    'Bournemouth': '127',
    'Brentford': '130',
    'Brighton-and-Hove-Albion': '131',
    'Chelsea': '4',
    'Crystal-Palace': '6',
    'Everton': '7',
    'Fulham': '34',
    'Leeds-United': '9',
    'Leicester-City': '26',
    'Liverpool': '10',
    'Manchester-City': '11',
    'Manchester-United': '12',
    'Newcastle-United': '23',
    'Nottingham-Forest': '15',
    'Southampton': '20',
    'Tottenham-Hotspur': '21',
    'West-Ham-United': '25',
    'Wolverhampton-Wanderers': '38'
} 

conn = sqlite3.connect('premiereLeague.db')
c = conn.cursor()

""" c.execute('''CREATE TABLE players(
    team TEXT,
    name TEXT,
    number INT,
    position TEXT,
    nationality TEXT
)''') """

def squadScraper (team_url, team):

    page = requests.get(team_url)

    soup = BeautifulSoup(page.content, 'html.parser')

    players = soup.find_all('a', class_ = 'playerOverviewCard')

    for player in players:
        player_team = team
        name = player.find('h4', class_ = 'name').text.replace('\n', '')
        number = player.find('span', class_ = 'number').text.replace('\n', '')
        position = player.find('span', class_ = 'position').text.replace('\n', '')
        nationality = player.find('span', class_ = 'playerCountry').text.replace('\n', '')
        
        c.execute('''INSERT INTO players VALUES(?, ?, ?, ?, ?)''', (player_team, name, number, position, nationality))
        conn.commit()

for k, v in teams.items():
    my_url = 'https://www.premierleague.com/clubs/'+ v + '/' + k + '/squad'
    squadScraper(my_url, k)


""" c.execute('''SELECT * FROM players''')
results = c.fetchall()
print(results)

conn.close() """

#url = 'https://www.premierleague.com/clubs/1/Arsenal/squad'


