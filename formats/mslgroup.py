from formats.composite import Composite
from formats.match import Match

class MSLGroup(Composite):
    
    def __init__(self, num):
        self._num = num
        Composite.__init__(self, [1]*4, [1]*4)

    def setup(self):
        self._first = [Match(self._num), Match(self._num)]
        self._second = [Match(self._num), Match(self._num)]
        self._final = Match(self._num)

        self._matches = self._first + self._second + [self._final]

        self._first[0].add_winner_link(self._second[0], 0)
        self._first[0].add_loser_link(self._second[1], 0)
        self._first[0].add_parent(self)
        self._first[1].add_winner_link(self._second[0], 1)
        self._first[1].add_loser_link(self._second[1], 1)
        self._first[1].add_parent(self)
        self._second[0].add_loser_link(self._final, 0)
        self._second[0].add_parent(self)
        self._second[1].add_winner_link(self._final, 1)
        self._second[1].add_parent(self)
        self._final.add_parent(self)

    def get_match(self, key):
        if key.lower() == 'first':
            return self._first[0]
        elif key.lower() == 'second':
            return self._first[1]
        elif key.lower() == 'winners':
            return self._second[0]
        elif key.lower() == 'losers':
            return self._second[1]
        elif key.lower() == 'final':
            return self._final
        else:
            return None

    def should_use_mc(self):
        return False

    def fill(self):
        self._first[0].set_players(self._players[:2])
        self._first[1].set_players(self._players[2:])

    def compute_exact(self):
        pass

    def detail(self, strings):
        raise NotImplementedError()

    def summary(self, strings, title=None):
        return 'yay'
