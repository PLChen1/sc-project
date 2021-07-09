"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman, 
and Jerry Liao

This programs has a menu which contains: gamemode, how to play, and a highscoreboard
The collision model has been fixed to simulate a real collision.
There will be some intersting powerups in game, and some interesting effect.
At the end of the game, there will be some quotes to cheer up the user if they lose.
"""
from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import GOval, GRect, GLabel, GRoundRect
from campy.gui.events.mouse import onmouseclicked, onmousemoved
from campy.gui.events.timer import pause
import random

BRICK_SPACING = 5  # Space between bricks (in pixels). This space is used for horizontal and vertical spacing.
BRICK_WIDTH = 40  # Height of a brick (in pixels).
BRICK_HEIGHT = 15  # Height of a brick (in pixels).
BRICK_ROWS = 10  # Number of rows of bricks.
BRICK_COLS = 10  # Number of columns of bricks.
BRICK_OFFSET = 50  # Vertical offset of the topmost brick from the window top (in pixels).
BALL_RADIUS = 10  # Radius of the ball (in pixels).
PADDLE_WIDTH = 75  # Width of the paddle (in pixels).
PADDLE_HEIGHT = 15  # Height of the paddle (in pixels).
PADDLE_OFFSET = 50  # Vertical offset of the paddle from the window bottom (in pixels).
BRICK_COLOR1 = 'red'
BRICK_COLOR2 = 'orange'
BRICK_COLOR3 = 'yellow'
BRICK_COLOR4 = 'green'
BRICK_COLOR5 = 'blue'

INITIAL_Y_SPEED = 5.0  # Initial vertical speed for the ball.
MAX_X_SPEED = 5  # Maximum initial horizontal speed for the ball.
NUM_LIVES = 3

BALL_CORECT = 3
CORRECT = 3


# Intro constants


class BreakoutGraphics:

    def __init__(self, ball_radius=BALL_RADIUS, paddle_width=PADDLE_WIDTH,
                 paddle_height=PADDLE_HEIGHT, paddle_offset=PADDLE_OFFSET,
                 brick_rows=BRICK_ROWS, brick_cols=BRICK_COLS,
                 brick_width=BRICK_WIDTH, brick_height=BRICK_HEIGHT,
                 brick_offset=BRICK_OFFSET, brick_spacing=BRICK_SPACING, num_lives=NUM_LIVES,
                 title='Breakout by Benson Chen'):

        # Create a graphical window, with some extra space.
        window_width = brick_cols * (brick_width + brick_spacing) - brick_spacing
        window_height = brick_offset + 3 * (brick_rows * (brick_height + brick_spacing) - brick_spacing)
        self.window = GWindow(width=window_width, height=window_height, title=title)

        # ball radius
        self.ball_radius = BALL_RADIUS

        # score board
        score = GLabel('Score:0')
        score.font = 'Helvetica-20-bold'
        self.score = score

        # highscore value
        self.first = 0
        self.second = 0
        self.third = 0
        self.fourth = 0
        self.fifth = 0

        # back button
        back_button = GLabel('<Back to menu')
        back_button.font = 'Arial-30-bold'
        self.back_button = back_button

        # the extra ball in game
        self.ball_available = True
        self.ball2 = GOval(BALL_RADIUS * 2, BALL_RADIUS * 2)
        self.ball2.filled=True
        self.ball2.fill_color='gold'


        # lives
        lives = GLabel('Balls left:3')
        lives.font = 'Arial-20-bold'
        self.lives = lives

        # intro
        self.intro()

    def intro(self):
        # clears the window
        self.window.clear()

        # creates the background as a loading illusion
        self.background_brick_row = self.window.height // 30
        self.background_brick_col = self.window.width // 30
        for i in range(32):
            pause(20)
            for j in range(32):
                backbrick = GRoundRect(self.background_brick_col, self.background_brick_row)
                backbrick.filled = True
                color = self.random_color()
                backbrick.color = color
                backbrick.fill_color = color
                self.window.add(backbrick, i * (self.background_brick_col + BRICK_SPACING),
                                j * (self.background_brick_row + BRICK_SPACING))

        # labels for the menu
        breakout = GLabel('Breakout')
        breakout.font = ('Arial-60-bold')
        self.breakout=breakout
        self.window.add(breakout, (self.window.width - breakout.width) / 2, (self.window.height - breakout.width) / 2)
        startgame = GLabel('--Startgame--')
        startgame.font = 'Arial-40-bold'
        self.startgame = startgame
        self.window.add(startgame, (self.window.width - startgame.width) / 2,
                        self.window.height * 7 / 12 - startgame.height / 2)
        howtoplay = GLabel('--How to play--')
        howtoplay.font = ('Arial-40-bold')
        self.howtoplay = howtoplay
        self.window.add(howtoplay, (self.window.width - howtoplay.width) / 2,
                        self.window.height * 9 / 12 - howtoplay.height / 2)
        highscore = GLabel('--Highscore--')
        highscore.font = ('Arial-40-bold')
        self.highscore = highscore
        self.window.add(highscore, (self.window.width - highscore.width) / 2,
                        self.window.height * 11 / 12 - highscore.height / 2)

        # mouse listeners that will bring us to other windows
        onmouseclicked(self.trigger)

    def random_color(self):
        # returns a random color as a string
        x = random.randint(1, 6)
        color = ''
        if x == 1:
            color = 'red'
        elif x == 2:
            color = 'orange'
        elif x == 3:
            color = 'yellow'
        elif x == 4:
            color = 'green'
        elif x == 5:
            color = 'blue'
        elif x == 6:
            color = 'purple'
        return color

    def back(self, event):
        # this button will go back to the menu
        click = self.window.get_object_at(event.x, event.y)
        if click == self.back_button:
            self.scoreboard_switch=False
            self.end_switch=False
            self.howto_switch=False

            self.intro()


    def trigger(self, event):
        # identifies which button is clicked
        click = self.window.get_object_at(event.x, event.y)

        # play mode
        if click == self.startgame:
            self.leave_intro()
            self.gamemode_switch=True
            self.window.clear()

            # labels for selecting gamemodes
            easy = GLabel('--Easy--')
            easy.font = ('Arial-40-bold')
            moderate = GLabel('--Moderate--')
            moderate.font = ('Arial-40-bold')
            hardcore = GLabel('--Hardcore--')
            hardcore.font = ('Arial-40-bold')
            self.easy = easy
            self.moderate = moderate
            self.hardcore = hardcore
            self.window.add(self.easy, x=self.window.width / 2 - easy.width / 2, y=self.window.height * 2 / 6)
            self.window.add(self.moderate, x=self.window.width / 2 - moderate.width / 2, y=self.window.height * 3 / 6)
            self.window.add(self.hardcore, x=self.window.width / 2 - hardcore.width / 2, y=self.window.height * 4 / 6)
            self.window.add(self.back_button, 0, self.window.height)

            self.easy.color='green'
            self.moderate.color='orange'
            self.hardcore.color='red'
            while self.gamemode_switch:
                onmouseclicked(self.gamemode)
                self.easy.color = 'green'
                self.moderate.color = 'orange'
                self.hardcore.color = 'red'
                pause(500)
                self.easy.color= 'black'
                self.moderate.color = 'black'
                self.hardcore.color = 'black'
                pause(500)

        # how to play
        elif click == self.howtoplay:
            self.leave_intro()
            self.how_to_play_setup()

        # highscore board
        elif click == self.highscore:
            self.leave_intro()
            self.window.clear()
            self.highscore_board()

    def move_paddle(self, event):
        if 0 < event.x < self.window.width - self.paddle.width:
            self.paddle.x = event.x

    def start(self, event):
        # this is when the ball starts moving during playmode
        if self.switch == 0:
            self.highscore_switch=False
            # the player is playing
            self.switch = 1
            # let the speed be random everytime
            self.__dx = random.randint(3, MAX_X_SPEED)
            if random.random() > 0.5:
                self.__dx = -self.__dx

            # this is the speed of the second ball
            self.__dx2 = self.__dx
            self.__dy2 = 6

            three=GLabel('3')
            three.font = ('Arial-30-bold')
            self.window.add(three,self.window.width/2-three.width/2,self.window.height / 2 - 30)
            pause(1000)
            self.window.remove(three)
            two = GLabel('2')
            two.font = ('Arial-30-bold')
            self.window.add(two, self.window.width / 2 - two.width / 2, self.window.height / 2 - 30)
            pause(1000)
            self.window.remove(two)
            one = GLabel('1')
            one.font = ('Arial-30-bold')
            self.window.add(one, self.window.width / 2 - one.width / 2, self.window.height / 2 - 30)
            pause(1000)
            self.window.remove(one)




            # while the player has lives left
            while self.__life > 0:
                # functions that will move the ball and detect collisions
                self.ball.move(self.__dx, self.__dy)
                self.collision_window()
                self.collision_paddle()

                # this is the special collision model for superball, which is a power up
                if self.superball_switch:
                    # super ball collision
                    self.ball.filled = True
                    self.ball.fill_color='red'
                    self.super_collision()
                else:
                    # a collision model that i created which is more realistic
                    self.ball.filled=True
                    self.ball.fill_color='black'
                    self.better_collision()

                # identify if ball2 is on screen, if so, operate the collision function for ball2
                if not self.ball_available:
                    self.ball2_collision()
                # if the power up touches the paddle
                self.drop_touches_paddle()

                # if the power up is on screen, move it
                if self.drop_switch:
                    self.drop.move(0, 3)

                    # remove the power up if it is out of window, and turn of the switch
                    if self.drop.y > self.window.height:
                        self.window.remove(self.drop)
                        self.drop_switch = False

                # update the score
                self.score.text = 'Score:' + str(self.scorepoints)

                # ball2 went under
                if self.ball2.y>self.window.height:
                    self.ball_available=True
                    self.window.remove(self.ball2)

                # ball went under
                if self.ball.y > self.window.height:
                    if not self.ball_available:
                        self.window.remove(self.ball2)
                        self.ball_available = True
                    # turn of the switch
                    self.switch = 0
                    # remove the power up on screen
                    if self.drop_switch:
                        self.window.remove(self.drop)
                        self.drop_switch = False
                    # put back the ball on the original position
                    self.window.add(self.ball, x=self.window.width / 2 - self.ball.width / 2,
                                    y=self.window.height / 2 - self.ball.height / 2)
                    # update lives left
                    self.__life -= 1
                    self.lives.text = 'Balls left:' + str(self.__life)

                    if self.__life == 0:
                        # gameover setup

                        gameover = GLabel('Game over')
                        gameover.font = ('Arial-40-bold')
                        gameover.color='red'
                        self.ball_available = True
                        self.highscore_caluculator()
                        self.window.add(gameover, self.window.width / 2 - gameover.width / 2,
                                        self.window.height / 2 - gameover.height / 2)
                        self.window.add(self.back_button, 0, self.window.height)
                        self.random_quote()
                        self.window.add(self.quote, self.window.width / 2 - self.quote.width / 2,
                                        self.window.height * 7 / 12)
                        self.window.add(self.quote2, self.window.width / 2 - self.quote2.width / 2,
                                        self.window.height * 8 / 12)
                        onmouseclicked(self.back)
                        if self.highscore_switch:
                            self.end_switch = True
                            new_highscore = GLabel('New highscore!')
                            new_highscore.font = ('Arial-40-bold')
                            self.window.add(new_highscore, self.window.width / 2 - new_highscore.width / 2,
                                            self.window.height * 3 / 12)
                            while self.end_switch:
                                new_highscore.color = 'red'
                                pause(100)
                                new_highscore.color = 'orange'
                                pause(100)
                                new_highscore.color = 'yellow'
                                pause(100)
                                new_highscore.color = 'green'
                                pause(100)
                                new_highscore.color = 'blue'
                                pause(100)
                                new_highscore.color = 'purple'
                                pause(100)


                    break

                # cleared all bricks
                if self.__brick_left == 0:

                    you_win = GLabel('You Win')
                    you_win.font = ('Arial-40-bold')
                    self.ball_available = True
                    self.highscore_caluculator()
                    self.window.add(you_win, self.window.width / 2 - you_win.width / 2,
                                    self.window.height / 2 - you_win.height / 2)
                    self.window.add(self.back_button, 0, self.window.height)
                    onmouseclicked(self.back)
                    self.random_win_quote()
                    self.window.add(self.quote, self.window.width / 2 - self.quote.width / 2,
                                    self.window.height * 7 / 12)
                    self.window.add(self.quote2, self.window.width / 2 - self.quote2.width / 2,
                                    self.window.height * 8 / 12)
                    if self.highscore_switch:
                        self.end_switch = True
                        new_highscore=GLabel('New highscore!')
                        new_highscore.font=('Arial-40-bold')
                        self.window.add(new_highscore, self.window.width / 2 - new_highscore.width / 2,
                                        self.window.height*3/12)
                        while self.end_switch:
                            new_highscore.color='red'
                            pause(100)
                            new_highscore.color = 'orange'
                            pause(100)
                            new_highscore.color = 'yellow'
                            pause(100)
                            new_highscore.color = 'green'
                            pause(100)
                            new_highscore.color = 'blue'
                            pause(100)
                            new_highscore.color = 'purple'
                            pause(100)

                    break




                pause(10)

    def collision_window(self):
        if 0 > self.ball.x:
            self.__dx = -self.__dx
        elif self.ball.x > self.window.width - self.ball.width:
            self.__dx = -self.__dx
        if 0 > self.ball.y:
            self.__dy = -self.__dy
            self.superball_switch = False

    def collision_paddle(self):
        if self.paddle.x - self.ball.width < self.ball.x < self.paddle.x + self.paddle.width:
            if 0 < self.paddle.y - self.ball.y - self.ball.height + 7 < 7:
                if self.__dy > 0:
                    self.__dy = -self.__dy

    def better_collision(self):
        """
        this is a special collision model, which i added 8 points to detect if there is any objects,
        the collision should be more realistic and smooth, but it is not perfect. Some
        special cases might make the collision look wired
        """
        if self.ball.y < self.window.height / 2:
            h = self.window.get_object_at(self.ball.x - BALL_CORECT, self.ball.y + self.ball.height / 2)
            f = self.window.get_object_at(self.ball.x + self.ball.width + BALL_CORECT,
                                          self.ball.y + self.ball.height / 2)
            if f != None and f != self.score and f != self.lives and f != self.drop and f!=self.ball2:
                self.__dx = -self.__dx
                self.window.remove(f)
                self.__brick_left -= 1
                self.random_drop(f)
                self.scorepoints += 1
            elif h != None and h != self.score and h != self.lives and h != self.drop and h!=self.ball2:
                self.__dx = -self.__dx
                self.window.remove(h)
                self.__brick_left -= 1
                self.random_drop(h)
                self.scorepoints += 1
            elif self.__dy < 0:
                a = self.window.get_object_at(
                    self.ball.x + self.ball.width / 2 + self.ball_radius / 1.414 + BALL_CORECT,
                    self.ball.y + self.ball.height / 2 - self.ball_radius / 1.414 - BALL_CORECT + CORRECT)
                d = self.window.get_object_at(
                    self.ball.x + self.ball.width / 2 - self.ball_radius / 1.414 - BALL_CORECT,
                    self.ball.y + self.ball.height / 2 - self.ball_radius / 1.414 - BALL_CORECT + CORRECT)
                e = self.window.get_object_at(self.ball.x + self.ball.width / 2, self.ball.y - BALL_CORECT - CORRECT)

                if e != None  and e != self.score and e != self.lives and e != self.drop and e != self.ball2:
                    self.__dy = -self.__dy
                    self.window.remove(e)
                    self.__brick_left -= 1
                    self.random_drop(e)
                    self.scorepoints += 1

                elif (a != None and a != self.score) and (e and f) == None and a != self.lives and a != self.drop and a!=self.ball2:
                    self.window.remove(a)
                    self.__dy = -self.__dy
                    self.__dx = -self.__dx
                    self.__brick_left -= 1
                    self.random_drop(a)
                    self.scorepoints += 1
                elif (d != None and d != self.score) and (e and h) == None and d != self.lives and d != self.drop and d!=self.ball2:
                    self.window.remove(d)
                    self.__dy = -self.__dy
                    self.__dx = -self.__dx
                    self.__brick_left -= 1
                    self.random_drop(d)
                    self.scorepoints += 1


            else:
                b = self.window.get_object_at(
                    self.ball.x + self.ball.width / 2 + self.ball_radius / 1.414 + BALL_CORECT,
                    self.ball.y + self.ball.height / 2 + self.ball_radius / 1.414 + BALL_CORECT - CORRECT)
                c = self.window.get_object_at(
                    self.ball.x + self.ball.width / 2 - self.ball_radius / 1.414 - BALL_CORECT,
                    self.ball.y + self.ball.height / 2 + self.ball_radius / 1.414 + BALL_CORECT - CORRECT)
                g = self.window.get_object_at(self.ball.x + self.ball.width / 2,
                                              self.ball.y + self.ball.height + BALL_CORECT + CORRECT)
                if g != None  and g != self.score and g != self.lives and g != self.drop and g!=self.ball2:
                    self.__dy = -self.__dy
                    self.window.remove(g)
                    self.__brick_left -= 1
                    self.random_drop(g)
                    self.scorepoints += 1

                elif b != None and (f and g) == None and b != self.score and b != self.lives and b != self.drop and b!=self.ball2:
                    self.window.remove(b)
                    self.__dy = -self.__dy
                    self.__dx = -self.__dx
                    self.__brick_left -= 1
                    self.random_drop(b)
                    self.scorepoints += 1

                elif c != None and c != self.score and (g and h) == None and c != self.lives and c != self.drop and c!=self.ball2:
                    self.window.remove(c)
                    self.__dy = -self.__dy
                    self.__dx = -self.__dx
                    self.__brick_left -= 1
                    self.random_drop(c)
                    self.scorepoints += 1


    def random_drop(self, brick):
        """
        This function will define a random powerup, which the percentage
        of dropping is 20%. And the percentage of getting a specific
         power up is 1/6.

        """
        a = random.randrange(1, 6)
        coordinatex = brick.x + brick.width / 2
        coordinatey = brick.y
        if a == 1 and not self.drop_switch:
            drop = GRoundRect(15, 15)
            drop.filled = True
            self.dropcolor = self.random_color()
            drop.fill_color = self.dropcolor

            """ 
            the green color powerup is a extra ball on screen, to prevent the 
            program to get the third ball, i wrote a switch for this.
            The reason is that the third ball might cause the program to lag
            """
            if self.dropcolor!='green' or  self.ball_available:
                self.window.add(drop, coordinatex, coordinatey)
                self.drop = drop
                self.drop_switch = True

    def highscore_caluculator(self):
        """
        It identifies the scores and will update the
        scoreboard everytime a player ends a game.
        """
        if self.scorepoints > self.first:
            self.fifth = self.fourth
            self.fourth = self.third
            self.third = self.second
            self.second = self.first
            self.first = self.scorepoints
            self.highscore_switch = True
        elif self.scorepoints > self.second:
            self.fifth = self.fourth
            self.fourth = self.third
            self.third = self.second
            self.second = self.scorepoints
            self.highscore_switch = True
        elif self.scorepoints > self.third:
            self.fifth = self.fourth
            self.fourth = self.third
            self.third = self.scorepoints
            self.highscore_switch = True
        elif self.scorepoints > self.fourth:
            self.fifth = self.fourth
            self.fourth = self.scorepoints
            self.highscore_switch = True
        elif self.scorepoints > self.fifth:
            self.fifth = self.scorepoints
            self.highscore_switch = True

    def drop_touches_paddle(self):
        # when the power up touches the paddle, it triggers the power up for that color
        if self.drop_switch:
            if self.drop.y + self.drop.height > self.paddle.y:
                if self.paddle.x < self.drop.x + self.drop.width / 2 < self.paddle.x + self.paddle.width:
                    self.drop_trigger()
                    self.window.remove(self.drop)
                    self.drop_switch = False

    def highscore_board(self):
        # setup for the highscore board
        self.scoreboard_switch=True
        self.window.add(self.back_button, 0, self.window.height)
        first_ = GLabel('1st:' + str(self.first))
        first_.font = ('Arial-30-bold')
        first_.color='gold'
        second_ = GLabel('2nd:' + str(self.second))
        second_.font = ('Arial-30-bold')
        second_.color='silver'
        third_ = GLabel('3rd:' + str(self.third))
        third_.font = ('Arial-30-bold')
        third_.color='brown'
        fourth_ = GLabel('4th:' + str(self.fourth))
        fourth_.font = ('Arial-30-bold')
        fifth_ = GLabel('5th:' + str(self.fifth))
        fifth_.font = ('Arial-30-bold')
        self.window.add(first_, x=self.window.width / 2 - first_.width / 2, y=self.window.height * 3 / 12)
        self.window.add(second_, x=self.window.width / 2 - second_.width / 2, y=self.window.height * 4.5 / 12)
        self.window.add(third_, x=self.window.width / 2 - third_.width / 2, y=self.window.height * 6 / 12)
        self.window.add(fourth_, x=self.window.width / 2 - fourth_.width / 2, y=self.window.height * 7.5 / 12)
        self.window.add(fifth_, x=self.window.width / 2 - fifth_.width / 2, y=self.window.height * 9 / 12)
        while self.scoreboard_switch:
            onmouseclicked(self.back)
            first_.color = 'gold'
            second_.color = 'silver'
            third_.color = 'brown'
            pause(500)
            first_.color = 'black'
            second_.color = 'black'
            third_.color = 'black'
            pause(500)

    def gamemode(self, event):
        """
        this program allows the user to pick a gamemode,
        for each gamemode, the paddle size is different as well
        as the speed of dy
        """
        mode = self.window.get_object_at(event.x, event.y)
        if mode == self.back_button:
            self.gamemode_switch=False
            self.intro()
        elif mode != None:
            self.__dx = MAX_X_SPEED
            if mode == self.easy:
                self.gamemode_switch = False
                self.__dy = 4
                paddle = GRect(PADDLE_WIDTH, PADDLE_HEIGHT)

                paddle.filled = True
                self.paddle = paddle
            elif mode == self.moderate:
                self.gamemode_switch = False
                self.__dy = 6
                paddle = GRect(PADDLE_WIDTH-7, PADDLE_HEIGHT)

                paddle.filled = True
                self.paddle = paddle
            elif mode == self.hardcore:
                self.gamemode_switch = False
                self.__dy = 8

                paddle = GRect(PADDLE_WIDTH - 14, PADDLE_HEIGHT)
                paddle.filled = True
                self.paddle = paddle

            self.screen_change()
            self.playmode_setup()

    def playmode_setup(self):
        """
        This function sets all the label, bricks, paddle, ball
        for the playmode. Furthermore, it resets all the important
        parameters for the game
        """

        # Create a paddle.
        self.window.clear()
        self.drop = None

        self.window.add(self.paddle, x=self.window.width / 2 - self.paddle.width / 2,
                        y=self.window.height - self.paddle.height - PADDLE_OFFSET)

        # Center a filled ball in the graphical window.
        ball = GOval(BALL_RADIUS * 2, BALL_RADIUS * 2)
        ball.filled = True
        self.ball = ball
        self.window.add(ball, x=self.window.width / 2 - ball.width / 2, y=self.window.height / 2 - ball.height / 2)

        # Switch
        self.switch = 0  # if ball is running=0 , if ball is stationary=1

        # Initialize our mouse listeners.
        onmouseclicked(self.start)
        onmousemoved(self.move_paddle)

        # Score board
        self.window.add(self.score, x=0, y=self.score.height + 3)
        self.window.add(self.lives, x=self.window.width - self.lives.width, y=self.lives.height + 2)

        self.superball_switch = False

        self.scorepoints = 0
        self.score.text = 'Score:' + str(self.scorepoints)
        # Draw bricks.
        for i in range(BRICK_COLS):
            for j in range(BRICK_ROWS):
                brick = GRect(BRICK_WIDTH, BRICK_HEIGHT)
                brick.filled = True
                if i <= 1:
                    brick.fill_color = BRICK_COLOR1
                    brick.color = BRICK_COLOR1
                elif i <= 3:
                    brick.fill_color = BRICK_COLOR2
                    brick.color = BRICK_COLOR2
                elif i <= 5:
                    brick.fill_color = BRICK_COLOR3
                    brick.color = BRICK_COLOR3
                elif i <= 7:
                    brick.fill_color = BRICK_COLOR4
                    brick.color = BRICK_COLOR4
                elif i <= 9:
                    brick.fill_color = BRICK_COLOR5
                    brick.color = BRICK_COLOR5
                else:
                    brick.fill_color = 'black'
                self.window.add(brick, x=j * (BRICK_WIDTH + BRICK_SPACING),
                                y=BRICK_OFFSET + i * (BRICK_HEIGHT + BRICK_SPACING))

        self.__brick_left = BRICK_COLS * BRICK_ROWS
        self.__life = NUM_LIVES
        self.lives.text = 'Balls left:' + str(self.__life)
        self.drop_switch = False

    def drop_trigger(self):
        x = self.paddle.x
        if self.dropcolor == 'red':
            # will decrease you paddle size
            # prevents the paddle to be unplayable
            if self.paddle.width>30:
                originalx = self.paddle.width
                paddle = GRect(originalx - 25, PADDLE_HEIGHT)
                paddle.filled = True
                self.window.remove(self.paddle)
                self.paddle = paddle
                self.window.add(paddle, x=x,
                                y=self.window.height - paddle.height - PADDLE_OFFSET)

        elif self.dropcolor == 'orange':
            # extra points
            self.scorepoints += 10
            self.score.text = 'Score:' + str(self.scorepoints)
        elif self.dropcolor == 'yellow':
            # ball ignores collisions until it reaches the top
            self.superball_switch = True

        elif self.dropcolor == 'green':
            # add a extra ball on screen
            self.ball_available=False
            self.window.add(self.ball2,self.window.width/2-self.ball2.width/2,self.window.height/2-self.ball2.height/2)

        elif self.dropcolor == 'blue':
            # increaces the paddle size
            originalx = self.paddle.width
            paddle = GRect(originalx + 25, PADDLE_HEIGHT)
            paddle.filled = True
            self.window.remove(self.paddle)
            self.paddle = paddle
            self.window.add(paddle, x=x, y=self.window.height - paddle.height - PADDLE_OFFSET)
        elif self.dropcolor == 'purple':
            # extra life
            self.__life += 1
            self.lives.text = 'Balls left:' + str(self.__life)

    def super_collision(self):


        # removes all bricks in path until it reaches the top

        if self.ball.y < self.window.height / 2:
            h = self.window.get_object_at(self.ball.x - BALL_CORECT, self.ball.y + self.ball.height / 2)
            f = self.window.get_object_at(self.ball.x + self.ball.width + BALL_CORECT,
                                          self.ball.y + self.ball.height / 2)
            if f != None and f != self.score and f != self.lives and f != (self.drop and self.ball2):
                self.window.remove(f)
                self.__brick_left -= 1
                self.random_drop(f)
                self.scorepoints += 1
            elif h != None and h != self.score and h != self.lives and h != (self.drop and self.ball2):

                self.window.remove(h)
                self.__brick_left -= 1
                self.random_drop(h)
                self.scorepoints += 1
            # elif self.__dy < 0:
            #     a = self.window.get_object_at(
            #         self.ball.x + self.ball.width / 2 + self.ball_radius / 1.414 + BALL_CORECT,
            #         self.ball.y + self.ball.height / 2 - self.ball_radius / 1.414 - BALL_CORECT + CORRECT)
            #     d = self.window.get_object_at(
            #         self.ball.x + self.ball.width / 2 - self.ball_radius / 1.414 - BALL_CORECT,
            #         self.ball.y + self.ball.height / 2 - self.ball_radius / 1.414 - BALL_CORECT + CORRECT)
            #     e = self.window.get_object_at(self.ball.x + self.ball.width / 2, self.ball.y - BALL_CORECT - CORRECT)
            #
            #     if a != None and a != self.score and a != self.lives and (a != self.drop and self.ball2):
            #         self.window.remove(a)
            #
            #         self.__brick_left -= 1
            #         self.random_drop(a)
            #         self.scorepoints += 1
            #     elif d != None and d != self.score and d != self.lives and (d != self.drop and self.ball2):
            #         self.window.remove(d)
            #
            #         self.__brick_left -= 1
            #         self.random_drop(d)
            #         self.scorepoints += 1
            #     elif e != None and e != self.score and e != self.lives and (e != self.drop and self.ball2):
            #
            #         self.window.remove(e)
            #         self.__brick_left -= 1
            #         self.random_drop(e)
            #         self.scorepoints += 1
            #
            # else:
            #     b = self.window.get_object_at(
            #         self.ball.x + self.ball.width / 2 + self.ball_radius / 1.414 + BALL_CORECT,
            #         self.ball.y + self.ball.height / 2 + self.ball_radius / 1.414 + BALL_CORECT - CORRECT)
            #     c = self.window.get_object_at(
            #         self.ball.x + self.ball.width / 2 - self.ball_radius / 1.414 - BALL_CORECT,
            #         self.ball.y + self.ball.height / 2 + self.ball_radius / 1.414 + BALL_CORECT - CORRECT)
            #     g = self.window.get_object_at(self.ball.x + self.ball.width / 2,
            #                                   self.ball.y + self.ball.height + BALL_CORECT + CORRECT)
            #     if b != None and  b != self.score and b != self.lives and (b != self.drop and self.ball2):
            #         self.window.remove(b)
            #
            #         self.__brick_left -= 1
            #         self.random_drop(b)
            #         self.scorepoints += 1
            #     elif c != None and c != self.score and c != self.lives and (c != self.drop and self.ball2):
            #         self.window.remove(c)
            #
            #         self.__brick_left -= 1
            #         self.random_drop(c)
            #         self.scorepoints += 1
            #     elif g != None  and g != self.score and g != self.lives and (g != self.drop and self.ball2):
            #
            #         self.window.remove(g)
            #         self.__brick_left -= 1
            #         self.random_drop(g)
            #         self.scorepoints += 1

    def how_to_play_setup(self):
        """
        tells the player how this game works and what
        does the powerup do
        """
        self.window.clear()
        self.howto_switch=True
        introduction = GLabel('Move the paddle and break bricks')
        introduction.font='Arial-20-bold'
        self.window.add(introduction,self.window.width/2-introduction.width/2, self.window.height*2/14)
        self.window.add(self.back_button, 0, self.window.height)

        red_drop = GRoundRect(15, 15)
        red_drop.filled = True
        red_drop.fill_color = 'red'
        self.window.add(red_drop, self.window.width*2/14, self.window.height*4/14 )
        redlabel=GLabel('Decreases your paddle size')
        redlabel.font='Arial-15-bold'
        self.window.add(redlabel, self.window.width * 3 / 14, self.window.height * 4.4 / 14)

        blue_drop = GRoundRect(15, 15)
        blue_drop.filled = True
        blue_drop.fill_color = 'blue'
        self.window.add(blue_drop, self.window.width * 2 / 14, self.window.height * 5 / 14)
        bluelabel = GLabel('Increases your paddle size')
        bluelabel.font = 'Arial-15-bold'
        self.window.add(bluelabel, self.window.width * 3 / 14, self.window.height * 5.4 / 14)

        green_drop = GRoundRect(15, 15)
        green_drop.filled = True
        green_drop.fill_color = 'green'
        self.window.add(green_drop, self.window.width * 2 / 14, self.window.height * 6 / 14)
        greenlabel = GLabel('Extra ball on screen')
        greenlabel.font = 'Arial-15-bold'
        self.window.add(greenlabel, self.window.width * 3 / 14, self.window.height * 6.4 / 14)

        purple_drop = GRoundRect(15, 15)
        purple_drop.filled = True
        purple_drop.fill_color = 'purple'
        self.window.add(purple_drop, self.window.width * 2 / 14, self.window.height * 7 / 14)
        purplelabel = GLabel('Extra life')
        purplelabel.font = 'Arial-15-bold'
        self.window.add(purplelabel, self.window.width * 3 / 14, self.window.height * 7.4 / 14)

        yellow_drop = GRoundRect(15, 15)
        yellow_drop.filled = True
        yellow_drop.fill_color = 'yellow'
        self.window.add(yellow_drop, self.window.width * 2 / 14, self.window.height * 8 / 14)
        yellowlabel = GLabel('Your ball ignores all brick collisions')
        yellowlabel.font = 'Arial-15-bold'
        self.window.add(yellowlabel, self.window.width * 3 / 14, self.window.height * 8.4 / 14)
        yellowlabel2 = GLabel('until it reaches the top')
        yellowlabel2.font = 'Arial-15-bold'
        self.window.add(yellowlabel2, self.window.width * 3 / 14, self.window.height * 9.4 / 14)

        orange_drop = GRoundRect(15, 15)
        orange_drop.filled = True
        orange_drop.fill_color = 'orange'
        self.window.add(orange_drop, self.window.width * 2 / 14, self.window.height * 10 / 14)
        orangelabel = GLabel('+15 points')
        orangelabel.font = 'Arial-15-bold'
        self.window.add(orangelabel, self.window.width * 3 / 14, self.window.height * 10.4 / 14)
        onmouseclicked(self.back)
        dy=6
        while self.howto_switch:
            red_drop.move(0,dy)
            green_drop.move(0,dy)
            blue_drop.move(0,dy)
            yellow_drop.move(0,dy)
            orange_drop.move(0,dy)
            purple_drop.move(0,dy)
            dy=-dy
            pause(500)



    def ball2_collision(self):
        # the collision model for the second ball
        self.collision2_window()
        self.collision2_paddle()
        self.better2_collision()
        self.ball2.move(self.__dx2, self.__dy2)

    def collision2_paddle(self):
        if self.paddle.x - self.ball2.width < self.ball2.x < self.paddle.x + self.paddle.width:
            if 0 < self.paddle.y - self.ball2.y - self.ball2.height + 7 < 8:
                if self.__dy2 > 0:
                    self.__dy2 = -self.__dy2

    def collision2_window(self):
        if 0 > self.ball2.x:
            self.__dx2 = -self.__dx2
        elif self.ball2.x > self.window.width - self.ball2.width:
            self.__dx2 = -self.__dx2
        if 0 > self.ball2.y:
            self.__dy2 = -self.__dy2

    def better2_collision(self):
        if self.ball2.y < self.window.height / 2:
            h = self.window.get_object_at(self.ball2.x - BALL_CORECT, self.ball2.y + self.ball2.height / 2)
            f = self.window.get_object_at(self.ball2.x + self.ball2.width + BALL_CORECT,
                                          self.ball2.y + self.ball2.height / 2)
            if f != None and f != self.score and f != self.lives and f != self.drop and f!=self.ball:

                self.window.remove(f)
                self.__dx2 = -self.__dx2
                self.__brick_left -= 1
                self.random_drop(f)
                self.scorepoints += 1
            elif h != None and h != self.score and h != self.lives and h != self.drop and h!=self.ball:

                self.window.remove(h)
                self.__dx2 = -self.__dx2
                self.__brick_left -= 1
                self.random_drop(h)
                self.scorepoints += 1
            elif self.__dy2 < 0:
                a = self.window.get_object_at(
                    self.ball2.x + self.ball2.width / 2 + self.ball_radius / 1.414 + BALL_CORECT,
                    self.ball2.y + self.ball2.height / 2 - self.ball_radius / 1.414 - BALL_CORECT + CORRECT)
                d = self.window.get_object_at(
                    self.ball2.x + self.ball2.width / 2 - self.ball_radius / 1.414 - BALL_CORECT,
                    self.ball2.y + self.ball2.height / 2 - self.ball_radius / 1.414 - BALL_CORECT + CORRECT)
                e = self.window.get_object_at(self.ball2.x + self.ball2.width / 2, self.ball2.y - BALL_CORECT - CORRECT)

                if (a != None and a != self.score) and (e and f) == None and a != self.lives and a != self.drop and a!=self.ball:
                    self.window.remove(a)
                    self.__dy2 = -self.__dy2
                    self.__dx2 = -self.__dx2
                    self.__brick_left -= 1
                    self.random_drop(a)
                    self.scorepoints += 1
                elif (d != None and d != self.score) and (e and h) == None and d != self.lives and d != self.drop and d!=self.ball:
                    self.window.remove(d)
                    self.__dy2 = -self.__dy2
                    self.__dx2 = -self.__dx2
                    self.__brick_left -= 1
                    self.random_drop(d)
                    self.scorepoints += 1
                elif e != None and (d and a) == None and e != self.score and e != self.lives and e != self.drop and e!=self.ball:
                    self.window.remove(e)
                    self.__dy2 = -self.__dy2

                    self.__brick_left -= 1
                    self.random_drop(e)
                    self.scorepoints += 1

            else:
                b = self.window.get_object_at(
                    self.ball2.x + self.ball2.width / 2 + self.ball_radius / 1.414 + BALL_CORECT,
                    self.ball2.y + self.ball2.height / 2 + self.ball_radius / 1.414 + BALL_CORECT - CORRECT)
                c = self.window.get_object_at(
                    self.ball2.x + self.ball2.width / 2 - self.ball_radius / 1.414 - BALL_CORECT,
                    self.ball2.y + self.ball2.height / 2 + self.ball_radius / 1.414 + BALL_CORECT - CORRECT)
                g = self.window.get_object_at(self.ball2.x + self.ball2.width / 2,
                                              self.ball2.y + self.ball2.height + BALL_CORECT + CORRECT)
                if b != None and (f and g) == None and b != self.score and b != self.lives and b != self.drop and b!=self.ball:
                    self.window.remove(b)
                    self.__dy2 = -self.__dy2
                    self.__dx2 = -self.__dx2
                    self.__brick_left -= 1
                    self.random_drop(b)
                    self.scorepoints += 1
                elif (c != None and c != self.score) and (g and h) == None and c != self.lives and c != self.drop and c!=self.ball:
                    self.window.remove(c)
                    self.__dy2 = -self.__dy2
                    self.__dx2 = -self.__dx2
                    self.__brick_left -= 1
                    self.random_drop(c)
                    self.scorepoints += 1
                elif g != None and (c and b) == None and g != self.score and g != self.lives and g != self.drop and g!=self.ball:
                    self.window.remove(g)
                    self.__dy2 = -self.__dy2

                    self.__brick_left -= 1
                    self.random_drop(g)
                    self.scorepoints += 1

    def random_quote(self):
        # generates a random quote to cheer up the player if they lose

        x = random.randint(1, 9)
        if x == 1:
            self.quote=GLabel('In the end… We only regret the chances we didn’t take')
            self.quote2=GLabel('- Lewis Carroll')
        elif x == 2:
            self.quote = GLabel("Don't hate the player, hate the game.")
            self.quote2 = GLabel('- Ice T')
        elif x == 3:
            self.quote = GLabel("Our doubts are traitors,and make us lose the")
            self.quote2 = GLabel('good we oft might win,by fearing to attempt.')

        elif x == 4:
            self.quote = GLabel("The pain I feel now is the happiness I had before. ")
            self.quote2 = GLabel('That is the deal. - C.S. Lewis')
        elif x == 5:
            self.quote = GLabel('This thing we call "failure" is not the falling down,')
            self.quote2 = GLabel(' but the staying down.- Mary Pickford')
        elif x == 6:
            self.quote = GLabel("Your failure here is a metaphor. To learn for ")
            self.quote2 = GLabel('what, please keep going.- Rob Dubbin')
        elif x == 7:
            self.quote = GLabel("To live is to suffer, to survive is to find some")
            self.quote2 = GLabel('meaning in the suffering.- Friedrich Nietzsche')
        elif x == 8:
            self.quote = GLabel("There are no regrets in life, just lessons.")
            self.quote2 = GLabel('- Jennifer Aniston')
        elif x==9:
            self.quote =GLabel("You suck at this game. Don't blame on your")
            self.quote2 = GLabel('mouse or computer- Benson Chen')
        self.quote.font = ('Arial-13-bold')
        self.quote2.font = ('Arial-13-bold')

    def random_win_quote(self):
        x = random.randint(1, 9)
        if x == 1:
            self.quote = GLabel('“When you win, say nothing. When you lose, say less.”')
            self.quote2 = GLabel('- Paul Brown')
        elif x == 2:
            self.quote = GLabel("A champion is afraid of losing. Everyone else is ")
            self.quote2 = GLabel('afraid of winning. - Billie Jean King')
        elif x == 3:
            self.quote = GLabel("Winning isn’t everything, but it beats anything ")
            self.quote2 = GLabel('that comes in second. -Paul Bryant')

        elif x == 4:
            self.quote = GLabel("A champion needs a motivation above and  ")
            self.quote2 = GLabel('beyond winning. -  Pat Riley')
        elif x == 5:
            self.quote = GLabel('It’s not whether you win or lose, it’s ')
            self.quote2 = GLabel(' how you play the game. - Grantland Rice')
        elif x == 6:
            self.quote = GLabel("Winning takes precedence over all. There’s  ")
            self.quote2 = GLabel('no gray area. No almosts. - Kobe Bryant')
        elif x == 7:
            self.quote = GLabel("Winning solves everything.")
            self.quote2 = GLabel('- Tiger Woods')
        elif x == 8:
            self.quote = GLabel("The critics are always right. The only way ")
            self.quote2 = GLabel('you shut them up is by winning.- Chuck Noll')
        elif x == 9:
            self.quote = GLabel("Winning isn’t getting ahead of others. It’s ")
            self.quote2 = GLabel('getting ahead of yourself. - Roger Staubach')
        self.quote.font = ('Arial-13-bold')
        self.quote2.font = ('Arial-13-bold')

    def leave_intro(self):
        background_brick_row = self.window.height // 30
        background_brick_col = self.window.width // 30
        for i in range(31,-1,-1):
            pause(20)
            for j in range(31,-1,-1):
                backbrick =self.window.get_object_at(i * (background_brick_col + BRICK_SPACING),
                                j * (background_brick_row + BRICK_SPACING))
                if backbrick==self.startgame:
                    self.window.remove(backbrick)
                    backbrick = self.window.get_object_at(i * (background_brick_col + BRICK_SPACING),
                                                          j * (background_brick_row + BRICK_SPACING))
                elif backbrick==self.highscore:
                    self.window.remove(backbrick)
                    backbrick = self.window.get_object_at(i * (background_brick_col + BRICK_SPACING),
                                                          j * (background_brick_row + BRICK_SPACING))
                elif backbrick==self.howtoplay:
                    self.window.remove(backbrick)
                    backbrick = self.window.get_object_at(i * (background_brick_col + BRICK_SPACING),
                                                          j * (background_brick_row + BRICK_SPACING))
                elif backbrick==self.breakout:
                    self.window.remove(backbrick)
                    backbrick = self.window.get_object_at(i * (background_brick_col + BRICK_SPACING),
                                                          j * (background_brick_row + BRICK_SPACING))
                self.window.remove(backbrick )


    def screen_change(self):
        self.window.clear()
        for i in range(32):
            pause(20)
            for j in range(32):
                backbrick = GRoundRect(self.background_brick_col, self.background_brick_row)
                backbrick.filled = True
                color = self.random_color()
                backbrick.color = color
                backbrick.fill_color = color
                self.window.add(backbrick, i * (self.background_brick_col + BRICK_SPACING),
                                j * (self.background_brick_row + BRICK_SPACING))

        for i in range(32):
            pause(10)
            for j in range(32):
                backbrick = self.window.get_object_at(i * (self.background_brick_col + BRICK_SPACING),
                                                      j * (self.background_brick_row + BRICK_SPACING))
                self.window.remove(backbrick)