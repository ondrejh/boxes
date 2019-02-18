# Boxes

Self solving tetris game writen in python.

## Description:

The project goal is to have tetris game writen in python, where there will be strictly divided the game implementation (creating and moving shapes), solver application (look at the current situation, find solution) and visual.
The visual output should be replaced by hardware "art-like" implemetation in future.

### ToDo:

- add missing game over
- automate playing - use solver results
- improve solver (now its quite spoony)
- add shadow boxes to visualise solver or predict next piece
- improve line deletion

### Files:

    play.py: the tetris game implementation with no visual output.
    solver.py: the solver function
    boxes.py: gui based on pygame
    
    boxes_tkinter (obsolete): gui based on tkinter
