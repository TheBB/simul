#!/usr/bin/python3

import sqlite3
import math
import time

class Player:

    def __init__(self):
        self.id = 0
        self.pre_rating = 1500
        self.pre_deviation = 350
        self.pre_volatility = 0.06
        self.games = []
        self._tau = 0.5

    def compute(self, p=False):
        mu = float(self.pre_rating-1500)/173.7178
        phi = float(self.pre_deviation)/173.7178
        vol = self.pre_volatility
        for i in range(0,len(self.games)):
            gm = self.games[i]
            self.games[i] = ((gm[0]-1500)/173.7178, gm[1]/173.7178, gm[2])

        if p:
            print(mu)
            print(phi)
            print(vol)
            print(self.games)

        try:
            g = lambda p: 1.0/math.sqrt(1+3*p**2/math.pi**2)
            E = lambda m, mj, pj: 1.0/(1.0+math.exp(-g(pj)*(m-mj)))

            v = 0
            exp = 0
            for gm in self.games:
                Ev = E(mu, gm[0], gm[1])
                v += g(gm[1])**2 * Ev * (1.0 - Ev)
                exp += g(gm[1]) * (gm[2]-Ev)
            v = 1.0 / v
            delta = exp * v

            if p:
                print(v)
                print(delta)
        except:
            print(self)

        # Volatility iteration
        eps = 1e-6
        a = math.log(self.pre_volatility**2)
        f = lambda x: math.exp(x) * (delta**2 - phi**2 - v - math.exp(x)) /\
                (2*(phi**2 + v + math.exp(x))) - (x-a)/self._tau**2

        A = a
        if delta**2 > phi**2 + v:
            B = math.log(delta**2 - phi**2 - v)
        else:
            k = 1
            while f(a - k*math.sqrt(self._tau**2)) < 0:
                k += 1
            B = a - k*math.sqrt(self._tau**2)
        fa = f(A)
        fb = f(B)

        while abs(A-B) > eps:
            if p:
                print(str(A) + ' ' + str(B))
            C = A + (A-B)*fa/(fb-fa)
            fc = f(C)
            if fc*fb < 0:
                A = B
                fa = fb
            else:
                fa = fa/2
            B = C
            fb = fc
            if p:
                time.sleep(1)

        self.post_volatility = math.exp(A/2)
        post_phi = math.sqrt(phi**2 + self.post_volatility**2)
        post_phi = 1.0/math.sqrt(1.0/post_phi**2 + 1.0/v)
        post_mu = mu + post_phi**2 * exp

        if p:
            print(post_mu)
            print(post_phi)
            print(self.post_volatility)

        self.post_rating = 173.7178*post_mu+1500
        self.post_deviation = 173.7178*post_phi

        if p:
            print(self)

    def __str__(self):
        return str((self.pre_rating, self.pre_deviation, self.pre_volatility))\
                + ' ' + str(self.games)

    def __repr__(self):
        return self.__str__()

class Glicko:

    _initial_volatility = 0.06

    def __init__(self, db):
        self._conn = sqlite3.connect(db)
        self._cursor = self._conn.cursor()

    def __del__(self):
        self._conn.close()

    def make_periods(self):
        c = self._cursor

        c.execute('UPDATE games SET period=-1')
        self._conn.commit()

        first = c.execute('''SELECT strftime('%Y',date), strftime('%m',date)
                         FROM games ORDER BY date asc LIMIT 1''').fetchall()[0]
        last = c.execute('''SELECT strftime('%Y',date), strftime('%m',date)
                         FROM games ORDER BY date desc LIMIT 1''').fetchall()[0]

        year = int(first[0])
        month = int(first[1])
        last_year = int(last[0])
        last_month = int(last[1])

        last_month += 1
        if last_month == 13:
            last_month = 1
            last_year += 1

        period = 1
        while not (year == last_year and month == last_month):
            month += 1
            if month == 13:
                month = 1
                year += 1

            str_month = str(month)
            while len(str_month) < 2:
                str_month = '0' + str_month

            c.execute('UPDATE games SET period=:per WHERE date<:lim and period=-1',\
                      {'per': period, 'lim': str(year) + '-' + str_month})

            period += 1

        self._conn.commit()

    def get_num_periods(self):
        c = self._cursor

        return c.execute('SELECT max(period) FROM games').fetchall()[0][0]

    def clear_ratings(self):
        c = self._cursor

        try:
            c.execute('DROP TABLE ratings')
            self._conn.commit()
        except:
            pass

        c.execute('''CREATE TABLE ratings (player integer, played integer,
                  rating real, deviation real, volatility real,
                  period integer)''')
        self._conn.commit()

    def compute_ratings(self, period):
        print('Updating ratings for period ' + str(period))

        copied = 0
        added = 0
        games = 0

        c = self._cursor

        c.execute('''DELETE FROM ratings WHERE period=:period''',\
                  {'period': period})

        pls = c.execute('''SELECT player, rating, deviation, volatility FROM 
                        ratings WHERE period=:period''',\
                        {'period': period-1}).fetchall()
        for pl in pls:
            c.execute('''INSERT INTO ratings (player, played, rating,
                      deviation, volatility, period) VALUES (:player, :played,
                      :rating, :deviation, :volatility, :period)''',\
                      {'player': pl[0], 'played': 0, 'rating': pl[1],\
                       'deviation': pl[2], 'volatility': pl[3],\
                       'period': period})
            copied += 1
        self._conn.commit()

        plw = c.execute('SELECT DISTINCT winner FROM games WHERE period=:period',\
                  {'period': period}).fetchall()
        pll = c.execute('SELECT DISTINCT loser FROM games WHERE period=:period',\
                  {'period': period}).fetchall()
        for p in plw + pll:
            f = c.execute('''SELECT count(*) FROM ratings WHERE player=:player
                          and period=:period''',\
                          {'player': p[0], 'period': period}).fetchall()[0][0]
            if f > 0:
                c.execute('''UPDATE ratings SET played=1 WHERE player=:player 
                          and period=:period''',\
                          {'player': p[0], 'period': period})
            else:
                c.execute('''INSERT INTO ratings (player, played, rating,
                          deviation, volatility, period) VALUES (:player,
                          :played, :rating, :deviation, :volatility, 
                          :period)''',\
                          {'player': p[0], 'played': 1, 'rating': 1500,\
                           'deviation': 350, 'volatility': 0.06,\
                           'period': period})
                added += 1
        self._conn.commit()

        players = dict()

        print('...copied ' + str(copied) + ' players from previous rating period')
        print('...added ' + str(added) + ' first-time players')

        pls = c.execute('''SELECT player, rating, deviation, volatility FROM 
                        ratings WHERE played=1 and period=:period''',\
                        {'period': period}).fetchall()
        for pl in pls:
            newplayer = Player()
            newplayer.id = pl[0]
            newplayer.pre_rating = pl[1]
            newplayer.pre_deviation = pl[2]
            newplayer.pre_volatility = pl[3]
            players[pl[0]] = newplayer

        gms = c.execute('''SELECT winner, loser FROM games WHERE
                        period=:period''', {'period': period}).fetchall()
        for gm in gms:
            w = players[gm[0]]
            l = players[gm[1]]
            w.games.append((l.pre_rating, l.pre_deviation, 1))
            l.games.append((w.pre_rating, w.pre_deviation, 0))
            games += 1

        print('...' + str(len(players)) + ' players competed in this period over ' + str(games) + ' games')
        print('...computing rating changes...')

        for pl in players.values():
            if period > 13 and pl.id == 624:
                pl.compute(True)
            else:
                pl.compute()

            c.execute('''UPDATE ratings SET rating=:rating,
                       deviation=:deviation, volatility=:volatility WHERE
                       player=:player and period=:period''',\
                       {'rating': pl.post_rating,\
                        'deviation': pl.post_deviation,\
                        'volatility': pl.post_volatility, 'player': pl.id,
                        'period': period})
        self._conn.commit()

        print('...updating deviations for ' + str(copied+added-len(players)) + ' non-competing players...')

        pls = c.execute('''SELECT player, deviation, volatility FROM ratings
                        WHERE played=0 and period=:period''',\
                        {'period': period}).fetchall()
        for pl in pls:
            phi = pl[1]/173.7178
            phi = math.sqrt(phi**2 + pl[2]**2)
            phi = phi*173.7178
            c.execute('''UPDATE ratings SET deviation=:deviation WHERE
                      player=:player and period=:period''',\
                      {'player': pl[0], 'deviation': phi, 'period': period})

        self._conn.commit()

if __name__ == '__main__':
    glicko = Glicko('database.sql')
    glicko.make_periods()
    glicko.clear_ratings()
    for p in range(0,15):
        glicko.compute_ratings(p+1)
