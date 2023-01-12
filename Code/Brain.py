import numpy as np
import csv
import htm
from htm.algorithms import SpatialPooler as SP
from htm.algorithms import TemporalMemory as TM
import htm.bindings.encoders as enc
from htm.bindings.sdr import *
from Code.CorticalColumn import *

class Brain:
    """
    Class Brain defines an object which takes encoded SDRs from sensory objects
     and carries out the operation of Spatial Pooling on the SDR. Further implementation to be determined
     (i.e. neuron interconnections, minicolumns, temporal memory, converting SDR input into motor outputs, etc)
    """
    def __init__(self, vision):
        self.thought_count = 0
        self.cc1 = CorticalColumn(vision, 32, 32)

    def initialize(self, vision, motion):
        self.thought_count += 1
        self.cc1.initialize(vision, motion)

    def think(self, track, vision, motion, learning):
        self.thought_count += 1
        self.cc1.process(vision, motion, learning)



    def cc_connect(self,cc1,cc2):
        cc1.cc_feedback(cc2)
        cc2.cc_feedback(cc1)