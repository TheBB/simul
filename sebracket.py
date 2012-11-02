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

            out += strings['exroundsi'].format(player=res.name,\
                                               rounds=sum(res.exrounds),\
                                               expl=expl)

        out += strings['footer']

        return out
