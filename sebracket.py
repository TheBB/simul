import match

class SEBracket:

    def __init__(self, num, rounds, players):
        self.type = 'SEBRACKET'
        self.players = players
        self.num = num
        self.rounds = rounds

    def compute(self):
        self.winners = []

        if len(self.players) == 2:
            vmatch = match.Match(self.num[0], self.players[0], self.players[1])
            self.winners.append((self.players[0], vmatch.prob_a))
            self.winners.append((self.players[1], vmatch.prob_b))
        else:
            half = int(len(self.players)/2)
            self.left = SEBracket(self.num[0:-1], self.rounds-1, \
                            self.players[:half])
            self.right = SEBracket(self.num[0:-1], self.rounds-1, \
                            self.players[half:])
            self.left.compute()
            self.right.compute()

            temp = dict()

            for res in self.left.winners:
                temp[res[0]] = 0
            for res in self.right.winners:
                temp[res[0]] = 0

            tot = 0
            for pa in self.left.winners:
                for pb in self.right.winners:
                    vmatch = match.Match(self.num[-1], pa[0], pb[0])
                    lhs = pa[1] * pb[1] * vmatch.prob_a
                    rhs = pa[1] * pb[1] * vmatch.prob_b
                    temp[pa[0]] += lhs
                    temp[pb[0]] += rhs
                    tot += lhs + rhs

            for res in self.left.winners:
                self.winners.append((res[0], temp[res[0]]/tot))
            for res in self.right.winners:
                self.winners.append((res[0], temp[res[0]]/tot))

    def trace_player(self, i):
        out = 0
        if self.rounds > 1:
            if i < (2 << self.rounds - 2):
                out = self.left.trace_player(i)
            else:
                out = self.right.trace_player(i % (2 << self.rounds - 2))

        out += self.winners[i][1]

        return out

    def output(self, strings, title=None):
        if title == None:
            title = str(pow(2,self.rounds)) + '-man single elimination bracket'
        out = strings['header'].format(title=title)

        sorted_winners = sorted(self.winners, key = lambda a: a[1],\
                                reverse=True)

        out += strings['mlwinnerlist']
        for res in sorted_winners[0:16]:
            out += strings['mlwinneri'].format(player=res[0].name,\
                                               prob=100*res[1])

        exrounds = []
        for i in range(0, 2 << self.rounds - 1):
            exrounds.append((self.winners[i][0].name, self.trace_player(i)))
        sorted_exrounds = sorted(exrounds, key = lambda a: a[1],\
                                reverse=True)

        out += strings['exroundslist']
        for res in sorted_exrounds:
            rounded = self.rounds - round(res[1])
            if rounded <= 0:
                expl = 'win'
            elif rounded == 1:
                expl = 'lose in the finals'
            elif rounded == 2:
                expl = 'lose in the semifinals'
            elif rounded == 3:
                expl = 'lose in the quarterfinals'
            elif rounded >= 4:
                expl = 'lose in the round of' + str(2 << rounded - 2)

            out += strings['exroundsi'].format(player=res[0], rounds=res[1],\
                                               expl=expl)

        out += strings['footer']

        return out
