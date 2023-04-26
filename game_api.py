import PIL
from PIL import Image, ImageChops, ImageGrab
import time
import functools
import math
from pynput.mouse import Button, Controller

STACK_COUNT = 6
INITIAL_CARDS = 6

GAME_UPPER_LEFT_X = 800
GAME_UPPER_LEFT_Y = 470
GAME_BOTTOM_RIGHT_X = 1762
GAME_BOTTOM_RIGHT_Y = 820

STARTING_X = 2
STARTING_Y = 2
CARD_WIDTH = 164
CARD_HEIGHT = 32
REF_WIDTH = 34
REF_HEIGHT = 24

class CardImageMatcher:
    def __init__(self):
        self.ref6 = list(Image.open("ref/6.png").getdata())
        self.ref7 = list(Image.open("ref/7.png").getdata())
        self.ref8 = list(Image.open("ref/8.png").getdata())
        self.ref9 = list(Image.open("ref/9.png").getdata())
        self.ref10 = list(Image.open("ref/10.png").getdata())
        self.refv = list(Image.open("ref/v.png").getdata())
        self.refd = list(Image.open("ref/d.png").getdata())
        self.refk = list(Image.open("ref/k.png").getdata())
        self.reft = list(Image.open("ref/t.png").getdata())

    def match(self, image):
        image_data = list(image.getdata())

        if image_data == self.ref6:
            return "6"
        if image_data == self.ref7:
            return "7"
        if image_data == self.ref8:
            return "8"
        if image_data == self.ref9:
            return "9"
        if image_data == self.ref10:
            return "10"
        if image_data == self.refv:
            return "v"
        if image_data == self.refd:
            return "d"
        if image_data == self.refk:
            return "k"
        if image_data == self.reft:
            return "t"
        raise Exception("Can't determine card value")

class GameApi:
    def __init__(self):
        self.stacks = []
        self.mouse = Controller()
        # Get window focus first
        self.__click_on((1280, 1015))
        self.__new_game()
        self.__populate_game_state()

    def __populate_game_state(self):
        game_image = ImageGrab.grab().crop((GAME_UPPER_LEFT_X, GAME_UPPER_LEFT_Y, GAME_BOTTOM_RIGHT_X, GAME_BOTTOM_RIGHT_Y))
        matcher = CardImageMatcher()

        for x in range(STACK_COUNT):
            stack = []
            for y in range(INITIAL_CARDS):
                current_x = STARTING_X + x * CARD_WIDTH
                current_y = STARTING_Y + y * CARD_HEIGHT
                current_card = game_image.crop((current_x, current_y, current_x + REF_WIDTH, current_y + REF_HEIGHT)).convert('L')
                stack.append(matcher.match(current_card))
            self.stacks.append(stack)

        print("Found card stacks:")
        print(self.stacks)

    def __click_on(self, position_tuple):
        self.mouse.position = position_tuple
        time.sleep(0.05)
        self.mouse.press(Button.left)
        time.sleep(0.05)
        self.mouse.release(Button.left)
        time.sleep(0.05)

    def __new_game(self):
        self.__click_on((1280, 1215))
        time.sleep(5)

    '''
    Card tuple consists of (stack index, card index).
    '''
    def click_card(self, card_tuple):

        stack_num = card_tuple[0]
        card_num = card_tuple[1]
        x_pos = GAME_UPPER_LEFT_X + STARTING_X + (stack_num * CARD_WIDTH)
        y_pos = GAME_UPPER_LEFT_Y + STARTING_Y + (card_num * CARD_HEIGHT)
        self.__click_on((x_pos, y_pos))
