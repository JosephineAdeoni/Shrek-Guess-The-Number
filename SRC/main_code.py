import pygame
from pygame.locals import *
import random
import sys

pygame.init()  # Initialize pygame

# Colors
white = (255, 255, 255)
black = (0, 0, 0)

# Screen dimensions
screen_height = 600
screen_width = 1000

# Text dimensions and font
textHeight = 170
textWidth = 330
fontSize = 18
textFont = pygame.font.SysFont('timesnewroman', fontSize)
buttonFont = pygame.font.SysFont('timesnewroman', fontSize)

# Button dimensions and colors
button_height = 50
button_width = 120
button_hover_colour = (69, 125, 67)
button_colour = (73, 146, 70)

# Set up screen
screen = pygame.display.set_mode((screen_width, screen_height))
background = pygame.image.load('../ASSETS/shrek_background.jpg')  # Ensure this file exists
pygame.display.set_caption("Shrek's Swampy Secret")

# Function to display text
def display_Text(text, font, text_colour, text_Width, text_Height):
    textImage = font.render(text, True, text_colour)
    screen.blit(textImage, (text_Width, text_Height))


# Button class
class Button:
    def __init__(self, position, text, font, button_colour, hover_colour):
        self.x_position = position[0]
        self.y_position = position[1]
        self.font = font
        self.button_colour = button_colour
        self.hover_colour = hover_colour
        self.text = text
        self.image = pygame.Surface((button_width, button_height))
        self.image.fill(button_colour)
        self.rect = self.image.get_rect(center=(self.x_position, self.y_position))
        self.text_surface = self.font.render(self.text, True, white)

    def update(self, screen):
        screen.blit(self.image, self.rect)
        text_rect = self.text_surface.get_rect(center=self.rect.center)
        screen.blit(self.text_surface, text_rect)

    def checkButtonInput(self, position):
        return self.rect.collidepoint(position)

    def changeColour(self, position):
        if self.rect.collidepoint(position):
            self.image.fill(self.hover_colour)
        else:
            self.image.fill(self.button_colour)


# Game class
class Game:
    def __init__(self, max_guesses):
        self.max_guesses = max_guesses
        self.reset_game()
        self.game_state = "menu_screen"

    def reset_game(self):
        self.guessesTaken = 0
        self.targetNumber = random.randint(1, 50)
        self.guess = ""
        self.feedback = ""
        self.game_over = False

    def start_game(self):
        self.reset_game()
        backButton = Button((70, 550), "BACK", buttonFont, button_colour, button_hover_colour)

        while True:
            mouse_position = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and not self.game_over:
                        if self.guess.isdigit():
                            guess_num = int(self.guess)
                            self.guessesTaken += 1
                            if guess_num == self.targetNumber:
                                self.feedback = "You guessed it! You win!"
                                self.game_over = True
                            elif self.guessesTaken == self.max_guesses:
                                self.feedback = f"Out of guesses! The number was {self.targetNumber}. You lose!"
                                self.game_over = True
                            elif guess_num < self.targetNumber:
                                self.feedback = "Your guess is too low!"
                            elif guess_num > self.targetNumber:
                                self.feedback = "Your guess is too high!"
                        self.guess = ""
                    elif event.key == pygame.K_BACKSPACE:
                        self.guess = self.guess[:-1]
                    else:
                        self.guess += event.unicode
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if backButton.checkButtonInput(mouse_position):
                        self.game_state = "menu_screen"
                        return

            # Display elements
            screen.blit(background, (0, 0))
            display_Text("Guess the number between 1-50!", textFont, black, textWidth, textHeight - 80)
            display_Text(f"Guesses Taken: {self.guessesTaken}", textFont, black, textWidth, textHeight - 60)
            display_Text(f"Your Guess: {self.guess}", textFont, black, textWidth, textHeight - 20)
            display_Text(f"Feedback: {self.feedback}", textFont, black, textWidth, textHeight)

            if self.game_over:
                display_Text("Game Over! Press BACK to return to the menu.", textFont, black, textWidth, textHeight + 20)

            backButton.changeColour(mouse_position)
            backButton.update(screen)
            pygame.display.update()


# Main loop
game = Game(15)

while True:
    screen.blit(background, (0, 0))
    if game.game_state == "menu_screen":
        display_Text("WHAT ARE YOU DOING IN MY SWAMP!!", textFont, black, textWidth, textHeight - 80)
        display_Text("Pick a level and guess the number between 1 and 50!", textFont, black, textWidth, textHeight - 60)

        mouse_position = pygame.mouse.get_pos()
        easyButton = Button((380, 220), "EASY", buttonFont, button_colour, button_hover_colour)
        mediumButton = Button((530, 220), "MEDIUM", buttonFont, button_colour, button_hover_colour)
        hardButton = Button((680, 220), "HARD", buttonFont, button_colour, button_hover_colour)

        for button in [easyButton, mediumButton, hardButton]:
            button.changeColour(mouse_position)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if easyButton.checkButtonInput(mouse_position):
                    game.max_guesses = 15
                    game.start_game()
                if mediumButton.checkButtonInput(mouse_position):
                    game.max_guesses = 10
                    game.start_game()
                if hardButton.checkButtonInput(mouse_position):
                    game.max_guesses = 5
                    game.start_game()

    pygame.display.update()





 