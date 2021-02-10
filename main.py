import pygame
from pygame.color import Color
from pygame.display import update
from pygame.locals import *
from math import floor

class Cell:
    def __init__(self, x, y, max_state, start_state, conditions, count_indirect_neighbours):

        self.x = x
        self.y = y
        self.state = start_state
        self.state_buffer = start_state # Store state while environment is updating

        self.max_state = max_state # Maximum value of state
        self.conditions = conditions # Conditions which dictate how state is updated
        self.count_indirect_neighbours = count_indirect_neighbours # cell can see diagonal neighbours
    
    # Get state of cell at <x, y> on grid, or return 0 if invalid
    def getNeigbourState(self, grid, x, y):
        if x >= 0 and x < len(grid) and y >= 0 and y < len(grid[0]):
            return grid[x][y].state
        else:
            return 0

    # Get sum of neighbour states (direct)
    def getNeighboursDirect(self, grid):
        x = self.x
        y = self.y
        return sum([
            self.getNeigbourState(grid, n[0], n[1])
            for n in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
            ])

    # Get sum of neighbour states (direct + diagonal)
    def getNeighboursIndirect(self, grid):
        x = self.x
        y = self.y
        neighbours = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if not(i == 0 and j == 0):
                    neighbours.append(self.getNeigbourState(grid, x+i, y+j))
        return sum(neighbours)

    # Set state of cell
    def setState(self, new_state):
        self.state = new_state
        self.state_buffer = new_state
    
    # Get neighbours, run conditions and store state in state_buffer
    def determineState(self, grid):
        if self.count_indirect_neighbours:
            neighbours = self.getNeighboursIndirect(grid)
        else:
            neighbours = self.getNeighboursDirect(grid)

        for condition in self.conditions:
            self.state_buffer = max(min(condition(neighbours, self.state_buffer), self.max_state), 0)
    
    # Set state to value of state_buffer
    def updateState(self):
        self.state = self.state_buffer

class Environment:
    def __init__(self, width, height, max_state, start_rule, conditions, count_indirect_neighbours):
        self.grid = []

        # Populate grid
        for i in range(width):
            row = []
            for j in range(height):
                row.append(Cell(
                        i, j, 
                        max_state,
                        start_rule(i, j),
                        conditions,
                        count_indirect_neighbours
                ))
            self.grid.append(row)
    
    # Set state of cell at <x, y>
    def setCellState(self, x, y, new_state):
        self.grid[x][y].setState(new_state)
    
    # Determine state of every cell then update all cells
    def updateEnvironment(self):
        for row in self.grid:
            for cell in row:
                cell.determineState(self.grid)
        for row in self.grid:
            for cell in row:
                cell.updateState()
    
    # Output environment to terminal
    def outputEnvironment(self):
        print("@ "*(self.width+2))
        for row in self.grid:
            print("@ ", end="")
            for cell in row:
                if cell.state > 0:
                    print(cell.state, end=" ")
                else:
                    print(" ", end=" ")
            
            print("@")
        print("@ "*(self.width+2))


## CONSTANTS

# Environment configuration
ENV_WIDTH, ENV_HEIGHT = 100, 100

# Experimental rules
# CONDITIONS = (
#     lambda n, s: s-1 if n < 4 or n > 9 else s,
#     lambda n, s: s+1 if n==7 else s
# )
# MAX_STATE = 11
# START_RULE = lambda x, y: 0 

# Original Conway's GOL rules
CONDITIONS = (
    lambda n, s: False if n < 2 or n > 3 else s,
    lambda n, s: True if n==3 else s
)
MAX_STATE = 1
START_RULE = lambda x, y: False
COUNT_INDIRECT_NEIGHBOURS = True

# GUI configuration
WIN_WIDTH, WIN_HEIGHT = 1000, 1000
CELL_GAP = 2

# Colours on screen
BG_COLOUR = Color(0, 0, 0)
ALIVE_COLOUR = Color(240, 0, 120)
DEAD_COLOUR = Color(30, 30, 30)


# Instantiate environment
env = Environment(ENV_WIDTH, ENV_HEIGHT, MAX_STATE, START_RULE, CONDITIONS, COUNT_INDIRECT_NEIGHBOURS)

# Calculate cell sizes
cell_width = floor(WIN_WIDTH / ENV_WIDTH)
cell_height = floor(WIN_HEIGHT / ENV_HEIGHT)

# Initialise pygame
pygame.init()
screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Conway's Game of Life")

# Render multi-line text in Pygame (not my function)
def blit_text(surface, text, pos, font, color=pygame.Color('black')):
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.

# Main loop
def main():
    loops_since_update = 0
    update_duration = 4
    auto_update = False
    mouse_draw_state = MAX_STATE

    pygame.time.delay(round(60/1000))
    while True:

        if auto_update:
            if loops_since_update > update_duration:
                env.updateEnvironment() 
                loops_since_update = 0
            else:
                loops_since_update += 1

        for event in pygame.event.get():
            # Quit event
            if event.type == QUIT:
                pygame.quit()
                return
            # Update the environment on space key
            # Toggle auto_update on forward slash key
            elif event.type == KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE]:
                    env.updateEnvironment() 
                if keys[pygame.K_SLASH]:
                    auto_update = not auto_update
                if keys[pygame.K_LEFTBRACKET]:
                    update_duration = max(int(update_duration/2), 1)
                if keys[pygame.K_RIGHTBRACKET]:
                    update_duration = min(update_duration*2, 64)
                if keys[pygame.K_COMMA]:
                    mouse_draw_state = max(mouse_draw_state-1, 1)
                if keys[pygame.K_PERIOD]:
                    mouse_draw_state = min(mouse_draw_state+1, MAX_STATE)

        # LMB: draw | RMB: erase
        lmb, _, rmb = pygame.mouse.get_pressed()
        if lmb or rmb:
            # Calculate which cell user is hovering over
            mouse_x, mouse_y = pygame.mouse.get_pos()
            cell_x = floor(mouse_x / cell_width)
            cell_y = floor(mouse_y / cell_height)
            # Set clicked cell's state 
            if lmb:
                env.setCellState(cell_x, cell_y, mouse_draw_state)
            else:
                env.setCellState(cell_x, cell_y, 0)
        
        # Draw display
        screen.fill(BG_COLOUR)
        for i, row in enumerate(env.grid):
            for j, cell in enumerate(row):
                # Interpolate between alive and dead colour based on the cell state
                colour = DEAD_COLOUR.lerp(ALIVE_COLOUR, cell.state/MAX_STATE)
                # Draw cell
                pygame.draw.rect(screen, colour, pygame.Rect(
                    i*cell_width, 
                    j*cell_height, 
                    cell_width - CELL_GAP, 
                    cell_height - CELL_GAP
                ))

        # Write text information
        information = (
            f"MAX STATE: {MAX_STATE}\n"
            f"COUNT INDIRECT NEIGHBOURS: {COUNT_INDIRECT_NEIGHBOURS}\n"
            f"UPDATE DURATION: {update_duration}\n"
            f"LOOPS SINCE UPDATE: {loops_since_update}\n"
            f"MOUSE DRAW STATE: {mouse_draw_state}\n"
        )
        font = pygame.font.SysFont(None, 24)
        blit_text(screen, information, (20, 20), font, color=Color("white"))


        # Update display
        pygame.display.flip()

main()

