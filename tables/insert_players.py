# This is a script to generate SQL commands to insert players
# Use it by piping output into Postgres client

import csv
import sys

# Length of batches to be inserted
batch = 100
# Expected length of each row
row_len = 6

countries_data = '../additional_data/countries_map_data.csv'
rankings_data = '../../tennis_atp/atp_rankings_current.csv'
player_data = '../../tennis_atp/atp_players.csv'

def country_map(country_filename):
	cmap = {}
	country_file = open(country_filename,'r')
	country_reader = csv.reader(country_file)
	for row in country_reader:
		cmap[row[0]] = row[1]
	return cmap

def rankings_map(rankings_filename):
	rmap = {}
	rankings_file = open(rankings_filename,'r')
	rankings_reader = csv.reader(rankings_file)
	for row in rankings_reader:
		rmap[row[2]] = row[1]
	return rmap

def main1():
	cmap = country_map(countries_data)
	rmap = rankings_map(rankings_data)
	player_file = open(player_data,'r')
	player_reader = csv.reader(player_file)
	for row in player_reader:
		if row[1] != '':
			first_name = row[1]
		else:
			first_name = 'NULL'
		if row[2] != '':
			last_name = row[2]
		else:
			last_name = 'NULL'
		if row[0] in rmap:
			rank = rmap[row[0]]
		else:
			rank = "NULL"
		if row[4] != '':
			bday = row[4]
			birth = bday[0:4] + '-' + bday[4:6] + '-' + bday[6:]
		else:
			birth = 'epoch'
		if (row[5] != ''):
			country = cmap[row[5]]
		else:
			country = 'NULL'
		print 'INSERT INTO PLAYERS (first_name, last_name, rank, birth, country) VALUES (\''+first_name+'\',\''+last_name+'\','+rank+',\''+birth+'\',\''+country+'\');'


def main2():
	cmap = country_map(countries_data)
	rmap = rankings_map(rankings_data)
	player_file = open(player_data,'r')
	player_reader = csv.reader(player_file)
	sys.stdout.write('INSERT INTO PLAYERS (first_name, last_name, rank, birth, country) VALUES') 
	first = True
	i = 0
	for row in player_reader:
		i = i + 1
		if not first:
			sys.stdout.write(',')
		else:
			first = False
		if row[1] != '':
			first_name = row[1]
		else:
			first_name = 'NULL'
		if row[2] != '':
			last_name = row[2]
		else:
			last_name = 'NULL'
		if row[0] in rmap:
			rank = rmap[row[0]]
		else:
			rank = "NULL"
		if row[4] != '':
			bday = row[4]
			birth = bday[0:4] + '-' + bday[4:6] + '-' + bday[6:]
		else:
			birth = 'epoch'
		if (row[5] != ''):
			country = cmap[row[5]]
		else:
			country = 'NULL'
		sys.stderr.write(i + ' ' + first_name+' '+last_name+'\n')
		sys.stdout.write(' (\''+first_name+'\',\''+last_name+'\','+rank+',\''+birth+'\',\''+country+'\')')
	sys.stdout.write(';\n')

def main3():
	# Tell PostGres how dates are being input
	print 'set datestyle = ymd;'
	# Get map for countries
	cmap = country_map(countries_data)
	# Get map for rankings
	rmap = rankings_map(rankings_data)
	# Read from players file
	player_file = open(player_data,'r')
	player_reader = csv.reader(player_file)
	# Insert in batches
	first = True
	i = 0
	for row in player_reader:
		if (i % batch == 0):
			sys.stdout.write('INSERT INTO PLAYERS (p_id,first_name, last_name, rank, birth, country) VALUES ')
			first = False 
		else:
			sys.stdout.write(',')
		i = i + 1
		# Grab player id
		p_id = row[0]
		# Grab first name (get rid of illegal characters)
		if row[1] != '':
			first_name = ''.join(c for c in row[1] if 0 < ord(c) < 127)
			first_name = first_name[:40]
		else:
			first_name = 'NULL'
		# Grab last name (get rid of illegal characters)
		if row[2] != '':
			last_name = ''.join(c for c in row[2] if 0 < ord(c) < 127)
			last_name = last_name[:40]
		else:
			last_name = 'NULL'
		# Grab ranking if it's in dictionary (current only)
		if row[0] in rmap:
			rank = rmap[row[0]]
		else:
			rank = 'NULL'
		# Grab birthday (for incomplete dates, set to epoch)
		if len(row[4]) == 8:
			bday = row[4]
			if (bday[4:6] == '00'):
				bday = bday[:5] + '1' + bday[6:7] + '1'
			birth = bday[0:4] + '-' + bday[4:6] + '-' + bday[6:]
		else:
			birth = 'epoch'
		# Grab country (deal with unknown countries)
		if (row[5] != ''):
			country = cmap[row[5]]
			if (country == ''):
				country = 'Unknown'
		else:
			country = 'Unknown'
		# Write tuple for query
		sys.stdout.write(' ('+p_id+',\''+first_name+'\',\''+last_name+'\','+rank+',\''+birth+'\',\''+country+'\')')
		if (i % batch == 0):
			sys.stdout.write(';\n')
			first = True
	sys.stdout.write(';\n')

#Run main
main3()
