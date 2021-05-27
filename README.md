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
- `,` : Decrease value of brush (when `MAX_STATE` > 1)
- `.` : Increase value of brush (when `MAX_STATE` > 1)

## Configuration
In the absence of a configuration file / command line arguments (I'm lazy), the environment can be configured through constants found on line `110` onwards.
- The **size of the grid** (in cells) can be configured through `ENV_WIDTH` and `ENV_HEIGHT`
- The list of **conditions** used to determine the new state of cells is set through `CONDITIONS`, and are defined as follows:
    - A list of functions which take integer parameters `n` and `s`, and return an integer
    - `n` is the sum of all neighbour cell states
    - `s` is the current state of the cell
    - The return value is the updated state of the cell
- Usually, cells in the GOL can only have a state of `0` or `1`. Setting the `MAX_STATE` above `1` allows you to **increase** this range. Cell colours are calculated by interpolating between the `ALIVE_COLOUR` and `DEAD_COLOUR`, based on the current state.
- The `START_RULE` allows you to define the **starting state of each cell** based on its x and y values. Currently, this just sets every cell to zero.

- The **size of the window** is set (in pixels) through `WIN_HEIGHT` and `WIN_WIDTH`.
- The **gap** between cells (in pixels) can be set through `CELL_GAP`.

- The background, alive and dead colours can be set through `BG_COLOUR`, `ALIVE_COLOUR` and `DEAD_COLOUR`.

## Contributing
Please feel free to open a pull request if you decide to contribute to my code. I would really appreciate the help!
