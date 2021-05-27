# Conway's Game of Life "Extended"
Conway's Game of Life with some extended / customisable functionality.
**Requires pygame to be installed.**

## Keybinds
- `LMB` : Draw cells on canvas
- `RMB` : Erase cells from canvas
- `[Space]` : Advance one step forward in time
- `/` : Play or pause the simulation
- `[` : Decrease time between updates 
- `]` : Increase time between updates
- `,` : Decrease value of brush (when `max_state` > 1)
- `.` : Increase value of brush (when `max_state` > 1)

## Configuration
The file `config.py` can be modified in order to configure the simulation.

### Rulesets
Rulesets define the behaviour of cells within the environment. 
- `conditions`: The list of **conditions** used to determine the new state of cells. Defined as follows:
    - A list of functions which take integer parameters `n` and `s`, and return an integer
    - `n` is the sum of all neighbour cell states
    - `s` is the current state of the cell
    - The return value is the updated state of the cell
    - *On every update, the current state of the cell will be passed through each condition in turn, so every condition will affect the cell at the same time. If you don't want a condition to change the state of a cell, simply `return s` to leave it unchanged.*
- `max_state`: The highest state value a cell can have. Usually, cells in the GOL can only have a state of `0` or `1`. Setting the `max_state` above `1` allows you to **increase** this range. Cell colours are calculated by interpolating between the `alive_colour` and `dead_colour`, based on the current state.
- `start_rule`: Allows you to define the **starting state of each cell** based on its x and y values. In most cases, you're best off just setting every cell to zero (blank canvas).
- `count_indirect_neighbours`: If true, cells diagonally adjacent to any given cell will be considered its "neighbours". If false, only the four directly adjacent cells will be considered.

### Main Config
- `behaviour`: The ruleset you want to apply to the environment.
- `env_width`, `env_width`: The width/height of the grid, in cells.
- `win_width`, `win_height`: The width/height of the window, in pixels.
- `cell_gap`: The gap between cells, in pixels.
- **Colours:**
    - `bg_colour`: The colour of the background behind cells. 
    - `alive_colour`: The colour of any cell at `max_state`.
    - `dead_colour`: The colour of a cell at state `0`.
        - *Colour values are interpolated between `alive_colour` and `dead_colour` for any state value that isn't `0` or `max_state`.*

## Contributing
Please feel free to open a pull request if you decide to contribute to my code. I would really appreciate the help!
