import itertools
from operator import attrgetter

import playerlist
import match

class Group:

    def __init__(self, num, tie, players):
        self._num = num
        self._players = players
        self._tie = tie
        self.make_match_list()

    def make_match_list(self):
        combs = itertools.combinations(self._players, 2)
        self._matches = [match.Match(self._num, a[0], a[1]) for a in combs]

    def get_match(self, matches, player_a, player_b):
        fits = lambda m: (m.player_a == player_a and m.player_b == player_b) or\
                         (m.player_b == player_a and m.player_a == player_b) 
        gen = (match for match in matches if fits(match))
        return next(gen)

    def get_player(self, name):
        fits = lambda p: p.name.lower() == name.lower()
        gen = (player for player in self._players if fits(player))
        return next(gen)

    def simulate(self):
        for player in self._players:
            player.mscore = 0
            player.sscore = 0
            player.swins = 0

        for match in self._matches:
            res = match.get_random_result()
            match.player_a.sscore += res[0] - res[1]
            match.player_a.swins += res[0]
            match.player_b.sscore += res[1] - res[0]
            match.player_b.swins += res[1]
            if res[0] > res[1]:
                match.player_a.mscore += 1
                match.player_b.mscore -= 1
            else:
                match.player_b.mscore += 1
                match.player_a.mscore -= 1

        table = self._players
        table = self.break_ties(table, self._tie)

        print('')
        for m in self._matches:
            res = m.random_result
            print(m.player_a.name + ' ' + str(res[0]) + '-' + str(res[1])\
                  + ' ' + m.player_b.name)
        print('')
        for p in table:
            print(p.name + ' ' + str(p.mscore) + ' ' + str(p.sscore) + ' ' + str(p.swins))

        return table

    def break_ties(self, table, tie):
        print(tie[0])
        if tie[0] == 'imscore' or tie[0] == 'isscore' or tie[0] == 'iswins':
            for p in table:
                p.imscore = 0
                p.isscore = 0
                p.iswins = 0

            combs = itertools.combinations(table, 2)
            for comb in combs:
                match = self.get_match(self._matches, comb[0], comb[1])
                res = match.random_result
                match.player_a.isscore += res[0] - res[1]
                match.player_a.iswins += res[0]
                match.player_b.isscore += res[1] - res[0]
                match.player_b.iswins += res[1]
                if res[0] > res[1]:
                    match.player_a.imscore += 1
                    match.player_b.imscore -= 1
                else:
                    match.player_b.imscore += 1
                    match.player_a.imscore -= 1

        if tie[0] == 'mscore' or tie[0] == 'sscore' or tie[0] == 'swins'\
        or tie[0] == 'imscore' or tie[0] == 'isscore' or tie[0] == 'iswins':
            key = attrgetter(tie[0])
            table = sorted(table, key=key, reverse=True)

            keyval = key(table[0])
            keyind = 0
            for i in range(1, len(table)):
                if key(table[i]) != keyval:
                    if i > keyind + 1:
                        table[keyind:i] = self.break_ties(table[keyind:i], tie)
                    keyval = key(table[i])
                    keyind = i

            if keyind < len(table) - 1 and keyind > 0:
                table[keyind:] = self.break_ties(table[keyind:], tie)
            elif keyind < len(table) - 1:
                table = self.break_ties(table, tie[1:])

        if tie[0] == 'ireplay':
            refplayers = []
            for p in table:
                newp = playerlist.Player(copy=p)
                newp.ref = p
                refplayers.append(newp)
            smallgroup = Group(self._num, self._tie, refplayers)
            smalltable = smallgroup.simulate()

            for i in range(0,len(table)):
                table[i] = smalltable[i].ref

        return table

    def output(self, strings):
        return "Yay"
