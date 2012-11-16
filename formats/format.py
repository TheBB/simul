class Tally:

    def __init__(self, rounds):
        self.finishes = [0] * rounds

    def __getitem__(self, key):
        return self.finishes[key]

    def __setitem__(self, key, value):
        self.finishes[key] = value

    def __iter__(self):
        return iter(self.finishes)

    def scale(self, scale):
        self.finishes = [f/scale for f in self.finishes]

class Format:

    def __init__(self, schema_in, schema_out):
        self._schema_in = schema_in
        self._schema_out = schema_out
        self._players = [None] * self.num_players()
        self._updated = False
        self._tally = None
        self._parents = []
        self._dependencies = []

        self.setup()

    def add_parent(self, parent):
        self._parents.append(parent)

    def add_dependency(self, dep):
        self._dependencies.append(dep)

    def schema_in(self):
        return self._schema_in

    def schema_out(self):
        return self._schema_out

    def num_players(self):
        return sum(self._schema_in)

    def is_ready(self):
        for p in self._players:
            if p == None:
                return False
        return True

    def is_fixed(self):
        return False

    def is_modified(self):
        return False

    def is_updated(self):
        return self._updated

    def notify(self):
        self._updated = False
        for p in self._parents:
            p.notify()

    def clear(self):
        return NotImplemented

    def get_tally(self):
        return self._tally

    def get_match(self, key):
        return None

    def get_player(self, key):
        fits = lambda p: p.name.lower() == key.lower()
        gen = (p for p in self._players if fits(p))
        try:
            return next(gen)
        except:
            return None

    def set_player(self, key, player):
        if self._players[key] != player:
            self._players[key] = player
            self.fill()

    def set_players(self, players):
        if len(players) == len(self._players):
            self._players = players
            self.fill()

    def should_use_mc(self):
        return True

    def setup(self):
        return NotImplemented

    def fill(self):
        return NotImplemented

    def instance(self):
        return NotImplemented

    def compute(self):
        if not self.is_ready():
            return

        self._tally = dict()
        for p in self._players:
            self._tally[p] = Tally(len(self._schema_out))

        if self.should_use_mc():
            self.compute_mc()
        else:
            self.compute_exact()

        self._updated = True

    def compute_mc(self, runs=1000):
        return NotImplemented

    def compute_exact(self):
        return NotImplemented

    def detail(self, strings):
        return NotImplemented

    def out(self, strings, title=None):
        return NotImplemented
