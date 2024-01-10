from nba_api.stats.static import players

# Find players by full name.
#print(players.find_players_by_full_name('james'))

# Find players by first name.
holder = players.find_players_by_first_name('lebron')
holder.append(players.find_players_by_last_name('durant'))

print(holder[0]['id'])
print(holder)

# Find players by last name.