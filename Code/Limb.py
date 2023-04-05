import math
import pygame.draw

class Limb:
    def __init__(self, joint_pos_x, joint_pos_y, move_angle, range_of_motion, length, ego_angle, color='black'):
        # Reference Positions and Angles
        self.joint_pos_x = joint_pos_x
        self.joint_pos_y = joint_pos_y
        self.move_angle = move_angle
        self.move_perpendicular = move_angle + 90

        # Leg Properties
        self.length = length
        self.rest_ego_angle = ego_angle
        self.ego_angle = ego_angle
        self.alloc_angle = move_angle + ego_angle
        self.foot_position_x = self.joint_pos_x + math.cos(math.radians(self.alloc_angle)) * self.length
        self.foot_position_y = self.joint_pos_y + math.sin(math.radians(self.alloc_angle)) * self.length

        #Foot Properties
        self.foot_range_of_motion = 2*self.length*math.sin(math.radians(range_of_motion))
        self.rel_foot_position = 0

        self.stance_bool = True

        self.color = color

    def move(self, speed, turn, head_direction, x, y):
        foot_speed = speed
        # Limb is a right limb, animal is turning right, and limb is in stance phase
        if turn > 0 and 0 <= self.rest_ego_angle < 180 and self.stance_bool:
            # angular speed is adjusted by the turn speed of the animal
            limb_speed = math.degrees(math.asin(self.rel_foot_position / self.length)) - \
                           math.degrees(math.asin((self.rel_foot_position - foot_speed) / self.length)) - turn
            foot_speed = self.length * math.sin(math.radians(limb_speed))

        # Limb is a left limb, animal is turning left, and limb is in stance phase
        elif turn < 0 and 180 <= self.rest_ego_angle < 360 and self.stance_bool:
            stance_speed = math.degrees(math.asin(self.rel_foot_position / self.length)) - \
                           math.degrees(math.asin((self.rel_foot_position - foot_speed) / self.length)) - turn
            self.rel_foot_position -= self.length * math.sin(math.radians(limb_speed))
            foot_speed = self.length * math.sin(math.radians(limb_speed))

        # try:
        # Limb is swinging and reaches the end of its range of motion, flip stance_bool
        if not self.stance_bool and self.rel_foot_position + 2 * foot_speed > self.foot_range_of_motion / 2:
            self.rel_foot_position = self.foot_range_of_motion / 2
            self.stance_bool = True

        # Limb is 'stancing' and reaches the end of its range of motion, flip stance_bool
        elif self.stance_bool and self.rel_foot_position - foot_speed < -self.foot_range_of_motion / 2:
            self.rel_foot_position = -self.foot_range_of_motion / 2
            self.stance_bool = False

        if self.stance_bool: self.stance(foot_speed)
        if self.stance_bool: self.swing(foot_speed)

        self.update(x, y, head_direction)

        return


    def swing(self, foot_speed):
        self.rel_foot_position += 2*foot_speed
        self.ego_angle = self.rest_ego_angle+math.degrees(math.asin(self.rel_foot_position/self.length))

        return


    def stance(self, foot_speed):
        self.rel_foot_position -= foot_speed
        self.ego_angle = self.rest_ego_angle+math.degrees(math.asin(self.rel_foot_position/self.length))

        return


    def update(self, x, y, head_direction):
        self.joint_pos_x = x
        self.joint_pos_y = y
        self.move_angle = head_direction
        self.move_perpendicular = head_direction + 90

        self.alloc_angle = self.move_angle + self.ego_angle
        self.foot_position_x = self.joint_pos_x + math.cos(math.radians(self.alloc_angle)) * self.length
        self.foot_position_y = self.joint_pos_y + math.sin(math.radians(self.alloc_angle)) * self.length

        return

    def draw(self, display):
        pygame.draw.line(display, self.color, (self.joint_pos_x, self.joint_pos_y), (self.foot_position_x, self.foot_position_y), 5)