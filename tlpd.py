from urllib.request import urlopen, Request

tlpd_url = "http://www.teamliquid.net/tlpd_search.php?search={player}"\
           "&type={db}:all"
user_agent = "Mozilla/5.0 (X11; Linux x86_64; rv:15.0) Gecko/20100101"\
             " Firefox/15.0.1"

def tlpd_search(player, db="sc2-korean"):
    url = tlpd_url.format(db=db, player=player)
    request = Request(url, headers={"User-Agent": user_agent})

    res = urlopen(request)
    return res.read()

print(tlpd_search("parting"))

