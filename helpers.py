import requests
from bs4 import BeautifulSoup
from datetime import datetime


def get_stats(choice):

    try:
        
        if choice == 'pts':
            url = 'https://www.championat.com/basketball/_nba/tournament/6174/statistic/player/point/'
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            players = soup.find_all('tr', class_ = 'table-responsive__row')
            player_name = []
            player_stat = []
            for player in players:
                temp = player.find('span', class_ = 'table-item__name')
                if temp:
                    player_name.append(temp.text)
            pts = soup.find_all("tr", class_ = 'table-responsive__row')
            for pt in pts:
                temp = pt.find("td", class_ = 'table-responsive__row-item _data basketball _order_2')
                if temp:
                    player_stat.append(temp.text.strip())
            ans = ''
            for i in range(10):
                ans += f' №{i + 1} {player_name[i]} : {player_stat[i]}\n'
            return ans
        
        elif choice == 'reb':
            url = 'https://www.championat.com/basketball/_nba/tournament/6174/statistic/player/rebound/'
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            players = soup.find_all('tr', class_ = 'table-responsive__row')
            player_name = []
            player_stat = []
            for player in players:
                temp = player.find('span', class_ = 'table-item__name')
                if temp:
                    player_name.append(temp.text)
            
            points = soup.find_all("tr", class_ = 'table-responsive__row')
            for point in points:
                temp = point.find("td", class_ = 'table-responsive__row-item _data basketball _order_2')
                if temp:
                    player_stat.append(temp.text.strip())
            ans = ''
            for i in range(10):
                ans += f' №{i + 1} {player_name[i]} : {player_stat[i]}\n'
            return ans
        

        elif choice == 'ast':
            url = 'https://www.championat.com/basketball/_nba/tournament/6174/statistic/player/assistent/'
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            players = soup.find_all('tr', class_ = 'table-responsive__row')
            player_name = []
            player_stat = []
            for player in players:
                temp = player.find('span', class_ = 'table-item__name')
                if temp:
                    player_name.append(temp.text)
            
            assists = soup.find_all("tr", class_ = 'table-responsive__row')
            for assist in assists:
                temp = assist.find("td", class_ = 'table-responsive__row-item _data basketball _order_2')
                if temp:
                    player_stat.append(temp.text.strip())
            ans = ''
            for i in range(10):
                ans += f' №{i + 1} {player_name[i]} : {player_stat[i]}\n'
            return ans
    except Exception as e:
        print(f'error {e}')



def get_nba_schedule(choice:int):
    url = 'https://www.championat.com/basketball/_nba/tournament/6174/calendar/'

    

    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        target_classes = [
            'stat-results__row js-tournament-filter-row',
            'stat-results__row js-tournament-filter-row _odd'
        ]
        matches = soup.find_all('tr', class_=target_classes)
        res = {}

        for match in matches:
            temp = match.find('td', class_ = 'stat-results__link')
            if temp:
                a_element = match.find('a')
                title = a_element.get('title')
                team = title[:title.index(',')]

            temp = match.find('div', class_ = 'stat-results__title-date _hidden-dt')
            if temp:
                a_element = temp.find('div')
                t = a_element.text.strip()
                ttime = t.replace('                                    \xa0', ' ')

            today = datetime.now()
            dt = datetime(2024, 12, 1, 2, 0)
            match_time = datetime.strptime(ttime, "%d.%m.%Y %H:%M")
            if match_time.month == today.month and match_time.year == today.year:
                res[team] = ttime

        ans = ''
        if choice == 1:
            ans += "🎯 Матчи сегодня:\n"
            for teams, timing in res.items():
                match_time = datetime.strptime(timing, "%d.%m.%Y %H:%M")
                if match_time.day == today.day:
                    ans += f'🕐 {timing[-5:]}\n {teams}\n\n'
            return ans


        elif choice == 3:
            ans += "📅 Матчи на 3 дня вперед:\n"
            matches_next_3_days = {}
            for teams, timing in res.items():
                match_time = datetime.strptime(timing, "%d.%m.%Y %H:%M")
                days_diff = (match_time - today).days
                if 0 < days_diff <= 3:
                    matches_next_3_days.setdefault(match_time.date(), []).append((timing[-5:], teams))
            
            for date, matches in sorted(matches_next_3_days.items()):
                ans += f'🗓 {date.strftime("%d.%m.%Y")}:\n'
                for time, teams in matches:
                    ans += f'🕐 {time}\n {teams}\n\n'
                ans += "\n"
            return ans


        elif choice == 7:
            ans += "📅 Матчи на 7 дня вперед:\n"
            matches_next_7_days = {}
            for teams, timing in res.items():
                match_time = datetime.strptime(timing, "%d.%m.%Y %H:%M")
                days_diff = (match_time - today).days
                if 0 <= days_diff <= 6:
                    matches_next_7_days.setdefault(match_time.date(), []).append((timing[-5:], teams))
            
            for date, matches in sorted(matches_next_7_days.items()):
                ans += f'🗓 {date.strftime("%d.%m.%Y")}:\n'
                for time, teams in matches:
                    ans += f'🕐 {time}\n {teams}\n\n'
                ans += "\n"
            return ans
    

    except Exception as e:
        print(f'error {e}')
        return False
    return(res)


# print(get_nba_schedule(1))
print(get_stats('pts'))