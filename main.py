import pygame

clock = pygame.time.Clock()

pygame.init()

image_path = '/data/data/org.game.myapp/files/app/'

width = 700
height = 400

screen = pygame.display.set_mode((width, height))

COLOR_WHITE = (255, 255, 255)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (0, 0, 128)

font = pygame.font.Font('fonts/font kodomarino.ttf', 40)
icon = pygame.image.load('images/icon.png').convert_alpha()
player_default = pygame.image.load('images/player_default.png').convert_alpha()
ghost = pygame.image.load('images/ghost.png').convert_alpha()
bullet = pygame.image.load('images/bullet.png').convert_alpha()
bg_sound = pygame.mixer.Sound( 'sounds/bg.mp3')
bg_sound.play()

pygame.display.set_icon(icon)

bg = pygame.image.load( 'images/background.png').convert_alpha()

walk_right = [
    pygame.image.load('images/player_right/1.png'),
    pygame.image.load('images/player_right/2.png'),
    pygame.image.load('images/player_right/3.png'),
    pygame.image.load('images/player_right/4.png'),
]

walk_left = [
    pygame.image.load('images/player_left/1.png'),
    pygame.image.load('images/player_left/2.png'),
    pygame.image.load('images/player_left/3.png'),
    pygame.image.load('images/player_left/4.png'),
]

player_anim_count = 0
player_speed = 5
player_x = 50
player_y = 215

is_jump = False
jump_count = 8

bullet_left = 5
bullet_out_time = None
bg_x = 0

ghost_timer = pygame.USEREVENT + 1
pygame.time.set_timer(ghost_timer, 5000)

ghost_list = []
bullet_list = []

gameplay = True

running = True
while running:
    clock.tick(15)

    screen.blit(bg, (bg_x, 0))
    screen.blit(bg, (bg_x + 700, 0))

    if gameplay:
        player_rect = walk_left[0].get_rect(topleft=(player_x, player_y))
        
        if ghost_list:
            for en in ghost_list:
                screen.blit(ghost, en)
                en.x -= 10

                if en.x <= 0:
                    ghost_list.remove(en)

                if player_rect.colliderect((en)):
                    gameplay = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            screen.blit(walk_left[player_anim_count], (player_x, player_y))
        elif keys[pygame.K_RIGHT]:
            screen.blit(walk_right[player_anim_count], (player_x, player_y))
        else:
            screen.blit(player_default, (player_x, player_y))

        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        elif keys[pygame.K_RIGHT]and player_x < width - 64:
            player_x += player_speed

        if not is_jump:
            if keys[pygame.K_SPACE]:
                is_jump = True
        else:
            if jump_count >= -8:
                if jump_count < 0:
                    player_y += (jump_count ** 2) / 2
                else:
                    player_y -= (jump_count ** 2) / 2
                jump_count -= 1
            else:
                is_jump = False
                jump_count = 8

        player_anim_count += 1
        if player_anim_count > 3:
            player_anim_count = 0

        bg_x -= 2
        if bg_x < -700:
            bg_x = 0
        
        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            if bullet_left > 0:
                bullet_list.append(bullet.get_rect(topleft=(player_x + 64, player_y + 32)))
                bullet_left -= 1
            elif bullet_out_time is None:
                bullet_out_time = pygame.time.get_ticks()

        if bullet_list:
            for b in bullet_list:
                screen.blit(bullet, b)
                b.x += 10
                if b.x > 700:
                    bullet_list.remove(b)

        if bullet_list and ghost_list:
            for b in bullet_list:
                for en in ghost_list:
                    if b.colliderect(en):
                        ghost_list.remove(en)
                        bullet_list.remove(b)
        
        if bullet_left == 0 and bullet_out_time is not None:
            if pygame.time.get_ticks() - bullet_out_time >= 5000:  # 5 seconds
                bullet_left = 5
                bullet_out_time = None
                text_bullet = font.render('Bullets refilled', True, COLOR_BLUE)
            else:
                text_bullet = font.render('No bullet left', True, COLOR_BLUE)
            screen.blit(text_bullet, (width // 2 - text_bullet.get_width() // 2, height // 2 - text_bullet.get_height() // 2))

        # Display remaining bullets
        text_bullets_left = font.render(f'Bullets: {bullet_left}', True, COLOR_BLUE)
        screen.blit(text_bullets_left, (width - text_bullets_left.get_width() - 10, 10))

    else:
        screen.fill(COLOR_WHITE)
        text = font.render('Game Over', True, COLOR_BLUE)
        screen.blit(text, (width // 2 - text.get_width() // 2, height // 2 - text.get_height() // 2))
        text_restart = font.render('Press R to restart', True, COLOR_BLUE)
        bg_sound.stop()
        screen.blit(text_restart, (width // 2 - text_restart.get_width() // 2, height // 2 - text_restart.get_height() // 2 + 50))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            gameplay = True
            player_x = 50
            player_y = 215
            ghost_list = []
            bullet_list = []  # Clear the bullet list
            bg_sound.play()
            bullet_left = 5
            bullet_out_time = None
    
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == ghost_timer:
            ghost_list.append(ghost.get_rect(topleft=(700, 215)))