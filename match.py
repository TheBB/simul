import random

def binomial(n, k):
    if k == 0:
        return 1
    else:
        return n/k * binomial(n-1, k-1)

class Match:

    def __init__(self, num, player_a, player_b):
        self.type = 'match'
        self.num = num
        self.player_a = player_a
        self.player_b = player_b
        self.players = [player_a, player_b]
        self.fixed_result = False
        self.result = (0, 0)
        self.dependences = []
        self.link_winner = None
        self.link_winner_slot = 0
        self.link_loser = None
        self.link_loser_slot = 0

        self.compute()

    def can_fix(self):
        for m in self.dependences:
            if not m.fixed_result:
                return False
        return True

    def set_player_a(self, player):
        if player != self.player_a:
            self.player_a = player
            self.players[0] = player
            self.unfix_result()

    def set_player_b(self, player):
        if player != self.player_b:
            self.player_b = player
            self.players[1] = player
            self.unfix_result()

    def set_player(self, player, slot):
        if slot == 0:
            self.set_player_a(player)
        else:
            self.set_player_b(player)

    def compute(self):
        self.outcomes = []

        if self.player_a == None or self.player_b == None:
            return

        pa = self.player_a.prob_of_winning(self.player_b)
        pb = 1 - pa
        num = self.num

        self.outcomes = []
        self.prob_a = 0
        self.prob_b = 0

        start_a = self.result[0]
        start_b = self.result[1]

        self.modified_result = (start_a != 0) or (start_b != 0)
        self.fixed_result = (start_a == num) or (start_b == num)

        for i in range(0, num-start_b):
            prob = binomial(num-start_a+i-1,i) * pow(pa,num-start_a) * pow(pb,i)
            self.outcomes.append((num, start_b+i, prob))
            self.prob_a += prob

        for i in range(0, num-start_a):
            prob = binomial(num-start_b+i-1,i) * pow(pb,num-start_b) * pow(pa,i)
            self.outcomes.append((start_a+i, num, prob))
            self.prob_b += prob

        self.probs = [self.prob_a, self.prob_b]

        if self.prob_a > self.prob_b:
            self.winner = self.player_a
            self.loser = self.player_b
            self.prob = self.prob_a
        else:
            self.winner = self.player_b
            self.loser = self.player_a
            self.prob = self.prob_b

    def fix_result(self, i, j):
        if i < 0 or j < 0 or i > self.num or j > self.num or\
           (i == self.num and j == self.num):
            return False

        for dep in self.dependences:
            if not dep.fixed_result:
                return False

        self.result = (i, j)
        self.compute()
        self.broadcast()

        return True

    def unfix_result(self):
        self.result = (0, 0)
        self.compute()
        self.broadcast()

    def broadcast(self):
        if not self.fixed_result:
            if self.link_winner != None:
                self.link_winner.unfix_result()
            if self.link_loser != None:
                self.link_loser.unfix_result()

    def get_random_result(self):
        if self.player_a == None or self.player_b == None:
            return None

        if not self.fixed_result:
            val = random.random()
            for outcome in self.outcomes:
                if val >= outcome[2]:
                    val -= outcome[2]
                else:
                    self.random_result = (outcome[0], outcome[1])
                    return self.random_result
            return self.get_random_result()
        else:
            return self.result

    def output(self, strings, title=None):
        if title == None:
            title = self.player_a.name + ' vs. ' + self.player_b.name

        out = strings['header'].format(title=title)

        out += strings['outcomelist'].format(player=self.player_a.name\
                                           , prob=100*self.prob_a)
        for outcome in self.outcomes:
            if outcome[0] > outcome[1]:
                out += strings['outcomei'].format(winscore=outcome[0]\
                                                , losescore=outcome[1]\
                                                , prob=100*outcome[2])

        out += strings['outcomelist'].format(player=self.player_b.name\
                                           , prob=100*self.prob_b)
        for outcome in self.outcomes:
            if outcome[1] > outcome[0]:
                out += strings['outcomei'].format(winscore=outcome[1]\
                                                , losescore=outcome[0]\
                                                , prob=100*outcome[2])

        out += strings['mlwinner'].format(player=self.winner.name\
                                        , prob=100*self.prob)

        outs = sorted(self.outcomes, key=lambda p: p[2], reverse=True)

        out += strings['mloutcome'].format(pa=self.player_a.name\
                                         , pb=self.player_b.name\
                                         , na=outs[0][0], nb=outs[0][1]\
                                         , prob=100*outs[0][2])

        out += strings['footer'].format(title=title)

        return out
