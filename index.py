import pygame
import random
import math
from pygame import mixer


# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 288
SCREEN_HEIGHT = 512
BASE_HEIGHT = 100
PIPE_GAP = 600
PIPE_SPEED = 1
GRAVITY = 0.25
JUMP_STRENGTH = -4.2

# Initialize game
def initialize_game():
    global screen, clock, font, birdimg, base_img, pipe_top, pipe_bottom, background, button_img
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Floppy Bird")
    clock = pygame.time.Clock()
    font = pygame.font.Font("flappy.ttf", 22)

    # Load images
    birdimg = pygame.image.load("photos/bluebird.png").convert_alpha()
    base_pic = pygame.image.load("photos/base.png").convert_alpha()
    base_img = pygame.transform.scale(base_pic, (500, BASE_HEIGHT))
    pipe_top = pygame.image.load("photos/pipetop.png").convert_alpha()
    pipe_bottom = pygame.image.load("photos/pipebottom.png").convert_alpha()
    background = pygame.image.load("photos/background.png").convert_alpha()
    button_img = pygame.image.load("photos/reset.png").convert_alpha()
    button_img = pygame.transform.scale(button_img, (button_img.get_width() // 2, button_img.get_height() // 2))

    # Initialize positions
    global birdX, birdY, birdChangeY, baseX, baseY, scroll, pipeuX, pipeuY, pipedX, pipedY, pipeuX1, pipeuY1, pipedX1, pipedY1
    birdX = 120
    birdY = 256
    birdChangeY = 0
    baseX = 0
    baseY = SCREEN_HEIGHT - BASE_HEIGHT
    scroll = 0
    pipeuX = 300
    pipeuY = random.randint(-450, -280)
    pipedX = 300
    pipedY = pipeuY + PIPE_GAP
    pipeuX1 = 500
    pipeuY1 = random.randint(-460, -280)
    pipedX1 = 500
    pipedY1 = pipeuY1 + PIPE_GAP

    # Game variables
    global score, finalscore, buttonX, buttonY, button_bollen, button_click_check, click_space
    score = 0
    finalscore = 0
    buttonX = 60
    buttonY = 280
    button_bollen = False
    button_click_check = False
    click_space = True

# Function to draw bird
def bird(x, y):
    screen.blit(birdimg, (x, y))

# Function to draw pipes
def draw_pipe(x, y):
    screen.blit(pipe_top, (x, y))
    screen.blit(pipe_bottom, (x, y + PIPE_GAP))

# Function to draw base
def base(x, y):
    no_of_tile = math.ceil(SCREEN_WIDTH / base_img.get_width()) + 1
    for i in range(no_of_tile):
        screen.blit(base_img, (i * base_img.get_width() + scroll, y))

# Function to display score
def scoreshow(x, y):
    text = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(text, (x, y))

    highscore = font.render("Highscore: " + str(finalscore), True, (255, 255, 255))
    screen.blit(highscore, (x + 130, y))

# Reset button
def button(x, y):
    screen.blit(button_img, (x, y))

# Main game loop
def main():
    initialize_game()
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    global birdChangeY
                    birdChangeY = JUMP_STRENGTH
                    swing_sound = mixer.Sound("music/snd_swoosh.wav")
                    swing_sound.play()


        # Update bird's vertical position
        global birdY
        birdY += birdChangeY
        birdChangeY += GRAVITY

        # Update the positions of the pipes
        global pipeuX, pipeuY, pipedX, pipedY, pipeuX1, pipeuY1, pipedX1, pipedY1
        pipeuX -= PIPE_SPEED
        pipeuX1 -= PIPE_SPEED

        # Update base position
        global scroll
        scroll -= PIPE_SPEED
        if abs(scroll) > base_img.get_width():
            scroll = 0

        # Check for pipe off-screen and reset position
        if pipeuX < -pipe_top.get_width():
            pipeuX = SCREEN_WIDTH
            pipeuY = random.randint(-450, -280)
            pipedX = pipeuX
            pipedY = pipeuY + PIPE_GAP

        if pipeuX1 < -pipe_top.get_width():
            pipeuX1 = SCREEN_WIDTH
            pipeuY1 = random.randint(-460, -280)
            pipedX1 = pipeuX1
            pipedY1 = pipeuY1 + PIPE_GAP

        # Collision detection
        bird_rect = pygame.Rect(birdX, birdY, birdimg.get_width(), birdimg.get_height())
        pipe_rect1 = pygame.Rect(pipeuX, pipeuY, pipe_top.get_width(), pipe_top.get_height())
        pipe_rect2 = pygame.Rect(pipeuX, pipedY, pipe_bottom.get_width(), pipe_bottom.get_height())
        pipe_rect3 = pygame.Rect(pipeuX1, pipeuY1, pipe_top.get_width(), pipe_top.get_height())
        pipe_rect4 = pygame.Rect(pipeuX1, pipedY1, pipe_bottom.get_width(), pipe_bottom.get_height())
        base_rect = pygame.Rect(baseX, baseY, base_img.get_width(), base_img.get_height())
        button_rect = pygame.Rect(buttonX, buttonY, button_img.get_width(), button_img.get_height())

        # Collision check
        if (bird_rect.colliderect(pipe_rect1) or
                bird_rect.colliderect(pipe_rect2) or
                bird_rect.colliderect(pipe_rect3) or
                bird_rect.colliderect(pipe_rect4) or
                bird_rect.colliderect(base_rect)):
            global button_bollen, score
            birdChangeY = 0
            birdY += 120
            if birdY > baseY:
                birdY = baseY
            button_bollen = True
            score = 0

        # Score check
        global finalscore
        if birdX == pipeuX or birdX == pipeuX1:
            score += 1
            if score > finalscore:
                finalscore = score
            score_sound = mixer.Sound("music/snd_point.wav")
            score_sound.play()        
 
        # Button click check
        global button_click_check
        Pos = pygame.mouse.get_pos()
        if button_rect.collidepoint(Pos):  
            if pygame.mouse.get_pressed()[0] == 1 and not button_click_check:
                button_click_check = True
                initialize_game()
                birdY = 256
                birdChangeY = 0
                score = 0
                button_bollen = False
                click_space = True



        # Draw everything on the screen
        
        screen.blit(background, (0, 0))  # Draw background
        draw_pipe(pipeuX, pipeuY)
        draw_pipe(pipeuX1, pipeuY1) 
        bird(birdX, birdY)
        base(baseX, baseY)
        scoreshow(12, 13)
        if button_bollen:
            button(buttonX, buttonY)
        pygame.display.update()  # Update display

        clock.tick(60)  # Limit to 60 frames per second

    pygame.quit()

if __name__ == "__main__":
    main()
 