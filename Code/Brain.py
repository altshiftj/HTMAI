import numpy as np
import csv
import htm
from htm.algorithms import SpatialPooler as SP
from htm.algorithms import TemporalMemory as TM
import htm.bindings.encoders as enc
from htm.bindings.sdr import *
from CorticalColumn import *

# from Code.helpers.cells_to_csv import *
from Code.helpers.neural_activity_read_write import initialize_output, write_active_cells_to_csv

class Brain:

    def __init__(self, vision, learning, record_activity, cc_width, cc_layer_depth):
        """
        Class Brain defines an object which takes encoded SDRs from sensory objects
        and carries out the operation of Spatial Pooling on the SDR. Further implementation to be determined
        (i.e. neuron interconnections, minicolumns, temporal memory, converting SDR input into motor outputs, etc)

        :param vision           (list): a list of rays representing the animal's vision
        :param learning         (bool): indicates whether the Brain is in learning mode
        :param record_activity  (bool): indicates whether the Brain should record its activity
        :param cc_width         (int): indicates the number of minicolumns in the cortical column
        :param cc_layer_depth   (int): indicates the depth of each layer within the cortical column
        """

        self.thought_count = 0
        self.cc1 = CorticalColumn(vision, cc_width, cc_layer_depth)
        self.learning = learning
        self.record_activity = record_activity

    def initialize(self, vision, distance_traveled, linear_movement, angular_movement):
        self.thought_count += 1
        initialize_output()
        self.cc1.initialize(vision, distance_traveled, linear_movement, angular_movement)

    def think(self, x, y, head_direction, vision, distance_traveled, speed, angular_velocity):
        """
       Process the given parameters, increment the thought_count, and optionally record the activity.

       :param x                     (int): The x-coordinate of the animal's position.
       :param y                     (int): The y-coordinate of the animal's position.
       :param head_direction        (int): The direction the animal is facing.
       :param vision                (list): a list of rays representing the animal's vision
       :param distance_traveled     (int): The distance the animal has traveled so far.
       :param speed                 (int): The current speed of the animal.
       :param angular_velocity      (int): The current angular velocity of the animal.
       """
        self.thought_count += 1
        self.cc1.process(vision, distance_traveled, speed, angular_velocity, self.learning)
        if self.record_activity:
            self.record(x, y, head_direction, speed, angular_velocity)

    def record(self, x, y, head_direction, speed, angular_velocity):
        """
        Record the neural activity of the animal by writing active cell information of each cortical column layer
        to CSV files.

        :param x                    (int): The x-coordinate of the animal's position.
        :param y                    (int): The y-coordinate of the animal's position.
        :param head_direction       (int): The direction the animal is facing.
        :param speed                (int): The current speed of the animal.
        :param angular_velocity     (int): The current angular velocity of the animal.
        """
        write_active_cells_to_csv(self.cc1.L23_tm,
                                'L23_active',
                                self.thought_count,
                                int(x),
                                int(y),
                                int(head_direction),
                                '-', '-')

        write_active_cells_to_csv(self.cc1.L4_tm,
                                'L4_active',
                                self.thought_count,
                                int(x),
                                int(y),
                                int(head_direction),
                                '-', '-')

        write_active_cells_to_csv(self.cc1.L6a_tm,
                                'L6a_active',
                                self.thought_count,
                                int(x),
                                int(y),
                                int(head_direction),
                                speed,
                                angular_velocity)

    def cc_connect(self,cc1,cc2):
        """
        Method to pass the feedback from one cortical column to another and vice versa
        :param cc1  (CorticalColumn): first cortical column
        :param cc2  (CorticalColumn): second cortical column
        :return:
        """
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