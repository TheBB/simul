#!/usr/bin/python3

import argparse
import pickle
import sys
import os

try:
    import pyreadline as readline
except ImportError:
    import readline

import playerlist
import output
import tlpd
import glicko

from formats import match, mslgroup
#import sebracket
#import debracket
#import roundrobin
#import mslgroup
#import combination

class Completer:
    def __init__(self, basewords):
        self.basewords = words
        self.words = words
        self.prefix = None

    def add_words(self, words):
        self.words = self.basewords + words

    def complete(self, prefix, index):
        if prefix != self.prefix:
            self.matching_words = [w for w in self.words if w.startswith(prefix)]
            self.prefix = prefix
        try:
            return self.matching_words[index]
        except IndexError:
            return None

def swipe_history():
    readline.remove_history_item(readline.get_current_history_length()-1)

def better_input(query, swipe=False):
    ret = input(query)
    if (swipe or ret.strip() == '') and ret != '':
        swipe_history()
    return ret

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

def print_matches(list, pre='Modified matches', post='none'):
    print(pre + ':', end='')
    found = False
    for match in list:
        if match.is_modified():
            if found:
                print(',', end='')
            found = True
            print(' ' + match.get_player(0).name + ' ' +\
                  str(match._result[0]) + '-' +\
                  str(match._result[1]) + ' ' +\
                  match.get_player(1).name, end='')
    if found:
        print('')
    else:
        print(' ' + post)

def sanity_check(args):
    if args['load'] != None:
        if not os.path.isfile(args['load']):
            print('File does not exist: \'' + args['load'] + '\'')
            sys.exit(1)

    for n in args['num']:
        if n < 1:
            print('Number of sets to win must be at least 1')
            sys.exit(1)

    if args['type'] == 'rrgroup':
        if len(args['tie']) < 2:
            print('Must have at least two tiebreakers')
            sys.exit(1)
        if args['tie'][-1] != 'ireplay':
            print('Last tiebreaker must be ireplay')
            sys.exit(1)
        if args['tie'][0] == 'ireplay':
            print('First tiebreaker must not be ireplay')
            sys.exit(1)
        if args['players'] < 2:
            print('Must have at least two players')
            sys.exit(1)
        if args['threshold'] < 1:
            print('Threshold must be at least 1')
            sys.exit(1)

    if args['rounds'] < 2 and args['type'] == 'debracket':
        print('Must have at least two rounds')
        sys.exit(1)
    if args['rounds'] < 1 and args['type'] == 'sebracket':
        print('Must have at least one round')
        sys.exit(1)
    if len(args['num']) != args['rounds'] and args['type'] == 'sebracket':
        print('Must have a num argument for each round')
        sys.exit(1)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Emulate a SC2 tournament'\
            + ' format.')
    parser.add_argument('-f', '--format', dest='format', default='term',\
            choices=['term','tl','tls','reddit'],\
            help='output format')
    parser.add_argument('-t', '--type', dest='type', default='match',\
            choices=['match','sebracket','rrgroup','mslgroup','debracket',\
                    'combination'],\
            help='tournament type')
    parser.add_argument('--title', dest='title', default=None,\
            help='title')
    parser.add_argument('--tie', dest='tie', nargs='*',\
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
    parser.add_argument('--glicko', dest='glicko', action='store_true',\
            help='search in SC2Charts database')
    parser.add_argument('-nc', '--no-console', dest='noconsole', action='store_true',\
            help='skip the console')
    parser.add_argument('--exact', dest='exact', action='store_true',\
            help='force exact computation')
    parser.add_argument('--glicko-update', dest='glicko-update', action='store_true',\
            help='update local glicko database')

    args = vars(parser.parse_args())
    sanity_check(args)

    if args['glicko-update']:
        glicko.update()
        sys.exit(0)

    strings = output.get_strings(args)

    finder = None
    if args['tlpd'] != 'none':
        iface = tlpd.Tlpd(args['tlpd'], args['tabulator'])
        finder = iface.search
    elif args['glicko']:
        finder = glicko.search

    obj = None
    if args['load'] != None:
        obj = get_from_file(args['load'])
    elif args['type'] == 'match':
        players = playerlist.PlayerList(2, finder)
        obj = match.Match(args['num'][0])
        obj.set_players(players.players)
        obj.compute()
    #elif args['type'] == 'sebracket':
        #players = playerlist.PlayerList(pow(2,args['rounds']), finder)
        #obj = sebracket.SEBracket(args['num'], args['rounds'], players.players)
        #obj.compute()
    #elif args['type'] == 'debracket':
        #players = playerlist.PlayerList(pow(2,args['rounds']), finder)
        #obj = debracket.DEBracket(args['num'][0], args['rounds'], players.players)
        #if args['exact']:
            #obj.compute_exact()
        #else:
            #obj.compute()
    elif args['type'] == 'mslgroup':
        players = playerlist.PlayerList(4, finder)
        obj = mslgroup.MSLGroup(args['num'][0])
        obj.set_players(players.players)
        obj.compute()
    #elif args['type'] == 'rrgroup':
        #players = playerlist.PlayerList(args['players'], finder)
        #obj = roundrobin.Group(args['num'][0], args['tie'], players.players,\
                               #args['threshold'])
        #if args['exact']:
            #obj.compute_exact()
        #else:
            #obj.compute()
    #elif args['type'] == 'combination':
        #players = playerlist.PlayerList(32, finder)
        #obj = combination.Combination(players.players)
        #obj.compute()

    print(obj.summary(strings, title=args['title']))

    if not args['noconsole']:
        supported = {'all': ['save','load','compute','out','exit','change'],\
                     match.Match: ['set','unset','list'],\
                     mslgroup.MSLGroup: ['set','unset','list','detail']}
                     #'rrgroup': ['set','unset','list'],\
                     #'sebracket': ['set','unset','list'],\
                     #'debracket': ['set','unset','list','detail'],\
                     #'combination': ['']}

        #words = supported['all'] + obj.words + supported[obj.type] +\
                #['name','race','elo']
        words = supported['all'] + supported[type(obj)] + ['name','race','elo']
        completer = Completer(words)
        completer.add_words([p.name for p in obj.get_players()])
        readline.parse_and_bind("tab: complete")
        readline.set_completer(completer.complete)

        while True:
            s = better_input('> ').lower().split(' ')
            s = filter(lambda p: p != '', s)
            s = list(map(lambda p: p.strip(), s))
            if len(s) < 1:
                continue

            if s[0] not in supported['all'] and s[0] not in supported[type(obj)]:
                print('Invalid command for type \'' + str(type(obj)) + '\'')
                continue

            if s[0] == 'exit':
                break

            elif s[0] == 'compute':
                #if obj.type not in ['rrgroup', 'debracket']:
                    #obj.compute()
                #elif (len(s) > 1 and s[1] == 'ex') or args['exact']:
                    #obj.compute_exact()
                #else:
                    #obj.compute()

                obj.compute()

            elif s[0] == 'out' or s[0] == 'detail':
                if not obj.is_updated():
                    print('Changes have been made - run \'compute\' to update')
                    continue

                #if len(s) > 1:
                    #strs = output.get_strings({'type': obj.type.lower(), 'format': s[1]})
                #else:
                    #strs = strings
                if s[0] == 'out':
                    print(obj.summary(strings, title=args['title']))
                elif s[0] == 'detail':
                    print(obj.detail(strings))

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

            elif s[0] == 'set' or s[0] == 'unset':
                m = False
                try:
                    if type(obj) in [mslgroup.MSLGroup] and len(s) > 1:
                        m = obj.get_match(s[1])
                    elif type(obj) in [match.Match]:
                        m = obj

                    if m == False:
                        print('Not enough arguments')
                        continue
                    elif m == None or not m.can_modify():
                        print('Match not yet ready (unresolved dependencies?)')
                        continue

                    if s[0] == 'set':
                        ia = int(better_input('Score for ' + m.get_player(0).name\
                                              + ': ', swipe=True))
                        ib = int(better_input('Score for ' + m.get_player(1).name\
                                              + ': ', swipe=True))
                        res = m.modify(ia, ib)
                        if not res:
                            print('Unable to modify match')
                    elif s[0] == 'unset':
                        m.clear()

                except Exception as e:
                    print(str(e))

            elif s[0] == 'list':
                if type(obj) in [match.Match]:
                    matches = [obj]
                else:
                    matches = obj.get_matches()

                if type(matches) == list:
                    print_matches(matches)
                elif type(matches) == dict:
                    for key in matches.keys():
                        print_matches(matches[key], pre=key)

            elif s[0] == 'change':
                pass
                #if len(s) < 2:
                    #print('Not enough arguments')
                    #continue

                #player = obj.get_player(s[-1])
                #if player == None:
                    #print('No such player \'' + s[-1] + '\'')

                #recompute = False

                #if len(s) < 3 or s[1] == 'name':
                    #player.name = better_input('Name: ')
                    #completer.add_words([p.name for p in obj.get_players()])

                #if len(s) < 3 or s[1] == 'race':
                    #race = ''
                    #while race not in ['P', 'Z', 'T']:
                        #race = better_input('Race: ', swipe=True).upper()
                    #player.race = race
                    #recompute = True

                #if len(s) < 3 or s[1] == 'elo':
                    #elo = playerlist.get_elo()
                    #if elo == False:
                        #player.elo = 0
                        #player.elo_race['T'] = 0
                        #player.elo_race['Z'] = 0
                        #player.elo_race['P'] = 0
                    #else:
                        #player.elo = elo
                        #player.elo_race['T'] = playerlist.get_elo('vT')
                        #player.elo_race['Z'] = playerlist.get_elo('vZ')
                        #player.elo_race['P'] = playerlist.get_elo('vP')
                    #recompute = True

                #if recompute:
                    #obj.compute()

    if args['save'] != None:
        put_to_file(obj, args['save'])
