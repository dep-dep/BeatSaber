# Assigmnet 4 is more challenging compared to other however and more fun to get right, this assignment deals with
# having two keys simultaneously to the game this allows us to always keep in mind what functions deals with which keys
# pressed. This assignment helps us use files, reading, writing and creating to allow us to have "saved" data, so we
# don't have to keep inputing the values. This also allows up to edit and rearrange the files in order to keep us
# updated. This assignment also allows us to input values before the game starts to get the date to run the game
# (meaning using the sys.argv values) this allows us to get information, so we don't have to ask or intrupt in the
# middle of the game

# import
from SimpleGame.simplegame import *
import sys

# Template
# python CPSC217W24A4-HarderickDhillon.py dep cake by the ocean Easy

# GLOBAL VARABLES
BEAT_DIRECTIONS = ['up', 'down', 'left', 'right']
WASD_DIRECTIONS = ['w', 'a', 's', 'd']
VISIBLE = 'visible'
SPEED = 5  # DO NOT CHANGE
generation_speed = 0.6

# variables that changes
frame_counter = 0
gameStart_Frame_Counter = 0
score = 0
displayScore = 0

game_ended = False
game_started = False

# dictionary that gets added
startScreenElements = {}
playScreenElements = {}
endScreenElements = {}

# list that gets added
displayTopTen = []
beatRightList = []
beatLeftList = []

# to get the information including Name song and difficulty
if len(sys.argv) > 4:
    playerName = str(sys.argv[1])
    songName = f"{(sys.argv[2])} {(sys.argv[3])} {(sys.argv[4])} {(sys.argv[5])}"
    difficulty = str(sys.argv[6])
else:
    playerName = "dep" #str(sys.argv[0])
    songName = "cake by the ocean" #str(sys.argv[1])
    difficulty = "Expert"#str(sys.argv[2])


# Start screen setup
def start_screen_setup():
    startScreenElements['ready'] = create_element('text-ready', (WIDTH / 2, HEIGHT / 2 - 100))
    startScreenElements['space'] = create_element('space-bar', (WIDTH / 2, HEIGHT / 2 + 50))
    startScreenElements['tap'] = create_element('tap-active', (WIDTH / 2 + 70, HEIGHT / 2 + 50))
    startScreenElements['tap'][VISIBLE] = True
    schedule_callback_every(toggle_tap, .5)


# End screen setup
def end_screen_setup():
    global game_ended
    game_ended = True
    endScreenElements['timeup'] = create_element('text-timeup', (WIDTH / 2, HEIGHT / 2))
    endScreenElements['timeup'][VISIBLE] = True
    schedule_callback_after(hide_timeup, 1)


# Game screen setup
def game_screen_setup():
    global game_started
    game_started = True
    cancel_callback_schedule(toggle_tap)
    playScreenElements['score'] = create_element('star2', (30, 30))
    playScreenElements['keyboard'] = create_element('keyboard_arrows', ((2 * WIDTH) / 3 + 25, HEIGHT - 50))
    playScreenElements['keyboard']['base'] = 'keyboard_arrows_'
    playScreenElements["wasd"] = create_element("keyboard_", (WIDTH / 3 - 25, HEIGHT - 50))
    playScreenElements["wasd"]['base'] = 'keyboard_'
    playScreenElements['go'] = create_element('text-go', (WIDTH / 2, HEIGHT / 2))
    playScreenElements['go'][VISIBLE] = True
    schedule_callback_after(hide_go, .5)


# hide the elements
def hide_go():
    playScreenElements['go'][VISIBLE] = False


# hide the time up screen
def hide_timeup():
    endScreenElements['timeup'][VISIBLE] = False


# toggle taps
def toggle_tap():
    startScreenElements['tap'][VISIBLE] = not startScreenElements['tap'][VISIBLE]


# draw functions
def draw():
    """
    - Called automatically everytime there's a change in the screen
    - Do not include any operations other than drawing inside this function.
    - The only allowed statements/functions are the ones that have draw_ in the name like
    draw_background_image(), draw_element(), etc
    """
    global flag, score, gameStart_Frame_Counter, displayTopTen
    # You may set different background for each step!
    draw_background('background4')

    if not game_started:
        # What you want to show *before* the game starts goes here. eg 'Press Space to Start!'
        for gameElement in startScreenElements.values():
            if VISIBLE not in gameElement or gameElement[VISIBLE]:
                draw_element(gameElement)
                draw_text_on_screen(playerName, centerPosition=(WIDTH / 2, HEIGHT / 4 - 50),
                                    lineheight=1.2, ocolor='lightseagreen',
                                    owidth=1.5, color="white", fontsize=100)
    elif game_ended:
        # What you want to show *after* the game ends goes here. eg 'You Scored x Beats!'
        global displayScore
        for gameElement in endScreenElements.values():
            if VISIBLE not in gameElement or gameElement[VISIBLE]:
                draw_element(gameElement)

            else:
                # displays the players score and the top ten scores
                draw_text_on_screen(f'SCORE: {displayScore}', (WIDTH / 2, 50), lineheight=1.2, ocolor='lightseagreen',
                                    owidth=1.5, color="white", fontsize=50)
                draw_text_on_screen(f'TOP SCORES:', (WIDTH / 2, 100), lineheight=1.2, ocolor='lightseagreen',
                                    owidth=1.5, color="white", fontsize=50)
                for i in range(0, len(displayTopTen), 3):
                    count = 150
                    draw_text_on_screen(f'{displayTopTen[i]}', (WIDTH / 6, (count + (17.5 * i))), lineheight=1.2,
                                        ocolor='lightseagreen',
                                        owidth=1.5, color="white", fontsize=50)
                    draw_text_on_screen(f'{displayTopTen[i + 1]}', (WIDTH / 2, (count + (17.5 * i))), lineheight=1.2,
                                        ocolor='lightseagreen',
                                        owidth=1.5, color="white", fontsize=50)
                    draw_text_on_screen(f'{displayTopTen[i + 2]}', ((WIDTH * 5) / 6, (count + (17.5 * i))),
                                        lineheight=1.2, ocolor='lightseagreen',
                                        owidth=1.5, color="white", fontsize=50)
    else:
        # What you want to show *during* the game goes here. e.g. beats, timer, etc

        # It will get the files beat and place it into a string
        string = []
        with open(f'{songName}\\{difficulty}.beat', 'r') as beats:
            string = beats.read().split()
        # splitting it and taking the important parts and genertate the beats with it only if the frames == the same
        # inside the beats from the song and difficulty.
        for i in range(4, len(string), 4):
            if int(string[i]) == gameStart_Frame_Counter:
                generate_beat(str(string[i + 2]), str(string[i + 3]))
        # draws the in game score
        draw_text_on_screen(f'{score}', (70, 32), color='yellow', fontsize=40)
        for gameElement in playScreenElements.values():
            if VISIBLE not in gameElement or gameElement[VISIBLE]:
                draw_element(gameElement)

        # it will move the beats that were created and if they get hit it will display the amount won for both sides
        for beat in beatRightList:
            draw_element(beat)
            if beatRightList[0]:
                beat = beatRightList[0]
                if beat['status']:
                    x = get_position(beat, 'top')
                    y = get_position(beat, 'right')
                    draw_text_on_screen("+2", (y + 13, x), color='black')

        for left in beatLeftList:
            draw_element(left)
            if beatLeftList[0]:
                beat = beatLeftList[0]
                if beat['status']:
                    x = get_position(beat, 'top')
                    y = get_position(beat, 'right')
                    draw_text_on_screen("+2", (y + 13, x), color='black')


def update():
    """
    - Called automatically 60 times per second (every 1/60th of a second) to
    maintain a smooth frame rate of 60 fps.
    - Ideal for game logic e.g. moving objects, updating score, and checking game conditions.
    """
    # The frame counter keeps track of which frame we're on, this can be helpful for
    # operations that are time sensitive. You may also use the callback functions instead of
    # using the frame_counter.

    global frame_counter, game_ended, score, gameStart_Frame_Counter, playerName, displayScore, displayTopTen
    frame_counter += 1
    # Uncomment the following line and see what happens when you run the program

    once = False
    if not game_started:
        # Game logic if any *before* the game starts.
        # will open a top10 file and if it's not their will create it with the numbers and -- so it can be replaced
        # later
        try:
            with open('top10.csv', 'r') as f:
                f.read()
        except FileNotFoundError:
            with open('top10.csv', 'w') as file:
                string = ""
                for i in range(10):
                    string += f"{i + 1}. ----- ---\n"
                file.write(string)
        pass

    elif game_ended:
        # Game logic if any *after* the game ends.

        # An algorithm that will sort the name and score and replace it in the right order and will move the rest down
        finalStr = ""
        try:
            with open('top10.csv', "r") as file:
                x = file.read()
                gettingScore = x.split()
                y = []
                old_Name = ""
                old_score = 0
                index = 0
                for i in range(len(gettingScore)):
                    y += gettingScore[i].split()
                for i in range(2, len(y), 3):
                    if playerName != "" and score != 0:
                        try: #
                            if score >= int(y[i]):
                                old_Name = y[i - 1]
                                old_score = int(y[i])
                                y[i - 1] = playerName
                                y[i] = score
                                score = old_score
                                playerName = old_Name
                            index = i + 3
                        except ValueError:
                            if playerName != "" and score != 0:
                                if index == 0:
                                    y[1] = playerName
                                    y[2] = score
                                else:
                                    y[index - 1] = playerName
                                    y[index] = score
                                playerName = ""
                                score = 0
                for i in range(0, len(y), 3):
                    finalStr += f"{y[i]} {y[i + 1]} {y[i + 2]}\n"
                if once == False:
                    displayTopTen = y
                    once = True
            with open('top10.csv', "w") as file:

                file.write(finalStr)
        except FileNotFoundError:
            # if there might be a bug later, it will catch it
            print("I JUST NEED THIS JUST IN CASE")

        pass
    else:
        # Game logic if any *during* the game.
        # move it 5 pixels down
        gameStart_Frame_Counter += 1
        # if the music stops playing then the games ends
        if not manage_background_music(songName, 'is-playing') or score < 0:
            end_game()

        # if the beat reaches the bottom or when the player hit before or after the hit screen it will change the score
        # for both sides
        for beat in beatRightList:
            if beat['moving']:
                move_by_offset(beat, (0, SPEED))
                if get_position(beat, 'top') >= 651:
                    beat['moving'] = False
                    beat['scoreStatus'] = 'miss'
                    displayScore -= 1
                    score -= 1
            elif beat['scoreStatus']:
                if beat['scoreStatus'] == 'hit':
                    score += 2
                    displayScore += 2
                score_beatRight(beat)

        for left in beatLeftList:
            if left['moving']:
                move_by_offset(left, (0, SPEED))
                if get_position(left, 'top') >= 651:
                    left['moving'] = False
                    left['scoreStatus'] = 'miss'
                    score -= 1
                    displayScore -= 1
            elif left['scoreStatus']:
                if left['scoreStatus'] == 'hit':
                    score += 2
                    displayScore += 2

                score_beatLeft(left)


def on_key_down(key):
    """
    Called when a key is pressed on the keyboard.
    - Do not use this function for game logic.

    Parameters:
    - key: An integer representative of the key that was pressed.
    In order to get a str value of the key pressed, use get_key() instead.

    """
    # if the user presses space the game starts
    global score, displayScore
    key_pressed = get_key_pressed(key)
    if key_pressed == 'space' and not game_started:
        start_game()
        return
    # gets the lowest beat from the left and right
    lowest_beat_Right = find_Lowest_moving_beat_Right()
    lowest_beat_Left = find_Lowest_moving_beat_Left()

    # If the lowest beat from left or right gets into the hit region then the beat can be hit or miss dependent on
    # which side reaches the hit zone or if they miss a beat when it reaches out of the hit zone.
    if not game_ended and lowest_beat_Right and key_pressed in BEAT_DIRECTIONS:
        if get_position(lowest_beat_Right, "bottom") >= 550:
            lowest_beat_Right['moving'] = False
            change_image(playScreenElements['keyboard'],
                         playScreenElements['keyboard']['base'] + key_pressed)
            schedule_callback_after(keyboardArrowChangeBack, .1)
            if (lowest_beat_Right['direction'] == key_pressed and get_position(lowest_beat_Right, 'bottom') >= 550
                    and get_position(lowest_beat_Right, 'top') <= 650):
                lowest_beat_Right['scoreStatus'] = 'hit'
                lowest_beat_Right['status'] = True
            else:
                lowest_beat_Right['scoreStatus'] = 'miss'
                score -= 1
                displayScore -= 1

    if not game_ended and lowest_beat_Left and key_pressed in WASD_DIRECTIONS:
        if get_position(lowest_beat_Left, "bottom") >= 550:
            lowest_beat_Left['moving'] = False
            change_image(playScreenElements['wasd'],
                         playScreenElements['wasd']['base'] + key_pressed)
            schedule_callback_after(keyboardWASDChangeBack, .2)
            if (lowest_beat_Left['wasd'] == key_pressed and get_position(lowest_beat_Left, "bottom") >= 550 and
                    get_position(lowest_beat_Left, 'top') <= 650):
                lowest_beat_Left['scoreStatus'] = 'hit'
                lowest_beat_Left['status'] = True
            else:
                lowest_beat_Left['scoreStatus'] = 'miss'
                score -= 1
                displayScore -= 1


# Changes the arrows keys that are displayed back
def keyboardArrowChangeBack():
    change_image(playScreenElements['keyboard'], playScreenElements['keyboard']['base'][:-1])


# Same with the wasd
def keyboardWASDChangeBack():
    change_image(playScreenElements['wasd'], playScreenElements['wasd']['base'])


# score if the user gets it right for the right column
def score_beatRight(beat):
    status = beat['scoreStatus']
    beat['scoreStatus'] = ''
    direction = beat['direction']
    change_image(beat, direction + '-' + status)
    schedule_callback_after(remove_lowest_beatRight, .2)


# score if the user gets it right for the left column
def score_beatLeft(beat):
    status = beat['scoreStatus']
    beat['scoreStatus'] = ''
    direction = beat['direction']
    change_image(beat, direction + '-' + status)
    schedule_callback_after(remove_lowest_beatLeft, .2)


# removes the lowest beat from the right column
def remove_lowest_beatRight():
    if beatRightList:
        beatRightList.pop(0)


# removes the lowest beat from the left column
def remove_lowest_beatLeft():
    if beatLeftList:
        beatLeftList.pop(0)


# Find the lowest beat from the right column
def find_Lowest_moving_beat_Right():
    for beat in beatRightList:
        if beat['moving']:
            return beat
    return None


# Find the lowest beat from the left column
def find_Lowest_moving_beat_Left():
    for beat in beatLeftList:
        if beat['moving']:
            return beat
    return None


# Starts the game
def start_game():
    # user-defined function
    # only put logic that'll happen once when the game starts
    game_screen_setup()
    manage_background_music(songName, 'play-once')
    manage_background_music(songName, 'change-volume', volume=0.3)


# when the games end it clears the screen
def end_game():
    # user-defined function
    end_screen_setup()
    beatRightList.clear()
    beatLeftList.clear()
    manage_background_music(songName, 'stop')


# generates the beats depending on which hand its given left or right and the direction givin from the beat list that
# the user inputs and creates them.
def generate_beat(hand, direction):
    beatDirection = direction.lower()
    if hand == "Left":
        side = -1
    else:
        side = 1

    beat = create_element(beatDirection + '-beat', centerPos=(WIDTH / 2 + side * 150, 0))
    if beatDirection == 'right':
        beat['wasd'] = 'd'
    elif beatDirection == 'down':
        beat['wasd'] = 's'
    elif beatDirection == 'up':
        beat['wasd'] = 'w'
    elif beatDirection == 'left':
        beat['wasd'] = 'a'
    beat['side'] = side
    beat['moving'] = True
    beat['status'] = False
    beat['scoreStatus'] = ''
    beat['direction'] = beatDirection
    if side == -1:
        beatLeftList.append(beat)
    else:
        beatRightList.append(beat)


# # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # DO NOT REMOVE THIS LINE!! # # # # # # # #

start_screen_setup()
run_game()
# # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # #
