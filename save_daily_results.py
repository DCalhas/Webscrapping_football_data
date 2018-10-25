from bs4 import BeautifulSoup
import urllib3
import csv
import datetime


def getSoup(url):
    http = urllib3.PoolManager()

    response = http.request('GET', url)
    soup = BeautifulSoup(response.data, 'html')

    return soup


def getTodaysResults(soup):

    competition = []
    home_teams = []
    away_teams = []
    scores = []


    for son in soup.findAll("td", {"class":"flag tipsy-active"}):
        competition += [son['title']]
        
    for son in soup.findAll("td", {"class":"team-a"}):
        home_teams += [son.p.text]

    for son in soup.findAll("td", {"class":"team-b"}):
        away_teams += [son.p.text]


    for son in soup.findAll("td", {"class":"score"}):
        s = []
        if(son.find("span", {"class":"fs_A"}).text.strip() == ''):
            s += [son.find("span", {"class":"fs_A"}).text.strip()]
            s += [son.find("span", {"class":"fs_B"}).text.strip()]
        else:
            s += [int(son.find("span", {"class":"fs_A"}).text.strip())]
            s += [int(son.find("span", {"class":"fs_B"}).text.strip())]
        scores += [s]

    results = []
    for i in range(len(competition)):
        results += [[competition[i], home_teams[i], away_teams[i], scores[i][0], scores[i][1]]]

    return results


def saveToFile(results):

    with open('daily-results/' + datetime.datetime.today().strftime('%d-%m-%Y') + '.csv', mode='w') as games_file:
        games_writer = csv.writer(games_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        
        games_writer.writerow(["competition", "home", "away", "hgoals", "agoals"])
        for game in results:
            print(game)
            games_writer.writerow(game)

if __name__ == "__main__":

    soup = getSoup('https://www.academiadasapostas.com/stats/livescores/popup')
    games = getTodaysResults(soup)
    saveToFile(games)

