import itertools

import match

class Group:

    def __init__(self, num, players):
        self._num = num
        self._players = players
        self.make_match_list()
        self.compute()

    def make_match_list(self):
        combs = itertools.combinations(self._players, 2)
        self._matches = [match.Match(self._num, a[0], a[1]) for a in combs]

    def get_match(self, player_a, player_b):
        fits = lambda m: (m.player_a == player_a and m.player_b == player_b) or\
                         (m.player_b == player_a and m.player_a == player_b) 
        gen = (match for match in self._matches if fits(match))
        return next(gen)

    def get_player(self, name):
        fits = lambda p: p.name.lower() == name.lower()
        gen = (player for player in self._players if fits(player))
        return next(gen)

    def compute(self):
        pass

    def output(self, strings):
        return "Yay"
