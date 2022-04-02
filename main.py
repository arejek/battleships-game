import pygame
import random

pygame.init()


class Cell:
    def __init__(self, x, y, for_computer):
        self.filled = False
        self.reserved = False
        self.checked = False
        self.has_been_hit = False
        self.x = x
        self.y = y
        self.for_computer = False
        if for_computer:
            self.for_computer = True

    def fill(self):
        if not self.for_computer:
            pygame.draw.rect(gameDisplay, grey, (self.x, self.y, 30, 30))
        self.filled = True

    def unfill(self):
        pygame.draw.rect(gameDisplay, pink, (self.x+2, self.y+2, 30-3, 30-3))
        self.filled = False

    def reserve(self):
        self.reserved = True

    def unreserve(self):
        self.reserved = False

    def make_checked(self):
        self.checked = True

    def hit(self):
        self.has_been_hit = True
        if self.filled:
            pygame.draw.rect(gameDisplay, red, (self.x+5, self.y+5, 30-9, 30-9))
        elif not self.filled:
            pygame.draw.rect(gameDisplay, blue, (self.x + 7, self.y + 7, 30 - 12, 30 - 12))


def reserve_surroundings(col_idx, row_idx, ship_orientation):
    """tries to reserve surrounding, returns a list of reserved cells if it was successful, empty one if not"""
    reserved = []
    no_collision = True

    if ship_orientation == "vertical":
        if col_idx - 1 >= 0:
            if cellsForComputer[col_idx - 1][row_idx].filled is not True:
                if cellsForComputer[col_idx - 1][row_idx].reserved is False:
                    cellsForComputer[col_idx - 1][row_idx].reserve()
                    reserved.append(cellsForComputer[col_idx - 1][row_idx])
            else:
                no_collision = False
        if col_idx + 1 <= 9 and no_collision:
            if cellsForComputer[col_idx + 1][row_idx].filled is not True:
                if cellsForComputer[col_idx + 1][row_idx].reserved is False:
                    cellsForComputer[col_idx + 1][row_idx].reserve()
                    reserved.append(cellsForComputer[col_idx + 1][row_idx])
            else:
                for r in reserved: r.unreserve()
                reserved.clear()
    elif ship_orientation == "horizontal":
        if row_idx - 1 >= 0:
            if cellsForComputer[col_idx][row_idx - 1].filled is not True:
                if cellsForComputer[col_idx][row_idx - 1].reserved is False:
                    cellsForComputer[col_idx][row_idx - 1].reserve()
                    reserved.append(cellsForComputer[col_idx][row_idx - 1])
            else:
                no_collision = False
        if row_idx + 1 <= 9 and no_collision:
            if cellsForComputer[col_idx][row_idx + 1].filled is not True:
                if cellsForComputer[col_idx][row_idx + 1].reserved is False:
                    cellsForComputer[col_idx][row_idx + 1].reserve()
                    reserved.append(cellsForComputer[col_idx][row_idx + 1])
            else:
                for r in reserved: r.unreserve()
                reserved.clear()

    return reserved


def reserve_head_tail_surroundings(col_idx, row_idx, ship_orientation, ship_length):
    """tries to reserve surrounding, returns a list of reserved cells if it was successful, empty one if not"""
    reserved = []
    no_collision = True

    if ship_orientation == "vertical":
        # head
        if row_idx - 1 >= 0:
            if cellsForComputer[col_idx][row_idx - 1].filled is False:
                if cellsForComputer[col_idx][row_idx - 1].reserved is False:
                    cellsForComputer[col_idx][row_idx - 1].reserve()
                    reserved.append(cellsForComputer[col_idx][row_idx - 1])
                if col_idx - 1 >= 0:
                    if cellsForComputer[col_idx - 1][row_idx - 1].reserved is False:
                        cellsForComputer[col_idx - 1][row_idx - 1].reserve()
                        reserved.append(cellsForComputer[col_idx - 1][row_idx - 1])
                if col_idx + 1 <= 9:
                    if cellsForComputer[col_idx + 1][row_idx - 1].reserved is False:
                        cellsForComputer[col_idx + 1][row_idx - 1].reserve()
                        reserved.append(cellsForComputer[col_idx + 1][row_idx - 1])
            else:
                no_collision = False
        # tail
        if row_idx + ship_length <= 9 and no_collision:
            if cellsForComputer[col_idx][row_idx + ship_length].filled is False:
                if cellsForComputer[col_idx][row_idx + ship_length].reserved is False:
                    cellsForComputer[col_idx][row_idx + ship_length].reserve()
                    reserved.append(cellsForComputer[col_idx][row_idx + ship_length])
                if col_idx - 1 >= 0:
                    if cellsForComputer[col_idx - 1][row_idx + ship_length].reserved is False:
                        cellsForComputer[col_idx - 1][row_idx + ship_length].reserve()
                        reserved.append(cellsForComputer[col_idx - 1][row_idx + ship_length])
                if col_idx + 1 <= 9:
                    if cellsForComputer[col_idx + 1][row_idx + ship_length].reserved is False:
                        cellsForComputer[col_idx + 1][row_idx + ship_length].reserve()
                        reserved.append(cellsForComputer[col_idx + 1][row_idx + ship_length])
            else:
                for r in reserved: r.unreserve()
                reserved.clear()
    elif ship_orientation == "horizontal":
        # head
        if col_idx - 1 >= 0:
            if cellsForComputer[col_idx - 1][row_idx].filled is False:
                if cellsForComputer[col_idx - 1][row_idx].reserved is False:
                    cellsForComputer[col_idx - 1][row_idx].reserve()
                    reserved.append(cellsForComputer[col_idx - 1][row_idx])
                if row_idx - 1 >= 0:
                    if cellsForComputer[col_idx - 1][row_idx - 1].reserved is False:
                        cellsForComputer[col_idx - 1][row_idx - 1].reserve()
                        reserved.append(cellsForComputer[col_idx - 1][row_idx - 1])
                if row_idx + 1 <= 9:
                    if cellsForComputer[col_idx - 1][row_idx + 1].reserved is False:
                        cellsForComputer[col_idx - 1][row_idx + 1].reserve()
                        reserved.append(cellsForComputer[col_idx - 1][row_idx + 1])
            else:
                no_collision = False
        # tail
        if col_idx + ship_length <= 9 and no_collision:
            if cellsForComputer[col_idx + ship_length][row_idx].filled is False:
                if cellsForComputer[col_idx + ship_length][row_idx].reserved is False:
                    cellsForComputer[col_idx + ship_length][row_idx].reserve()
                    reserved.append(cellsForComputer[col_idx + ship_length][row_idx])
                if row_idx - 1 >= 0:
                    if cellsForComputer[col_idx + ship_length][row_idx - 1].reserved is False:
                        cellsForComputer[col_idx + ship_length][row_idx - 1].reserve()
                        reserved.append(cellsForComputer[col_idx + ship_length][row_idx - 1])
                if row_idx + 1 <= 9:
                    if cellsForComputer[col_idx + ship_length][row_idx + 1].reserved is False:
                        cellsForComputer[col_idx + ship_length][row_idx + 1].reserve()
                        reserved.append(cellsForComputer[col_idx + ship_length][row_idx + 1])
            else:
                for r in reserved: r.unreserve()
                reserved.clear()

    return reserved


def add_ship_to_computer_board(length):

    orientation = ["horizontal", "vertical"]
    o = random.choice(orientation)

    found_ok_cell = False

    while True:  # searches for not filled and not reserved cell

        r = random.choice(cellsForComputer)
        chosen_cell = random.choice(r)

        while found_ok_cell is False:
            if chosen_cell.reserved is True or chosen_cell.filled is True:
                r = random.choice(cellsForComputer)
                chosen_cell = random.choice(r)
            else:
                found_ok_cell = True

        found_ok_cell = False

        row_idx = r.index(chosen_cell)
        original_row_idx = row_idx

        col_idx = cellsForComputer.index(r)
        original_col_idx = col_idx

        cells_to_be_filled = []
        reserved_cells = []
        problem = False

        if o == "vertical":
            currently_reserving = reserve_surroundings(col_idx, row_idx, "vertical")
            if len(currently_reserving) > 0:
                cells_to_be_filled.append(chosen_cell)
                reserved_cells = reserved_cells + currently_reserving
            else:
                problem = True

            while len(cells_to_be_filled) < length and problem is False:
                if row_idx != 9:
                    currently_reserving = reserve_surroundings(col_idx, row_idx + 1, "vertical")
                    if len(currently_reserving) > 0:
                        cells_to_be_filled.append(r[row_idx + 1])
                        reserved_cells = reserved_cells + currently_reserving
                        row_idx += 1
                    else:
                        problem = True
                else:
                    currently_reserving = reserve_surroundings(col_idx, original_row_idx - 1, "vertical")
                    if len(currently_reserving) > 0:
                        cells_to_be_filled.append(r[original_row_idx - 1])
                        reserved_cells = reserved_cells + currently_reserving
                        original_row_idx -= 1
                    else:
                        problem = True

            if problem is False:
                currently_reserving = reserve_head_tail_surroundings(col_idx, original_row_idx, "vertical", length)
                if len(currently_reserving) > 0:
                    for cf in cells_to_be_filled:
                        cf.fill()
                else:
                    problem = True

            if problem is False:
                break
            elif problem is True:
                for r in reserved_cells:
                    r.unreserve()
                cells_to_be_filled.clear()

        elif o == "horizontal":
            currently_reserving = reserve_surroundings(col_idx, row_idx, "horizontal")
            if len(currently_reserving) > 0:
                cells_to_be_filled.append(chosen_cell)
                reserved_cells = reserved_cells + currently_reserving
            else:
                problem = True

            while len(cells_to_be_filled) < length and problem is False:
                if col_idx != 9:
                    currently_reserving = reserve_surroundings(col_idx + 1, row_idx, "horizontal")
                    if len(currently_reserving) > 0:
                        cells_to_be_filled.append(cellsForComputer[col_idx + 1][row_idx])
                        reserved_cells = reserved_cells + currently_reserving
                        col_idx += 1
                    else:
                        problem = True
                else:
                    currently_reserving = reserve_surroundings(original_col_idx - 1, row_idx, "horizontal")
                    if len(currently_reserving) > 0:
                        cells_to_be_filled.append(cellsForComputer[original_col_idx - 1][row_idx])
                        reserved_cells = reserved_cells + currently_reserving
                        original_col_idx -= 1
                    else:
                        problem = True

            if problem is False:
                currently_reserving = reserve_head_tail_surroundings(original_col_idx, row_idx, "horizontal", length)
                if len(currently_reserving) > 0:
                    for cf in cells_to_be_filled:
                        cf.fill()
                else:
                    problem = True

            if problem is False:
                break
            elif problem is True:
                for r in reserved_cells:
                    r.unreserve()
                cells_to_be_filled.clear()


def check_if_correct_ship(m, n):
    """returns ship's length if everything is correct, 0 otherwise"""
    length = 1
    ship_direction = "none yet"
    for k in range(6):
        if ship_direction == "none yet":
            if m + 1 <= 9 and n + 1 <= 9:  # we are not on board edge
                if n - 1 >= 0:
                    if cellsForUser[m + 1][n - 1].filled:
                        return 0
                if cellsForUser[m + 1][n + 1].filled:
                    return 0
                # ship with branches
                if cellsForUser[m + 1][n].filled and cellsForUser[m][n + 1].filled:
                    return 0
                # horizontal ship
                elif cellsForUser[m + 1][n].filled:
                    cellsForUser[m + 1][n].make_checked()
                    ship_direction = "left"
                    length += 1
                    m += 1
                # vertical ship
                elif cellsForUser[m][n + 1].filled:
                    cellsForUser[m][n + 1].make_checked()
                    ship_direction = "down"
                    length += 1
                    n += 1
            elif m + 1 <= 9 and n + 1 > 9:
                if n - 1 >= 0:
                    if cellsForUser[m + 1][n - 1].filled:
                        return 0
                # horizontal ship
                if cellsForUser[m + 1][n].filled:
                    cellsForUser[m + 1][n].make_checked()
                    ship_direction = "left"
                    length += 1
                    m += 1
                elif not cellsForUser[m + 1][n].filled:
                    return 0
            elif m + 1 > 9 and n + 1 <= 9:
                # vertical ship
                if cellsForUser[m][n + 1].filled:
                    cellsForUser[m][n + 1].make_checked()
                    ship_direction = "down"
                    length += 1
                    n += 1
                elif not cellsForUser[m][n + 1].filled:
                    return 0
            elif m + 1 > 9 and n + 1 > 9:
                return 0
        elif ship_direction == "left":
            if m + 1 <= 9:
                if n - 1 >= 0:
                    if cellsForUser[m + 1][n - 1].filled:
                        return 0
                if n + 1 <= 9:
                    if cellsForUser[m + 1][n + 1].filled:
                        return 0
                if cellsForUser[m + 1][n].filled:
                    cellsForUser[m + 1][n].make_checked()
                    length += 1
                    m += 1
                elif not cellsForUser[m + 1][n].filled:
                    return length
            elif m + 1 > 9:
                return length
        elif ship_direction == "down":
            if n + 1 <= 9:
                if m + 1 <= 9:
                    if cellsForUser[m + 1][n + 1].filled:
                        return 0
                if cellsForUser[m][n + 1].filled:
                    cellsForUser[m][n + 1].make_checked()
                    length += 1
                    n += 1
                elif not cellsForUser[m][n + 1].filled:
                    return length
            elif n + 1 > 9:
                return length

    return length


def check_user_board():
    """checks if everything is correct (number, length and arrangement of ships) returns True or False"""
    correct_ship_lengths = [2, 2, 3, 3, 3, 4, 5]
    actual_ship_lengths = []
    for m in range(len(cellsForUser)):
        for n in range(len(cellsForUser[m])):
            if cellsForUser[m][n].filled is True and cellsForUser[m][n].checked is False:
                current = check_if_correct_ship(m, n)
                if current > 0:
                    actual_ship_lengths.append(current)
                elif current == 0:
                    return False

    actual_ship_lengths.sort()
    is_ok = actual_ship_lengths == correct_ship_lengths

    return is_ok


def check_direction_of_ship(col_idx, row_idx, case):
    if case == "for user":
        left, right, up, down = col_idx - 1, col_idx + 1, row_idx - 1, row_idx + 1
        has_left, has_right, has_up, has_down = left >= 0, right <= 9, up >= 0, down <= 9

        left_right, up_down = [], []

        direction = ""

        if has_left: left_right.append(left)
        if has_right: left_right.append(right)
        if has_up: up_down.append(up)
        if has_down: up_down.append(down)

        if left_right:
            for el in left_right:
                if cellsForComputer[el][row_idx].filled:
                    direction = "left-right"
        if up_down:
            for el in up_down:
                if cellsForComputer[col_idx][el].filled:
                    direction = "up-down"

        return direction

    elif case == "for computer":
        left, right, up, down = col_idx - 1, col_idx + 1, row_idx - 1, row_idx + 1
        has_left, has_right, has_up, has_down = left >= 0, right <= 9, up >= 0, down <= 9

        left_right, up_down = [], []

        direction = ""

        if has_left: left_right.append(left)
        if has_right: left_right.append(right)
        if has_up: up_down.append(up)
        if has_down: up_down.append(down)

        if left_right:
            for el in left_right:
                if cellsForUser[el][row_idx].filled:
                    direction = "left-right"
        if up_down:
            for el in up_down:
                if cellsForUser[col_idx][el].filled:
                    direction = "up-down"

        return direction


def is_sunk(col_idx, row_idx):

    direction = check_direction_of_ship(col_idx, row_idx, "for user")

    original_col_idx = col_idx
    original_row_idx = row_idx

    if direction == "left-right":
        left_checked = False
        while True:
            if col_idx - 1 >= 0 and not left_checked:
                c = cellsForComputer[col_idx - 1][row_idx]
                if c.filled:
                    if c.has_been_hit:
                        col_idx = col_idx - 1
                    elif not c.has_been_hit:
                        return False
                elif not c.filled:
                    col_idx = original_col_idx
                    left_checked = True
            if not col_idx - 1 >= 0:
                col_idx = original_col_idx
                left_checked = True
            if col_idx + 1 <= 9 and left_checked:
                c = cellsForComputer[col_idx + 1][row_idx]
                if c.filled:
                    if c.has_been_hit:
                        col_idx = col_idx + 1
                    elif not c.has_been_hit:
                        return False
                elif not c.filled:
                    return True
            if not col_idx + 1 <= 9:
                return True
    if direction == "up-down":
        up_checked = False
        while True:
            if row_idx - 1 >= 0 and not up_checked:
                c = cellsForComputer[col_idx][row_idx - 1]
                if c.filled:
                    if c.has_been_hit:
                        row_idx = row_idx - 1
                    elif not c.has_been_hit:
                        return False
                elif not c.filled:
                    row_idx = original_row_idx
                    up_checked = True
            if not row_idx - 1 >= 0:
                row_idx = original_row_idx
                up_checked = True
            if row_idx + 1 <= 9 and up_checked:
                c = cellsForComputer[col_idx][row_idx + 1]
                if c.filled:
                    if c.has_been_hit:
                        row_idx = row_idx + 1
                    elif not c.has_been_hit:
                        return False
                elif not c.filled:
                    return True
            if not row_idx + 1 <= 9:
                return True


def sink_after_get(col_idx, row_idx):

    direction = check_direction_of_ship(col_idx, row_idx, "for computer")

    left, right, up, down = col_idx - 1, col_idx + 1, row_idx - 1, row_idx + 1

    left_done, right_done, up_done, down_done = False, False, False, False

    if direction == "left-right":
        while left_done is False:
            if left >= 0:
                c = cellsForUser[left][row_idx]
                if c.filled:
                    c.hit()
                    left = left - 1
                elif not c.filled:
                    left_done = True
            elif not left >= 0:
                left_done = True
        while right_done is False:
            if right <= 9:
                c = cellsForUser[right][row_idx]
                if c.filled:
                    c.hit()
                    right = right + 1
                elif not c.filled:
                    right_done = True
            elif not right <= 9:
                right_done = True
    elif direction == "up-down":
        while up_done is False:
            if up >= 0:
                c = cellsForUser[col_idx][up]
                if c.filled:
                    c.hit()
                    up = up - 1
                elif not c.filled:
                    up_done = True
            elif not up >= 0:
                up_done = True
        while down_done is False:
            if down <= 9:
                c = cellsForUser[col_idx][down]
                if c.filled:
                    c.hit()
                    down = down + 1
                elif not c.filled:
                    down_done = True
            elif not down <= 9:
                down_done = True


def computer_takes_random_hit():
    # search for a cell with False has_been_hit
    found_cell = False
    r = random.choice(cellsForUser)
    chosen_cell = random.choice(r)

    col_idx = cellsForUser.index(r)
    row_idx = r.index(chosen_cell)

    while found_cell is False:
        if not chosen_cell.has_been_hit:
            chosen_cell.hit()
            found_cell = True
        elif chosen_cell.has_been_hit:
            r = random.choice(cellsForUser)
            chosen_cell = random.choice(r)
            col_idx = cellsForUser.index(r)
            row_idx = r.index(chosen_cell)

    if chosen_cell.filled:
        sink_after_get(col_idx, row_idx)
        return "hit"
    elif not chosen_cell.filled:
        return "miss"


def print_win():
    pygame.draw.rect(gameDisplay, green, playButton)
    font = pygame.font.SysFont(None, 55)
    text = font.render('You won!', True, green, None)
    gameDisplay.blit(text, (instructX + 100, instructY + 45 + 25 * 10 + 35 + 35))


def print_loose():
    pygame.draw.rect(gameDisplay, green, playButton)
    font = pygame.font.SysFont(None, 55)
    text = font.render('You lost :(', True, red, None)
    gameDisplay.blit(text, (instructX + 100, instructY + 45 + 25 * 10 + 35 + 35))


# --- lists of cells for boards ---
cellsForComputer, cellsForUser = [], []
y = 50

for i in range(10):
    rowC, rowU = [], []
    c = 20
    u = 350
    for j in range(10):
        rowC.append(Cell(y, c, True))
        rowU.append(Cell(y, u, False))
        c += 30
        u += 30
    cellsForComputer.append(rowC)
    cellsForUser.append(rowU)
    y += 30

# --- graphics of the game ---
pink = (255, 182, 193)
grey = (132, 132, 132)
grey_for_text = (102, 102, 102)
green = (0, 200, 0)
red = (255, 100, 100)
blue = (0, 0, 255)

windowHeight = 670
windowWidth = 850

gameDisplay = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption('Battleships Game')

image = pygame.image.load(r'E:/battleships.jpg')
image = pygame.transform.scale(image, (windowWidth, windowHeight))
center = ((windowWidth - image.get_width()) / 2, (windowHeight - image.get_height()) / 2)
gameDisplay.blit(image, center)

x_boardPos = 50
y_boardPosUpper = 20
y_boardPosLower = 350

gapBtwBoards = 30

computerBoard = pygame.Rect(x_boardPos, y_boardPosUpper, 300, 300)
userBoard = pygame.Rect(x_boardPos, y_boardPosLower, 300, 300)

pygame.draw.rect(gameDisplay, pink, computerBoard)
pygame.draw.rect(gameDisplay, pink, userBoard)

# - draws grid -
a = x_boardPos
for i in range(11):
    pygame.draw.line(gameDisplay, grey, (a, y_boardPosUpper), (a, y_boardPosUpper + 300), 3)
    pygame.draw.line(gameDisplay, grey, (a, y_boardPosLower), (a, y_boardPosLower + 300), 3)
    a += 30
a = y_boardPosUpper
for i in range(11):
    pygame.draw.line(gameDisplay, grey, (x_boardPos, a), (x_boardPos + 300, a), 3)
    pygame.draw.line(gameDisplay, grey, (x_boardPos, a+300+gapBtwBoards), (x_boardPos + 300, a+300+gapBtwBoards), 3)
    a += 30

# - play button -
pbWidth = 100
pbHeight = 50

pbX = x_boardPos + 350
pbY = y_boardPosLower + 250

playButton = pygame.Rect(pbX, pbY, pbWidth, pbHeight)

pygame.draw.rect(gameDisplay, pink, playButton)

pygame.draw.line(gameDisplay, grey, (pbX, pbY), (pbX + pbWidth, pbY), 3)
pygame.draw.line(gameDisplay, grey, (pbX + pbWidth, pbY), (pbX + pbWidth, pbY + pbHeight), 3)
pygame.draw.line(gameDisplay, grey, (pbX + pbWidth, pbY + pbHeight), (pbX, pbY + pbHeight), 3)
pygame.draw.line(gameDisplay, grey, (pbX, pbY), (pbX, pbY + pbHeight), 3)

# - instruction -
instructX = x_boardPos + 300 + 100
instructY = y_boardPosUpper + 100

instructWidth = 370
instructHeight = 400

shipsInstruction = pygame.Rect(instructX, instructY, instructWidth, instructHeight)

pygame.draw.rect(gameDisplay, pink, shipsInstruction)

# - frame -
pygame.draw.line(gameDisplay, grey, (instructX, instructY), (instructX, instructY + instructHeight), 3)
pygame.draw.line(gameDisplay, grey, (instructX, instructY), (instructX + instructWidth, instructY), 3)
pygame.draw.line(gameDisplay, grey, (instructX, instructY + instructHeight),
                 (instructX + instructWidth, instructY + instructHeight), 3)
pygame.draw.line(gameDisplay, grey, (instructX + instructWidth, instructY),
                 (instructX + instructWidth, instructY + instructHeight), 3)

font = pygame.font.SysFont(None, 30)
text = font.render('Rules', True, grey_for_text, None)
textRect = text.get_rect()
textRect.center = shipsInstruction.center
gameDisplay.blit(text, (instructX + 20, instructY + 15))

font = pygame.font.SysFont(None, 35)
text = font.render('Play', True, grey_for_text, None)
textRect = text.get_rect()
textRect.center = playButton.center
gameDisplay.blit(text, textRect)

rule1 = "The lower board is Yours. "
font2 = pygame.font.SysFont(None, 25)
text2 = font2.render(rule1, True, grey_for_text, None)
gameDisplay.blit(text2, (instructX + 10, instructY + 45))

rule1 = "Select location of Your ships by clicking."
text2 = font2.render(rule1, True, grey_for_text, None)
gameDisplay.blit(text2, (instructX + 10, instructY + 45 + 25))

rule1 = "They cannot touch in any way"
text2 = font2.render(rule1, True, grey_for_text, None)
gameDisplay.blit(text2, (instructX + 10, instructY + 45 + 25 * 2))

rule1 = "and have to be of lengths:"
text2 = font2.render(rule1, True, grey_for_text, None)
gameDisplay.blit(text2, (instructX + 10, instructY + 45 + 25 * 3))

rule1 = "  1x 5,   1x 4,   3x 3,   2x 2"
text2 = font2.render(rule1, True, grey_for_text, None)
gameDisplay.blit(text2, (instructX + 10, instructY + 45 + 25 * 4))

rule1 = "(Otherwise the game wont start)"
text2 = font2.render(rule1, True, grey_for_text, None)
gameDisplay.blit(text2, (instructX + 10, instructY + 45 + 25 * 5))

rule1 = "The computer has less ships (one of each),"
text2 = font2.render(rule1, True, grey_for_text, None)
gameDisplay.blit(text2, (instructX + 10, instructY + 45 + 25 * 6))

rule1 = "but if It hits Your ship, the ship sinks."
text2 = font2.render(rule1, True, grey_for_text, None)
gameDisplay.blit(text2, (instructX + 10, instructY + 45 + 25 * 7))

rule1 = "The counter raises when You sink a ship."
text2 = font2.render(rule1, True, grey_for_text, None)
gameDisplay.blit(text2, (instructX + 10, instructY + 45 + 25 * 8))

rule1 = "Red is hit, Blue is miss. Good luck!"
text2 = font2.render(rule1, True, grey_for_text, None)
gameDisplay.blit(text2, (instructX + 10, instructY + 45 + 25 * 9))

counter = 0
counter_string = str(counter)
font2 = pygame.font.SysFont(None, 45)
counter_text = font2.render("Counter: " + counter_string, True, grey_for_text, None)
gameDisplay.blit(counter_text, (instructX + 20, instructY + 45 + 25 * 10 + 35))

# --- preparation for game ---
add_ship_to_computer_board(5)
add_ship_to_computer_board(4)
add_ship_to_computer_board(3)
add_ship_to_computer_board(2)

computersTurn = False
usersTurn = True

gameFinished = False
nowPlaying = False

sinking_users_ships = 0

while True:  # --- game loop ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                if computerBoard.collidepoint(pos) and nowPlaying and usersTurn and not gameFinished:
                    col_idx = (pos[0] - 50) // 30
                    row_idx = (pos[1] - 20) // 30
                    c = cellsForComputer[col_idx][row_idx]
                    c.hit()
                    if c.filled:
                        if is_sunk(col_idx, row_idx):
                            pygame.draw.rect(gameDisplay, pink, (instructX + 10, instructY + 35 * 10 - 20, 250, 60))
                            counter = counter + 1
                            counter_string = str(counter)
                            font2 = pygame.font.SysFont(None, 45)
                            counter_text = font2.render("Counter: " + counter_string, True, grey_for_text, None)
                            gameDisplay.blit(counter_text, (instructX + 20, instructY + 45 + 25 * 10 + 35))
                            if counter == 4:
                                print_win()
                                gameFinished = True
                    usersTurn = False
                    computers_move = computer_takes_random_hit()
                    if computers_move == "hit":
                        sinking_users_ships = sinking_users_ships + 1
                    if sinking_users_ships == 7:
                        print_loose()
                        gameFinished = True
                    usersTurn = True
                if userBoard.collidepoint(pos) and not nowPlaying:
                    c = cellsForUser[(pos[0] - 50) // 30][(pos[1] - 350) // 30]
                    if c.filled:
                        c.unfill()
                    else:
                        c.fill()
                if playButton.collidepoint(pos):
                    if check_user_board():
                        pygame.draw.rect(gameDisplay, green, playButton)
                        font = pygame.font.SysFont(None, 30)
                        text = font.render('Playing', True, grey_for_text, None)
                        textRect = text.get_rect()
                        textRect.center = playButton.center
                        gameDisplay.blit(text, textRect)

                        nowPlaying = True

    pygame.display.update()
