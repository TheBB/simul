import itertools
from operator import attrgetter

import playerlist
import match

class ScoreTally:

    def __init__(self, num_players):
        self.finishes = [0] * num_players
        self.mscore = 0
        self.sscore = 0
        self.swins = 0
        self.replays = 0

    def scale_by(self, total):
        self.mscore /= total
        self.sscore /= total
        self.swins /= total
        self.replays /= total
        self.finishes = [f / total for f in self.finishes]

class Group:

    def __init__(self, num, tie, players, threshold=1, subgroups=None):
        self.type = 'rrgroup'
        self._num = num
        self._players = players
        self._tie = tie
        self._threshold = threshold
        self.make_match_list()

        if subgroups == None:
            self._subgroups = dict()
            for i in range(0,len(players)):
                players[i].flag = 1 << i
        else:
            self._subgroups = subgroups

        self.words = []
        for p in players:
            self.words.append(p.name)

    def get_players(self):
        return self._players

    def make_match_list(self):
        combs = itertools.combinations(self._players, 2)
        self._matches = [match.Match(self._num, a[0], a[1]) for a in combs]

    def find_match(self, pa=None, pb=None, search=''):
        match = None
        if pa != None and pb != None:
            pa = self.get_player(pa)
            pb = self.get_player(pb)
            match = self.get_match(self._matches, pa, pb)

        if match == None:
            raise Exception('No such match found: \'' + pa.name + ' vs. ' + pb.name)
        else:
            return match

    def get_match_list(self):
        return self._matches

    def get_match(self, matches, player_a, player_b):
        fits = lambda m: (m.player_a == player_a and m.player_b == player_b) or\
                         (m.player_b == player_a and m.player_a == player_b) 
        gen = (match for match in matches if fits(match))
        return next(gen)

    def get_player(self, name):
        fits = lambda p: p.name.lower() == name.lower()
        gen = (player for player in self._players if fits(player))
        try:
            return next(gen)
        except:
            return None

    def compute(self):
        matches = self._matches
        for match in matches:
            match.compute()

        outcome = [0] * len(matches)

        tally = dict()
        for p in self._players:
            tally[p] = ScoreTally(len(self._players))

        total = 0
        while outcome != False:
            base = 1
            for j in range(0,len(matches)):
                outc = matches[j].outcomes[outcome[j]]
                matches[j].iter_outcome = (outc[0], outc[1])
                base *= outc[2]

            table = self.collect_table(matches, self._players)

            if table != False:
                for i in range(0,len(table)):
                    t = tally[table[i]]
                    for (shift, prob) in table[i].spread:
                        t.finishes[i+shift] += prob * base
                    t.mscore += float(table[i].mscore) * base
                    t.sscore += float(table[i].sscore) * base
                    t.swins += float(table[i].swins) * base
                    if table[i].replayed:
                        t.replays += base
                total += base

            outcome = self.get_next_outcome(outcome, matches)

        for t in tally.values():
            t.scale_by(total)

        self.tally = tally

    def get_next_outcome(self, outcome, matches):
        j = len(outcome) - 1

        while j >= 0:
            outcome[j] += 1
            if outcome[j] == len(matches[j].outcomes):
                outcome[j] = 0
                j -= 1
            else:
                break

        if j == -1:
            return False
        else:
            return outcome

    def collect_table(self, matches, players):
        for player in players:
            player.mscore = 0
            player.sscore = 0
            player.swins = 0
            player.replayed = False
            player.spread = [(0,1)]

        for i in range(0,len(matches)):
            res = matches[i].iter_outcome
            matches[i].player_a.sscore += res[0] - res[1]
            matches[i].player_a.swins += res[0]
            matches[i].player_b.sscore += res[1] - res[0]
            matches[i].player_b.swins += res[1]
            if res[0] > res[1]:
                matches[i].player_a.mscore += 1
                matches[i].player_b.mscore -= 1
            else:
                matches[i].player_a.mscore -= 1
                matches[i].player_b.mscore += 1

        return self.break_ties(players, self._tie)

    def break_ties(self, table, tie):
        if tie[0] == 'imscore' or tie[0] == 'isscore' or tie[0] == 'iswins':
            for p in table:
                p.imscore = 0
                p.isscore = 0
                p.iswins = 0

            combs = itertools.combinations(table, 2)
            for comb in combs:
                match = self.get_match(self._matches, comb[0], comb[1])
                res = match.iter_outcome
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
                        temp = self.break_ties(table[keyind:i], tie)
                        if temp != False:
                            table[keyind:i] = temp
                        else:
                            return False
                    keyval = key(table[i])
                    keyind = i

            if keyind < len(table) - 1 and keyind > 0:
                temp = self.break_ties(table[keyind:], tie)
                if temp != False:
                    table[keyind:] = temp
                else:
                    return False
            elif keyind < len(table) - 1:
                table = self.break_ties(table, tie[1:])
                if table == False:
                    return False

        if tie[0] == 'ireplay':
            if len(table) == len(self._players):
                return False

            subgroup_id = 0
            newplayers = []
            s = ''
            for p in table:
                subgroup_id += p.flag
                s += p.name
                p.replayed = True
                newp = playerlist.Player(copy=p)
                newplayers.append(newp)

            if not subgroup_id in self._subgroups:
                subgroup = Group(self._num, self._tie, newplayers,\
                                 subgroups=self._subgroups)
                self._subgroups[subgroup_id] = subgroup
                subgroup.compute()
            else:
                subgroup = self._subgroups[subgroup_id]

            root = 0
            for p in table:
                p.spread = []
                ref = next(filter(lambda q: q.flag == p.flag, subgroup._players))
                finishes = subgroup.tally[ref].finishes
                for f in range(0,len(finishes)):
                    p.spread.append((root+f, finishes[f]))
                root -= 1

        return table

    def output(self, strings, title=None):
        if title == None:
            title = str(len(self._players)) + '-player round robin'
        out = strings['header'].format(title=title)

        nm = len(self._players) - 1
        players = sorted(self._players, key=lambda p:\
                         sum(self.tally[p].finishes[0:self._threshold])*100,\
                         reverse=True)

        for p in players:
            t = self.tally[p]
            out += strings['gplayer'].format(player=p.name)
            out += strings['gpexpscore'].format(mw=(nm+t.mscore)/2,\
                    ml=(nm-t.mscore)/2, sw=t.swins, sl=t.swins-t.sscore)

            if self._threshold == 1:
                out += strings['gpprobwin'].format(prob=t.finishes[0]*100)
            else:
                out += strings['gpprobthr'].format(prob=sum(\
                        t.finishes[0:self._threshold])*100,\
                        thr=self._threshold)

            place = str(t.finishes.index(max(t.finishes)) + 1)
            if place[-1] == '1' and (place[0] != '1' or len(place) == 1):
                place += 'st'
            elif place[-1] == '2' and (place[0] != '1' or len(place) == 1):
                place += 'nd'
            elif place[-1] == '3' and (place[0] != '1' or len(place) == 1):
                place += 'rd'
            else:
                place += 'th'
            out += strings['gpmlplace'].format(place=place,\
                    prob=max(t.finishes)*100)

        out += strings['footer'].format(title=title)

        return out
