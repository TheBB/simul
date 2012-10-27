import itertools

import match

class Group:

    def __init__(self, num, players):
        self.type = 'MSLGROUP'
        self._num = num
        self._players = players

    def compute(self):
        self.make_matches()

        for p in self._players:
            p.places = [0, 0, 0, 0]

        for winner_1 in range(0,2):
            for winner_2 in range(0,2):
                w1 = self._players[winner_1]
                l1 = self._players[1-winner_1]
                w2 = self._players[2+winner_2]
                l2 = self._players[3-winner_2]

                base = self._matches[(w1,l1)].prob_a *\
                       self._matches[(w2,l2)].prob_a

                wmatch = self._matches[(w1,w2)]
                lmatch = self._matches[(l1,l2)]

                w1.places[0] += base * wmatch.prob_a
                w2.places[0] += base * wmatch.prob_b

                l1.places[3] += base * lmatch.prob_b
                l2.places[3] += base * lmatch.prob_a

                self.subcase(base * wmatch.prob_b * lmatch.prob_a, w1, l1)
                self.subcase(base * wmatch.prob_a * lmatch.prob_a, w2, l1)
                self.subcase(base * wmatch.prob_b * lmatch.prob_b, w1, l2)
                self.subcase(base * wmatch.prob_a * lmatch.prob_b, w2, l2)

    def subcase(self, base, w, l):
        pw = base * self._matches[(w,l)].prob_a
        pl = base * self._matches[(w,l)].prob_b
        w.places[1] += pw
        w.places[2] += pl
        l.places[1] += pl
        l.places[2] += pw

    def make_matches(self):
        self._matches = dict()
        for (pa,pb) in itertools.combinations(self._players, 2):
            match1 = match.Match(self._num, pa, pb)
            match1.compute()
            self._matches[(pa,pb)] = match1

            match2 = match.Match(self._num, pb, pa)
            match2.compute()
            self._matches[(pb,pa)] = match2

    def output(self, strings, title=None):
        if title == None:
            title = 'MSL-style four-player group'
        out = strings['header'].format(title=title)

        players = sorted(self._players, key=lambda a: sum(a.places[0:2]),\
                         reverse=True)

        for p in players:
            out += strings['mslgplayer'].format(player=p.name,\
                                                prob=100*sum(p.places[0:2]))

        out += strings['footer'].format(title=title)

        return out
