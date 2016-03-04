# This is a script to generate SQL commands to insert matches
# Use it by piping output into Postgres client

import csv
import sys
from math import log, ceil, pow

# Length of batches to be inserted
batch = 100

matches_data = '../../tennis_atp/atp_matches_2015.csv'

def main():
	# Read from matches file
	matches_file = open(matches_data,'r')
	matches_reader = csv.reader(matches_file)
	# Insert in batches
	first = True
	i = 0
	# Skip first row
	matches_reader.next()
	# Iterate through all other rows
	for row in matches_reader:
		if (i % batch == 0):
			sys.stdout.write('INSERT INTO MATCHES (tournament_name, tournament_year, round, round_number,  winner_set1_games,  loser_set1_games,  winner_set2_games, loser_set2_games,  winner_set3_games, loser_set3_games, winner_set4_games, loser_set4_games, winner_set5_games, loser_set5_games, winner, loser) VALUES ')
			first = False 
		else:
			sys.stdout.write(',')
		i = i + 1
		# Grab tournament information
		tour_name = row[1]
		tour_year = row[0][:4]
		# Grab round information
		if 'Tour Finals' not in tour_name and 'Davis Cup' not in tour_name:
			size = pow(2,ceil(log(float(row[3]))/log(2)))
			num = float(row[6])
			tour_round = str(int(log(size) / log(2) + 1 - ceil(log(1 - num/size) / (-log(2)))))
			round_num = str(int(num - size*(1 -  0.5**(-1 + ceil(log(1 - num/size) / (-log(2)) ) ) ) ))
		elif 'Tour Finals' in tour_name:
			tour_round = '\'RR\''
			round_num = row[6]
		else:
			tour_round = '\'DC\''
			round_num = row[6]
		# Grab winner and loser
		winner = row[7]
		loser = row[17]
		# Grab score infomation
		win_games = [None] * 5
		lose_games = [None] * 5
		split_score = row[27].split('-')
		for j in range(1, len(split_score)):
			win_games[j-1] = str(split_score[j-1][-1])
			lose_games[j-1] = str(split_score[j][0])
		for j in range(len(split_score),6):
			win_games[j-1] = 'NULL'
			lose_games[j-1] = 'NULL'
		# Write tuple for query
		sys.stdout.write('(\''+tour_name+'\','+tour_year+','+tour_round+','+round_num)
		for j in range(5):
			sys.stdout.write(','+win_games[0]+','+lose_games[0])
		sys.stdout.write(','+winner+','+loser+')')
		if (i % batch == 0):
			sys.stdout.write(';\n')
			first = True
	sys.stdout.write(';\n')

#Run main
main()
