#!/usr/bin/python3

from urllib.request import urlopen, Request
import re
import time
import sqlite3

_user_agent = 'Mozilla/5.0 (X11; Linux x86_64; rv:16.0) Gecko/20100101'\
        + ' Firefox/16.0'

def _from_file():
    return True

def get_tabulator_id(type, db='sc2-korean'):
    if type == 'players-detailed-elo':
        url = 'http://www.teamliquid.net/tlpd/{db}/players/detailed-elo'
    elif type == 'games':
        url = 'http://www.teamliquid.net/tlpd/{db}/games'
    else:
        url = 'http://www.teamliquid.net/tlpd/{db}/players'

    if not _from_file():
        url = url.format(db=db)
        try:
            request = Request(url, headers={'User-Agent': _user_agent})
            result = urlopen(request)
            result = result.read().decode()
        except Exception as e:
            print(' > tlpd.get_tabulator_id (request): ' + str(e))
            return -1
        with open('testtabulator-' + type, 'w') as f:
            f.write(result)
    else:
        with open('testtabulator-' + type, 'r') as f:
            result = f.read()

    out = re.compile('tblt_ids\[\'tblt\'\] = \'\d+\';').findall(result)
    if len(out) > 0:
        return int(re.compile('\d+').findall(out[0])[0])
    else:
        print(' > tlpd.get_tabulator_id (parse)')
        return -1

class Tlpd:

    _tlpd_url = 'http://www.teamliquid.net/tlpd/tabulator/update.php?'\
            + 'tabulator_id={tabulator}&tabulator_page={page}&'\
            + 'tabulator_order_col={col}&tabulator_search={search}'

    def __init__(self, db='sc2-korean'):
        self._tabulator = -1
        self._db = db
        self._type = ''

    def get_games(self, page=1, col=0, search='', desc=False):
        if self._tabulator == -1 or self._type != 'games':
            self._tabulator = get_tabulator_id('games', self._db)
            self._type = 'games'

        if not _from_file():
            if self._tabulator == -1:
                return None
            
            url = self._tlpd_url.format(tabulator=self._tabulator,\
                                       page = page, col=col, search=search)
            if desc:
                url += 'tabulator_order_desc=1'
            try:
                request = Request(url, headers={'User-Agent': _user_agent})
                result = urlopen(request)
                result = result.read().decode()
            except Exception as e:
                print(' > tlpd.get_games (request): ' + str(e))
                return None

            with open('testsearch', 'a') as f:
                f.write(result)
        else:
            with open('testsearch', 'r') as f:
                result = f.read()

        out = re.compile('Game Info( \\+ VOD)?" ?href="\\/tlpd\\/' + self._db +
                         '\\/games\\/\d+_').finditer(result)

        intervals = []
        prev = None
        for match in out:
            if prev != None:
                this = match.span()
                that = prev.span()
                intervals.append(result[that[0]:this[0]])
            prev = match
        this = match.span()
        intervals.append(result[this[0]:])
       
        results = []
        for plstr in intervals:
            res = dict()
            res['add'] = True

            try:
                temp = re.compile('\\/games\\/\\d+').findall(plstr)
                res['game_id'] = int(re.compile('\\d+').findall(temp[0])[0])

                temp = re.compile('background:.*\n *\\d+-\\d+-\\d+').findall(plstr)
                if len(temp) > 0:
                    res['date'] = '20' + re.compile('\\d+-\\d+-\\d+').findall(temp[0])[0]

                temp = re.compile('\\/maps\\/\\d+').findall(plstr)
                if len(temp) > 0:
                    res['map_id'] = int(re.compile('\\d+').findall(temp[0])[0])
                else:
                    res['map_id'] = 222

                temp = re.compile('\\/players\\/\\d+').findall(plstr)
                if len(temp) > 1:
                    res['winner_id'] = int(re.compile('\\d+').findall(temp[0])[0])
                    res['loser_id'] = int(re.compile('\\d+').findall(temp[1])[0])
                if len(temp) > 4:
                    res['add'] = False
            except Exception as e:
                print(' > tlpd.get_games (parse): ' + str(e))
            finally:
                if res['add']:
                    results.append(res)

        return results

    def get_players(self, page=1, col=0, search=''):
        if self._tabulator == -1 or self._type != 'players':
            self._tabulator = get_tabulator_id('players', self._db)
            self._type = 'players'

        if not _from_file():
            if self._tabulator == -1:
                return None

            url = self._tlpd_url.format(tabulator=self._tabulator,\
                                        page=page, col=col, search=search)
            try:
                request = Request(url, headers={'User-Agent': _user_agent})
                result = urlopen(request)
                result = result.read().decode()
            except Exception as e:
                print(' > tlpd.get_players (request): ' + str(e))
                return None

            with open('testsearch', 'a') as f:
                f.write(result)
        else:
            with open('testsearch', 'r') as f:
                result = f.read()

        out = re.compile('\\/tlpd\\/images\\/[PTZR\\?]icon\\.png').finditer(result)

        intervals = []
        prev = None
        for match in out:
            if prev != None:
                this = match.span()
                that = prev.span()
                intervals.append(result[that[0]:this[0]])
            prev = match
        this = match.span()
        intervals.append(result[this[0]:])

        results = []
        for plstr in intervals:
            res = dict()

            try:
                res['race'] = plstr[13]

                temp = re.compile('\\/flags\\/[a-z]?[a-z]?\\.png').findall(plstr)
                if len(temp) > 0 and len(temp[0]) == 13:
                    res['nationality'] = temp[0][-6:-4]
                else:
                    res['nationality'] = 'unknown'

                temp = re.compile('\\/players\\/\\d+_[^ ]* *">').findall(plstr)
                if len(temp) > 0:
                    ids = re.compile('\d+').finditer(temp[0])
                    for id in ids:
                        span = id.span()
                        res['tlpd_id'] = int(temp[0][span[0]:span[1]])
                        res['tag'] = temp[0][span[1]+1:-2].strip()
                        break

                temp = re.compile('<td.*background.*>\n.*\n?<\\/td>').findall(plstr)
                if len(temp) > 2:
                    names = re.compile('\n.*\n?<').findall(temp[0])
                    if len(names) > 0:
                        res['name'] = names[0][1:-1].strip()

                    teams = re.compile('\\/teams/\\d+').findall(temp[2])
                    if len(teams) > 0:
                        res['team'] = int(re.compile('\\d+').findall(teams[0])[0])
                    else:
                        res['team'] = -1

            except Exception as e:
                print(' > tlpd.get_players (parse): ' + str(e))
            finally:
                results.append(res)

        return results

if __name__ == '__main__':

    conn_old = sqlite3.connect('tlpd.sql')
    conn_new = sqlite3.connect('database.sql')
    co = conn_old.cursor()
    cn = conn_new.cursor()

    f = co.execute('SELECT name, tlpd_id FROM teams').fetchall()
    for r in f:
        cn.execute('INSERT INTO teams (name, tlpd_id) VALUES (:name,:tlpd)',\
                   {'name': r[0], 'tlpd': r[1]})

    f = co.execute('SELECT name FROM maps').fetchall()
    for r in f:
        cn.execute('INSERT INTO maps (name) VALUES (:name)',\
                   {'name': r[0]})

    f = co.execute('SELECT version, map, tlpd_id FROM map_versions').fetchall()
    for r in f:
        cn.execute('INSERT INTO map_versions (version, map, tlpd_id) VALUES (:version,:map,:tlpd)',\
                   {'version': r[0], 'map': r[1], 'tlpd': r[2]})

    f = co.execute('SELECT tag, race, name, nationality, team, tlpd_id FROM players').fetchall()
    for r in f:
        cn.execute('INSERT INTO players (tag, race, name, nationality, team, tlpd_id) VALUES (:tag,:race,:name,:nationality,:team,:tlpd)',\
                   {'tag': r[0], 'race': r[1], 'name': r[2], 'nationality': r[3], 'team': r[4], 'tlpd': r[5]})

    conn_new.commit()

    f = co.execute('SELECT winner, loser, map, date, tlpd_id FROM games ORDER BY date, tlpd_id').fetchall()
    for r in f:
        t = co.execute('SELECT tlpd_id FROM players WHERE ROWID=' + str(r[0])).fetchall()
        winner_tlpd = t[0][0]
        t = co.execute('SELECT tlpd_id FROM players WHERE ROWID=' + str(r[1])).fetchall()
        loser_tlpd = t[0][0]

        t = cn.execute('SELECT ROWID FROM players WHERE tlpd_id=' + str(winner_tlpd)).fetchall()
        winner = t[0][0]
        t = cn.execute('SELECT ROWID FROM players WHERE tlpd_id=' + str(loser_tlpd)).fetchall()
        loser = t[0][0]

        cn.execute('INSERT INTO games (winner, loser, map, period, date, tlpd_id) VALUES (:winner,:loser,:map,-1,:date,:tlpd)',\
                   {'winner': winner, 'loser': loser, 'map': r[2], 'date': r[3], 'tlpd': r[4]})

    conn_new.commit()
    conn_new.close()
    conn_old.close()
