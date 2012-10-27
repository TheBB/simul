simul
=====

Simulator for various tournament formants, intended for Starcraft.

Supports the following tournament formats:
-   Round robin with customisable tiebreakers
-   MSL-style four player groups
-   Singe best of N matches
-   Single elimination brackets

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

Gives the tournament format to simulate. There are currently four choices:
-   *match*
