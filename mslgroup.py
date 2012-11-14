import itertools

import match

class Group:

    def __init__(self, num, players):
        self.type = 'mslgroup'
        self._num = num
        self._players = players

        self.first = match.Match(num, players[0], players[1])
        self.second = match.Match(num, players[2], players[3])
        self.winners = None
        self.losers = None
        self.final = None

        self.words = ['first', 'second', 'winners', 'losers', 'final']

    def find_match(self, pa=None, pb=None, search=''):
        if search == 'first':
            return self.first
        elif search == 'second':
            return self.second
        elif search == 'winners':
            return self.winners
        elif search == 'losers':
            return self.losers
        elif search == 'final':
            return self.final
        raise Exception('Match must be one of (first, second, winners, losers, final)')

    def get_players(self):
        return self._players

    def get_player(self, name):
        fits = lambda p: p.name.lower() == name.lower()
        gen = (player for player in self._players if fits(player))
        try:
            return next(gen)
        except:
            return None

    def get_match_list(self):
        return list(filter(None, [self.first, self.second, self.winners,\
                                  self.losers, self.final]))

    def update(self):
        if not (self.first.fixed_result and self.second.fixed_result):
            self.winners = None
            self.losers = None
            self.final = None
        else:
            if self.winners == None or self.losers == None or\
                    (self.winners.player_a != self.first.winner) or\
                    (self.winners.player_b != self.second.winner) or\
                    (self.losers.player_a != self.first.loser) or\
                    (self.losers.player_b != self.second.loser):
                self.winners = match.Match(self._num, self.first.winner,\
                                           self.second.winner)
                self.losers = match.Match(self._num, self.first.loser,\
                                          self.second.loser)

            if not (self.winners.fixed_result and self.losers.fixed_result):
                self.final = None
            else:
                if self.final == None or\
                        (self.final.player_a != self.winners.loser) or\
                        (self.final.player_b != self.losers.winner):
                    self.final = match.Match(self._num, self.winners.loser,\
                                             self.losers.winner)

    def compute(self):
        self.update()

        for p in self._players:
            p.places = [0, 0, 0, 0]

        self.pairs = dict()
        for pair in itertools.permutations(self._players, 2):
            if pair[0] != pair[1]:
                self.pairs[pair] = 0

        for m in self.get_match_list():
            m.compute()

        if self.first.fixed_result and self.second.fixed_result:
            self.compute_wl(base=1, wm=self.winners, lm=self.losers)
            return

        for iw1 in range(0,2):
            for iw2 in range(0,2):
                w1 = self.first.players[iw1]
                l1 = self.first.players[1-iw1]
                w2 = self.second.players[iw2]
                l2 = self.second.players[1-iw2]

                base = self.first.probs[iw1] * self.second.probs[iw2]

                wmatch = match.Match(self._num, w1, w2)
                lmatch = match.Match(self._num, l1, l2)

                self.compute_wl(base=base, wm=wmatch, lm=lmatch)

    def compute_wl(self, base=1, wm=None, lm=None):
        if wm == None or lm == None:
            return

        if wm.fixed_result and lm.fixed_result:
            wm.winner.places[0] += base
            lm.loser.places[3] += base
            self.compute_fin(base=base, fm=self.final, first=wm.winner)
            return

        for iw in range(0,2):
            for il in range(0,2):
                wmw = wm.players[iw]
                wml = wm.players[1-iw]
                lmw = lm.players[il]
                lml = lm.players[1-il]

                base_p = base * wm.probs[iw] * lm.probs[il]

                wmw.places[0] += base_p
                lml.places[3] += base_p

                fmatch = match.Match(self._num, wml, lmw)

                self.compute_fin(base=base_p, fm=fmatch, first=wmw)

    def compute_fin(self, base=1, fm=None, first=None):
        if fm == None:
            return

        fm.player_a.places[1] += base * fm.prob_a
        fm.player_b.places[2] += base * fm.prob_a
        fm.player_b.places[1] += base * fm.prob_b
        fm.player_a.places[2] += base * fm.prob_b

        self.pairs[(first,fm.player_a)] += base * fm.prob_a
        self.pairs[(first,fm.player_b)] += base * fm.prob_b

    def detail(self, strings):
        out = strings['detailheader']

        out += strings['ptabletitle'].format(title='Detailed placement probabilities')
        out += strings['ptableheader']
        out += strings['ptableheading'].format(heading='4th')
        out += strings['ptableheading'].format(heading='3rd')
        out += strings['ptableheading'].format(heading='2nd')
        out += strings['ptableheading'].format(heading='1st')

        for p in self._players:
            out += '\n'
            out += strings['ptablename'].format(player=p.name)
            for i in p.places[-1::-1]:
                out += strings['ptableentry'].format(prob=100*i)

        out += strings['ptablebetween']

        out += strings['ptabletitle'].format(title='Probability of each pair advancing')
        out += strings['ptableheader']
        for p in self._players:
            out += strings['ptableheading'].format(heading=p.name[:6])
        for p in self._players:
            out += '\n'
            out += strings['ptablename'].format(player=p.name)
            for q in self._players:
                if p != q:
                    out += strings['ptableentry'].format(prob=100*self.pairs[(p,q)])
                else:
                    out += strings['ptableempty']

        out += strings['detailfooter']

        return out

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
