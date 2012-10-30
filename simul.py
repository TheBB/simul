#!/usr/bin/python3

import argparse
import pickle
import sys

import playerlist
import output
import tlpd

import match
import sebracket
import debracket
import roundrobin
import mslgroup

def get_from_file(file):
    try:
        with open(file, 'rb') as f:
            ret = pickle.load(f)
        return ret
    except Exception as e:
        print(' > simul.get_from_file: ' + str(e))
        return None

def put_to_file(obj, file):
    try:
        with open(file, 'wb') as f:
            pickle.dump(obj, f)
    except Exception as e:
        print(' > simul.put_to_file: ' + str(e))

parser = argparse.ArgumentParser(description='Emulate a SC2 tournament'\
        + ' format.')
parser.add_argument('-f', '--format', dest='format', default='term',\
        choices=['term','tl','tls','reddit'],\
        help='output format')
parser.add_argument('-t', '--type', dest='type', default='match',\
        choices=['match','sebracket','rrgroup','mslgroup','debracket'],\
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
parser.add_argument('--no-console', dest='noconsole', default=False, type=bool,\
        help='skip the console')

args = vars(parser.parse_args())
strings = output.get_strings(args)

tlpd_search = None
if args['tlpd'] != 'none':
    tlpd_search = tlpd.Tlpd(args['tlpd'], args['tabulator'])

obj = None
if args['load'] != None:
    obj = get_from_file(args['load'])
elif args['type'] == 'match':
    player_a = playerlist.get_player(1, tlpd_search)
    player_b = playerlist.get_player(2, tlpd_search)
    obj = match.Match(args['num'][0], player_a, player_b)
    obj.compute()
elif args['type'] == 'sebracket':
    players = playerlist.PlayerList(pow(2,args['rounds']), tlpd_search)
    obj = sebracket.SEBracket(args['num'], args['rounds'], players.players)
    obj.compute()
elif args['type'] == 'debracket':
    players = playerlist.PlayerList(pow(2,args['rounds']), tlpd_search)
    obj = debracket.DEBracket(args['num'][0], args['rounds'], players.players)
    obj.compute()
elif args['type'] == 'mslgroup':
    players = playerlist.PlayerList(4, tlpd_search)
    obj = mslgroup.Group(args['num'][0], players.players)
    obj.compute()
elif args['type'] == 'rrgroup':
    players = playerlist.PlayerList(args['players'], tlpd_search)
    obj = roundrobin.Group(args['num'][0], args['tie'], players.players,\
                           args['threshold'])
    obj.compute()

print(obj.output(strings, title=args['title']))

if not args['noconsole'] and obj.type in ['RRGROUP', 'MATCH', 'MSLGROUP']:
    while True:
        s = input('> ').lower().split(' ')
        s = filter(lambda p: p != '', s)
        s = list(map(lambda p: p.strip(), s))
        if len(s) < 1:
            continue

        if s[0] == 'exit':
            break

        elif s[0] == 'set':
            match = None
            if obj.type in ['RRGROUP']:
                if len(s) > 2:
                    match = obj.find_match(pa=s[1], pb=s[2])
            elif obj.type in ['MSLGROUP']:
                if len(s) > 1:
                    match = obj.find_match(search=s[1])
            elif obj.type == 'MATCH':
                match = obj
            else:
                print('Invalid command in current mode')
                continue

            if match != None:
                ia = int(input('Score for ' + match.player_a.name + ': '))
                ib = int(input('Score for ' + match.player_b.name + ': '))
                res = match.fix_result(ia, ib)
                if not res:
                    print('Invalid result')
                elif obj.type in ['MSLGROUP']:
                    obj.compute()
            else:
                print('No such match found')

        elif s[0] == 'unset':
            match = None
            if obj.type in ['RRGROUP']:
                if lens(s) > 2:
                    match = obj.find_match(pa=s[1], pb=s[2])
            elif obj.type in ['MSLGROUP']:
                if len(s) > 1:
                    match = obj.find_match(search=s[1])
            elif obj.type == 'MATCH':
                match = obj
            else:
                print('Invalid command in current mode')
                continue

            if match != None:
                match.unfix_result()
                if obj.type in ['MSLGROUP']:
                    obj.compute()
            else:
                print('No such match found')

        elif s[0] == 'list':
            if obj.type not in ['RRGROUP', 'MATCH', 'MSLGROUP']:
                print('Invalid command in current mode')
                continue

            if obj.type == 'RRGROUP':
                print('Modified matches:', end='')
                found = False
                for match in obj.get_match_list():
                    if match.modified_result:
                        if found:
                            print(',', end='')
                        found = True
                        print(' ' + match.player_a.name + ' ' +\
                              str(match.result[0]) + '-' +\
                              str(match.result[1]) + ' ' +\
                              match.player_b.name, end='')
                if found:
                    print('')
                else:
                    print(' none')

            elif obj.type == 'MSLGROUP':
                print('Modified matches:', end='')
                found = False
                for match in [obj.first, obj.second, obj.winners, obj.losers, obj.final]:
                    if match == None:
                        continue
                    if match.modified_result:
                        if found:
                            print(',', end='')
                        found = True
                        print(' ' + match.player_a.name + ' ' +\
                             str(match.result[0]) + '-' +\
                             str(match.result[1]) + ' ' +\
                             match.player_b.name, end='')
                if found:
                    print('')
                else:
                    print(' none')

            elif obj.type == 'MATCH':
                if obj.fixed_result or obj.modified_result:
                    if obj.fixed_result:
                        print('Result fixed: ', end='')
                    elif obj.modified_result:
                        print('Result modified: ', end='')
                    print(obj.player_a.name + ' ' + str(obj.result[0]) + '-' +\
                          str(obj.result[1]) + ' ' + obj.player_b.name)

        elif s[0] == 'compute':
            obj.compute()

        elif s[0] == 'out':
            if len(s) > 1:
                strs = output.get_strings({'type': obj.type.lower(),\
                                           'format': s[1]})
                print(obj.output(strs, title=args['title']))
            else:
                print(obj.output(strings, title=args['title']))

        elif s[0] == 'save':
            if len(s) > 1:
                put_to_file(obj, s[1])
            elif args['save'] != None:
                put_to_file(obj, args['save'])
            else:
                print('No filename given')

        elif s[0] == 'load':
            temp = None
            if len(s) > 1:
                temp = get_from_file(s[1])
            elif args['load'] != None:
                temp = get_from_file(args['load'])
            else:
                print('No filename given')
            
            if temp != None:
                obj = temp

if args['save'] != None:
    put_to_file(obj, args['save'])
