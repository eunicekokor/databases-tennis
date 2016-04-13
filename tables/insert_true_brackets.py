"""
Script for adding true brackets into our database, given existing matches for the tournament
"""

from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response
from math import log, ceil
import random

DATABASEURI = "postgresql://eek2138:7145@w4111a.eastus.cloudapp.azure.com/proj1part2"
engine = create_engine(DATABASEURI)
app = Flask(__name__, template_folder='')

# Information about current tournament
tname = 'Wimbledon'
tyear = 2014

# Setup connection to database
@app.before_request
def setup():
    try:
        g.conn = engine.connect()
    except:
        print "problem connecting to database"
        import traceback; traceback.print_exc()
        g.conn = None

# Tear down connection to database
@app.teardown_request
def after(exception):
    try:
        g.conn.close()
    except Exception as e:
        pass

# Node class for binary tree
class Node:
    def __init__(self, val):
        self.l = None
        self.r = None
        self.v = val

# Insertion method
def insert(node, val):
    if (node == None):
        return False
    # If there's room for a child
    if (node.l == None and node.v[0] == val[0]):
        node.l = Node(val)
        return True
    elif (node.r == None and node.v[1] == val[0]):
        node.r = Node(val)
        return True
    # Try insertion on left, then on right
    if (insert(node.l,val)):
        return True
    return insert(node.r,val)

# Tree conversion method
def convert_tree(node,rounds):
    tree_levels = []
    for i in range(rounds+1):
        tree_levels.append([])
    tree_levels[0].append(node.v[0])
    tree_levels = add_to_level(node,1,tree_levels,rounds)
    return tree_levels

# Randomizing method
def randomize(node):
    r = int(random.random() * 2)
    if (r == 1):
        temp = node.r
        node.r = node.l
        node.l = temp
        temp2 = node.v[0]
        node.v[0] = node.v[1]
        node.v[1] = temp2
    if (node.l != None):
        randomize(node.l)
    if (node.r != None):
        randomize(node.r)

# Tree conversion helper method
def add_to_level(node,l,tree_levels,max_depth):
    if (node == None):
        tree_levels[l].append(None)
        tree_levels[l].append(None)
    else:
        tree_levels[l].append(node.v[0])
        tree_levels[l].append(node.v[1])
        if (l < max_depth):
            tree_levels = add_to_level(node.l,l+1,tree_levels,max_depth)
            tree_levels = add_to_level(node.r,l+1,tree_levels,max_depth)
    return tree_levels

# Main method
def main():
    with app.test_request_context():
        #setup()
        g.conn = engine.connect()
        
        # Request a batch of matches from database
        matches = g.conn.execute("SELECT m.winner, m.loser FROM matches m WHERE tournament_name = 'Wimbledon' AND tournament_year = 2014 ORDER BY m.round DESC, m.round_number DESC").fetchall()
        
        # Calculate number of rounds
        rounds = rounds = int(ceil(log(len(matches),2)))

        # Begin constructing matches tree
        head = Node(matches[-1])
        for i in range(len(matches)-2,-1,-1):
            insert(head, matches[i])
        
        # Randomize bracket
        randomize(head)
        
        # Convert into tree of players, not matches
        converted_tree = convert_tree(head,rounds)
        
        # Display converted tree
        """for i in range(len(converted_tree)):
            print converted_tree[i]"""

        # Insert bracket into brackets table
        #g.conn.execute("INSERT INTO brackets (tournament_name,tournament_year,true_bracket,creator_id,made_date) VALUES (%s,%s,%s,%s,%s)",(tname,tyear,'true',1,'2016-04-08'))
        
        # Get bracket id of bracket just inserted
        b_id = g.conn.execute("SELECT b_id FROM brackets WHERE tournament_name = %s AND tournament_year = %s",tname,tyear).fetchone()[0]
        
        # Use converted tree to make insertions to database
        for i in range(len(converted_tree)):
            player_list = converted_tree[i]
            for j in range(len(player_list)):
                g.conn.execute("INSERT INTO placed_in (player_id,bracket,round,round_number) VALUES (%s,%s,%s,%s)",(player_list[j],b_id,i+1,j+1))

        #after()
        g.conn.close()

main()