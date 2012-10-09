def get_elo(s=''):
    elo = -1
    while elo == -1:
        try:
            elo = int(input('Elo' + (' ' if s != '' else '') + s + ': '))
        except:
            elo = -1
    return elo

def get_player(i):
    print('Entering player ' + str(i))
    name = input('ID: ')

    race = ''
    while race == '':
        race = input('Race: ').upper()
        if race != 'P' and race != 'Z' and race != 'T':
            race = ''

    elo = get_elo()
    elo_vt = get_elo('vT')
    elo_vz = get_elo('vZ')
    elo_vp = get_elo('vP')

    print('')

    return Player(name, race, elo, elo_vp, elo_vt, elo_vz)

class Player:

    def __init__(self, name, race, elo, elo_vp, elo_vt, elo_vz):
        self.name = name
        self.race = race
        self.elo = elo
        self.elo_race = {'P': elo_vp, 'T': elo_vt, 'Z': elo_vz}

    def prob_of_winning(self, opponent):
        mix = 0.5
        my_elo = mix * self.elo + (1 - mix)*self.elo_race[opponent.race]
        op_elo = mix * opponent.elo + (1 - mix)*opponent.elo_race[self.race]
        my_q = pow(10, float(my_elo)/400)
        op_q = pow(10, float(op_elo)/400)
        return my_q/(my_q + op_q)

class PlayerList:

    def __init__(self, num):
        self.players = []
        while len(self.players) < num:
            i = len(self.players) + 1
            player = get_player(i)
            self.players.append(player)
