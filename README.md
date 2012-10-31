simul
=====

Simulator for various tournament formants, intended for Starcraft.

Supports the following tournament formats:
-   Best-of-N matches
-   Single and double elimination brackets
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

### Major command-line arguments

The following arguments are valid and usable in all modes.

#### -t, --type

    ./simul.py -t match

Gives the tournament format to simulate. There are currently four choices:
-   **match**: a single best-of-N match between two players (default)
-   **sebracket**: a single elimination bracket with 2^n players
-   **debracket**: a double elimination bracket with 2^n players
-   **rrgroup**: a standard round-robin group with customizable tiebreakers
-   **mslgroup**: a four-player group format used in the MSL and GSL

#### -f, --format

    ./simul.py -f tl

Gives the output format. There are currently four choices:
-   **term**: Useful for display and easy reading in the terminal (default)
-   **tl**: Optimized for readability on the Team Liquid forums
-   **tls**: Same as **tl**, except wrapped in spoiler tags
-   **reddit**: Optimized for readability on Reddit

#### -s, --save

    ./simul.py -s my_group.sc2

Saves the match/group/bracket to a file, so that if changes have to be made,
all the data doesn't have to be input again.

#### -l, --load

    ./simul.py -l my_group.sc2

Loads the match/group/bracket from a file. If this parameter is specified, the
**type** argument, along with whatever secondary arguments it requires, is
ignored.

#### --tlpd

    ./simul.py --tlpd sc2-korean

If this argument is given, the Team Liquid Progaming Database (TLPD) is
consulted for player ratings. Currently, there are two relevant SC2 databases:
-   sc2-korean
-   sc2-international

If this argument is not given, you will be asked to input ratings manually.

TLPD does not currently offer an API, so this feature can be prone to problems,
if Team Liquid changes the layout of their site.

#### --tlpd-tabulator

    ./simul.py --tlpd-tabulator 1031

The TLPD lookup requires a *tabulator ID*. When too many tabulator IDs are
requested too quickly, the remote website will respond with HTTP: 503
service unavailable.

When simulating several matches or groups in quick succession, you can reuse a
single tabulator ID. Whenever a tabulator ID is requested from TLPD, it will be
written to the terminal. You can then pass it along as an argument in
subsequent executions.

#### --no-console

    ./simul.py --no-console

For certain formats, the program will launch a rudimentary console for making
changes or updates as the tournament progresses. Use this argument to skip the
console.

#### --title

    ./simul.py --title "My custom title"

Use this argument to specify a title used when outputting results.

### Type-specific command-line arguments

The following arguments are only usable for some tournament types, or work
differently depending on the type.

#### -n, --num

    ./simul.py -n 3
    ./simul.py -t sebracket -n 3 3 4

Specifies how many sets are required to win a match. If the matches are
best-of-3, this value should be **2** (not 3), because two wins suffice to win
a best-of-3 match. In general, for best-of-*N*, use (*N*+1)/2.

For single elimination brackets, input a value for each round, beginning with
the earliest round. Thus, if the quarter- and semifinals are best-of-5 and the
final is best-of-7 (such as the GSL), use **-n 3 3 4**.

#### -r, --rounds

    ./simul.py -t [sebracket|debracket] -r 4

Specifies how many rounds to play in a single- or double elimination bracket.
In either case, for *r* rounds there will be 2^*r* players.

A single elimination bracket will work fine with one round (which is
essentially just a match), while a double elimination bracket requires at least
two rounds (so four players at minimum.)

#### -p, --players

    ./simul.py -t rrgroup -p 4

For round robin groups, this argument specifies the number of players in the
group.

#### --threshold

    ./simul.py -t rrgroup --threshold 2

For round robin groups, this argument specifies the size of the "acceptable"
region on the top of the rankings. Use this for qualifying groups where you are
not interested in the probability of a player to *win*, but rather the
probability to achieve top *N*.

#### --tie

    ./simul.py -t rrgroup --tie mscore sscore imscore isscore ireplay

For round robin groups, this argument specifies which tiebreakers are in force,
and in which order they are applied. They are given in order from most to least
important.

-   **mscore**: Total match score
-   **sscore**: Total set score
-   **swins**: Total set wins
-   **imscore**: Internal match score, counted between the tied players
-   **isscore**: Internal set score, counted between the tied players
-   **iswins**: Internal number of set wins, counted between the tied players
-   **ireplay**: Rematch between the tied players

In case of a rematch, it is assumed to take place under the exact same
conditions as the original group (specifically, best-of-*N* with the same
tiebreaker structure).

Undefined behavior may occur if **ireplay** is first tiebreaker, or if it is
not present at all. Any tiebreakers after **ireplay** will necessarily be
ignored.

Formats
-------

The following section describes details on how to use each of the supported
tournament formants.

### Match

Use of the **match** format req

### Single elimination bracket

### Double elimination bracket

### Round robin

### MSL-style group

Console
-------
