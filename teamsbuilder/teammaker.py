import http.client
import csv
from urllib.parse import urlparse
import random
import heapq
import copy
import time
import urllib.request
import json



class Player:
    def __init__(self, name, stats):
        self.name = name
        self.stats = stats
    
    def get_name(self):
        return self.name
    
    def get_all_stats(self):
        return self.stats

    def set_stat(self, stat, value):
        self.stats[stat] = value

    def get_stat(self, stat):
        return self.stats[stat]
    

class Team:
    def __init__(self, name):
        self.name = name
        self.players = {}
        self.avg_stats = {}
        self.total_stats = {}
        self.avg_all_stats = 0

    def get_name(self):
        return self.name
    
    def get_all_avg_stats(self):
        return self.avg_stats
    
    def get_avg_of_all_stats(self):
        return self.avg_all_stats
    
    def get_all_total_stats(self):
        return self.total_stats

    def get_avg_stat(self, stat):
        return self.avg_stats[stat]

    def get_total_stat(self, stat):
        return self.total_stats[stat]
    
    def get_players(self):
        return self.players
    
    def get_player(self, name):
        if name in self.players:
            return self.players[name]
        else:
            return -1
    
    def add_player(self, player_name, player_stats):
        self.players[player_name] = player_stats

        for s in player_stats:
            if(isinstance(player_stats[s], float)):
                if s not in self.avg_stats:
                    self.avg_stats[s] = player_stats[s]
                    self.total_stats[s] = player_stats[s]
                else:
                    self.total_stats[s] += player_stats[s]
                    self.avg_stats[s] = round(self.total_stats[s] / len(self.players), 3)
        all_stats = 0
        for s in self.avg_stats:
            all_stats += self.avg_stats[s]
        self.avg_all_stats = all_stats / len(self.avg_stats)


    def get_size(self):
        return len(self.players)
    

def convert(value):
        if value == '':
            return None
        try:
            return float(value)
        except ValueError:
            return value  


def lambda_handler(event, context):
    sheet_url = event.get("sheet_url")
    
    if not sheet_url:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Missing 'sheet_url' in input"})
        }
    

    # Get the present players 
    present_players = {}
    print("Loading Player Data")
    parsed_url = urlparse(sheet_url)
    conn = http.client.HTTPSConnection(parsed_url.hostname)
    path = parsed_url.path + "?" + parsed_url.query
    try:
        conn.request("GET", path)
        res = conn.getresponse()
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": f"Failed to retrieve sheet: {str(e)}"})
        }

    if res.status in (301, 302, 303, 307, 308):
        redirect_url = res.getheader('Location')
        if not redirect_url:
            return {
                "statusCode": 502,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": "Redirected but no Location header found."})
            }
        with urllib.request.urlopen(redirect_url) as redirected_response:
            data = redirected_response.read().decode('utf-8').splitlines()

    else:
        data = res.read().decode('utf-8').splitlines()

    # Parse CSV
    reader = csv.DictReader(data)

    captains = []
    for row in reader:
        key = row['Name']
        cleaned_row = {k: convert(v) for k, v in row.items()}
        if cleaned_row["Present"] == "Y":
            present_players[key] = cleaned_row
            if(present_players[key]["Captain"] == "Y"):
                captains.append(key)

    # Create the teams 
    print("Successfully Loaded Player Data")

    num_players = len(present_players)
    num_teams = 2
    if(num_players < 15):
        num_teams = 2
    elif(num_players < 22):
        num_teams = 3
    elif(num_players < 29):
        num_teams = 4
    else:
        num_teams = 5
    
    event_teams = event.get("num_teams")
    
    if not event_teams:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Missing 'num_teams' in input"})
        }
    if event_teams != -1:
        if not isinstance(event_teams, int) or event_teams < 2 or event_teams > 5:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "'num_teams' must be between 2 and 5"})
            }
        num_teams = event_teams

    
    team_names = []
    teams = {}

    if(num_teams == 2):
        team_names = ["Pikachu", "Clefary"]
        for team_name in team_names:
            teams[team_name] = Team(team_name)

    elif(num_teams == 3):
        team_names = ["Piplup", "Turtwig", "Chimchar"]
        for team_name in team_names:
            teams[team_name] = Team(team_name)


    elif(num_teams == 4):
        team_names = ["Pikachu", "Piplup", "Turtwig", "Chimchar"]
        for team_name in team_names:
            teams[team_name] = Team(team_name)

    else:
        team_names = ["Pikachu", "Piplup", "Turtwig", "Chimchar", "Clefary"]
        for team_name in team_names:
            teams[team_name] = Team(team_name)


    random.shuffle(team_names)

    team_filler = []
    for tn in team_names:
        heapq.heappush(team_filler, (0, tn))


    random.shuffle(captains)

    for c in captains:
        if(c in present_players):
            prio, curr_team = heapq.heappop(team_filler)
            teams[curr_team].add_player(c, present_players[c])
            bewith = present_players[c]["BeWith"]
            if (bewith != None and bewith in present_players):
                teams[curr_team].add_player(bewith, present_players[bewith])
                present_players.pop(bewith)
            heapq.heappush(team_filler, (teams[curr_team].get_size(), curr_team))
            present_players.pop(c)

    # Find pairs 
    pairs = {}
    asterisks = []
    for player in present_players:
        if present_players[player]["Asterisk"] != None:
            asterisks.append(player)
        if present_players[player]["BeWith"] != None:
            bewith = (present_players[player]["BeWith"])
            if bewith not in pairs:
                pairs[player] = bewith
        
    for p in asterisks:
        bewith = present_players[p]["BeWith"]
        prio, curr_team = heapq.heappop(team_filler)
        if(p in present_players):
            teams[curr_team].add_player(p, present_players[p])
            present_players.pop(p)
        if(bewith != None and bewith in present_players):
            teams[curr_team].add_player(bewith, present_players[bewith])
            present_players.pop(bewith)
        heapq.heappush(team_filler, (teams[curr_team].get_size(), curr_team))


    for pair in pairs:
        player = pair
        bewith = pairs[pair]
        prio, curr_team = heapq.heappop(team_filler)
        if (player in present_players):
            teams[curr_team].add_player(player, present_players[player])
            present_players.pop(player)
        if(bewith in present_players): 
            teams[curr_team].add_player(bewith, present_players[bewith])
            present_players.pop(bewith)
        heapq.heappush(team_filler, (teams[curr_team].get_size(), curr_team))


    keys = list(teams.keys())
    values = list(teams.values())
    random.shuffle(values)
    teams = dict(zip(keys, values))

    found_team = False

    def check_balance(teams, balance_val):
        for t1 in teams:
            for t2 in teams:
                t1_stats = teams[t1].get_all_avg_stats()
                t2_stats = teams[t2].get_all_avg_stats()
                
                for stat in t1_stats:
                    val1 = t1_stats.get(stat, 0)
                    val2 = t2_stats.get(stat, 0)
                    
                    if abs(val1 - val2) > balance_val:
                        return False
                
                if abs(teams[t1].get_avg_of_all_stats() - teams[t2].get_avg_of_all_stats()) > balance_val:
                        return False

        return True

    start_time = time.time()
    balance_val = .5
    if(len(present_players) < 1):
        found_team = True
    while(not found_team):
        teams_copy = copy.deepcopy(teams)
        team_filler_copy = copy.deepcopy(team_filler)
        
        shuffled_names = list(present_players.keys())
        random.shuffle(shuffled_names)
        
        while(len(shuffled_names) > 0):
            curr_name = shuffled_names.pop()
            prio, curr_team = heapq.heappop(team_filler_copy)
            teams_copy[curr_team].add_player(curr_name, present_players[curr_name])
            heapq.heappush(team_filler_copy, (teams_copy[curr_team].get_size(), curr_team))
        
        found_team = check_balance(teams_copy, balance_val)

        if(found_team):
            teams = teams_copy

        if(time.time() - start_time > 7):
            start_time = time.time()
            print()
            print("Timeout no teams found with balance value " + str(balance_val) +  ". Adjusting balance value")
            print()
            balance_val += .25




    output = {}
    output["balance_val"] = balance_val
    output["teams"] = {}

    for t in teams:
        output["teams"][str(t)] = {}
        output["teams"][str(t)]["team_stats"] = teams[t].get_all_avg_stats()
        output["teams"][str(t)]["team_stat_average"] = round(teams[t].get_avg_of_all_stats(), 3)
        team_players = []
        for p in teams[t].get_players():
            team_players.append(p)
        output["teams"][str(t)]["players"] = team_players
    
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(output)
    }
    # print(output['balance_val'])
    # for team in output["teams"]:
    #     print(team, output["teams"][team])


# Sample Usage:
sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTet6UPHdfdsaKkFN_VB5ggHacxEDxakmZH6syhroLB7oJ3aHr5clmSbEipnQTTfLy6nfdYe6M6ZAHs/pub?output=csv"
event = {}
event["sheet_url"] = sheet_url
event["num_teams"] = -1
output = json.loads(lambda_handler(event, None)["body"])

print(output['balance_val'])
for team in output["teams"]:
    print(team, output["teams"][team])