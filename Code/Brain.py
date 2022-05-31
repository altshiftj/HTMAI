import numpy as np

import htm
from htm.algorithms import SpatialPooler as SP
from htm.algorithms import TemporalMemory as TM
from htm.algorithms import Predictor
import htm.bindings.encoders as enc
from htm.bindings.sdr import *
import pygame
from helpers.display_SDR import *
from helpers.encode_helper import *

class Brain:
    """
    Class Brain defines an object which takes encoded SDRs from sensory objects
     and carries out the operation of Spatial Pooling on the SDR. Further implementation to be determined
     (i.e. neuron interconnections, minicolumns, temporal memory, converting SDR input into motor outputs, etc)
    """
    def __init__(self, eye):
        self.encoded_vision = []
        self.vision_angle_encoder = enc.RDSE()
        self.length_encoder = enc.RDSE()
        self.vision_SDR = htm.SDR(1)
        self.sensory_sp = SP()
        self.active_columns = SDR(1)
        self.thought_count = 0

        # region Encoders
        # Ray Angle and Length encoding parameters
        self.angle_enc_param = rdse_encoder_parameters(
            active_bits=0,
            category=0,
            radius=7,
            resolution=0,
            seed=0,
            size=500,
            sparsity=0.1
        )

        self.length_enc_param = rdse_encoder_parameters(
            active_bits=0,
            category=0,
            radius=25,
            resolution=0,
            seed=0,
            size=750,
            sparsity=0.1
        )

        self.move_dir_enc_param = rdse_encoder_parameters(
            active_bits=0,
            category=0,
            radius=25,
            resolution=0,
            seed=0,
            size=750,
            sparsity=0.1
        )

        self.move_vel_enc_param = rdse_encoder_parameters(
            active_bits=0,
            category=0,
            radius=25,
            resolution=0,
            seed=0,
            size=750,
            sparsity=0.1
        )

        #Ray Angle and Length Encoders

        self.vision_angle_encoder = rdse_encoder(self.angle_enc_param)
        self.length_encoder = rdse_encoder(self.length_enc_param)
        self.ray_encoding_width = self.length_encoder.size + self.vision_angle_encoder.size

        self.vision_encoding_width = self.ray_encoding_width * len(eye.vision)
        self.vision_enc_info = Metrics([self.vision_encoding_width], 999999999)

        # Movement Direction and Velocity Encoders


        # endregion

        # region Spatial Pooler
        self.sensory_sp = SP(
            inputDimensions=[self.vision_encoding_width],   #57500
            columnDimensions=[512],
            potentialRadius=self.ray_encoding_width,        #1250
            potentialPct=0.85,
            globalInhibition=True,
            localAreaDensity=0.04,
            #numActiveColumnsPerInhArea=0,
            #stimulusThreshold=0,
            synPermInactiveDec=0.006,
            synPermActiveInc=0.04,
            synPermConnected=0.14,
            #minPctOverlapDutyCycle=0,
            #dutyCyclePeriod=0,
            boostStrength=3,
            #seed=0,
            #spVerbosity=0,
            wrapAround=True
        )
        self.sp_info = Metrics(self.sensory_sp.getColumnDimensions(), 999999999)
        # endregion

        # region Temporal Memory
        self.tm = TM(
            columnDimensions=self.sensory_sp.getColumnDimensions(),     #2048
            cellsPerColumn=32,
            activationThreshold=15,
            initialPermanence=0.21,
            connectedPermanence=self.sensory_sp.getSynPermConnected(),  #0.5
            #minThreshold=10,
            maxNewSynapseCount=16,
            permanenceIncrement=0.1,
            permanenceDecrement=0.1,
            predictedSegmentDecrement=0.01,
            #seed=0,
            maxSegmentsPerCell=64,
            maxSynapsesPerSegment=64,
            #checkInputs=0,
            #externalPredictiveInputs=0
        )
        self.tm_info = Metrics([self.tm.numberOfCells()], 999999999)
        # endregion

        self.cells_active = []
        self.cells_freq = []
        self.most_active_cells = []
        self.cell_fire_location = []

    def encode(self, eye):
        """Function encode encodes the length and orientation of each ray in vision into SDRs"""
        self.encoded_vision.clear()
        for ray in eye.vision:
            ray_length_SDR = self.length_encoder.encode(int(ray.length))
            ray_angle_SDR = self.vision_angle_encoder.encode(int(ray.degree_angle))

            rdse_ray_SDR = htm.SDR(self.ray_encoding_width)
            rdse_ray_SDR.concatenate(ray_length_SDR,ray_angle_SDR)
            self.encoded_vision.append(rdse_ray_SDR)

        self.vision_SDR = htm.SDR(self.vision_encoding_width)
        self.vision_SDR.concatenate(self.encoded_vision)
        self.vision_enc_info.addData(self.vision_SDR)

        return

    def pool(self):

        self.active_columns = SDR(self.sensory_sp.getColumnDimensions())
        self.sensory_sp.compute(self.vision_SDR, True, self.active_columns)
        self.sp_info.addData( self.active_columns )

        return

    def temporal(self):

        self.tm.compute(self.active_columns, learn=True)
        self.tm_info.addData(self.tm.getActiveCells().flatten())

        return

    def find_most_active_neuron(self):
        self.cells_freq = self.tm_info.activationFrequency.activationFrequency
        #index = np.argmax(self.cells_freq)
        self.most_active_cells = np.argpartition(self.cells_freq,-5)[-5:]
        return

    def track_most_active_neuron(self,animal):
        self.cells_active = self.tm.getActiveCells().sparse

        for i in range(len(self.most_active_cells)):
            if self.most_active_cells[i] in self.cells_active:
                self.cell_fire_location.append([self.most_active_cells[i],int(animal.x),int(animal.y)])

        return

    def draw_most_active_cell(self,display):
        size = 2

        for i in range(len(self.cell_fire_location)):
            if self.cell_fire_location[i][0] == self.most_active_cells[0]:
                color = 'red'
                pygame.draw.circle(display, color, self.cell_fire_location[i][1:3], size)
            elif self.cell_fire_location[i][0] == self.most_active_cells[1]:
                color = 'yellow'
                pygame.draw.circle(display, color, self.cell_fire_location[i][1:3], size)
            elif self.cell_fire_location[i][0] == self.most_active_cells[2]:
                color = 'green'
                pygame.draw.circle(display, color, self.cell_fire_location[i][1:3], size)
            elif self.cell_fire_location[i][0] == self.most_active_cells[3]:
                color = 'blue'
                pygame.draw.circle(display, color, self.cell_fire_location[i][1:3], size)
            elif self.cell_fire_location[i][0] == self.most_active_cells[4]:
                color = 'purple'
                pygame.draw.circle(display, color, self.cell_fire_location[i][1:3], size)
        return

    def clear_cell_fire_location(self):
        self.cell_fire_location.clear()