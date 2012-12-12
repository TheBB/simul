try:
    import pyreadline as readline
except ImportError:
    import readline

from scipy.stats import norm

import simul

debug = False

def get_elo(s=''):
    elo = -1
    while elo == -1:
        try:
            elo = simul.better_input('Elo' + (' ' if s != '' else '') + s + ': ',\
                                     swipe=True)
            if elo.strip().lower() == '':
                return False
            elo = int(elo)
        except:
            elo = -1
    return elo

def get_player(i, finder=None):
    print('Entering player ' + str(i))

    result = None
    while result == None:
        name = simul.better_input('Name: ')

        if name == '-':
            print('')
            return Player('BYE', 'T', -10000, 0, 0, 0)

        results = []
        if finder != None:
            results = finder(name)

        if results != None and len(results) > 0:
            pl = len(results) > 1
            print('Possible match' + ('es' if pl else '') + ':')

            i = 1
            for res in results:
                print((str(i) + ': ' if pl else '') + res['name'] + ' ('\
                      + res['race'] + ') from '\
                      + res['team'] + ' (' + str(round(res['elo'])) + ', '\
                      + str(round(res['elo_vt'])) + ', '\
                      + str(round(res['elo_vz'])) + ', '\
                      + str(round(res['elo_vp'])) + ')')
                i += 1

            if pl:
                s = 'Which is correct? (1-' + str(len(results)) + ', 0 for none) '
                choice = simul.better_input(s, swipe=True)
                if choice == 'y':
                    result = results[0]
                elif int(choice) > 0:
                    result = results[int(choice)-1]
            else:
                choice = simul.better_input('Accept? (y/n) ', swipe=True)
                if choice.lower() == 'y':
                    result = results[0]
        elif finder != None:
            if results == []:
                print('No matches for \'' + name + '\' in database.')
            elif results == None:
                print('Unable to consult database.')
        elif finder == None:
            break

    if result != None:
        name = result['name']
        race = result['race']
        elo = result['elo']
        elo_vt = result['elo_vt']
        elo_vz = result['elo_vz']
        elo_vp = result['elo_vp']
    else:
        race = ''
        while race not in ['P', 'Z', 'T']:
            race = simul.better_input('Race: ', swipe=True).upper()

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
            self.flag = -1
        else:
            self.name = copy.name
            self.race = copy.race
            self.elo = copy.elo
            self.elo_race = copy.elo_race
            self.flag = copy.flag

    def prob_of_winning(self, opponent):
        mix = 0.3
        my_elo = self.elo + self.elo_race[opponent.race]
        op_elo = opponent.elo + opponent.elo_race[self.race]
        return norm.cdf((my_elo - op_elo)/1000)

    def copy(self):
        return Player(copy=self)

class PlayerList:

    def __init__(self, num, finder=None):
        self.players = []
        k = 1
        while len(self.players) < num:
            if not debug:
                i = len(self.players) + 1
                player = get_player(i, finder)
                self.players.append(player)
            else:
                self.players.append(Player('player' + str(k), 'T', 50*k, 50*k,\
                                           50*k, 50*k))
                k += 1
