from API_serv import *
from Local_serv import *
from Team import *

print("Welcome to the Fantasy Hockey Manager's Helper \n")

#get all teams from API

teams = get_active_teams()

# print(Team.all)

# select a team by name
# my_team = Team.select_team("New Jersey Devils")
print("\n")
print("\n")

# print(my_team.name)
print("\n")
print("\n")


###commented player information to reduce run-time while working on Teams
# #get all players from API

players = get_active_players()

#select a player by name
# my_player = Player.select_player("Joonas Donskoi")

# print(my_player.name)
# print("\n")
# print("\n")
# print(my_player.data_from_player)
# print("\n")
# print("\n")
# print(my_player.season_stats)

# #print of Class variables example

# print(Player.all)
# print("\n")
# print("\n")

# #print pf class variables example
# print(Player.player_count)
# print("\n")
# print("\n")




# #continue
# print("Please search for a player by name")