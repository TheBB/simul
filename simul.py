#!/usr/bin/python3

import argparse
import pickle

import playerlist
import match
import sebracket
import output
import tlpd

parser = argparse.ArgumentParser(description='Emulate a SC2 tournament'\
        + ' format.')
parser.add_argument('-f', '--format', dest='format', default='term',\
        choices=['term','tl','tls'],\
        help='output format')
parser.add_argument('-t', dest='type', default='match',\
        choices=['match','sebracket'],\
        help='tournament type')
parser.add_argument('-n', dest='num', nargs='+', default=[2], type=int,\
        help='number of sets required to win a match')
parser.add_argument('-r', dest='rounds', default=3, type=int,\
        help='number of rounds in a bracket')
parser.add_argument('-s', dest='save',\
        help='save data to file')
parser.add_argument('-l', dest='load',\
        help='load data from file')
parser.add_argument('--tlpd', dest='tlpd', default='none',\
        help='search in TLPD database')

args = vars(parser.parse_args())
print(args)
strings = output.get_strings(args)

tlpd_search = None
if args['tlpd'] != 'none':
    tlpd_search = tlpd.Tlpd(args['tlpd'])

if args['type'] == 'match':
    if args['load'] == None:
        player_a = playerlist.get_player(1, tlpd_search)
        player_b = playerlist.get_player(2, tlpd_search)
        match = match.Match(args['num'][0], player_a, player_b)
    else:
        read_file = open(args['load'], mode='rb')
        match = pickle.load(read_file)
        read_file.close()

    print(match.output(strings))

    if args['save'] != None:
        write_file = open(args['save'], mode='wb')
        pickle.dump(match, write_file)
        write_file.close()

elif args['type'] == 'sebracket':
    if args['load'] == None:
        players = playerlist.PlayerList(pow(2,args['rounds']), tlpd_search)
        bracket = sebracket.SEBracket(args['num'], args['rounds'],\
                                      players.players)
    else:
        read_file = open(args['load'], mode='rb')
        bracket = pickle.load(read_file)
        read_file.close()

    print(bracket.output(strings))

    if args['save'] != None:
        write_file = open(args['save'], mode='wb')
        pickle.dump(bracket, write_file)
        write_file.close()
