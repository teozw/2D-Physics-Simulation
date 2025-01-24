import math


def seperate(ball1, ball2, extra, dx, dy) -> float:
    if dx == 0:
        angle = -math.pi/2 if dy < 0 else math.pi/2
    else:
        angle = round(math.atan(dy/dx), 10)
    delta_x = extra * round(math.cos(angle), 10)
    delta_y = extra * round(math.sin(angle), 10)

    if dx == 0:
        ball1.pos[1] += extra / 2
        ball2.pos[1] -= extra / 2
    else:
        ball1.pos[0] -= delta_x / 2
        ball1.pos[1] -= delta_y / 2
        ball2.pos[0] += delta_x / 2
        ball2.pos[1] += delta_y / 2

    return angle


def get_distance(pos1: list[float], pos2: list[float]) -> float:
    return math.sqrt((pos2[0] - pos1[0]) ** 2 + (pos2[1] - pos1[1]) ** 2)


def get_angle(pos1: list[float], pos2: list[float]) -> float:
    if abs(pos1[0] - pos2[0]) == 0:
        return math.pi/2
    else:
        return math.atan2((pos1[1] - pos2[1]), (pos1[0] - pos2[0]))
