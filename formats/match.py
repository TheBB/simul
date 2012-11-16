import formats.format as format

def binomial(n, k):
    if k == 0:
        return 1
    else:
        return n/k * binomial(n-1, k-1)

class Match(format.Format):

    def __init__(self, num):
        format.Format.__init__(self, [1,1], [1,1])
        self._num = num
        self._result = (0, 0)
        self._winner_links = []
        self._loser_links = []

        self.words = []
    
    def is_fixed(self):
        return self._result[0] == self._num or self._result[1] == self._num

    def is_modified(self):
        return self._result[0] != 0 or self._result[1] != 0

    def should_use_mc(self):
        return False

    def setup(self):
        pass

    def modify(self, num_a, num_b):
        if not self.is_ready():
            return False

        if num_a < 0 or num_b < 0 or num_a > self._num or num_b > self._num or\
           (num_a == self._num and num_b == self._num):
            return False

        for dep in self._dependencies:
            if not dep.is_fixed():
                return False

        if self._result[0] != num_a or self._result[1] != num_b:
            self._result = (num_a, num_b)
            self.notify()

    def clear(self):
        self.modify(0, 0)

    def fill(self):
        self.notify()

    def instance(self):
        if not self.is_updated():
            return None

        res = self.instance_detail()
        if res[0] > res[1]:
            return [self._players[0], self._players[1]]
        else:
            return [self._players[1], self._players[0]]
    
    def instance_detail(self):
        if not self.is_updated():
            return None

        if self.is_fixed():
            return self._result

        val = random.random()
        for outcome in self._outcomes:
            if val >= outcome[2]:
                val -= outcome[2]
            else:
                res = (outcome[0], outcome[1])
                return res

    def compute_exact(self):
        start_a = self._result[0]
        start_b = self._result[1]

        if self.is_fixed():
            winner = self._players[0] if start_a > start_b else self._players[1]
            loser = self._players[1] if start_a > start_b else self._players[0]
            self._outcomes = [(start_a, start_b, 1, winner)]
            self._tally[winner][1] = 1
            self._tally[loser][0] = 1
            return

        pa = self._players[0].prob_of_winning(self.player_b)
        pb = 1 - pa
        num = self._num

        self._outcomes = []
        self._prob_a = 0
        self._prob_b = 0

        for i in range(0, num - start_b):
            base = binomial(num-start_a+i-1,i) * pa**(num-start_a) * pb**i
            self._outcomes.append((num, start_b+i, base, self._players[0]))
            self._tally[self._players[0]][1] += base
            self._tally[self._players[1]][0] += base

        for i in range(0, num - start_a):
            base = binomial(num-start_b+i-1,i) * pb**(num-start_b) * pa**i
            self._outcomes.append((start_a+i, num, base, self._players[1]))
            self._tally[self._players[1]][1] += base
            self._tally[self._players[0]][0] += base

    def detail(self, strings):
        return NotImplemented

    def out(self, strings, title=None):
        if title == None:
            title = self._players[0].name + ' vs. ' + self._players[1].name
