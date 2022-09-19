import numpy as np
import csv
import htm
from htm.algorithms import SpatialPooler as SP
from htm.algorithms import TemporalMemory as TM
import htm.bindings.encoders as enc
from htm.bindings.sdr import *
from CorticalColumn import *

from Code.helpers.cells_to_csv import *

class Brain:
    """
    Class Brain defines an object which takes encoded SDRs from sensory objects
     and carries out the operation of Spatial Pooling on the SDR. Further implementation to be determined
     (i.e. neuron interconnections, minicolumns, temporal memory, converting SDR input into motor outputs, etc)
    """
    def __init__(self, vision1,vision2,vision3):
        self.thought_count = 0
        self.cc1 = CorticalColumn(vision1)
        self.cc2 = CorticalColumn(vision2)
        self.cc3 = CorticalColumn(vision3)
        self.ccs = [self.cc1, self.cc2, self.cc3]

    def initialize(self, vision1,vision2,vision3, l1_distance, linear_movement, l1_angle, angular_movement):
        self.thought_count += 1
        initialize_csv()
        self.cc1.initialize(vision1, l1_distance, linear_movement, l1_angle, angular_movement)
        self.cc2.initialize(vision2, l1_distance, linear_movement, l1_angle, angular_movement)
        self.cc3.initialize(vision3, l1_distance, linear_movement, l1_angle, angular_movement)

    def think(self, vision1,vision2,vision3, l1_distance, linear_motion, l1_angle, angular_motion, learning):
        self.thought_count += 1
        self.cc1.process(vision1, l1_distance, linear_motion, l1_angle, angular_motion, learning)
        self.cc2.process(vision2, l1_distance, linear_motion, l1_angle, angular_motion, learning)
        self.cc3.process(vision3, l1_distance, linear_motion, l1_angle, angular_motion, learning)

        self.cc_connect(self.cc2,self.cc1)
        self.cc_connect(self.cc1,self.cc2)
        self.cc_connect(self.cc3,self.cc1)
        self.cc_connect(self.cc1,self.cc3)
        self.cc_connect(self.cc2,self.cc3)
        self.cc_connect(self.cc3,self.cc2)

    def cc_connect(self,cc1,cc2):
        cc1.cc_feedback(cc2)
        cc2.cc_feedback(cc1)