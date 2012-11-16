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
        self._first[1].add_winner_link(self._second[0], 1)
        self._first[1].add_loser_link(self._second[1], 1)
        self._second[0].add_loser_link(self._)
