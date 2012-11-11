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
    strings['outcomelist'] = '\n\n{player} wins ({prob:.2f}%):'
    if args['format'] == 'reddit':
        strings['outcomelist'] += '\n'
    strings['mlwinner'] = '\n\nMost likely winner: {player} ({prob:.2f}%)'
    if args['format'] == 'reddit':
        strings['mlwinner'] += '  '
    strings['mloutcome'] = '\nMost likely outcome: {pa} {na}-{nb} {pb} ({prob:.2f}%)'
    if args['format'] == 'term':
        strings['outcomei'] = '\n{winscore: >5}-{losescore: <1}: {prob: >6.2f}%'
    elif args['format'] == 'tl' or args['format'] == 'tls':
        strings['outcomei'] = '\n[indent]{winscore}-{losescore}: {prob:.2f}%'
    elif args['format'] == 'reddit':
        strings['outcomei'] = '\n* {winscore}-{losescore}: {prob:.2f}%'

    # Bracket-specific
    strings['mlwinnerlist'] = '\n\nMost likely winners:'
    strings['exroundslist'] = '\n\nLife expectancy:'
    if args['format'] == 'reddit':
        strings['mlwinnerlist'] += '\n'
        strings['exroundslist'] += '\n'
    if args['format'] == 'term':
        strings['mlwinneri'] = '\n{player:>14}: {prob: >6.2f}%'
        strings['exroundsi'] = '\n{player:>14}: {rounds: >4.2f} rounds ({expl})'
    elif args['format'] == 'tl' or args['format'] == 'tls':
        strings['mlwinneri'] = '\n[indent]{player}: {prob:.2f}%'
        strings['exroundsi'] = '\n[indent]{player}: {rounds:.2f} rounds ({expl})'
    elif args['format'] == 'reddit':
        strings['mlwinneri'] = '\n* {player}: {prob:.2f}%'
        strings['exroundsi'] = '\n* {player}: {rounds:.2f} rounds ({expl})'

    # Round robin-specific
    strings['gplayer'] = '\n\n{player}'
    if args['format'] == 'reddit':
        strings['gplayer'] += '\n'
    if args['format'] == 'term':
        strings['gpexpscore'] = '\n   Expected score: {mw:.2f}-{ml:.2f} (sets: {sw:.2f}-{sl:.2f})'
        strings['gpprobwin'] = '\n   Probability of winning: {prob:.2f}%'
        strings['gpprobthr'] = '\n   Probability of achieving top {thr}: {prob:.2f}%'
        strings['gpmlplace'] = '\n   Most likely place: {place} ({prob:.2f}%)'
    elif args['format'] == 'tl' or args['format'] == 'tls':
        strings['gpexpscore'] = '\n[indent]Expected score: {mw:.2f}-{ml:.2f} (sets: {sw:.2f}-{sl:.2f})'
        strings['gpprobwin'] = '\n[indent]Probability of winning: {prob:.2f}%'
        strings['gpprobthr'] = '\n[indent]Probability of achieving top {thr}: {prob:.2f}%'
        strings['gpmlplace'] = '\n[indent]Most likely place: {place} ({prob:.2f}%)'
    elif args['format'] == 'reddit':
        strings['gpexpscore'] = '\n* Expected score: {mw:.2f}-{ml:.2f} (sets: {sw:.2f}-{sl:.2f})'
        strings['gpprobwin'] = '\n* Probability of winning: {prob:.2f}%'
        strings['gpprobthr'] = '\n* Probability of achieving top {thr}: {prob:.2f}%'
        strings['gpmlplace'] = '\n* Most likely place: {place} ({prob:.2f}%)'

    # MSL group-specific
    if args['type'] == 'mslgroup':
        strings['header'] += '\n'
    if args['format'] == 'term':
        strings['mslgplayer'] = '\n{player:>14}: {prob: >6.2f}%'
    elif args['format'] == 'tl' or args['format'] == 'tls':
        strings['mslgplayer'] = '\n[indent]{player}: {prob:.2f}%'
    elif args['format'] == 'reddit':
        strings['mslgplayer'] = '\n* {player}: {prob:.2f}%'

    # Probability table
    if args['format'] == 'term':
        strings['ptableheader'] = ' '*15
        strings['ptableheading'] = '{heading: >8}'
        strings['ptablename'] = '{player:>14}:'
        strings['ptableentry'] = '{prob: >7.2f}%'
    elif args['format'] == 'tls' or args['format'] == 'tl':
        strings['ptableheader'] = 'Not implemented.'
        strings['ptableheading'] = ''
        strings['ptablename'] = ''
        strings['ptableentry'] = ''
    elif args['format'] == 'reddit':
        strings['ptableheader'] = 'Not implemented.'
        strings['ptableheading'] = ''
        strings['ptablename'] = ''
        strings['ptableentry'] = ''

    return strings
