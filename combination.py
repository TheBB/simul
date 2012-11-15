import mslgroup
import sebracket
import progressbar

class ScoreTally:
    
    def __init__(self):
        self.finishes = [0] * 7

class Combination:

    def __init__(self, players):
        self.type = 'combination'
        self._players = players
        self.setup()

        self.words = []

    def get_players(self):
        return self._players

    def setup(self):
        self._groups = []
        for i in range(0,8):
            group = mslgroup.Group(3, self._players[4*i:4*(i+1)])
            group.compute()
            self._groups.append(group)

    def compute(self):
        tally = dict()
        for p in self._players:
            tally[p] = ScoreTally()

        N = 200000
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

        self.tally = tally

    def simulate(self, tally):
        nextround = [None] * 16

        for i in range(0,8):
            ps = self._groups[i].instance()
            tally[ps[3]].finishes[0] += 1
            tally[ps[2]].finishes[1] += 1
            nextround[2*i] = ps[0]
            nextround[15-2*i] = ps[1]

        bracket = sebracket.SEBracket([3, 3, 3, 4], 4, nextround)
        bracket.compute()
        for p in nextround:
            tally[p].finishes[2] += 1 - p.exrounds[0]
            tally[p].finishes[3] += p.exrounds[0] - p.exrounds[1]
            tally[p].finishes[4] += p.exrounds[1] - p.exrounds[2]
            tally[p].finishes[5] += p.exrounds[2] - p.exrounds[3]
            tally[p].finishes[6] += p.exrounds[3]

    def output(self, strings, title=None):
        def header(out, title):
            out += strings['ptabletitle'].format(title=title)
            out += strings['ptableheader']
            out += strings['ptableheading'].format(heading='Top 32')
            out += strings['ptableheading'].format(heading='Top 24')
            out += strings['ptableheading'].format(heading='Top 16')
            out += strings['ptableheading'].format(heading='Top 8')
            out += strings['ptableheading'].format(heading='Top 4')
            out += strings['ptableheading'].format(heading='Top 2')
            out += strings['ptableheading'].format(heading='Win')
            return out

        out = strings['detailheader']

        players = sorted(self._players, key=lambda p: self.tally[p].finishes[-1],\
                         reverse=True)

        out = header(out, 'Probability of finishing exactly...')
        for p in players:
            out += '\n'
            t = self.tally[p]
            out += strings['ptablename'].format(player=p.name)
            for i in t.finishes:
                out += strings['ptableentry'].format(prob=100*i)

        out += strings['ptablebetween']
        out = header(out, 'Probability of doing no better than...')
        for p in players:
            out += '\n'
            t = self.tally[p]
            out += strings['ptablename'].format(player=p.name)
            tot = 0
            for i in t.finishes:
                tot += i
                out += strings['ptableentry'].format(prob=100*tot)

        out += strings['ptablebetween']
        out = header(out, 'Probability of doing no worse than...')
        for p in players:
            out += '\n'
            t = self.tally[p]
            out += strings['ptablename'].format(player=p.name)
            tot = 1
            for i in t.finishes:
                out += strings['ptableentry'].format(prob=100*tot)
                tot -= i

        out += strings['detailfooter']

        return out
