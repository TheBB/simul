import match

class SEBracket:

    def __init__(self, num, rounds, players):
        self.type = 'sebracket'
        self._players = players
        self._num = num
        self._rounds = rounds
        self.setup_matches()

        self.words = []
        for i in range(0,len(self.bracket)):
            for j in range(0,len(self.bracket[i])):
                self.words.append(str(i+1) + '-' + str(j+1))

    def get_players(self):
        return self._players

    def setup_matches(self):
        rounds = self._rounds

        bracket = []
        for i in range(0,rounds):
            rnd = []
            for j in range(0,2**(rounds-1-i)):
                rnd.append(match.Match(self._num[i], None, None))
            bracket.append(rnd)

        for j in range(0,len(bracket[0])):
            bracket[0][j].set_player(self._players[2*j], 0)
            bracket[0][j].set_player(self._players[2*j+1], 1)

        for i in range(0,len(bracket)-1):
            for j in range(0,len(bracket[i])):
                bracket[i][j].link_winner = bracket[i+1][j//2]
                bracket[i][j].link_winner_slot = j % 2
                bracket[i+1][j//2].dependences.append(bracket[i][j])

        self.bracket = bracket

    def compute(self):
        for p in self._players:
            p.exrounds = [0] * self._rounds

        self.winners = self.do_match(self.bracket[-1][0], self._rounds-1)

        #self.winners = []
#
        #if len(self.players) == 2:
            #vmatch = match.Match(self.num[0], self.players[0], self.players[1])
            #self.winners.append((self.players[0], vmatch.prob_a))
            #self.winners.append((self.players[1], vmatch.prob_b))
        #else:
            #half = int(len(self.players)/2)
            #self.left = SEBracket(self.num[0:-1], self.rounds-1, \
                            #self.players[:half])
            #self.right = SEBracket(self.num[0:-1], self.rounds-1, \
                            #self.players[half:])
            #self.left.compute()
            #self.right.compute()
#
            #temp = dict()

            #for res in self.left.winners:
                #temp[res[0]] = 0
            #for res in self.right.winners:
                #temp[res[0]] = 0
#
            #tot = 0
            #for pa in self.left.winners:
                #for pb in self.right.winners:
                    #vmatch = match.Match(self.num[-1], pa[0], pb[0])
                    #lhs = pa[1] * pb[1] * vmatch.prob_a
                    #rhs = pa[1] * pb[1] * vmatch.prob_b
                    #temp[pa[0]] += lhs
                    #temp[pb[0]] += rhs
                    #tot += lhs + rhs
#
            #for res in self.left.winners:
                #self.winners.append((res[0], temp[res[0]]/tot))
            #for res in self.right.winners:
                #self.winners.append((res[0], temp[res[0]]/tot))

    def do_match(self, match, round):
        if match.can_fix():
            if round != 0:
                match.set_player_a(match.dependences[0].winner)
                match.set_player_b(match.dependences[1].winner)
            match.player_a.exrounds[round] = match.prob_a
            match.player_b.exrounds[round] = match.prob_b
            for m in match.dependences:
                self.backtrack(m, round-1)
            return [match.player_a, match.player_b]
        else:
            res_left = self.do_match(match.dependences[0], round-1)
            res_right = self.do_match(match.dependences[1], round-1)

            for l in res_left:
                for r in res_right:
                    prob = l.exrounds[round-1] * r.exrounds[round-1]
                    match.set_player_a(l)
                    match.set_player_b(r)
                    l.exrounds[round] += match.prob_a * prob
                    r.exrounds[round] += match.prob_b * prob

            return res_left + res_right

    def backtrack(self, match, round):
        match.winner.exrounds[round] = 1
        for m in match.dependences:
            self.backtrack(m, round-1)

    def find_match(self, pa=None, pb=None, search=''):
        ex = 'No such match found \'' + search + '\''

        search = search.split('-')
        if len(search) < 2:
            raise Exception(ex)

        try:
            return self.bracket[int(search[0])-1][int(search[1])-1]
        except:
            raise Exception(ex)

    def get_player(self, name):
        fits = lambda p: p.name.lower() == name.lower()
        gen = (player for player in self.players if fits(player))
        try:
            return next(gen)
        except:
            return None

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
            title = str(pow(2,self._rounds)) + '-man single elimination bracket'
        out = strings['header'].format(title=title)

        sorted_winners = sorted(self.winners, key = lambda a: a.exrounds[-1],\
                                reverse=True)

        out += strings['mlwinnerlist']
        for res in sorted_winners[0:16]:
            out += strings['mlwinneri'].format(player=res.name,\
                                               prob=100*res.exrounds[-1])

        sorted_exrounds = sorted(self._players, key = lambda a: sum(a.exrounds),\
                                reverse=True)
#
        out += strings['exroundslist']
        for res in sorted_exrounds:
            rounded = self._rounds - round(sum(res.exrounds))
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
#
            out += strings['exroundsi'].format(player=res.name,\
                                               rounds=sum(res.exrounds),\
                                               expl=expl)

        out += strings['footer']

        return out
