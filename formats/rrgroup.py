import itertools

from formats.composite import Composite
from formats.match import Match

class RRGroup(Composite):

    def __init__(self, nplayers, num, tie, threshold=1, subgroups=None):
        self._num = num
        self._tie = tie
        self._threshold = threshold

        schema_in = [nplayers]
        schema_out = [1] * nplayers
        Composite.__init__(self, schema_in, schema_out)

        if subgroups != None:
            self._subgroups = subgroups
        else:
            self._subgroups = dict()

    def setup(self):
        nmatches = len(self._schema_out) * (len(self._schema_out) - 1) // 2
        self._matches = []

        for r in range(0, nmatches):
            m = Match(self._num)
            self._matches.append(m)

            m.add_parent(self)

    def players_to_id(self, pa, pb):
        i = min(pa.num, pb.num)
        j = max(pa.num, pb.num)

        return round(i*(len(self._schema_out) - (i+3)/2)) + j - 1

    def get_match(self, key):
        ex = 'No such match found \'' + key + '\''

        key = key.lower().split(' ')
        if len(key) < 2:
            raise Exception(ex)

        fits = lambda m: (m.player_a == key[0] and m.player_b == key[1]) or\
                         (m.player_b == key[0] and m.player_a == key[1])
        gen = (player for player in self._player if fits(player))

        try:
            return next(gen)
        except:
            raise Exception(ex)
    
    def should_use_mc(self):
        return false

    def fill(self):
        for i in range(0,len(self._players)):
            if players[i].flag == -1:
                players[i].flag = 1 << i
            players[i].num = i

        m = 0
        for pair in itertools.combinations(self._players, 2):
            self._matches[m].set_players(list(pair))
            m += 1

    def compute_exact(self):
        for m in self._matches:
            m.compute()

        gens = [m.instances_detail() for m in self._matches]
        for instances in itertools.product(*gens):
            prob = 1
            for inst in instances:
                prob *= inst[0]

            self.compute_table(instances, prob)

    def compute_table(self, instances, prob=1):
        for inst in instances:
            inst[3].temp_mscore += 1
            inst[4].temp_mscore -= 1
            inst[3].temp_sscore += inst[1] - inst[2]
            inst[4].temp_sscore += inst[2] - inst[1]
            inst[3].temp_swins += inst[1]
            inst[4].temp_swins += inst[2]

        table = self.break_ties(list(self._players), self._tie, instances)

    def break_ties(self, table, tie, instances)
        if tie[0] == 'imscore' or tie[0] == 'isscore' or tie[0] == 'iswins':
            for p in table:
                p.temp_imscore = 0
                p.temp_isscore = 0
                p.temp_iswins = 0

            combs = itertools.combinations(table, 2)
            for comb in combs:
                id = self.players_to_id(comb[0], comb[1])
                inst = instances[id]
                inst[3].temp_imscore += 1
                inst[4].temp_imscore -= 1
                inst[3].temp_isscore += inst[1] - inst[2]
                inst[4].temp_isscore += inst[2] - inst[1]
                inst[3].temp_iswins += inst[1]
                inst[4].temp_iswins += inst[2]

        if tie[0] == 'mscore' or tie[0] == 'sscore' or tie[0] == 'swins'\
        or tie[0] == 'imscore' or tie[0] == 'isscore' or tie[0] == 'iswins':
            key = attrgetter('temp_' + tie[0])
            table = sorted(table, key=key, reverse=True)

            keyval = key(table[0])
            keyind = 0
            for i in range(1, len(table)):
                if key(table[i]) != keyval:
                    if i > keyind + 1:
                        temp = self.break_ties(table[keyind:i], tie)
                        if temp != False:
                            table[keyind:i] = temp
                        else:
                            return False
                    keyval = key(table[i])
                    keyind = i

            if keyind < len(table) - 1 and keyind > 0:
                temp = self.break_ties(table[keyind:], tie)
                if temp != False:
                    table[keyind:] = temp
                else:
                    return False
            elif keyind < len(table) - 1:
                table = self.break_ties(table, tie[1:])
                if table == False:
                    return False

        if tie[0] == 'ireplay':
            if len(table) == len(self._players):
                return False

            subgroup_id = sum([p.flag for p in table])

            if not subgroup_id in self._subgroups:
                newplayers = []
                for p in table:
                    newplayers.append(playerlist.Player(copy=p))
                subgroup = RRGroup(len(table), self._num, self._tie,\
                                  subgroups=self._subgroups)
                self._subgroups[subgroup_id] = subgroup
                subgroup.set_players(newplayers)
                subgroup.compute()
            else:
                subgroup = self._subgroups[subgroup_id]

            root = 0
            for p in table:
                p.temp_spread = []
                ref = next(filter(lambda q: q.flag == p.flag, subgroup._players))
                reftally = subgroup.get_tally()[ref]
                for f in range(0,len(ref)):
                    p.temp_spread.append((root+f, finishes[f]))
                root -= 1

        return table
