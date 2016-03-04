# This is a script to generate tournament & match data

import csv
import datetime
import sys

match_data = '../tennis_atp/atp_matches_2015.csv'
tourney_dict = {}
def main1():
  match_file = open(match_data,'r')
  match_reader = csv.reader(match_file)

  '''name CHAR(20),
    year SMALLINT,
    level SMALLINT,
    location CHAR(20),
    surface CHAR(10)'''
  count = 0
  for row in match_reader:
    count += 1
    if row[1] != '':
      tourn_name = row[1]
    else:
      tourn_name = 'NULL'
    if row[0] != '':
      year = row[0].split('-')[0]
    else:
      year = 'NULL'
    if row[4] != '':
      level = row[4]
    else:
      level = "NULL"
    if row[2] != '':
      surface = row[2]
    else:
      surface = 'NULL'
    if tourn_name not in tourney_dict:
      tourney_dict[tourn_name] = {'year': year, 'level': level, 'surface': surface}

  # for k,v in tourney_dict.iteritems():
  #   print 'INSERT INTO TOURNAMENTS (name, year, level, surface) VALUES (\'{}\',\'{}\',\'{}\',\'{}\');'.format(k, v['year'],v['level'], v['surface'])
  return tourney_dict

def main2():
  tourney =  main1()
  #creates true brackets
  now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
  creator_id = 3
  true_bracket = True
  completed = True
  locked = True
  score = 1000 #some maximum value
  for k,v in tourney.iteritems():
    print 'INSERT INTO BRACKETS (tournament_name, tournament_year, true_bracket, creator_id, made_date, last_save, completed, locked, score) VALUES (\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\');'.format(k, v['year'], true_bracket, creator_id, now, now, completed, locked, score)

#Run main

main2()
