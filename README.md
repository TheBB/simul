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
a best-of-3 match. In general, for best-of-N, use (N+1)/2.

For single elimination brackets, input a value for each round, beginning with
the earliest round. Thus, if the quarter- and semifinals are best-of-5 and the
final is best-of-7 (such as the GSL), use **-n 3 3 4**.

#### -r, --rounds

    ./simul.py -t [sebracket|debracket] -r 4

Specifies how many rounds to play in a single- or double elimination bracket.
In either case, for *r* rounds there will be 2^r players.

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

Modes
-----

The following section describes details on how to use each of the supported
tournament formants.

### Match

Use of the **match** mode requires the **-n** argument for the number of sets
required to win the match. 

You are then asked to supply the names of the players, as well as their races
and ratings (if not gotten from TLPD).

### Single and double elimination bracket

Use of the **sebracket** and **debracket** modes require the **-r** argument
for the number of rounds (r rounds for 2^r players), as well as the **-n**
argument with the number of sets to win a match. In **sebracket** mode, you
should supply this argument for *each* round (starting with the earliest). In
**debracket** mode, different match lengths is not supported.

You are then asked to supply the names of the players, as well as their races
and ratings (if not gotten from TLPD). The order in which the players are
entered is not arbitrary, but follows the usual way to display a bracket.

### Round robin

Use of the **rrgroup** mode requires the **-p** argument for the number of
players in the group as well as the **-n** argument for number of sets to win a
match.

Optionally, supply the **--threshold** argument to denote the number of players
who "win" (e.g. how many players qualify to the next stage, if applicable). The
default threshold is 1. Also optionally, use the **--tie** argument to supply
custom tiebreakers and their order of application as described earlier.

You are then asked to supply the names of the players, as well as their races
and ratings (if not gotten from TLPD). The order is arbitrary.

### MSL-style group

Use of the **mslgroup** mode, just as the **match** mode, requires the **-n**
argument for the number of sets to win a match.

You are then asked to supply the names of the players, as well as their races
and ratings (if not gotten from TLPD). The order is not arbitrary—the first
round is player 1 vs. player 2 and player 3 vs. player 4.

Console
-------

After starting the program, and the initial input of player data (unless loaded
from a file), you are presented with the *console*, where you can modify the
results of matches and see the resulting data change accordingly.

If you wish to skip the console, run with the **--no-console** command-line
argument.

The following commands are available. You can always use tab-completion for
hints.

#### exit

Closes the program. If the **-s** command-line argument is given, the setup is
saved.

#### save [filename]

Saves the setup to the given file. If no filename is given, it will default to
the value of the **-s** command-line argument.

#### load [filename]

Loads the setup from the given file. If no filename is given, it will default
to the vlaue of the **-l** command-line argument.

#### compute

Recomputes the probabilities after making changes.

#### out [format]

Outputs the results in the given format (one of **term**, **tl**, **tls** or
**reddit**.) If the format is not given, it will default to the value of the
**-f** command-line argument.

#### set [match], unset [match]

Use **set** to set the final or temporary result of a match, and use **unset**
to clear it.

-   In **rrgroup** mode, specify the match by giving the names of the two
players.
-   In **mslgroup** mode, the match name must be one of **first**, **second**
(for the two initial matches), **winners**, **losers** (for the winner's and
loser's matches) and **final** (for the final game).
-   In **debracket** mode, the match name must be on the form **wbR-N** or
**lbR-N**, where *R* is the round number and *N* is the match number, for the
winner's and loser's brackets respectively. For the final matche(s), use **f1**
and **f2**.
-   In **match** mode, you don't need to supply any additional arguments.
-   This feature is currently unavailable in **sebracket** mode.

If applicable, you will be asked to input the number of sets won for each
player in the match.

Note that it is not possible to provide results for matches whose players are
not yet ready. It is, however, possible to provide unfinished results for two
or more matches at the same time, as long as none of them depend on each other.

#### list

Use this command to output a list over the currently modified results. This is
helpful if you are experimenting, and have lost track of which matches are
modified, and which are not.
