# This is a script to generate SQL commands to insert players
# Use it by piping output into Postgres client

import csv
import sys

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
	print 'set datestyle = ymd;'
	cmap = country_map(countries_data)
	rmap = rankings_map(rankings_data)
	player_file = open(player_data,'r')
	player_reader = csv.reader(player_file)
	first = True
	i = 0
	for row in player_reader:
		if (i % 100 == 0):
			sys.stdout.write('INSERT INTO PLAYERS (first_name, last_name, rank, birth, country) VALUES ') 
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
			rank = 'NULL'
		if len(row[4]) == 8:
			bday = row[4]
			if (bday[4:6] == '00'):
				bday = bday[:5] + '1' + bday[6:7] + '1'
			birth = bday[0:4] + '-' + bday[4:6] + '-' + bday[6:]
		else:
			birth = 'epoch'
		if (row[5] != ''):
			country = cmap[row[5]]
			if (country == ''):
				country = 'NULL'
		else:
			country = 'NULL'
		sys.stdout.write(' (\''+first_name+'\',\''+last_name+'\','+rank+',\''+birth+'\',\''+country+'\')')
		if (i % 100 == 0):
			sys.stdout.write(';\n')
			first = True
	sys.stdout.write(';\n')

#Run main
main3()
