import numpy as np
import csv
from CorticalColumn import *

from Code.helpers.neural_activity_visualization import *

class Brain:
    """
    Class Brain maintains the relationship between the senses of the animal and the cortical columns that process the them.
    It also manages the learning and recording of the animal's activity, and can, in the future, be used to manage intercolumn connections.
    """
    def __init__(self, vision, learning, record_activity):
        self.thought_count = 0
        self.cc1 = CorticalColumn(vision)
        self.learning = learning
        self.record_activity = record_activity

    def initialize(self, vision, l1_distance, linear_movement, angular_movement):
        self.thought_count += 1
        initialize_csv()
        self.cc1.initialize(vision, l1_distance, linear_movement, angular_movement)

    def think(self, x, y, head_direction, vision, l1_distance, speed, angular_velocity):
        self.thought_count += 1
        self.cc1.process(vision, l1_distance, speed, angular_velocity, self.learning)
        if self.record_activity:
            self.record(x, y, head_direction, speed, angular_velocity)

    def record(self, x, y, head_direction, speed, angular_velocity):
        write_activecell_to_csv(self.cc1.L23_tm,
                                'L23_active',
                                self.thought_count,
                                int(x),
                                int(y),
                                int(head_direction),
                                '-', '-')

        write_activecell_to_csv(self.cc1.L4_tm,
                                'L4_active',
                                self.thought_count,
                                int(x),
                                int(y),
                                int(head_direction),
                                '-', '-')

        write_activecell_to_csv(self.cc1.L6a_tm,
                                'L6a_active',
                                self.thought_count,
                                int(x),
                                int(y),
                                int(head_direction),
                                speed,
                                angular_velocity)

    # Function to laterally connect two cortical columns
    def cc_connect(self,cc1,cc2):
        cc1.cc_feedback(cc2)
        cc2.cc_feedback(cc1)

    # Function to turn on the learning state of the brain
    def start_learning(self):
        self.learning = True

    # Function to turn off the learning state of the brain
    def stop_learning(self):
        self.learning = False

    # Function to turn of the recording state of the brain
    def start_recording(self):
        self.record_activity = True

    # Function to turn off the recording state of the brain
    def stop_recording(self):
        self.record_activity = False