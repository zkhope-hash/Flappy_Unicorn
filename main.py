import pygame
import random


def main():
    pygame.init()

    SCREEN = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Flappy Unicorn")

    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 40)
    title_font = pygame.font.Font(None, 70)

    # ---------------- UNICORN ----------------

    unicorn = pygame.image.load("unicorn.png").convert_alpha()
    unicorn = pygame.transform.scale(unicorn, (120, 120))

    START_X = 30
    GROUND_Y = 340

    unicorn_x = START_X
    unicorn_y = GROUND_Y

    vertical_velocity = 0
    gravity = 0.8
    jump_strength = -14
    is_jumping = False

    # ---------------- CLOUDS ----------------

    clouds = [
        [100, 50, 0.5],
        [300, 100, 0.3],
        [500, 40, 0.7]
    ]

    # ---------------- HURDLES ----------------

    hurdle_image = pygame.image.load("hurdle.png").convert_alpha()
    hurdle_image = pygame.transform.scale(
        hurdle_image,
        (130, 150)
    )

    hurdle_width = hurdle_image.get_width()
    hurdle_height = hurdle_image.get_height()

    hurdle_y = 340
    hurdle_speed = 5
    hurdle_gap = 20

    def create_hurdles():
        amount = random.randint(1, 2)

        new_hurdles = []
        hurdle_start_x = 700

        for i in range(amount):
            new_hurdles.append({
                "x": hurdle_start_x + i * (hurdle_width + hurdle_gap),
                "y": hurdle_y
            })

        return new_hurdles

    hurdles = create_hurdles()

    # ---------------- SCORE ----------------

    score = 0
    high_score = 0
    group_scored = False

    # ---------------- GAME STATE ----------------

    game_state = "start"

    # ---------------- GAME LOOP ----------------

    while True:

        # EVENTS
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.KEYDOWN:

                # START
                if game_state == "start":

                    if event.key == pygame.K_SPACE:
                        score = 0
                        hurdles = create_hurdles()
                        group_scored = False

                        unicorn_x = START_X
                        unicorn_y = GROUND_Y

                        game_state = "playing"

                # PLAYING
                elif game_state == "playing":

                    if (
                        event.key == pygame.K_UP
                        or event.key == pygame.K_w
                        or event.key == pygame.K_SPACE
                    ) and not is_jumping:

                        vertical_velocity = jump_strength
                        is_jumping = True

                # GAME OVER
                elif game_state == "game_over":

                    if event.key == pygame.K_SPACE:

                        score = 0

                        unicorn_x = START_X
                        unicorn_y = GROUND_Y

                        vertical_velocity = 0
                        is_jumping = False

                        hurdles = create_hurdles()
                        group_scored = False

                        game_state = "playing"

        # ==================================================
        # EVERYTHING HERE ONLY RUNS WHILE PLAYING
        # ==================================================

        if game_state == "playing":

            # Unicorn jumping
            if is_jumping:

                vertical_velocity += gravity
                unicorn_y += vertical_velocity

                if unicorn_y >= GROUND_Y:
                    unicorn_y = GROUND_Y
                    vertical_velocity = 0
                    is_jumping = False

            # Move hurdles
            for hurdle in hurdles:
                hurdle["x"] -= hurdle_speed

            # Unicorn hitbox
            unicorn_rect = pygame.Rect(
                int(unicorn_x) + 30,
                int(unicorn_y) + 35,
                65,
                55
            )

            hit_hurdle = False

            # Hurdle collision
            for hurdle in hurdles:

                # Smaller and LOWER hurdle hitbox
                hurdle_rect = pygame.Rect(
                    int(hurdle["x"]) + 70,
                    int(hurdle["y"]) + 80,
                    hurdle_width - 110,
                    hurdle_height - 100
                )

                if unicorn_rect.colliderect(hurdle_rect):
                    hit_hurdle = True

            # GAME OVER
            if hit_hurdle:

                game_state = "game_over"

                vertical_velocity = 0
                is_jumping = False

            # SCORE ONLY IF YOU DID NOT HIT
            else:

                if len(hurdles) > 0:

                    last_hurdle_right = max(
                        hurdle["x"] + hurdle_width
                        for hurdle in hurdles
                    )

                    # Cleared the entire hurdle group
                    if (
                        not group_scored
                        and last_hurdle_right < unicorn_x
                    ):
                        score += 1
                        group_scored = True

                        if score > high_score:
                            high_score = score

                    # Create next hurdle group
                    if last_hurdle_right < 0:
                        hurdles = create_hurdles()
                        group_scored = False

        # ---------------- BACKGROUND ----------------

        SCREEN.fill((135, 206, 250))

        # Clouds
        for cloud in clouds:

            cloud[0] += cloud[2]

            if cloud[0] > 700:
                cloud[0] = -60
                cloud[1] = random.randint(20, 150)

            cx, cy = cloud[0], cloud[1]

            pygame.draw.circle(
                SCREEN,
                (255, 255, 255),
                (int(cx), int(cy)),
                25
            )

            pygame.draw.circle(
                SCREEN,
                (255, 255, 255),
                (int(cx) - 25, int(cy) + 5),
                20
            )

            pygame.draw.circle(
                SCREEN,
                (255, 255, 255),
                (int(cx) + 25, int(cy) + 5),
                20
            )

        # Ground
        pygame.draw.rect(
            SCREEN,
            (34, 139, 34),
            (0, 400, 640, 80)
        )

        # ---------------- START SCREEN ----------------

        if game_state == "start":

            SCREEN.blit(
                unicorn,
                (unicorn_x, unicorn_y)
            )

            title = title_font.render(
                "FLAPPY UNICORN",
                True,
                (255, 255, 255)
            )

            instructions = font.render(
                "Press SPACE to Start",
                True,
                (0, 0, 0)
            )

            SCREEN.blit(
                title,
                title.get_rect(center=(320, 150))
            )

            SCREEN.blit(
                instructions,
                instructions.get_rect(center=(320, 230))
            )

        # ---------------- PLAYING ----------------

        elif game_state == "playing":

            # Draw hurdles
            for hurdle in hurdles:
                SCREEN.blit(
                    hurdle_image,
                    (int(hurdle["x"]), hurdle["y"])
                )

            # Draw unicorn
            SCREEN.blit(
                unicorn,
                (unicorn_x, unicorn_y)
            )

            score_text = font.render(
                f"Score: {score}",
                True,
                (0, 0, 0)
            )

            high_score_text = font.render(
                f"High Score: {high_score}",
                True,
                (0, 0, 0)
            )

            SCREEN.blit(score_text, (20, 20))
            SCREEN.blit(high_score_text, (20, 55))

        # ---------------- GAME OVER ----------------

        elif game_state == "game_over":

            game_over_text = title_font.render(
                "GAME OVER",
                True,
                (255, 255, 255)
            )

            final_score = font.render(
                f"Score: {score}",
                True,
                (0, 0, 0)
            )

            high_score_text = font.render(
                f"High Score: {high_score}",
                True,
                (0, 0, 0)
            )

            restart_text = font.render(
                "Press SPACE to Play Again",
                True,
                (0, 0, 0)
            )

            SCREEN.blit(
                game_over_text,
                game_over_text.get_rect(center=(320, 120))
            )

            SCREEN.blit(
                final_score,
                final_score.get_rect(center=(320, 190))
            )

            SCREEN.blit(
                high_score_text,
                high_score_text.get_rect(center=(320, 230))
            )

            SCREEN.blit(
                restart_text,
                restart_text.get_rect(center=(320, 290))
            )

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
