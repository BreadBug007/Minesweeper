class Cell:
    def __init__(self, x, y, w):
        self.x = x
        self.y = y
        self.visible = False
        self.mine = False
        self.mine_count = 0
        self.neighbours = []
        self.clicked = False
        self.flag = False
        
    def show(self):
        if not self.clicked:
            stroke(255)
            fill(50, 50, 50)
            rect(self.x * w, self.y * w, w, w)
            if self.visible:
                if self.mine:
                    fill(150, 100, 200)
                    rect(self.x * w, self.y * w, w, w)
                    fill(255, 0, 0)
                    circle(self.x*w + w/2, self.y*w + w/2, w/2)
                    self.clicked = True
                else:
                    stroke(100, 100, 100)
                    fill(100, 100, 100)
                    rect(self.x * w, self.y * w, w, w)
                    if self.mine_count != 0:
                        textSize(w/2)
                        if self.mine_count == 1:
                            fill(0, 0, 255)
                        if self.mine_count == 2:
                            fill(0, 255, 0)
                        if self.mine_count == 3:
                            fill(255, 0, 0)
                        if self.mine_count > 3:
                            fill(255, 127, 0)
                        text("{}".format(self.mine_count), self.x * w + w/3, self.y * w + 2*w/3)
                        self.clicked = True




    def find_value(self, grid):
        if self.mine:
            return []
        i = self.x
        j = self.y
        for l in range(i-1, i+2):
            for m in range(j-1, j+2):
                if -1 < l < cols and -1 < m < rows:
                    if l != i or m != j:
                        self.neighbours.append(grid[index(l, m)])

stack = []

def flood_fill(cell):
    global stack
    for cell in cell.neighbours:
        cell.visible = True
        cell.show()
        if cell.mine_count == 0 and not cell.mine and cell not in stack:
            stack.append(cell)
            flood_fill(cell)
            
            
def index(x, y):
    if x < 0 or y < 0 or x > cols - 1 or y > rows - 1:
        return -1
    return x + y * cols
 

grid = []

def setup():
    
    global w, grid, cols, rows, num_bombs
    size(800, 800)
    background(0)
    w = 40
    cols, rows = width/w, height/w

    for j in range(rows):
        for i in range(cols):
            cell = Cell(i, j, w)
            grid.append(cell)
    
    num_bombs = 0
    for i in range(50):
        num_bombs += 1    
        bomb = index(int(random(cols)), int(random(rows)))
        grid[bomb].mine = True
    
    for j in range(rows):
        for i in range(cols):
            grid[index(i, j)].find_value(grid)
            for cell in grid[index(i, j)].neighbours:
                if cell.mine:
                    grid[index(i, j)].mine_count += 1
    
    for cell in grid:
        fill(40, 40, 40)
        cell.show()

def draw():

    value = 0
    for cell in grid:
        if not cell.mine and cell.visible:
            value += 1
            if value == len(grid) - num_bombs:
                textSize(120)
                fill(0, 255, 0)
                text("Victory", 0, height/3, width, height)
    if mousePressed and mouseButton == LEFT:
        x = int(mouseX/w)
        y = int(mouseY/w)
        cell = grid[index(x, y)]
        
        cell.visible = True
        cell.show()
        
        if cell.mine_count == 0:
            flood_fill(cell)
        
        if cell.mine:
            for row in range(rows):
                for col in range(cols):
                    if grid[index(col, row)].mine:
                        grid[index(col, row)].visible = True
                        grid[index(col, row)].show()
                        textSize(120)
                        fill(40, 240, 100)
                        text("Game Over", 0, height/3, width, height)
            noLoop()
            return
    for row in range(rows):
        for col in range(cols):
            grid[index(col, row)].show()

        

    # if mouseButton == RIGHT:
    #     x = int(mouseX/w)
    #     y = int(mouseY/w)
    #     cell = grid[index(x, y)]
    #     if not cell.visible:
    #         fill(0)
    #         circle(cell.x*w + w/2, cell.y*w + w/2, w/2) 




        
        
        
