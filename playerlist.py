def get_elo(s=''):
    elo = -1
    while elo == -1:
        try:
            elo = input('Elo' + (' ' if s != '' else '') + s + ': ')
            if elo.strip().lower() == '':
                return False
            elo = int(elo)
        except:
            elo = -1
    return elo

def get_player(i, tlpd=None):
    print('Entering player ' + str(i))
    name = input('ID: ')

    results = []
    if tlpd != None:
        results = tlpd.search(name)

    result = None
    if results != None and len(results) > 0:
        pl = len(results) > 1
        print('Possible match' + ('es' if pl else '') + ':')

        i = 1
        for res in results:
            print((str(i) + ': ' if pl else '') + res['name'] + ' ('\
                  + res['race'] + ') from '\
                  + res['team'] + ' (' + str(res['elo']) + ', '\
                  + str(res['elo_vt']) + ', ' + str(res['elo_vz']) + ', '\
                  + str(res['elo_vp']) + ')')
            i += 1

        if pl:
            choice = int(input('Which is correct? (1-' + str(len(results))\
                            + ', 0 for none) '))
            if choice > 0:
                result = results[choice-1]
        else:
            choice = input('Accept? (y/n) ')
            if choice.lower() == 'y':
                result = results[0]
    elif tlpd != None:
        if results == []:
            print('No matches for \'' + name + '\' in TLPD.')
        elif results == None:
            print('Unable to consult TLPD.')

    if result != None:
        name = result['name']
        race = result['race']
        elo = result['elo']
        elo_vt = result['elo_vt']
        elo_vz = result['elo_vz']
        elo_vp = result['elo_vp']
    else:
        race = ''
        while race == '':
            race = input('Race: ').upper()
            if race != 'P' and race != 'Z' and race != 'T':
                race = ''

        elo = get_elo()
        if elo == False:
            elo = 0
            elo_vt = 0
            elo_vz = 0
            elo_vp = 0
        else:
            elo_vt = get_elo('vT')
            elo_vz = get_elo('vZ')
            elo_vp = get_elo('vP')

    print('')

    return Player(name, race, elo, elo_vp, elo_vt, elo_vz)

class Player:

    def __init__(self, name='', race='', elo=0, elo_vp=0, elo_vt=0, elo_vz=0,\
                 copy=None):
        if copy == None:
            self.name = name
            self.race = race
            self.elo = elo
            self.elo_race = {'P': elo_vp, 'T': elo_vt, 'Z': elo_vz}
        else:
            self.name = copy.name
            self.race = copy.race
            self.elo = copy.elo
            self.elo_race = copy.elo_race

    def prob_of_winning(self, opponent):
        mix = 0.5
        my_elo = mix * self.elo + (1 - mix)*self.elo_race[opponent.race]
        op_elo = mix * opponent.elo + (1 - mix)*opponent.elo_race[self.race]
        my_q = pow(10, float(my_elo)/400)
        op_q = pow(10, float(op_elo)/400)
        return my_q/(my_q + op_q)

class PlayerList:

    def __init__(self, num, tlpd=None):
        self.players = []
        while len(self.players) < num:
            i = len(self.players) + 1
            player = get_player(i, tlpd)
            self.players.append(player)
