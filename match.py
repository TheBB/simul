import random

def binomial(n, k):
    if k == 0:
        return 1
    else:
        return n/k * binomial(n-1, k-1)

class Match:

    def __init__(self, num, player_a, player_b):
        self.num = num
        self.player_a = player_a
        self.player_b = player_b
        self.compute()

    def compute(self):
        pa = self.player_a.prob_of_winning(self.player_b)
        pb = 1 - pa
        num = self.num

        self.outcomes = []
        self.prob_a = 0
        self.prob_b = 0

        for i in range(0, num):
            proba = binomial(num+i-1, i) * pow(pa, num) * pow(pb, i)
            probb = binomial(num+i-1, i) * pow(pb, num) * pow(pa, i)
            self.outcomes.append((num, i, proba))
            self.outcomes.append((i, num, probb))
            self.prob_a += proba
            self.prob_b += probb

        if self.prob_a > self.prob_b:
            self.winner = self.player_a
            self.prob = self.prob_a
        else:
            self.winner = self.player_b
            self.prob = self.prob_b

    def get_random_result(self):
        val = random.random()
        for outcome in self.outcomes:
            if val >= outcome[2]:
                val -= outcome[2]
            else:
                self.random_result = (outcome[0], outcome[1])
                return self.random_result
        return self.get_random_result()

    def output(self, strings):
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
        mloutcome = self.outcomes[0]
        for outcome in self.outcomes[1:-1]:
            if outcome[2] > mloutcome[2]:
                mloutcome = outcome

        out += strings['mloutcome'].format(pa=self.player_a.name\
                                         , pb=self.player_b.name\
                                         , na=mloutcome[0], nb=mloutcome[1]\
                                         , prob=100*mloutcome[2])

        out += strings['footer'].format(title=title)

        return out
