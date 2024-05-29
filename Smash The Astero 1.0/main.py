import pygame
from sys import exit
from time import time
from random import randint, randrange, choices
import os

# Classes
class Asteroids(pygame.sprite.Sprite):

    def __init__(self, type):
        super().__init__()
        # Simple Asteroids
        self.type = type
        if type == "simple_asteroid":
            simple_asteroids = pygame.image.load('asteroids/simple_asteroid.png').convert_alpha()
            simple_asteroids = pygame.transform.rotozoom(simple_asteroids, 0, 0.12)
            self.asteroids_surf = simple_asteroids
        else:
            bomb_asteroids = pygame.image.load('asteroids/bomb_asteroid.png').convert_alpha()
            bomb_asteroids = pygame.transform.rotozoom(bomb_asteroids, 0, 0.12)
            self.asteroids_surf = bomb_asteroids

        blast_animation_1 = pygame.image.load('asteroids/blast_animation/animation_1.png').convert_alpha()
        blast_animation_2 = pygame.image.load('asteroids/blast_animation/animation_2.png').convert_alpha()
        blast_animation_3 = pygame.image.load('asteroids/blast_animation/animation_3.png').convert_alpha()

        frames = [blast_animation_1, blast_animation_2, blast_animation_3]
        self.frames = [pygame.transform.rotozoom(frame, 90, 0.2) for frame in frames]

        self.blast_animation_index = 0
        self.blast_astero = self.frames[self.blast_animation_index]

        self.image = self.asteroids_surf
        self.rect = self.image.get_rect(midbottom=(randint(20, 380), 0))
        self.collided = False
        self.blast_hit = pygame.mixer.Sound('SFX/blast_hit.wav') 
        self.block_hit = pygame.mixer.Sound('SFX/block_hit.wav') 

    def get_hit(self):
        
        if self.collission():
            if self.type == "simple_asteroid":
                
                self.blast_animation()
            elif self.type == "bomb_asteroid":
                self.blast_hit.play()
                self.blast_animation()
                game_over()
                pygame.quit()
                exit()

    def blast_animation(self):
       
        if self.collission():
            self.blast_animation_index += 0.5
            if self.blast_animation_index >= len(self.frames):
                self.block_hit.play()
                self.kill()
                if self in self.groups():
                    self.groups().remove(self)
                global score
                score += 1
            else:
                
                self.blast_astero = self.frames[int(self.blast_animation_index)]
                self.image = self.blast_astero
        else:
            self.image = self.asteroids_surf  # Reset the image if collision is not happening

    def collission(self):
        if mouse_down:
            mouse_pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse_pos):
                return True
        else:
            return False

    def update(self):
        self.rect.y += 5
        if self.rect.y >= 700:
            self.kill()  # Add any movement or update logic here
        self.get_hit()

def show_score():
    global digit_images, shadow_images  # Ensure these are accessible within the function

    score_str = str(score)
    x_offset = 10
    y_offset = 10
    shadow_offset = 2  # Offset for shadow
    sapcing = -30

    for digit in score_str:
        digit_image = digit_images[int(digit)]
        shadow_image = shadow_images[int(digit)]

        # Draw shadow first
        shadow_pos = (x_offset + shadow_offset, y_offset + shadow_offset)
        screen.blit(shadow_image, shadow_pos)

        # Draw the actual digit
        digit_pos = (x_offset, y_offset)
        screen.blit(digit_image, digit_pos)

        x_offset += digit_image.get_width() + sapcing

def pause_game():
    paused = True

    bf_img = pygame.image.load('buttons/bf.png').convert()
    bf_img = pygame.transform.smoothscale(bf_img, (400, 700))

    resume_button = pygame.Rect(150, 200, 100, 50)
    restart_button = pygame.Rect(150, 300, 100, 50)
    quit_button = pygame.Rect(150, 400, 100, 50)

    resume_img = pygame.image.load('buttons/resume.png').convert_alpha()
    resume_img = pygame.transform.rotozoom(resume_img,0,0.1)

    resume_hover_img = pygame.image.load('buttons/resume.png').convert_alpha()
    resume_hover_img = pygame.transform.rotozoom(resume_hover_img,0,0.09)

    restart_img = pygame.image.load('buttons/restart.png').convert_alpha()
    restart_img = pygame.transform.rotozoom(restart_img,0,0.1)

    restart_hover_img = pygame.image.load('buttons/restart.png').convert_alpha()
    restart_hover_img = pygame.transform.rotozoom(restart_hover_img,0,0.09)

    quit_img = pygame.image.load('buttons/quit.png').convert_alpha()
    quit_img = pygame.transform.rotozoom(quit_img,0,0.1)

    quit_hover_img = pygame.image.load('buttons/quit.png').convert_alpha()
    quit_hover_img = pygame.transform.rotozoom(quit_img,0,0.9)




    click_tone = pygame.mixer.Sound('SFX/click_tone.wav')
    jump_button = pygame.mixer.Sound('SFX/jump_button.wav')

    # Dictionary to keep track of which buttons have had their sounds played
    button_sounds_played = {
        "resume": False,
        "restart": False,
        "quit": False
    }

    while paused:
        mouse_pos = pygame.mouse.get_pos()
        mouse_over_button = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if resume_button.collidepoint(event.pos):
                    click_tone.play()
                    paused = False
                if restart_button.collidepoint(event.pos):
                    click_tone.play()
                    main()  # Call the main function to restart the game
                if quit_button.collidepoint(event.pos):
                    click_tone.play()
                    pygame.quit()
                    exit()

        screen.blit(bf_img, (0, 0))  # Clear screen with black

        # Draw buttons with hover effect
        if resume_button.collidepoint(mouse_pos):
            if not button_sounds_played["resume"]:
                jump_button.play()
                button_sounds_played["resume"] = True
            screen.blit(resume_hover_img, (resume_button.centerx - resume_hover_img.get_width() // 2, resume_button.centery - resume_hover_img.get_height() // 2))
            mouse_over_button = True
        else:
            button_sounds_played["resume"] = False
            screen.blit(resume_img, (resume_button.centerx - resume_img.get_width() // 2, resume_button.centery - resume_img.get_height() // 2))

        if restart_button.collidepoint(mouse_pos):
            if not button_sounds_played["restart"]:
                jump_button.play()
                button_sounds_played["restart"] = True
            screen.blit(restart_hover_img, (restart_button.centerx - restart_hover_img.get_width() // 2, restart_button.centery - restart_hover_img.get_height() // 2))
            mouse_over_button = True
        else:
            button_sounds_played["restart"] = False
            screen.blit(restart_img, (restart_button.centerx - restart_img.get_width() // 2, restart_button.centery - restart_img.get_height() // 2))

        if quit_button.collidepoint(mouse_pos):
            if not button_sounds_played["quit"]:
                jump_button.play()
                button_sounds_played["quit"] = True
            screen.blit(quit_hover_img, (quit_button.centerx - quit_hover_img.get_width() // 2, quit_button.centery - quit_hover_img.get_height() // 2))
            mouse_over_button = True
        else:
            button_sounds_played["quit"] = False
            screen.blit(quit_img, (quit_button.centerx - quit_img.get_width() // 2, quit_button.centery - quit_img.get_height() // 2))

        # Change cursor to pointer if hovering over any button
        if mouse_over_button:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        pygame.display.flip()
        clock.tick(Frame_rate)


def show_intro():
    intro_img = pygame.image.load('intro/intro.png').convert()
    intro_img = pygame.transform.smoothscale(intro_img, (400, 700))
    img_p =  pygame.image.load('press sapce to play the game.png').convert_alpha()
    img_p = pygame.transform.rotozoom(img_p,0,0.3)

    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    intro = False

        screen.blit(intro_img, (0, 0))
        screen.blit(img_p, (-27, 380))

        pygame.display.update()
        clock.tick(Frame_rate)

def show_score_game_over():
    global digit_images, shadow_images, high_score  # Ensure these are accessible within the function

    score_str = str(score)
    x_offset = 150
    y_offset = 482
    shadow_offset = 2  # Offset for shadow
    sapcing = -40

    for digit in score_str:
        digit_image = digit_images[int(digit)]
        shadow_image = shadow_images[int(digit)]

        # Draw shadow first
        shadow_pos = (x_offset + shadow_offset, y_offset + shadow_offset)
        screen.blit(shadow_image, shadow_pos)

        # Draw the actual digit
        digit_pos = (x_offset, y_offset)
        screen.blit(digit_image, digit_pos)

        x_offset += digit_image.get_width() + sapcing

    if int(score) > int(high_score):
        high_score = score
        with open('high_score.txt','w') as file:
            file.write(str(high_score))


def high_score_game_over():
    global digit_images, shadow_images, high_score  # Ensure these are accessible within the function

    score_str = str(high_score)
    x_offset = 265
    y_offset = 543
    shadow_offset = 2  # Offset for shadow
    sapcing = -36

    for digit in score_str:
        digit_image = digit_images[int(digit)]
        shadow_image = shadow_images[int(digit)]

        # Draw shadow first
        shadow_pos = (x_offset + shadow_offset, y_offset + shadow_offset)
        screen.blit(shadow_image, shadow_pos)

        # Draw the actual digit
        digit_pos = (x_offset, y_offset)
        screen.blit(digit_image, digit_pos)

        x_offset += digit_image.get_width() + sapcing

def game_over():
    pygame.init()

    screen_width = 400
    screen_height = 700

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Smash The Astero")

    # FPS
    clock = pygame.time.Clock()
    Frame_rate = 60

    game_over_img = pygame.image.load('game over/game_over.png').convert_alpha()
    game_over_img = pygame.transform.rotozoom(game_over_img,0,0.38)
    img_p =  pygame.image.load('press sapce to play the game.png').convert_alpha()
    img_p = pygame.transform.rotozoom(img_p,0,0.3)

    score = pygame.image.load('game over/score.png').convert_alpha()
    score = pygame.transform.rotozoom(score,0,0.18)
    
    game_over = True
    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_over = False                   
                    main()
                    

        screen.blit(game_over_img, (0, 100))
        screen.blit(img_p,(-27,300))
        screen.blit(score, (12, 500))
        show_score_game_over()
        high_score_game_over()

        pygame.display.update()
        clock.tick(Frame_rate)

def main():
    global start_time, screen, clock, Frame_rate, mouse_down, score, high_score, digit_images, shadow_images, bg_surf, asteroids

    # Initializing the game
    pygame.init()

    screen_width = 400
    screen_height = 700

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Smash The Astero")

    # FPS
    clock = pygame.time.Clock()
    Frame_rate = 60

    # Global Variables
    mouse_down = True
    score = 0
    high_score = 0
    if not os.path.exists('high_score.txt'):
        with open('high_score.txt', 'w') as file:
            file.write('0')

    with open('high_score.txt', 'r') as file:
        content = file.read().strip()
        if content.isdigit():
            high_score = int(content)
        else:
            high_score = 0
            with open('high_score.txt', 'w') as file:
                file.write('0')    

 
    # Variables
    spawn_astero_event = randrange(200, 700)

    # Load digit images and scale them
    shadow_images = []
    digit_images = [pygame.image.load(f'numbers/{i}.png').convert_alpha() for i in range(10)]
    digit_images = [pygame.transform.rotozoom(img, 0, 0.03) for img in digit_images]

    # Create shadow images
    shadow_images = []
    for img in digit_images:
        shadow_img = pygame.Surface(img.get_size(), pygame.SRCALPHA)
        shadow_img.fill((0, 0, 0, 255))  # Black color with full opacity
        shadow_img.blit(img, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        shadow_images.append(shadow_img)

    bg_surf = pygame.image.load('background.png').convert()
    bg_surf = pygame.transform.smoothscale(bg_surf, (400, 700))

    # Asteroids Class
    asteroids = pygame.sprite.Group()

    # Events
    SPAWNASTEROIDS = pygame.USEREVENT + 1
    pygame.time.set_timer(SPAWNASTEROIDS, spawn_astero_event)
    

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause_game()  # Call pause_game function when ESC is pressed
           

            if event.type == SPAWNASTEROIDS:
                asteroids.add(Asteroids(choices(["simple_asteroid", "bomb_asteroid"], [0.75, 0.25])[0]))
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_down = True
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_down = False
    


        if start_time == 0:
            start_time = time()
            show_intro() 
        screen.blit(bg_surf, (0, 0))
        asteroids.draw(screen)
        asteroids.update()
        show_score()
    
        pygame.display.update()
        clock.tick(Frame_rate)

pygame.init()

screen_width = 400
screen_height = 700

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Smash The Astero")

bg_music = pygame.mixer.music.load('Music/Synthetic Surge.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.4)

global start_time
start_time = 0

if __name__ == "__main__":
    main()