import pygame
import random
import asyncio

async def main():
    pygame.init()
    SCREEN = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Flappy Unicorn")

    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 40)
    title_font = pygame.font.Font(None, 70)

#Unicorn Code
    unicorn = pygame.image.load("unicorn.png").convert_alpha()
    unicorn = pygame.transform.scale(unicorn, (120, 120))

    unicorn_x = 30
    GROUND_Y = 340

    start_x = unicorn_x
    unicorn_y = GROUND_Y

    vertical_velocity = 0
    gravity = 0.8
    jump_strength = -14
    is_jumping = False
#Clouds Code
    clouds = [
        [100, 50, 0.5],
        [300, 100, 0.3],
        [500, 40, 0.7]
    ]
#Hurdle Code
    hurdle_image = pygame.image.load("hurdle.png").convert_alpha()
    hurdle_image = pygame.transform.scale(hurdle_image, (100, 150))

    hurdle_width = hurdle_image.get_width()
    hurdle_height = hurdle_image.get_height()

    hurdle_y = 340
    hurdle_speed = 5
    hurdle_gap = -75

    def create_hurdles():
        amount = random.randint(1, 3)

        new_hurdles = []
        start_x = 700

        for i in range(amount):
            new_hurdles.append({
                "x": start_x + i * (hurdle_width + hurdle_gap),
                "y": hurdle_y
            })
        return new_hurdles

    hurdles = create_hurdles()
    #Score
    score = 0
    high_score = 0
    group_scored = False
    #Game State
    game_state = "start"
#Game Code
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.KEYDOWN:
                #Start Game
                if game_state == "start":

                    if event.key == pygame.K_SPACE:
                        score = 0
                        hurdles = create_hurdles()
                        group_scored = False
                        game_state = "playing"
                #Jump
                elif game_state == "playing":
                    if (
                            event.key == pygame.K_UP
                            or event.key == pygame.K_w
                            or event.key == pygame.K_SPACE
                    ) and not is_jumping:
                        vertical_velocity = jump_strength
                        is_jumping = True
                #Restart after game over
                elif game_state == "game_over":
                    if event.key == pygame.K_SPACE:
                        score = 0
                        unicorn_x = start_x
                        unicorn_y = GROUND_Y
                        vertical_velocity = 0
                        is_jumping = False
                        hurdles = create_hurdles()
                        group_scored = False
                        game_state = "playing"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if game_state == "start":
                    score = 0
                    hurdles = create_hurdles()
                    group_scored = False
                    game_state = "playing"
                elif game_state == "playing" and not is_jumping:
                    vertical_velocity = jump_strength
                    is_jumping = True
                elif game_state == "game_over":
                    score = 0
                    unicorn_x = start_x
                    unicorn_y = GROUND_Y
                    vertical_velocity = 0
                    is_jumping = False
                    hurdles = create_hurdles()
                    group_scored = False
                    game_state = "playing"
        #Playing Code
        if game_state == "playing":
            #Unicorn jumping
            if is_jumping:
                vertical_velocity += gravity
                unicorn_y += vertical_velocity

                if unicorn_y >= GROUND_Y:
                    unicorn_y = GROUND_Y
                    vertical_velocity = 0
                    is_jumping = False
        #Move Hurdles
            for hurdle in hurdles:
                hurdle["x"] -= hurdle_speed
        #Unicorn hitbox
            unicorn_rect = pygame.Rect(
                int(unicorn_x) + 20,
                int(unicorn_y) + 25,
                55,
                45
            )
            hit_hurdle = False
        #Hurdle Hitboxes
            for hurdle in hurdles:
                hurdle_rect = pygame.Rect(
                    int(hurdle["x"]) + 40,
                    int(hurdle["y"]) + 65,
                    hurdle_width - 55,
                    hurdle_height - 75
                )
                if unicorn_rect.colliderect(hurdle_rect):
                    hit_hurdle = True
        #Game Over
            if hit_hurdle:
                game_state = "game_over"
            else:
        #Score
                if len(hurdles) > 0:
                    last_hurdle_right = max(
                        hurdle["x"] + hurdle_width
                        for hurdle in hurdles
                    )
            # Score only after clearing whole hurdle
                    if (
                        not group_scored
                        and last_hurdle_right < unicorn_x
                    ):
                        score += 1
                        group_scored = True
                        if score > high_score:
                            high_score = score
                    if last_hurdle_right < 0:
                        hurdles = create_hurdles()
                        group_scored = False
# Clouds Code
        SCREEN.fill((135,206,250))
        for cloud in clouds:
            cloud[0] += cloud[2]
            if cloud[0] > 640 + 60:
                cloud[0] = -60
                cloud[1] = random.randint(20, 150)
            cx, cy = cloud[0], cloud[1]
            pygame.draw.circle(SCREEN, (255, 255, 255), (int(cx), int(cy)), 25)
            pygame.draw.circle(SCREEN, (255, 255, 255), (int(cx) - 25, int(cy) + 5), 20)
            pygame.draw.circle(SCREEN, (255, 255, 255), (int(cx) + 25, int(cy) + 5), 20)
#Ground Code
        pygame.draw.rect(SCREEN, (34, 139, 34), (0, 400, 640, 80))
#Scoreboard Code
        score_text = font.render(
            f"Score: {score}", True, (0,0,0)
        )
        high_score_text = font.render(
            f"High Score: {high_score}", True, (0, 0, 0)
        )
#Start Screen
        if game_state == "start":
            SCREEN.blit(unicorn, (unicorn_x, unicorn_y))
            title = title_font.render(
                f"FLAPPY UNICORN", True, (255, 255, 255)
            )
            instructions = font.render(
                "Press SPACE to Start", True, (0,0,0)
            )
            SCREEN.blit(title,title.get_rect(center=(320, 150))
            )
            SCREEN.blit(instructions,instructions.get_rect(center=(320, 230))
            )
        elif game_state == "playing":
            for hurdle in hurdles:
                SCREEN.blit(hurdle_image, (int(hurdle["x"]), hurdle["y"]))
                SCREEN.blit(unicorn,(unicorn_x, unicorn_y))
            score_text = font.render(
                f"Score: {score}", True, (0, 0, 0)
            )
            high_score_text = font.render(
                f"High Score: {high_score}", True, (0, 0, 0)
            )
            SCREEN.blit(score_text, (20, 20))
            SCREEN.blit(high_score_text, (50, 50))
        elif game_state == "game_over":
            game_over_text = title_font.render(
                f"GAME OVER", True, (255, 255, 255)
            )
            final_score = font.render(
                f"Score: {score}", True, (0, 0, 0)
            )
            high_score_text = font.render(
                f"High Score: {high_score}", True, (0, 0, 0)
            )
            restart_text = font.render(
                "Press SPACE to Play Again", True, (0,0,0)
            )
            SCREEN.blit(
                game_over_text, game_over_text.get_rect(center =(320, 120))
            )
            SCREEN.blit(
                final_score, final_score.get_rect(center=(320, 190))
            )
            SCREEN.blit(
                high_score_text, high_score_text.get_rect(center=(320, 230))
            )
            SCREEN.blit(
                restart_text, restart_text.get_rect (center=(320, 290))
            )
        pygame.display.flip()
        clock.tick(60)
        await asyncio.sleep(0)


if __name__ == "__main__":
    asyncio.run(main())



