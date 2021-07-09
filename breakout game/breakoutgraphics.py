"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman, 
and Jerry Liao

YOUR DESCRIPTION HERE
"""
from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import GOval, GRect, GLabel
from campy.gui.events.mouse import onmouseclicked, onmousemoved
from campy.gui.events.timer import pause
import random

BRICK_SPACING = 5      # Space between bricks (in pixels). This space is used for horizontal and vertical spacing.
BRICK_WIDTH = 40       # Height of a brick (in pixels).
BRICK_HEIGHT = 15      # Height of a brick (in pixels).
BRICK_ROWS = 10       # Number of rows of bricks.
BRICK_COLS = 10      # Number of columns of bricks.
BRICK_OFFSET = 50      # Vertical offset of the topmost brick from the window top (in pixels).
BALL_RADIUS = 10       # Radius of the ball (in pixels).
PADDLE_WIDTH = 75      # Width of the paddle (in pixels).
PADDLE_HEIGHT = 15     # Height of the paddle (in pixels).
PADDLE_OFFSET = 50     # Vertical offset of the paddle from the window bottom (in pixels).
BRICK_COLOR1='red'
BRICK_COLOR2='orange'
BRICK_COLOR3='yellow'
BRICK_COLOR4='green'
BRICK_COLOR5='blue'


INITIAL_Y_SPEED = 5.0  # Initial vertical speed for the ball.
MAX_X_SPEED = 5      # Maximum initial horizontal speed for the ball.
NUM_LIVES = 3
class BreakoutGraphics:

    def __init__(self, ball_radius = BALL_RADIUS, paddle_width = PADDLE_WIDTH,
                 paddle_height = PADDLE_HEIGHT, paddle_offset = PADDLE_OFFSET,
                 brick_rows = BRICK_ROWS, brick_cols = BRICK_COLS,
                 brick_width = BRICK_WIDTH, brick_height = BRICK_HEIGHT,
                 brick_offset = BRICK_OFFSET, brick_spacing = BRICK_SPACING,num_lives=NUM_LIVES,
                 title='Breakout'):

        # Create a graphical window, with some extra space.
        window_width = brick_cols * (brick_width + brick_spacing) - brick_spacing
        window_height = brick_offset + 3 * (brick_rows * (brick_height + brick_spacing) - brick_spacing)
        self.window = GWindow(width=window_width, height=window_height, title=title)

        # Create a paddle.
        paddle=GRect(paddle_width,paddle_height)
        paddle.filled=True
        self.paddle=paddle
        self.window.add(paddle,x=self.window.width/2-paddle.width/2,y=self.window.height-paddle.height-paddle_offset)

        # Center a filled ball in the graphical window.
        ball=GOval(ball_radius*2,ball_radius*2)
        ball.filled=True
        self.ball=ball
        self.window.add(ball,x=self.window.width/2-ball.width/2,y=self.window.height/2-ball.height/2)

        # Default initial velocity for the ball.

        self.__dx=MAX_X_SPEED
        self.__dy=INITIAL_Y_SPEED

        # Switch
        self.switch = 0  # if ball is running=0 , if ball is stationary=1

        # Initialize our mouse listeners.
        onmouseclicked(self.start)
        onmousemoved(self.move_paddle)
        # Draw bricks.
        for i in range(brick_cols):
            for j in range(brick_rows):
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
                    brick.fill_color= 'black'
                self.window.add(brick, x=j*(BRICK_WIDTH+BRICK_SPACING), y=BRICK_OFFSET+i*(BRICK_HEIGHT+BRICK_SPACING))

        # identification for the bricks left
        self.__brick_left=brick_rows*brick_cols

        #lives left
        self.__life=num_lives

    def move_paddle(self,event):

        #lets the paddle be with the mouse
        if 0<event.x<self.window.width-self.paddle.width:
            self.paddle.x=event.x

    def start(self,event):
        # self.switch identifies if the game has started or not
        if self.switch==0:

            # turns on the switch
            self.switch=1

            # randomize the speed everytime
            self.__dx=random.randint(1,MAX_X_SPEED)
            if random.random() > 0.5:
                self.__dx = -self.__dx

            # while the player has lives left
            while self.__life>0:

                # moves the ball for a short distance
                self.ball.move(self.__dx, self.__dy)

                # identifies the collision when the ball touches the window
                self.collision_window()

                # identifies the collision when the ball touches the paddle
                self.collision_paddle()

                # identifies the collision for the bricks
                self.collision_brick()

                # if the ball went out of the bottom of window
                if self.ball.y>self.window.height:

                    # pauses the game
                    self.switch=0

                    # return the ball
                    self.window.add(self.ball, x=self.window.width / 2 - self.ball.width / 2,
                                    y=self.window.height / 2 - self.ball.height / 2)

                    # life minus one
                    self.__life-=1

                    # if there is no lives left
                    if self.__life==0:
                        gameover=GLabel('Game over')
                        gameover.font='-40-bold'
                        self.window.add(gameover,self.window.width/2-gameover.width/2,self.window.height/2-gameover.height/2)

                    break

                # if player successfully broke all bricks
                if self.__brick_left==0:
                    you_win = GLabel('You Win')
                    you_win.font = '-40-bold'
                    self.window.add(you_win, self.window.width / 2 - you_win.width / 2,
                                    self.window.height / 2 - you_win.height / 2)
                    break
                pause(15)

    def collision_window(self):
        if 0>self.ball.x:
            self.__dx=-self.__dx
        elif self.ball.x>self.window.width-self.ball.width:
            self.__dx = -self.__dx
        if 0>self.ball.y:
            self.__dy=-self.__dy

    def collision_paddle(self):
        # I changed some coefficients to let the ball feels like a real collision
        if self.paddle.x-self.ball.width<self.ball.x<self.paddle.x+self.paddle.width:
            if 0<self.paddle.y-self.ball.y-self.ball.height+7<7:
                if self.__dy>0:
                    self.__dy=-self.__dy

    def collision_brick(self):
        """
        uses the four points of the GOval to identify if there is any collision present
        """

        if self.ball.y<self.window.height/2:
            a=self.window.get_object_at(self.ball.x,self.ball.y)
            b=self.window.get_object_at(self.ball.x+self.ball.width,self.ball.y)
            c=self.window.get_object_at(self.ball.x,self.ball.y+self.ball.height)
            d=self.window.get_object_at(self.ball.x+self.ball.width,self.ball.y+self.ball.height)
            if a != None:
                self.window.remove(a)
                self.__brick_left-=1
                self.__dy=-self.__dy
            elif b!=None:
                self.window.remove(b)
                self.__brick_left -= 1
                self.__dy = -self.__dy
            elif c!=None:
                self.window.remove(c)
                self.__brick_left -= 1
                self.__dy = -self.__dy
            elif d!=None:
                self.window.remove(d)
                self.__brick_left -= 1
                self.__dy = -self.__dy

