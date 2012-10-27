simul
=====

Simulator for various tournament formants, intended for Starcraft.

Supports the following tournament formats:
-   Best-of-N matches
-   Single elimination brackets
-   Round robin with customisable tiebreakers
-   MSL-style four player groups

Outputs results intended for display
-   in the terminal
-   on the Team Liquid forums
-   on Reddit

Probabilities for the outcome of any single game are based on Elo ratings of
the players involved, which is collected from the Team Liquid Progaming
Database (TLPD) automatically, or input manually.

Requires
--------

Nothing but Python. The program has been written to run on Python 3.x, but will
likely work on Python 2.x with only minor changes.

Installation
------------

Simply put the files in a folder, and run the simul.py script. See the
following sections for details on command-line arguments.

Usage
-----

Execute the following command:

    ./simul.py [arguments]

The major command-line arguments are:

### -t, --type

    ./simul.py -t match

Gives the tournament format to simulate. There are currently four choices:
-   **match**: a single best-of-N match between two players (default)
-   **sebracket**: a single elimination bracket with 2^n players
-   **rrgroup**: a standard round-robin group with customizable tiebreakers
-   **mslgroup**: a four-player group format used in the MSL and GSL

### -f, --format

    ./simul.py -f tl

Gives the output format. There are currently four choices:
-   **term**: Useful for display and easy reading in the terminal (default)
-   **tl**: Optimized for readability on the Team Liquid forums
-   **tls**: Same as **tl**, except wrapped in spoiler tags
-   **reddit**: Optimized for readability on Reddit

### -s, --save

    ./simul.py -s my_group.sc2

Saves the match/group/bracket to a file, so that if changes have to be made,
all the data doesn't have to be input again.

### -l, --load

    ./simul.py -l my_group.sc2

Loads the match/group/bracket from a file. If this parameter is specified, the
**type** argument, along with whatever secondary arguments it requires, is
ignored.

### --tlpd

    ./simul.py --tlpd sc2-korean

If this argument is given, the Team Liquid Progaming Database (TLPD) is
consulted for player ratings. Currently, there are two relevant SC2 databases:
-   sc2-korean
-   sc2-international

If this argument is not given, you will be asked to input ratings manually.

TLPD does not currently offer an API, so this feature can be prone to problems,
if Team Liquid changes the layout of their site.

### --tlpd-tabulator

    ./simul.py --tlpd-tabulator 1031

The TLPD lookup requires a *tabulator ID*. When too many tabulator IDs are
requested too quickly, the remote website will respond with HTTP: 503
service unavailable.

When simulating several matches or groups in quick succession, you can reuse a
single tabulator ID. Whenever a tabulator ID is requested from TLPD, it will be
written to the terminal. You can then pass it along as an argument in
subsequent executions.

### --no-console

    ./simul.py --no-console

For certain formats, the program will launch a rudimentary console for making
changes or updates as the tournament progresses. Use this argument to skip the
console.

Formats
-------

The following section describes details on how to use each of the supported
tournament formants.

### Match

### Single elimination bracket

### Round robin

### MSL-style group

Console
-------
