#!/usr/bin/python3

import argparse
import pickle

import playerlist
import output
import tlpd

import match
import sebracket
import roundrobin

def get_from_file(file):
    with open(file, 'rb') as f:
        ret = pickle.load(f)
    return ret

def put_to_file(obj, file):
    with open(file, 'wb') as f:
        pickle.dump(obj, f)

parser = argparse.ArgumentParser(description='Emulate a SC2 tournament'\
        + ' format.')
parser.add_argument('-f', '--format', dest='format', default='term',\
        choices=['term','tl','tls'],\
        help='output format')
parser.add_argument('-t', '--type', dest='type', default='match',\
        choices=['match','sebracket','rrgroup'],\
        help='tournament type')
parser.add_argument('--tie', dest='tie', nargs='*',
        choices=['mscore', 'sscore', 'swins', 'imscore', 'isscore', 'ireplay'],\
        default=['mscore', 'sscore', 'imscore', 'isscore',\
                 'ireplay'],\
        help='order of tiebreaks in a round robin group')
parser.add_argument('-n', '--num', dest='num', nargs='+', default=[2], type=int,\
        help='number of sets required to win a match')
parser.add_argument('-r', '--rounds', dest='rounds', default=3, type=int,\
        help='number of rounds in a bracket')
parser.add_argument('-p', '--players', dest='players', default=4, type=int,\
        help='number of players in a group')
parser.add_argument('-s', '--save', dest='save',\
        help='save data to file')
parser.add_argument('-l', '--load', dest='load',\
        help='load data from file')
parser.add_argument('--tlpd', dest='tlpd', default='none',\
        help='search in TLPD database')

args = vars(parser.parse_args())
strings = output.get_strings(args)

if args['load'] != None:
    obj = get_from_file(args['load'])
    print(obj.output(strings))
    sys.exit(0)

tlpd_search = None
if args['tlpd'] != 'none':
    tlpd_search = tlpd.Tlpd(args['tlpd'])

if args['type'] == 'match':
    player_a = playerlist.get_player(1, tlpd_search)
    player_b = playerlist.get_player(2, tlpd_search)
    obj = match.Match(args['num'][0], player_a, player_b)
elif args['type'] == 'sebracket':
    players = playerlist.PlayerList(pow(2,args['rounds']), tlpd_search)
    bracket = sebracket.SEBracket(args['num'], args['rounds'],\
            players.players)
elif args['type'] == 'rrgroup':
    players = playerlist.PlayerList(args['players'], tlpd_search)
    obj = roundrobin.Group(args['num'][0], players.players)

print(obj.output(strings))

if args['save'] != None:
    put_to_file(obj, args['save'])
