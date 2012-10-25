def get_strings(args):

    strings = dict()

    # Newline
    strings['nl'] = '\n'

    # Header and footer
    strings['header'] = ''
    strings['footer'] = ''

    if args['format'] == 'tls':
        strings['header'] = '[spoiler={title}][b]{title}[/b]'
        strings['footer'] = '[/spoiler]'
    elif args['format'] == 'tl':
        strings['header'] = '[b]{title}[/b]'
    elif args['format'] == 'reddit':
        strings['header'] = '**{title}**'
    elif args['format'] == 'term':
        strings['header'] = '{title}'

    # Match-specific
    strings['outcomelist'] = '\n\n{player} wins ({prob:.3f}%):'
    if args['format'] == 'reddit':
        strings['outcomelist'] += '\n'
    strings['mlwinner'] = '\n\nMost likely winner: {player} ({prob:.3f}%)'
    if args['format'] == 'reddit':
        strings['mlwinner'] += '  '
    strings['mloutcome'] = '\nMost likely outcome: {pa} {na}-{nb} {pb} ({prob:.3f}%)'
    if args['format'] == 'term':
        strings['outcomei'] = '\n{winscore: >5}-{losescore: <1}: {prob: >6.3f}%'
    elif args['format'] == 'tl' or args['format'] == 'tls':
        strings['outcomei'] = '\n[indent]{winscore}-{losescore}: {prob:.3f}%'
    elif args['format'] == 'reddit':
        strings['outcomei'] = '\n* {winscore}-{losescore}: {prob:.3f}%'

    # Bracket-specific
    strings['mlwinnerlist'] = '\n\nMost likely winners:'
    strings['exroundslist'] = '\n\nLife expectancy:'
    if args['format'] == 'reddit':
        strings['mlwinnerlist'] += '\n'
        strings['exroundslist'] += '\n'
    if args['format'] == 'term':
        strings['mlwinneri'] = '\n{player:>10}: {prob: >6.3f}%'
        strings['exroundsi'] = '\n{player:>10}: {rounds: >5.3f} rounds ({expl})'
    elif args['format'] == 'tl' or args['format'] == 'tls':
        strings['mlwinneri'] = '\n[indent]{player}: {prob:.3f}%'
        strings['exroundsi'] = '\n[indent]{player}: {rounds:.3f} rounds ({expl})'
    elif args['format'] == 'reddit':
        strings['mlwinneri'] = '\n* {player}: {prob:.3f}%'
        strings['exroundsi'] = '\n* {player}: {rounds:.3f} rounds ({expl})'

    # Round robin-specific
    strings['gplayer'] = '\n\n{player}'
    if args['format'] == 'reddit':
        strings['gplayer'] += '\n'
    if args['format'] == 'term':
        strings['gpexpscore'] = '\n   Expected score: {mw:.2f}-{ml:.2f} (sets: {sw:.2f}-{sl:.2f})'
        strings['gpprobwin'] = '\n   Probability of winning: {prob:.3f}%'
        strings['gpprobthr'] = '\n   Probability of achieving top {thr}: {prob:.3f}%'
        strings['gpmlplace'] = '\n   Most likely place: {place} ({prob:.3f}%)'
    elif args['format'] == 'tl' or args['format'] == 'tls':
        strings['gpexpscore'] = '\n[indent]Expected score: {mw:.2f}-{ml:.2f} (sets: {sw:.2f}-{sl:.2f})'
        strings['gpprobwin'] = '\n[indent]Probability of winning: {prob:.3f}%'
        strings['gpprobthr'] = '\n[indent]Probability of achieving top {thr}: {prob:.3f}%'
        strings['gpmlplace'] = '\n[indent]Most likely place: {place} ({prob:.3f}%)'
    elif args['format'] == 'reddit':
        strings['gpexpscore'] = '\n* Expected score: {mw:.2f}-{ml:.2f} (sets: {sw:.2f}-{sl:.2f})'
        strings['gpprobwin'] = '\n* Probability of winning: {prob:.3f}%'
        strings['gpprobthr'] = '\n* Probability of achieving top {thr}: {prob:.3f}%'
        strings['gpmlplace'] = '\n* Most likely place: {place} ({prob:.3f}%)'

    return strings
