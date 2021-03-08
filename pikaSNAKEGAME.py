# SNAKE GAME
# Use ARROW KEYS to play, SPACE BAR for pausing/resuming and Esc Key for exiting
import curses
import random

def game():                                          #set def to call the game for a replay.
    s = curses.initscr()                             #Initialize curses and return window.
    curses.curs_set(0)                               #Hide the curser.
    curses.noecho()                                  #Only display certain keys.
    sh, sw = s.getmaxyx()                            #Set values for the max height and max width of the screen.
    w = curses.newwin(sh, sw, 0, 0)                  #Creates a new window of a given size.
    w.nodelay(1)                                     #To not wait for the user to a key.
    w.border(0)                                      #Set a border.
    w.keypad(1)                                      #To accsept keys from the new window

    score = 0                                        #Set a score varisble.
    key = curses.KEY_RIGHT                           #Set inatial key.

    snk_y = sh//2                                    #Set snake initial co-ordinates.
    snk_x = sw//4
    snake = [
        [snk_y, snk_x],
        [snk_y, snk_x-1],
        [snk_y, snk_x-2]
    ]

    food = [sh//2, sw//2]                            #Set first food co-ordinates and how it looks.
    w.addch(food[0], food[1], '*')

    while key != 27:                                     #while Esc key is not pressed.
        w.border(0)
        w.addstr(0, 2, "Score: " + str(score) + " ")     #Printing "score" and
        w.addstr(0, 27, "Snake - for Pika & Gado, try to reach score '25'")                         #"Snake" on the border .
        w.timeout(150 - (len(snake)//5 + len(snake)//10)%120)#Increasing the speed of Snake as its lingtg increases.

        prevkey = key                                    #Previous key.
        nextkey = w.getch()                              #Refreshes the screen and waits for user next key.
        key = key if nextkey == -1 else nextkey           #If no key is pressed continue on the previous key.

        if key == ord(' '):                              #If space bar is pressed, wait for another
            key = -1                                     #one (Pause/Resume).
            while key != ord(' '):
                key = w.getch()
            key = prevkey
            continue

        if key not in [curses.KEY_RIGHT, curses.KEY_LEFT, curses.KEY_DOWN, curses.KEY_UP, 27]:
            key = prevkey                                   #If invalid key is pressed continue on the previous key.

        new_head = [snake[0][0], snake[0][1]]               #Adding a new head at the direction of the pressed arrow.
        if key == curses.KEY_RIGHT:
            new_head[1] += 1
        if key == curses.KEY_LEFT:
            new_head[1] -= 1
        if key == curses.KEY_UP:
            new_head[0] -= 1
        if key == curses.KEY_DOWN:
            new_head[0] += 1
        snake.insert(0, new_head)

        if snake[0] in snake[1:]: break                    #Lose if snake bitten itself.
        # if snake[0][0] in [0, sh] or snake[0][1] in [0, sw]: break #Lose if snake run into the border.

        if snake[0][0] == 0: snake[0][0] = sh -2           #If snake run into the border return from the other side.
        if snake[0][0] == sh-1: snake[0][0] =  1
        if snake[0][1] == 0: snake[0][1] =  sw-2
        if snake[0][1] == sw-1: snake[0][1] =  1


        if snake[0] == food:                              #When snake eats food.
            food = None
            score += 1
            while food is None:
                nf = [
                    random.randint(2, sh-2),            #New food location.
                    random.randint(2, sw-2)
                ]
                food = nf if nf not in snake else None
            w.addch(food[0], food[1], "*")
        else:
            tail = snake.pop()                            #When does not eat food.
            w.addch(tail[0], tail[1], " ")
        w.addch(snake[0][0], snake[0][1], "o")            #Add snake and its looks.
    curses.endwin()
    print("\nScore: "+ str(score))
    if score <= 10 and key != 27:
        print("Noob :) You lost when Snake is so short lol\n")
    elif 11 <= score <= 24:
        print('Good you are starting to get the hang of this\n')
    elif score >= 25:
        print("Amaizing you are pro in this game :)\n")


while True:
    game()
    restart = input("If you want to play again, type again: ")
    if restart.lower() != "again": break
