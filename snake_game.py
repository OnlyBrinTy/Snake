def leave_game(points, height, width):
    if points < height * width:
        print(f"You've lost.\nTotal score: {points}")
    else:
        print(f"You've won!!!\nTotal score: {points}")

    exit()


def if_game_is_won(func):
    def check(matrix):
        if (matrix == 1).all():
            screen.fill(COLOR['GREEN'])
            pygame.display.flip()
            leave_game(snake.length, HEIGHT, WIDTH)
        else:
            return func(matrix)

    return check


def cords_of_num(matrix, value):
    return array(where(matrix == value)).transpose()


@if_game_is_won
def place_apple(field):
    field[tuple(choice(cords_of_num(field, 0)))] = 2

    return field


@if_game_is_won
def display_frame(field):
    def adapt(x, y):
        return x * CELL_SIZE, y * CELL_SIZE

    def draw_background():
        screen.fill(COLOR['GREEN'])

        for cords in filterfalse(lambda *t: sum(*t) % 2 == 0, product(range(WIDTH), range(HEIGHT))):
            pygame.draw.rect(screen, COLOR['DARK_GREEN'], pygame.Rect(*adapt(*cords), *(CELL_SIZE,) * 2))

    def draw_snake():
        for i, part in enumerate(snake.body_map):
            if i == 0:
                screen.blit(rotations[part['view']](PART['TAIL']), adapt(*part['cords']))
            elif part['bend_turn'] is None:
                if i == len(snake.body_map) - 1:
                    screen.blit(rotations[part['view']](PART['HEAD']), adapt(*part['cords']))
                else:
                    screen.blit(rotations[part['view']](PART['BODY']), adapt(*part['cords']))
            else:
                right_flipped_bend = pygame.transform.flip(PART['BEND'], part['bend_turn'], False)
                screen.blit(rotations[part['view']](right_flipped_bend), adapt(*part['cords']))

    def draw_apple():
        y, x = cords_of_num(field, 2)[0]
        screen.blit(PART['APPLE'], adapt(x, y))

    draw_background()
    draw_snake()
    draw_apple()

    pygame.display.update()


def main():
    directions = {pygame.K_UP: 'up', pygame.K_DOWN: 'down',
                  pygame.K_LEFT: 'left', pygame.K_RIGHT: 'right'}
    clock = pygame.time.Clock()
    first_frame = True
    game_paused = False

    def manage_pygame_events():
        nonlocal game_paused, clock

        def unpause():
            snake.turns_cache.clear()
            pygame.time.delay(1000 // FPS)
            clock.tick(FPS)
            manage_pygame_events()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                leave_game(snake.length, HEIGHT, WIDTH)
            elif event.type == pygame.KEYDOWN:
                if event.key in directions and not game_paused:
                    if len(snake.turns_cache) == 2:
                        del snake.turns_cache[0]

                    snake.turns_cache.append(directions[event.key])
                elif event.key == pygame.K_SPACE:
                    game_paused = not game_paused

                    if not game_paused:
                        unpause()

    while True:
        manage_pygame_events()
        if game_paused:
            continue

        if first_frame:
            field = snake.field
            field = place_apple(field)
            first_frame = False
        else:
            snake.go()
            field = snake.field

            if snake.apple_eaten:
                pygame.display.set_caption(f'score: {snake.length}')
                field = place_apple(field)

        display_frame(field)
        clock.tick(FPS)


if __name__ == '__main__':
    from snake import Snake
    from random import choice
    from itertools import product, filterfalse
    from numpy import where, array
    import pygame

    pygame.init()

    couples = zip(('TAIL', 'BODY', 'BEND', 'HEAD', 'APPLE'),
                  ('snake_tail_up.png', 'snake_body_up.png',
                   'snake_bend_up_left.png', 'snake_head_up.png', 'apple.png'))
    rotations = {'up': lambda img: img, 'down': lambda img: pygame.transform.rotate(img, 180),
                 'left': lambda img: pygame.transform.rotate(img, 90),
                 'right': lambda img: pygame.transform.rotate(img, -90)}
    PART = {part: pygame.image.load(fr'pictures\{name}') for part, name in couples}
    COLOR = {'GREEN': (12, 85, 28), 'DARK_GREEN': (10, 69, 23)}
    WIDTH, HEIGHT = 16, 16
    CELL_SIZE = 16
    FPS = 8

    snake = Snake(HEIGHT, WIDTH)
    screen = pygame.display.set_mode((WIDTH * CELL_SIZE, HEIGHT * CELL_SIZE), pygame.SCALED | pygame.RESIZABLE,
                                     vsync=True)
    pygame.display.set_icon(pygame.image.load(r'pictures\snake_icon.png'))
    pygame.display.set_caption(f'score: {snake.length}')

    main()
