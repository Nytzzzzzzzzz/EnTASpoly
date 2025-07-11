# EnTASpoly

CLI tool to record, edit, save, and play input sequences back.

Could theoratically be used for other games compatible with x360 controllers but its main purpose is to be used in the game entropoly, thus the repo name.

# Setup

```
pip install vgamepad
```

# Launching

```
py tas_main.py
```

# Commands

## Playback commands

- ### **run** [length] [pause]
Plays the loaded input sequence

Notes:
- This command automatically pauses and restarts the level
- [length] is -1 by default, which plays the whole input sequence
- [pause] is 0 by default, which does not pause the game after playback

*Examples*:
```
run
run 100 0
run -10 1
```

- ### **run_debug** [length]
Plays the loaded input sequence in debug mode

Notes:
- This command automatically pauses and restarts the level
- [length] is -1 by default, which plays the whole input sequence

*Examples*:
```
run_debug
run_debug 75
run_debug -30
```

## File editing commands

- ### **save**
Saves the input sequence in the loaded file

- ### **load** [filepath]
Loads the input sequence of a file

Notes:
- Extensions will always be ``.tas`` no matter what, so you don't need to type it out every time

*Examples*:
```
load earth_2
load tases/fire_1
```

## Input editing commands

- ### **load_inputs** [input_sequence]
Loads an input sequence

Here is a chart of what character maps to what input:
```
u: up
d: down
l: left
r: right
a: normal
b: dash/special
y: jump
s: brake/airdodge
n: no input (don't use alongside other characters)
```

Notes:
- Frames are separated using ``;``
- ``u``/``d``+``l``/``r`` yield diagonal inputs
- Ordering your inputs from top to bottom according to the chart is preferred for consistency, but not required as the ``save`` command automatically does so to read inputs consistently

*Examples*:
```
load_inputs dr;r;r;rs;n;n;n;n;n;n;n;n;n;b;n;n;n;ry;r;r;s (spawn ff waveland -> waveshine)
load_inputs dr;r;r;rs;n;n;n;n;n;n;n;n;n;r;r;ry;r;r;r;rb;r;r;r;r;dr;ry (spawn ff waveland -> boostdash)
```

- ### **add** [input]
Adds an input at the end of the input sequence

*Examples*:
```
add n
add dr
add ry
```

- ### **insert** [index] [input]
Inserts an input at an index

*Examples*:
```
insert 67 rb
insert -2 y
```

- ### **replace** [index] [input]
Replaces an input at an index

*Examples*:
```
replace 10 r
replace -50 ub
```

- ### **delete** [index]
Deletes an input at an index

*Examples*:
```
delete 50
delete -10
```

- ### **record** [overwrite]
Records an input sequence

Notes:
- This command is only meant to be used while in debug mode, in frame advance mode, using the keyboard to record inputs
- This command only accepts the following inputs:
```
up arrow: right
down arrow: right
left arrow: right
right arrow: right
a: normal
b: dash/special
y: jump
s: brake/airdodge
f: frame advance
```
- [overwrite] is 0 by default, which does not overwrite the current loaded inputs, but rather extends it

*Examples*:
```
record
record 0 (effectively no different than record)
record 1
```

- ### **print**
Prints the loaded input sequence

*Examples*:
```
>>> print
>>> dr;r;r;rs;n;n;n;n;n;n;n;n;n;b;n;n;n;ry;r;r;rs (spawn ff waveland -> waveshine)
```
insider knowledge this command is so useful

# Other

I included ``test_delay.tas`` as a 2-minute long control for how much delay your machine may add. I recommend running it to see when it starts desyncing, since it might be different for every machine.

Feel free to edit the code to your preference, or reach out to me on discord if you have ideas to improve on this or run into issues. It's pretty barebones for now (cli lol) and i have some ideas of things to add, but maybe you have some too.
