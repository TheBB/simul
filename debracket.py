import match
import progressbar

class ScoreTally:

    def __init__(self, rounds):
        self.finishes = [0] * 2*rounds

    def compute(self):
        self.exrounds = 0
        for i in range(0,len(self.finishes)):
            self.exrounds += i * self.finishes[i]

class DEBracket:

    def __init__(self, num, rounds, players):
        self.type = 'debracket'
        self._num = num
        self._rounds = rounds
        self._players = players
        self.setup_matches()
        
        self.words = []
        for i in range(0,len(self.winners)):
            for j in range(0,len(self.winners[i])):
                self.words.append('wb' + str(i+1) + '-' + str(j+1))
        for i in range(0,len(self.losers)):
            for j in range(0,len(self.losers[i])):
                self.words.append('lb' + str(i+1) + '-' + str(j+1))
        self.words.append('f1')
        self.words.append('f2')

    def get_players(self):
        return self._players

    def find_match(self, pa=None, pb=None, search=''):
        ex = 'No such match found \'' + search + '\''

        if search[0:2].lower() == 'lb':
            array = self.losers
        elif search[0:2].lower() == 'wb':
            array = self.winners
        elif search[0:2].lower() == 'f1':
            return self.final1
        elif search[0:2].lower() == 'f2':
            return self.final2
        else:
            raise Exception(ex)

        search = search[2:].split('-')
        if len(search) < 2:
            raise Exception(ex)

        try:
            return array[int(search[0])-1][int(search[1])-1]
        except:
            raise Exception(ex)

    def get_player(self, name):
        fits = lambda p: p.name.lower() == name.lower()
        gen = (player for player in self._players if fits(player))
        try:
            return next(gen)
        except:
            return None

    def setup_matches(self):
        rounds = self._rounds

        winners = []
        losers = []
        all = []
        final1 = match.Match(self._num, None, None)

        for i in range(0,rounds):
            rnd = []
            for j in range(0,2**(rounds-1-i)):
                m = match.Match(self._num, None, None)
                m.winners_bracket = True
                m.round = -1
                rnd.append(m)
                all.append(m)
            winners.append(rnd)

        for j in range(0,len(winners[0])):
            winners[0][j].set_player(self._players[2*j], 0)
            winners[0][j].set_player(self._players[2*j+1], 1)

        for i in range(0,2*(rounds-1)):
            rnd = []
            for j in range(0,2**(rounds-2-i//2)):
                m = match.Match(self._num, None, None)
                m.winners_bracket = False
                m.round = i
                rnd.append(m)
                all.append(m)
            losers.append(rnd)

        for i in range(0,len(winners)):
            lbr = max(2*i-1, 0)
            flip = (i % 2 == 1)
            for j in range(0,len(winners[i])):
                if i < len(winners) - 1:
                    winners[i][j].link_winner = winners[i+1][j//2]
                    winners[i][j].link_winner_slot = j % 2
                    winners[i+1][j//2].dependences.append(winners[i][j])

                if i > 0:
                    k = j
                    if flip:
                        k = len(losers[lbr]) - 1 - k
                    winners[i][j].link_loser = losers[lbr][k]
                    winners[i][j].link_loser_slot = 0
                    losers[lbr][k].dependences.append(winners[i][j])
                else:
                    winners[i][j].link_loser = losers[0][j//2]
                    winners[i][j].link_loser_slot = j % 2
                    losers[0][j//2].dependences.append(winners[i][j])

        winners[-1][0].link_winner = final1
        winners[-1][0].link_winner_slot = 0
        final1.dependences.append(winners[-1][0])

        for i in range(0,len(losers)):
            for j in range(0,len(losers[i])):
                losers[i][j].link_loser = None
                if i % 2 == 0:
                    losers[i][j].link_winner = losers[i+1][j]
                    losers[i][j].link_winner_slot = 1
                    losers[i+1][j].dependences.append(losers[i][j])
                elif i < len(losers) - 1:
                    losers[i][j].link_winner = losers[i+1][j//2]
                    losers[i][j].link_winner_slot = j % 2
                    losers[i+1][j//2].dependences.append(losers[i][j])

        losers[-1][0].link_winner = final1
        losers[-1][0].link_winner_slot = 1
        final1.dependences.append(losers[-1][0])

        self.winners = winners
        self.losers = losers
        self.final1 = final1
        self.final2 = match.Match(self._num, None, None)
        self.final2.dependences = [final1]

        all.append(final1)
        all.append(self.final2)
        self.all = all

    def can_use_exact(self):
        ms = 2 + sum([len(a) for a in self.winners]) +\
                sum([len(a) for a in self.losers])
        num = (2*self._num)**ms
        return num < 1e5

    def compute(self):
        if self.can_use_exact():
            self.compute_exact()
        else:
            self.compute_mc()

    def compute_mc(self):
        tally = dict()
        for p in self._players:
            tally[p] = ScoreTally(self._rounds)

        N = 50000
        progress = progressbar.ProgressBar(N, exp='Monte Carlo')
        for i in range(0,N):
            self.simulate(tally)
            if i % 500 == 0:
                progress.update_time(i)
                print(progress.dyn_str())
        progress.update_time(N)
        print(progress.dyn_str())
        print('')

        for t in tally.values():
            t.finishes = [f/N for f in t.finishes]
            t.compute()

        self.tally = tally

    def compute_exact(self):
        matches = self.all
        for match in matches:
            match.compute()

        outcome = [0] * len(matches)

        tally = dict()
        for p in self._players:
            tally[p] = ScoreTally(self._rounds)
        
        while outcome != False:
            base = 1
            for j in range(0,len(matches)):
                m = matches[j]
                base *= m.probs[outcome[j]]
                if base == 0:
                    break

                if not m.fixed_result:
                    if m.link_winner != None:
                        m.link_winner.set_player(m.players[outcome[j]], m.link_winner_slot)
                    if m.link_loser != None:
                        m.link_loser.set_player(m.players[1-outcome[j]], m.link_loser_slot)
                if j == len(matches) - 2:
                    matches[-1].set_player(m.player_a, 0)
                    matches[-1].set_player(m.player_b, 1)

            if base == 0:
                continue

            for j in range(0,len(matches)-2):
                m = matches[j]
                if not m.winners_bracket:
                    tally[m.players[1-outcome[j]]].finishes[m.round] += base

            if outcome[-1] == 0 or outcome[-2] == 0:
                tally[self.final1.player_a].finishes[-1] += base
                tally[self.final1.player_b].finishes[-2] += base
            else:
                tally[self.final1.player_b].finishes[-1] += base
                tally[self.final1.player_a].finishes[-2] += base

            outcome = self.get_next_outcome(outcome)

        for t in tally.values():
            t.compute()

        self.tally = tally

    def get_next_outcome(self, outcome):
        j = len(outcome) - 1

        while j >= 0:
            outcome[j] += 1
            if outcome[j] == 2:
                outcome[j] = 0
                j -= 1
            else:
                break

        if j == -1:
            return False
        else:
            return outcome

    def simulate(self, tally):
        winners = self.winners
        losers = self.losers
        final1 = self.final1
        final2 = self.final2

        for i in range(0,len(winners)):
            for match in winners[i]:
                self.do_match(match, tally, -1)

        for i in range(0,len(losers)):
            for match in losers[i]:
                self.do_match(match, tally, i)

        final2.set_player_a(final1.player_a)
        final2.set_player_b(final1.player_b)
        final1.compute()
        final2.compute()

        res1 = final1.get_random_result()
        res2 = final2.get_random_result()

        if res1[0] > res1[1] or res2[0] > res2[1]:
            tally[final1.player_a].finishes[-1] += 1
            tally[final1.player_b].finishes[-2] += 1
        else:
            tally[final1.player_a].finishes[-2] += 1
            tally[final1.player_b].finishes[-1] += 1

    def do_match(self, match, tally, round):
        match.compute()
        res = match.get_random_result()

        winner = (match.player_a if res[0] > res[1] else match.player_b)
        loser = (match.player_a if res[1] > res[0] else match.player_b)

        if match.link_winner != None:
            match.link_winner.set_player(winner, match.link_winner_slot)
        if match.link_loser != None:
            match.link_loser.set_player(loser, match.link_loser_slot)

        if round > -1:
            tally[loser].finishes[round] += 1

        return winner

    def detail(self):
        out = ' ' * 15

        top = 16
        dec = top // 4
        for i in range(0,len(self.losers)+2):
            out += ' ' * (5+2-len(str(top))) + 'T' + str(top)
            top -= dec
            if i % 2 == 1:
                dec = max(dec // 2, 1)

        for p in self._players:
            out += '\n'
            t = self.tally[p]
            out += '{a:>14}: '.format(a=p.name)
            for i in t.finishes:
                out += '{a: >6.2f}% '.format(a=100*i)

        return out

    def output(self, strings, title=None):
        if title == None:
            title = str(2**self._rounds) + '-man double elimination bracket'
        out = strings['header'].format(title=title)

        tally = self.tally
        players = sorted(self._players, key=lambda p: tally[p].finishes[-1], reverse=True)

        out += strings['mlwinnerlist']
        for p in players[0:16]:
            out += strings['mlwinneri'].format(player=p.name,\
                                              prob=100*tally[p].finishes[-1])

        players = sorted(players, key=lambda p: tally[p].exrounds, reverse=True)
        placings = [1, 1]
        for r in range(0,self._rounds-1):
            k = 2**r
            placings.append(k)
            placings.append(k)

        out += strings['exroundslist']
        for p in players:
            expl = round(tally[p].exrounds)
            if expl > 0:
                expl = sum(placings[:-expl])
            else:
                expl = sum(placings)
            expl = 'top ' + str(expl)
            out += strings['exroundsi'].format(player=p.name,\
                                               rounds=tally[p].exrounds,\
                                               expl=expl)

        out += strings['footer'].format(title=title)

        return out
