#!/usr/bin/python3

import argparse
import pickle
import sys

import playerlist
import output
import tlpd

import match
import sebracket
import roundrobin
import mslgroup

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
        choices=['term','tl','tls','reddit'],\
        help='output format')
parser.add_argument('-t', '--type', dest='type', default='match',\
        choices=['match','sebracket','rrgroup','mslgroup'],\
        help='tournament type')
parser.add_argument('--title', dest='title', default=None,\
        help='title')
parser.add_argument('--tie', dest='tie', nargs='*',
        choices=['mscore', 'sscore', 'swins', 'imscore', 'isscore', 'iswins',\
                 'ireplay'],\
        default=['mscore', 'sscore', 'imscore', 'isscore', 'ireplay'],\
        help='order of tiebreaks in a round robin group')
parser.add_argument('-n', '--num', dest='num', nargs='+', default=[2], type=int,\
        help='number of sets required to win a match')
parser.add_argument('-r', '--rounds', dest='rounds', default=3, type=int,\
        help='number of rounds in a bracket')
parser.add_argument('-p', '--players', dest='players', default=4, type=int,\
        help='number of players in a group')
parser.add_argument('--threshold', dest='threshold', default=1, type=int,\
        help='placement threshold in a group')
parser.add_argument('-s', '--save', dest='save',\
        help='save data to file')
parser.add_argument('-l', '--load', dest='load',\
        help='load data from file')
parser.add_argument('--tlpd', dest='tlpd', default='none',\
        help='search in TLPD database')
parser.add_argument('--tlpd-tabulator', dest='tabulator', default=-1, type=int,\
        help='tabulator ID for the TLPD database')

args = vars(parser.parse_args())
strings = output.get_strings(args)

obj = None
if args['load'] != None:
    obj = get_from_file(args['load'])

tlpd_search = None
if args['tlpd'] != 'none':
    tlpd_search = tlpd.Tlpd(args['tlpd'], args['tabulator'])

if args['type'] == 'match':
    if obj == None:
        player_a = playerlist.get_player(1, tlpd_search)
        player_b = playerlist.get_player(2, tlpd_search)
        obj = match.Match(args['num'][0], player_a, player_b)

    print(obj.output(strings, title=args['title']))

elif args['type'] == 'sebracket':
    if obj == None:
        players = playerlist.PlayerList(pow(2,args['rounds']), tlpd_search)
        bracket = sebracket.SEBracket(args['num'], args['rounds'],\
                players.players)

    print(obj.output(strings, title=args['title']))

elif args['type'] == 'mslgroup':
    if obj == None:
        players = playerlist.PlayerList(4, tlpd_search)
        obj = mslgroup.Group(args['num'][0], players.players)
        obj.compute()

    print(obj.output(strings, title=args['title']))

elif args['type'] == 'rrgroup':
    if obj == None:
        players = playerlist.PlayerList(args['players'], tlpd_search)
        obj = roundrobin.Group(args['num'][0], args['tie'], players.players,\
                          args['threshold'])
        obj.compute()

    print(obj.output(strings), title=args['title'])

    while True:
        s = input('> ').lower().split(' ')
        s = filter(lambda p: p != '', s)
        s = list(map(lambda p: p.strip(), s))
        if len(s) < 1:
            continue

        if s[0] == 'exit':
            break
        elif s[0] == 'set':
            pa = obj.get_player(s[1])
            pb = obj.get_player(s[2])
            match = obj.get_match(obj._matches, pa, pb)
            ia = int(input('Score for ' + match.player_a.name + ': '))
            ib = int(input('Score for ' + match.player_b.name + ': '))
            match.fix_random_result(ia, ib)
        elif s[0] == 'unset':
            pa = obj.get_player(s[1])
            pb = obj.get_player(s[2])
            match = obj.get_match(obj._matches, pa, pb)
            match.fixed_random_result = False
        elif s[0] == 'list':
            print('Fixed:', end='')
            found = False
            for match in obj._matches:
                if match.fixed_random_result:
                    if found:
                        print(',', end='')
                    found = True
                    print(' ' + match.player_a.name + ' ' + str(match.random_result[0])\
                          + '-' + str(match.random_result[1]) + ' ' + match.player_b.name, end='')
            if found:
                print('')
            else:
                print(' none')
        elif s[0] == 'compute':
            obj.compute()
        elif s[0] == 'out':
            print(obj.output(strings, title=args['title']))

if args['save'] != None:
    put_to_file(obj, args['save'])
