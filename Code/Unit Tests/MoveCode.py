from Code.Brain import *
from Code.Eye import *
from Code.Limb import *
from Code.helpers.collisions import *


class Animal:
    """
    Animal class defines an object which can move and see in a given environment. Class Animal "sees" with an Eye object
    which casts rays in an environment and encodes their distance and orientation into an SDR. Animal then interprets
    this encoding using Class Brain, which inplements Spatial Pooling to learn patterns of movement and sensation, using
    the learned patterns to decide on future movements.

    x - animal x-position
    y - animal y-position
    size - Animal size, that is drawn radius. Also important in collision calculations
    head_direction - direction of movement and center of Animal vision (degrees)
    field_of_view - angular width of Animal view
    """
    def __init__(self, x_pos, y_pos, size, head_direction, limb_length, field_of_view, num_of_rays, color='black'):
        self.x = x_pos
        self.y = y_pos
        self.l1_distance = 0
        self.linear_speed = 0
        self.angular_velocity = 0
        self.motions = [self.l1_distance, self.linear_speed, self.angular_velocity]

        self.size = size

        self.head_direction = head_direction
        self.field_of_view = field_of_view

        self.eye = Eye(x_pos,
                       y_pos,
                       head_direction,
                       field_of_view,
                       size,
                       1200,
                       num_of_rays)

        self.right_limb = Limb(joint_pos_x=x_pos,
                               joint_pos_y=y_pos,
                               move_angle=head_direction,
                               range_of_motion=120,
                               length=limb_length,
                               ego_angle=90)

        self.left_limb = Limb(joint_pos_x=x_pos,
                              joint_pos_y=y_pos,
                              move_angle=head_direction,
                              range_of_motion=120,
                              length=limb_length,
                              ego_angle=270)

        self.brain = Brain(self.eye.vision)

        self.color = color


    def look(self, box):
        """Function look takes in an environment and looks at it using Eye at Animal x and y in head_direction"""
        self.eye.see(box, self.x, self.y, self.head_direction)


    def think(self, track, move_speed, thought_step, learning):
        """Function think passes encoded Eye SDR to Brain for Spatial Pooling and Temporal Memory functions"""
        if self.brain.thought_count == 0:
            self.brain.initialize(self.eye.vision, self.motions)
            create_location_csv()

        self.motions = [self.l1_distance, self.linear_speed, self.angular_velocity]

        self.brain.think(track, self.eye.vision, self.motions, learning)

        if track == 1:
            self.record()

        if self.l1_distance>5*move_speed*thought_step:
            self.l1_distance = 0

        self.angular_velocity = 0
        return


    def record(self):
        write_activecell_to_csv(self.brain.cc1.L23_tm,
                                'L23_active',
                                self.brain.thought_count,
                                int(self.x),
                                int(self.y),
                                int(self.head_direction),
                                '-', '-')

        write_activecell_to_csv(self.brain.cc1.L4_tm,
                                'L4_active',
                                self.brain.thought_count,
                                int(self.x),
                                int(self.y),
                                int(self.head_direction),
                                '-', '-')

        write_activecell_to_csv(self.brain.cc1.L6a_tm,
                                'L6a_active',
                                self.brain.thought_count,
                                int(self.x),
                                int(self.y),
                                int(self.head_direction),
                                self.linear_speed,
                                self.angular_velocity)


    def move(self, step_size_move, box, direction):
        """Function move takes in a step size (speed), environment, and forward or backward direction
        to define movement. Animal moves within the environment checking for collisions as it goes"""
        if direction == 'forward':

            for wall in box.walls:
                collision = move_collision(self, wall, True)
                if collision:
                    break

            if not collision:
                self.linear_speed = step_size_move
                self.l1_distance += step_size_move

                self.x += step_size_move * math.cos(math.radians(self.head_direction))
                self.y += step_size_move * math.sin(math.radians(self.head_direction))

                self.left_limb.move(step_size_move, self.head_direction, 0, self.x, self.y)
                self.right_limb.move(step_size_move, self.head_direction, 0, self.x, self.y)


        if direction == 'backward':
            for wall in box.walls:
                collision = move_collision(self, wall, False)
                if collision:
                    break

            if not collision:
                self.linear_speed = -step_size_move
                self.l1_distance -= step_size_move
                self.x -= step_size_move * math.cos(math.radians(self.head_direction))
                self.y -= step_size_move * math.sin(math.radians(self.head_direction))


    def turn(self, xdir, ydir):
        theta = math.degrees(math.atan2(ydir,xdir))
        if theta < 0:
            theta+=360

        if abs((theta - self.head_direction))>180 and theta>self.head_direction:
            self.angular_velocity += round(theta - (self.head_direction+360))
        elif abs((theta - self.head_direction))>180 and theta<self.head_direction:
            self.angular_velocity += round((theta+360) - self.head_direction)
        else:
            self.angular_velocity += round(theta - self.head_direction)

        self.head_direction = round(theta)

        return



import math
import pygame.draw

class Limb:
    def __init__(self, joint_pos_x, joint_pos_y, move_direction, range_of_motion, length, ego_angle, color='black'):
        # Reference Positions and Angles
        self.joint_pos_x = joint_pos_x
        self.joint_pos_y = joint_pos_y
        self.move_direction = move_direction
        self.move_perpendicular = move_direction + 90

        # Leg Properties
        self.length = length
        self.rest_ego_angle = ego_angle
        self.ego_angle = ego_angle
        self.alloc_angle = move_direction + ego_angle
        self.foot_position_x = self.joint_pos_x + math.cos(math.radians(self.alloc_angle)) * self.length
        self.foot_position_y = self.joint_pos_y + math.sin(math.radians(self.alloc_angle)) * self.length

        #Foot Properties
        self.foot_range_of_motion = 2*self.length*math.sin(math.radians(range_of_motion))
        self.rel_foot_position = 0

        self.stance_bool = True

        self.color = color


    def move(self, speed, turn, head_direction, x, y):
        range_of_motion = int(self.foot_range_of_motion*(-19.5*turn/(self.foot_range_of_motion)+1))

        if self.rel_foot_position <= -range_of_motion/2 or self.rel_foot_position >= range_of_motion/2:
            self.stance_bool = not self.stance_bool

        self.swing(speed)
        self.stance(speed)

        self.update(x, y, head_direction)


    def swing(self, foot_speed):
        if not self.stance_bool:
            self.rel_foot_position += 2*foot_speed
            self.ego_angle += math.degrees(math.asin(self.rel_foot_position/self.length))

    def stance(self, foot_speed):
        if self.stance_bool:
            self.rel_foot_position -= foot_speed
            self.ego_angle += math.degrees(math.asin(self.rel_foot_position/self.length))


    def update(self, x, y, head_direction):
        self.joint_pos_x = x
        self.joint_pos_y = y
        self.move_direction = head_direction
        self.move_perpendicular = head_direction + 90

        self.alloc_angle = self.move_direction + self.ego_angle
        self.foot_position_x = self.joint_pos_x + math.cos(math.radians(self.alloc_angle)) * self.length
        self.foot_position_y = self.joint_pos_y + math.sin(math.radians(self.alloc_angle)) * self.length

        return