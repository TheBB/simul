#!/usr/bin/python3

from urllib.request import urlopen, Request
import re

user_agent = "Mozilla/5.0 (X11; Linux x86_64; rv:16.0) Gecko/20100101"\
        + " Firefox/16.0"

tlpd_tabulator = "http://www.teamliquid.net/tlpd/{db}/players/detailed-elo"

tlpd_url = "http://www.teamliquid.net/tlpd/tabulator/update.php?"\
        + "tabulator_id={tabulator}&tabulator_page=1&tabulator_order_col="\
        + "default&tabulator_search={player}"

def tlpd_search(player, tabulator):
    url = tlpd_url.format(player=player, tabulator=tabulator)
    request = Request(url, headers={"User-Agent": user_agent})
    res = urlopen(request)
    return res.read()

def get_tabulator_id(db="sc2-korean"):
    #url = tlpd_tabulator.format(db="sc2-korean")
    #request = Request(url, headers={"User-Agent": user_agent})
    #res = urlopen(request)
    #q = str(res.read())

    #f = open('test', 'w')
    #f.write(q)
    #f.close()

    res = open('test', 'r')
    q = str(res.read())
    res.close()

    p = re.compile("tblt_ids\[\\\\'tblt\\\\'\] = \\\\'\d+\\\\';")
    out = p.findall(q)
    if len(out) > 0:
        p = re.compile('\d+')
        return int(p.findall(out[0])[0])
    else:
        return -1

tabulator = get_tabulator_id()
if tabulator != -1:
    print(tlpd_search("parting", tabulator))
