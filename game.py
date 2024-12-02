import pygame
import sys
import random
import numpy as np


#Initialization
pygame.init()
screen = pygame.display.set_mode((850, 650))
pygame.display.set_caption("Ping Pong")
clock = pygame.time.Clock()
player_score, opponent_score = 0, 0

# player sprite class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, up, down):
        super().__init__()
        self.image = pygame.Surface((25, 100))
        self.image.fill((255, 255, 255))  
        self.rect = self.image.get_rect(topleft=(x, y))  
        self.up_key = up
        self.down_key = down
        self.frozen = False

    def user_input(self):
        if not self.frozen: 
            keys = pygame.key.get_pressed()
            if keys[self.up_key]:
                self.rect.y -= 5
            if keys[self.down_key]:
                self.rect.y += 5
        
    

    def update(self):
        self.user_input()
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= 650:
            self.rect.bottom = 650

# ball sprite class
class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)  
        pygame.draw.circle(self.image, (255, 255, 255), (15, 15), 15)  
        self.rect = self.image.get_rect(center=(425, 325))
        self.speedx = 3
        self.speedy = 3
        self.last_hit = None

    def move(self):
        self.rect.x += self.speedx * 2
        self.rect.y += self.speedy * 2

    def update(self):
        self.move()

        # Ball collision with top and bottom walls
        if self.rect.top <= 0 or self.rect.bottom >= 650:
            self.speedy *= -1

        # Ball collision with left and right walls (scoring)
        if self.rect.left <= 0:
            global opponent_score
            opponent_score += 1
            self.reset_ball()

        if self.rect.right >= 850:
            global player_score
            player_score += 1
            self.reset_ball()

        # Ball collision with player paddle
        if self.rect.colliderect(player1.rect):
            self.reflect(player1)
            self.last_hit = 'player'

        # Ball collision with opponent paddle
        if self.rect.colliderect(opponent.rect):
            self.reflect(opponent)
            self.last_hit = 'opponent'
        #Ball collision with freeze power-up
        if self.rect.colliderect(freeze_rect):
            self.freeze_player_or_opponent()
            freeze_rect.center = (-9000,-9000)  

    def freeze_player_or_opponent(self):
        if player1.frozen or opponent.frozen:
            return  

        if self.last_hit == 'player' and not opponent.frozen:
            opponent.frozen = True
            pygame.time.set_timer(pygame.USEREVENT + 2, 1000)  
        elif self.last_hit == 'opponent' and not player1.frozen:
            player1.frozen = True
            pygame.time.set_timer(pygame.USEREVENT + 3, 1000)  
        freeze_rect.center = (random.randint(50, 800), random.randint(50, 600))


    def reset_ball(self):
        self.rect.center = (425, 325)
        self.speedx, self.speedy = random.choice([(-3, 3), (3, 3), (-3, -3), (3, -3)])
        global ball
        if len(ball) > 1:  
            for b in ball:
                if b != self:
                    ball.remove(b)  

    def reflect(self, paddle):
        relative_intersect_y = (self.rect.centery - paddle.rect.centery)
        normalized_intersect_y = relative_intersect_y / (paddle.rect.height / 2)

        self.speedy = normalized_intersect_y * 3

        if paddle == player1:
            self.speedx = abs(self.speedx)  
        else:
            self.speedx = -abs(self.speedx)  

        total_speed = 4  
        current_speed = np.sqrt(self.speedx**2 + self.speedy**2)
        self.speedx = (self.speedx / current_speed) * total_speed
        self.speedy = (self.speedy / current_speed) * total_speed

# Helper Functions

def draw_dotted_line():
    for y in range(0, 650, 30): 
        pygame.draw.line(screen, (255, 255, 255), (425, y), (425, y + 15), 2)

# Font
font = pygame.font.Font('font/Pixeltype.ttf', 50)
font_text = font.render("Press Space to Start", False, (255, 255, 255))
font_rect = font_text.get_rect(center=(425, 400))
game_name=font.render("Dark Pong", False, (255, 255, 255))
game_name_rect=game_name.get_rect(center=(425, 300))

def display_score():
    player1_score = font.render(f"Player : {str(player_score)}", False, (255, 255, 255))
    player1_rect = player1_score.get_rect(midleft=(100, 50))
    screen.blit(player1_score, player1_rect)

    player2_score = font.render(f"Opponent : {str(opponent_score)}", False, (255, 255, 255))
    player2_rect = player2_score.get_rect(midright=(750, 50))
    screen.blit(player2_score, player2_rect)

game_active = False
power_up = None

#timer
power_timer=pygame.USEREVENT+1
pygame.time.set_timer(power_timer, 6500)

#power
extra=pygame.image.load("power/extra.png").convert_alpha()
extra=pygame.transform.scale(extra, (100, 100))
extra_rect=extra.get_rect(center=(random.randint(50, 800), random.randint(50, 600)))

freeze=pygame.image.load("power/freeze.png").convert_alpha()
freeze=pygame.transform.scale(freeze, (50, 50))
freeze_rect=freeze.get_rect(center=(random.randint(50, 800), random.randint(50, 600)))

speed=pygame.image.load("power/speed.png").convert_alpha()
speed=pygame.transform.scale(speed, (50, 50))
speed_rect=speed.get_rect(center=(random.randint(50, 800), random.randint(50, 600)))



# player
player = pygame.sprite.Group()
player1 = Player(50, 325, pygame.K_w, pygame.K_s)
opponent = Player(800, 325, pygame.K_UP, pygame.K_DOWN)
player.add(player1)
player.add(opponent)

# ball
ball= pygame.sprite.Group()
ball.add(Ball())

# Extra ball function
def extra_ball():
    if ball.sprites():
        for ball_sprite in ball.sprites():  
            if ball_sprite.rect.colliderect(extra_rect): 
                new_ball = Ball()  
                new_ball.speedx, new_ball.speedy = 3, 3  
                if random.choice([True, False]):
                    new_ball.speedx = 3  
                else:
                    new_ball.speedx = -3  
                ball.add(new_ball)
                extra_rect.center = (-300, -300) 
                break  

# Player win message
def player_win():
    global player_score
    if player_score == 5:
        win_message = font.render("Player Wins", False, (255, 255, 255))
        win_rect = win_message.get_rect(center=(425, 325))
        global game_active
        game_active = False
        global opponent_score
        opponent_score = 0
        message = font.render("Press Space to restart", False, (255, 255, 255))
        message_rect = message.get_rect(center=(425, 375))

        screen.fill((0, 0, 0))
        screen.blit(win_message, win_rect)
        screen.blit(message, message_rect)
        pygame.display.update()
        win_time = pygame.time.get_ticks()

        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE: 
                        game_active = True
                        player_score = 0
                        opponent_score = 0
                        waiting_for_input = False 

            if pygame.time.get_ticks() - win_time >= 5000:
                game_active = False
                player_score = 0
                opponent_score = 0
                waiting_for_input = False 

# Opponent win message
def opponent_win():
    global opponent_score
    if opponent_score == 5:
        win_message = font.render("Opponent Wins", False, (255, 255, 255))
        win_rect = win_message.get_rect(center=(425, 325))
        global game_active
        game_active = False
        global player_score
        player_score = 0
        opponent_score = 0
        message = font.render("Press Space to restart", False, (255, 255, 255))
        message_rect = message.get_rect(center=(425, 375))

        screen.fill((0, 0, 0))
        screen.blit(win_message, win_rect)
        screen.blit(message, message_rect)
        pygame.display.update()
        win_time = pygame.time.get_ticks()

        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE: 
                        game_active = True
                        player_score = 0
                        opponent_score = 0
                        waiting_for_input = False 

            if pygame.time.get_ticks() - win_time >= 5000:
                game_active = False
                player_score = 0
                opponent_score = 0
                waiting_for_input = False 

# Main Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == power_timer:
            power_up = random.choice(['extra', 'freeze'])
            if power_up == 'extra':
                extra_rect.center = (random.randint(50, 800), random.randint(50, 600))
            elif power_up == 'freeze':
                freeze_rect.center = (random.randint(50, 800), random.randint(50, 600))
        if event.type == pygame.USEREVENT + 2:
            opponent.frozen = False
        if event.type == pygame.USEREVENT + 3:
            player1.frozen = False
        if game_active:
            continue
        else:
            screen.fill((169, 172, 55))
            screen.blit(game_name, game_name_rect)
            screen.blit(font_text, font_rect)
            display_score()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_active = True
    if game_active:
        screen.fill((0, 0, 0))
        display_score()
        player.draw(screen)
        player.update()

        ball.draw(screen)
        ball.update()
        draw_dotted_line()
        player_win()
        opponent_win()

        # Blit power-ups
        if power_up == 'extra':
            screen.blit(extra, extra_rect)
            extra_ball()
        elif power_up == 'freeze':
            screen.blit(freeze, freeze_rect)

    pygame.display.update()
    clock.tick(60)
