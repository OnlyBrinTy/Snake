from numpy import zeros, subtract, int8
import pygame

pygame.init()


class Snake:
    def __init__(self, *shape):
        self.field = zeros(shape, dtype=int8)
        self.length = min(4, self.field.shape[1])
        head_x, head_y = self.length - 1, max(self.field.shape[0] // 2, 1) - 1
        tale_x = 0
        self.head_view = 'right'
        self.body_map = [{'cords': (x, head_y),
                          'view': 'right',
                          'bend_turn': None} for x in range(tale_x, head_x + 1)]
        self.tale_turns = []
        self.turns_cache = []
        self.apple_eaten = False
        self.clockwise_way = ('right', 'down', 'left', 'up', 'right')
        self.move_directions = {'up': lambda x, y: (x, y - 1), 'down': lambda x, y: (x, y + 1),
                                'left': lambda x, y: (x - 1, y), 'right': lambda x, y: (x + 1, y)}

        self.field[head_y, 0:head_x + 1] = 1

    def go(self):
        from snake_game import leave_game

        def move_check(way, ignore_1st_check=False):
            opposites = ({'up', 'down'}, {'left', 'right'})

            if way != self.head_view and {way, self.head_view} not in opposites or ignore_1st_check:
                head_x, head_y = self.move_directions[way](*self.body_map[-1]['cords'])

                return bool(-1 in (head_x, head_y) or 0 in subtract(self.field.shape, (head_y, head_x))
                            or self.field[head_y, head_x] == 1 and (head_x, head_y) != (self.body_map[0]['cords']))

        first_check_passed = False
        for direction in self.turns_cache.copy():
            test_result = move_check(direction)

            if test_result:
                first_check_passed = True
            elif test_result is False:
                self.turn(direction)
                self.turns_cache.remove(direction)
                break
            else:
                first_check_passed = False

            self.turns_cache.remove(direction)
        else:
            if first_check_passed or move_check(self.head_view, ignore_1st_check=True):
                leave_game(self.length, *self.field.shape)

        self.move()

    def move(self):
        def move_tail():
            tale_x, tale_y = self.body_map[0]['cords']
            self.field[tale_y, tale_x] = 0
            del self.body_map[0]

            if len(self.body_map) > 1:
                self.body_map[0]['view'] = self.body_map[1]['view']
            else:
                self.body_map[0]['view'] = self.head_view

        head_x, head_y = self.move_directions[self.head_view](*self.body_map[-1]['cords'])

        if self.field[head_y, head_x] == 2:
            self.length += 1
            self.apple_eaten = True
        else:
            move_tail()
            self.apple_eaten = False

        self.field[head_y, head_x] = 1
        self.body_map.append({'cords': (head_x, head_y),
                              'view': self.head_view,
                              'bend_turn': None})

    def turn(self, way):
        bend_turn = way == self.clockwise_way[self.clockwise_way.index(self.head_view) + 1]
        self.body_map[-1]['bend_turn'] = bend_turn
        self.head_view = way
        self.tale_turns.append((self.body_map[-1]['cords'], way))
