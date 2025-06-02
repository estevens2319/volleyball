import csv
import random
import heapq
import copy
import time


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

    def get_name(self):
        return self.name
    
    def get_all_avg_stats(self):
        return self.avg_stats
    
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


    def get_size(self):
        return len(self.players)

def convert(value):
    if value == '':
        return None
    try:
        return float(value)
    except ValueError:
        return value  

# Get the present players 

present_players = {}
with open('names.csv', mode='r', newline='') as file:
    reader = csv.DictReader(file)
    for row in reader:
        key = row['Name']
        cleaned_row = {k: convert(v) for k, v in row.items()}
        if(cleaned_row["Present"] == "Y"):
            present_players[key] = cleaned_row


# Create the teams 

num_players = len(present_players)
team_names = []
teams = {}

if(num_players < 15):
    team_names = ["Pikachu", "Clefary"]
    for team_name in team_names:
        teams[team_name] = Team(team_name)


elif(num_players < 22):
    team_names = ["Piplup", "Turtwig", "Chimchar"]
    for team_name in team_names:
        teams[team_name] = Team(team_name)


elif(num_players < 29):
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



# Separate the best players:

if "Adam" in present_players and "Benjamin" in present_players and "Aaron" in present_players and "Geon" in present_players:
    
    prio, adam_team = heapq.heappop(team_filler)
    teams[adam_team].add_player("Adam", present_players["Adam"])
    heapq.heappush(team_filler, (teams[adam_team].get_size(), adam_team))

    prio, benjamin_team = heapq.heappop(team_filler)
    teams[benjamin_team].add_player("Benjamin", present_players["Benjamin"])
    heapq.heappush(team_filler, (teams[benjamin_team].get_size(), benjamin_team))



    prio, aaron_team = heapq.heappop(team_filler)
    teams[aaron_team].add_player("Aaron", present_players["Aaron"])
    heapq.heappush(team_filler, (teams[aaron_team].get_size(), aaron_team))

    prio, geon_team = heapq.heappop(team_filler)
    teams[geon_team].add_player("Geon", present_players["Geon"])
    
    if("Jenna" in present_players):
        teams[geon_team].add_player("Jenna", present_players["Jenna"])
        present_players.pop("Jenna")

    heapq.heappush(team_filler, (teams[geon_team].get_size(), geon_team))



    present_players.pop("Adam")
    present_players.pop("Benjamin")
    present_players.pop("Aaron")
    present_players.pop("Geon")

elif "Adam" in present_players and "Benjamin" in present_players and "Aiden" in present_players and "Geon" in present_players:
    
    prio, adam_team = heapq.heappop(team_filler)
    teams[adam_team].add_player("Adam", present_players["Adam"])
    heapq.heappush(team_filler, (teams[adam_team].get_size(), adam_team))

    prio, benjamin_team = heapq.heappop(team_filler)
    teams[benjamin_team].add_player("Benjamin", present_players["Benjamin"])
    heapq.heappush(team_filler, (teams[benjamin_team].get_size(), benjamin_team))

    prio, aiden_team = heapq.heappop(team_filler)
    teams[aiden_team].add_player("Aiden", present_players["Aiden"])
    heapq.heappush(team_filler, (teams[aiden_team].get_size(), aiden_team))

    prio, geon_team = heapq.heappop(team_filler)
    teams[geon_team].add_player("Geon", present_players["Geon"])
    if("Jenna" in present_players):
        teams[geon_team].add_player("Jenna", present_players["Jenna"])
        present_players.pop("Jenna")
    heapq.heappush(team_filler, (teams[geon_team].get_size(), geon_team))

    
    present_players.pop("Adam")
    present_players.pop("Benjamin")
    present_players.pop("Aiden")
    present_players.pop("Geon")



elif "Adam" in present_players and "Benjamin" in present_players and "Aaron" in present_players: 
    
    prio, adam_team = heapq.heappop(team_filler)
    teams[adam_team].add_player("Adam", present_players["Adam"])
    heapq.heappush(team_filler, (teams[adam_team].get_size(), adam_team))

    prio, benjamin_team = heapq.heappop(team_filler)
    teams[benjamin_team].add_player("Benjamin", present_players["Benjamin"])
    heapq.heappush(team_filler, (teams[benjamin_team].get_size(), benjamin_team))

    prio, aaron_team = heapq.heappop(team_filler)
    teams[aaron_team].add_player("Aaron", present_players["Aaron"])
    heapq.heappush(team_filler, (teams[aaron_team].get_size(), aaron_team))

    
    present_players.pop("Adam")
    present_players.pop("Benjamin")
    present_players.pop("Aaron")

elif "Adam" in present_players and "Benjamin" in present_players: 
    
    prio, adam_team = heapq.heappop(team_filler)
    teams[adam_team].add_player("Adam", present_players["Adam"])
    heapq.heappush(team_filler, (teams[adam_team].get_size(), adam_team))

    prio, benjamin_team = heapq.heappop(team_filler)
    teams[benjamin_team].add_player("Benjamin", present_players["Benjamin"])
    heapq.heappush(team_filler, (teams[benjamin_team].get_size(), benjamin_team))

    
    present_players.pop("Adam")
    present_players.pop("Benjamin")

elif "Adam" in present_players and "Aaron" in present_players:
    
    prio, adam_team = heapq.heappop(team_filler)
    teams[adam_team].add_player("Adam", present_players["Adam"])
    heapq.heappush(team_filler, (teams[adam_team].get_size(), adam_team))

    prio, aaron_team = heapq.heappop(team_filler)
    teams[aaron_team].add_player("Aaron", present_players["Aaron"])
    heapq.heappush(team_filler, (teams[aaron_team].get_size(), aaron_team))

    
    present_players.pop("Adam")
    present_players.pop("Aaron")

elif "Aaron" in present_players and "Benjamin" in present_players: 

    prio, benjamin_team = heapq.heappop(team_filler)
    teams[benjamin_team].add_player("Benjamin", present_players["Benjamin"])
    heapq.heappush(team_filler, (teams[benjamin_team].get_size(), benjamin_team))

    prio, aaron_team = heapq.heappop(team_filler)
    teams[aaron_team].add_player("Aaron", present_players["Aaron"])
    heapq.heappush(team_filler, (teams[aaron_team].get_size(), aaron_team))
    
    present_players.pop("Benjamin")
    present_players.pop("Aaron")




# Find pairs and asterisks
pairs = {}
for player in present_players:
    if present_players[player]["BeWith"] != None:
        bewith = (present_players[player]["BeWith"])
        if bewith not in pairs:
            pairs[player] = bewith
    
for pair in pairs:
    player = pair
    bewith = pairs[pair]
    if(bewith in present_players):
        prio, curr_team = heapq.heappop(team_filler)
        teams[curr_team].add_player(player, present_players[player])
        teams[curr_team].add_player(bewith, present_players[bewith])
        present_players.pop(player)
        present_players.pop(bewith)
        heapq.heappush(team_filler, (teams[curr_team].get_size(), curr_team))



keys = list(teams.keys())
values = list(teams.values())
random.shuffle(values)
teams = dict(zip(keys, values))


# for t in teams:
#     print(t, teams[t].get_size(), teams[t].get_all_avg_stats())
#     for p in teams[t].get_players():
#         print(teams[t].get_player(p))


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

    return True

start_time = time.time()
balance_val = 1
while(not found_team):
    
    player_copy = present_players.copy()
    teams_copy = copy.deepcopy(teams)
    team_filler_copy = copy.deepcopy(team_filler)
    
    shuffled_names = list(player_copy.keys())
    random.shuffle(shuffled_names)
    
    while(len(shuffled_names) > 0):
        curr_name = shuffled_names.pop()
        prio, curr_team = heapq.heappop(team_filler_copy)
        teams_copy[curr_team].add_player(curr_name, player_copy[curr_name])
        heapq.heappush(team_filler_copy, (teams_copy[curr_team].get_size(), curr_team))
    
    found_team = check_balance(teams_copy, balance_val)

    if(found_team):
        teams = teams_copy

    if(time.time() - start_time > 10):
        print("Timeout no teams found, adjusting balance value")
        balance_val += .5


    
for t in teams:
    print(t, teams[t].get_size(), teams[t].get_all_avg_stats())
    team_players = ""
    for p in teams[t].get_players():
        team_players += p + ", "
    print(team_players)