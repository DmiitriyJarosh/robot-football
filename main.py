# Made according to this (many thanks):
# https://www.youtube.com/watch?v=Mdg9ElewwA0&feature=emb_logo

import cv2
import copy
import numpy
import time

from typing import List, Tuple

import constants
from constants import Color
from models import Robot, MovingObstacle, Ball
from obstacle_avoidance import dump_obstacle_avoidance, drawable_dump_obstacle_avoidance
from obstacle_detection.mser import MSERObstacleDetector
from utils import cast_detector_coordinates, move_to_dot

drawable_obstacle_avoidance = drawable_dump_obstacle_avoidance
obstacle_avoidance = dump_obstacle_avoidance
obstacle_detection = MSERObstacleDetector()


def _generate_obstacles(cnt=10):
    barriers = []
    for i in range(cnt):
        barrier = MovingObstacle.create_randomized()
        barriers.append(barrier)
    return barriers


def _draw_edges(screen, predicted_coords: List[Tuple[float, float]], color: Tuple[int, int, int]):
    for coord in predicted_coords:
        x = int(constants.u0 + constants.k * coord[0])
        y = int(constants.v0 - constants.k * coord[1])
        cv2.circle(screen, (x, y), MovingObstacle.SCREEN_RADIUS, color, 2)


def _draw_scene(robot: Robot, ball: Ball, obstacles: List[MovingObstacle],
                ball_predicted_positions, barriers_predicted_positions):

    screen = numpy.full((constants.WINDOW_HEIGHT, constants.WINDOW_WIDTH, 3), Color.BLACK, dtype=numpy.uint8)

    robot.draw(screen)
    for obstacle in obstacles:
        obstacle.draw(screen)
    ball.draw(screen)

    screen_picture = copy.deepcopy(screen)
    _draw_edges(screen, ball_predicted_positions, Color.YELLOW)
    _draw_edges(screen, barriers_predicted_positions, Color.GREEN)
    return screen, screen_picture


def run_simulation(robot, ball, obstacles, simulation_delay=10, enable_detection=True, drawable_obs_avoidance=False):
    start_time = time.time()
    dt = constants.dt

    ball_predicted_positions = []
    barriers_predicted_positions = []

    target_achieved = False

    while True:
        screen, screen_picture = _draw_scene(
            robot, ball, obstacles, ball_predicted_positions, barriers_predicted_positions)

        if enable_detection:
            ball_predicted_positions, barriers_predicted_positions = obstacle_detection.forward(
                screen_picture, [(Color.RED, 1), (Color.LIGHTBLUE, 9)]
            )
            ball_predicted_positions = cast_detector_coordinates(ball_predicted_positions)
            barriers_predicted_positions = cast_detector_coordinates(barriers_predicted_positions)
        else:
            ball_predicted_positions = [ball.get_pos()]
            barriers_predicted_positions = [barrier.get_pos() for barrier in obstacles]

        # Planning
        #
        # Call obstacle avoidance algorithm and move to returned dot.
        #
        # At the moment it has the same call rate as simulation update rate:
        # it is called each quantum of time as the simulation updates.
        #
        # If obstacle_avoidance() call rate will be different than simulation update rate
        # then move_to_dot_again() should be called instead of obstacle_avoidance() and move_to_dot()
        # in this 'while' cycle if time of caliing obstacle_avoidance() is not reached yet.

        if drawable_obs_avoidance:
            target_x, target_y = drawable_obstacle_avoidance(
                screen, robot, ball_predicted_positions, barriers_predicted_positions)
        else:
            target_x, target_y = obstacle_avoidance(
                robot.get_pos(),robot.angle, ball_predicted_positions, barriers_predicted_positions)

        cv2.imshow('robot football',  cv2.cvtColor(screen, cv2.COLOR_BGR2RGB))

        vl, vr = move_to_dot(robot, ball, (target_x, target_y))

        ball.move(dt)

        robot.set_velocity(vl, vr)
        robot.move(dt)

        for player in obstacles:
            player.move(dt)

        dist_to_obstacle = robot.get_closest_dist_to_obstacle(obstacles)
        dist_to_target = robot.get_dist_to_target(ball)
        if dist_to_obstacle < 0.001 or dist_to_target < MovingObstacle.RADIUS + Robot.RADIUS:
            if dist_to_obstacle < 0.001:
                print('Crash!')
            else:
                target_achieved = True
            print(f'Result: {time.time() - start_time} sec')
            while cv2.getWindowProperty('robot football', cv2.WND_PROP_VISIBLE) == 1:
                cv2.waitKey(int(dt * 10))
            break

        cv2.waitKey(int(dt * simulation_delay))
        if cv2.getWindowProperty('robot football', cv2.WND_PROP_VISIBLE) < 1:
            break

    cv2.destroyAllWindows()
    return target_achieved


def _main():
    ball = Ball.create_randomized()
    obstacles = _generate_obstacles(cnt=constants.OBSTACLES_COUNT)
    robot = Robot(constants.x_start, constants.y_start, constants.theta_start)
    run_simulation(robot, ball, obstacles,
                   enable_detection=True,
                   drawable_obs_avoidance=constants.DRAWABLE_OBS_AVOIDANCE)


if __name__ == '__main__':
    _main()
