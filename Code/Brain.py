import numpy as np
import csv
import htm
from htm.algorithms import SpatialPooler as SP
from htm.algorithms import TemporalMemory as TM
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
    def __init__(self, eye, metrics_on):
        self.number_of_columns = 256
        self.layer_depth = 32

        self.encoded_vision = []

        self.ray_angle_encoder = enc.RDSE()
        self.ray_length_encoder = enc.RDSE()
        self.vision_SDR = htm.SDR(1)

        self.linear_speed_encoder = enc.RDSE()
        self.angular_velocity_encoder = enc.RDSE()
        self.movement_SDR = htm.SDR(1)

        self.L23_object_sp = SP()
        self.L23_object_tm = TM()
        self.L23_active_columns = SDR(1)

        self.L4_sensory_sp = SP()
        self.L4_sensory_tm = TM()
        self.L4_active_columns = SDR(1)

        self.L6a_location_sp = SP()
        self.L6a_location_tm = TM()
        self.L6a_active_columns = SDR(1)

        self.metrics_on = metrics_on
        self.thought_count = 0

        # region Encoders
        # Ray Angle and Length encoding parameters
        self.angle_enc_param = scalar_encoder_parameters(
            #region Angle Encoder Parameters
            active_bits=0,
            category=0,
            clip_input=0,
            maximum=360,
            minimum=0,
            periodic=1,
            radius=0,
            resolution=0,
            size=100,
            sparsity=0.1
            #endregion
        )

        self.color_enc_param = scalar_encoder_parameters(
            #region Color Encoder Parameters
            active_bits=0,
            category=0,
            clip_input=0,
            maximum=5,
            minimum=0,
            periodic=0,
            radius=0,
            resolution=0,
            size=50,
            sparsity=0.1
            #endregion
        )

        self.linear_speed_enc_param = scalar_encoder_parameters(
            #region Linear Speed Encoder Parameters
            active_bits=0,
            category=0,
            clip_input=0,
            maximum=20,
            minimum=0,
            periodic=0,
            radius=0,
            resolution=0,
            size=50,
            sparsity=0.1
            #endregion
        )

        self.ang_velocity_enc_param = scalar_encoder_parameters(
            #region Anglular Velocity Encoder Parameters
            active_bits=0,
            category=0,
            clip_input=0,
            maximum=360,
            minimum=-360,
            periodic=0,
            radius=0,
            resolution=0,
            size=100,
            sparsity=0.1
            #endregion
        )

        #Ray Angle and Length Encoders
        self.ray_angle_encoder = scalar_encoder(self.angle_enc_param)
        self.ray_length_encoder = scalar_encoder(self.color_enc_param)
        self.ray_encoding_width = self.ray_length_encoder.size + self.ray_angle_encoder.size

        self.vision_encoding_width = self.ray_encoding_width * len(eye.vision)
        self.vision_enc_info = Metrics([self.vision_encoding_width], 999999999)

        # Turn and Speed Encoders
        self.linear_speed_encoder = scalar_encoder(self.linear_speed_enc_param)
        self.angular_velocity_encoder = scalar_encoder(self.ang_velocity_enc_param)

        self.movement_encoding_width = self.linear_speed_encoder.size + self.angular_velocity_encoder.size
        self.movement_enc_info = Metrics([self.movement_encoding_width], 999999999)
        # endregion

        # region Spatial Pooler
        self.L23_object_sp = SP(
            # region L23_sp Parameters
            inputDimensions=[self.number_of_columns*self.layer_depth],
            columnDimensions=[self.number_of_columns],
            potentialRadius=self.layer_depth,
            potentialPct=0.85,
            globalInhibition=True,
            localAreaDensity=0.04,
            # numActiveColumnsPerInhArea=0,
            # stimulusThreshold=0,
            synPermInactiveDec=0.006,
            synPermActiveInc=0.04,
            synPermConnected=0.14,
            # minPctOverlapDutyCycle=0,
            # dutyCyclePeriod=0,
            boostStrength=3,
            # seed=0,
            # spVerbosity=0,
            wrapAround=False
            # endregion
        )
        self.L23_sp_info = Metrics(self.L23_object_sp.getColumnDimensions(), 999999999)
        
        
        self.L4_sensory_sp = SP(
            #region L4_sp Parameters
            inputDimensions=[self.vision_encoding_width],
            columnDimensions=[self.number_of_columns],
            potentialRadius=int(self.ray_encoding_width/2),
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
            wrapAround=False
            #endregion
        )
        self.L4_sp_info = Metrics(self.L4_sensory_sp.getColumnDimensions(), 999999999)

        self.L6a_location_sp = SP(
            #region L6a_sp Parameters
            inputDimensions=[self.movement_encoding_width],
            columnDimensions=[self.number_of_columns],
            potentialRadius=self.movement_encoding_width,
            potentialPct=0.85,
            globalInhibition=True,
            localAreaDensity=0.04,
            # numActiveColumnsPerInhArea=0,
            # stimulusThreshold=0,
            synPermInactiveDec=0.006,
            synPermActiveInc=0.04,
            synPermConnected=0.14,
            # minPctOverlapDutyCycle=0,
            # dutyCyclePeriod=0,
            boostStrength=3,
            #seed=0,
            # spVerbosity=0,
            wrapAround=False
            #endregion
        )
        self.L6a_location_sp_info = Metrics(self.L6a_location_sp.getColumnDimensions(), 999999999)


        # region Temporal Memory
        self.L23_object_tm = TM(
            # region L23_tm Parameters
            columnDimensions=[self.number_of_columns],
            cellsPerColumn=self.layer_depth,
            activationThreshold=15,
            initialPermanence=0.21,
            connectedPermanence=0.14,
            # minThreshold=10,
            maxNewSynapseCount=32,
            permanenceIncrement=0.1,
            permanenceDecrement=0.1,
            predictedSegmentDecrement=0.01,
            # seed=0,
            maxSegmentsPerCell=32,
            maxSynapsesPerSegment=32,
            # checkInputs=0,
            externalPredictiveInputs=(self.number_of_columns * self.layer_depth)
            # endregion
        )
        self.L23_object_tm_info = Metrics([self.L23_object_tm.numberOfCells()], 999999999)
        
        
        self.L4_sensory_tm = TM(
            #region L4_tm Parameters
            columnDimensions=[self.number_of_columns],
            cellsPerColumn=self.layer_depth,
            activationThreshold=15,
            initialPermanence=0.21,
            connectedPermanence=self.L4_sensory_sp.getSynPermConnected(),
            #minThreshold=10,
            maxNewSynapseCount=32,
            permanenceIncrement=0.1,
            permanenceDecrement=0.1,
            predictedSegmentDecrement=0.01,
            #seed=0,
            maxSegmentsPerCell=32,
            maxSynapsesPerSegment=32,
            #checkInputs=0,
            externalPredictiveInputs=(self.number_of_columns*self.layer_depth)
            #endregion
        )
        self.L4_sensory_tm_info = Metrics([self.L4_sensory_tm.numberOfCells()], 999999999)

        self.L6a_location_tm = TM(
            # region L6a_tm Parameters
            columnDimensions=[self.number_of_columns],
            cellsPerColumn=self.layer_depth,
            activationThreshold=15,
            initialPermanence=0.21,
            connectedPermanence=self.L6a_location_sp.getSynPermConnected(),
            # minThreshold=10,
            maxNewSynapseCount=32,
            permanenceIncrement=0.1,
            permanenceDecrement=0.1,
            predictedSegmentDecrement=0.01,
            #seed=0,
            maxSegmentsPerCell=32,
            maxSynapsesPerSegment=32,
            # checkInputs=0,
            externalPredictiveInputs=(self.number_of_columns*self.layer_depth)
            # endregion
        )
        self.L6a_location_tm_info = Metrics([self.L6a_location_tm.numberOfCells()], 999999999)

        # endregion

        self.cells_active = []
        self.cells_freq = []
        self.most_active_cells = []
        self.cell_fire_location = []



    def encode_vision(self, eye):
        """Function encode encodes the length and orientation of each ray in vision into SDRs"""

        self.encoded_vision.clear()
        for ray in eye.vision:
            ray_length_SDR = self.ray_length_encoder.encode(ray.color_num)
            ray_angle_SDR = self.ray_angle_encoder.encode(int(ray.degree_ego_angle))

            rdse_ray_SDR = htm.SDR(self.ray_encoding_width)
            rdse_ray_SDR.concatenate(ray_length_SDR,ray_angle_SDR)
            self.encoded_vision.append(rdse_ray_SDR)

        self.vision_SDR = htm.SDR(self.vision_encoding_width)
        self.vision_SDR.concatenate(self.encoded_vision)

        if self.metrics_on:
            self.vision_enc_info.addData(self.vision_SDR)

        return


    def encode_movement(self, linear_move, angular_turn):
        linear_move_SDR = self.linear_speed_encoder.encode(linear_move)
        angular_move_SDR = self.angular_velocity_encoder.encode(angular_turn)

        self.movement_SDR = htm.SDR(self.movement_encoding_width)
        self.movement_SDR.concatenate(linear_move_SDR,angular_move_SDR)

        if self.metrics_on:
            self.movement_enc_info.addData(self.movement_SDR)

        return

    def pool_object(self):
        self.L23_active_columns = SDR(self.L23_object_sp.getColumnDimensions())
        self.L23_object_sp.compute(self.L4_sensory_tm.getActiveCells(), True, self.L23_active_columns)

        if self.metrics_on:
            self.L23_sp_info.addData(self.L23_active_columns)

        return

    def pool_senses(self):
        self.L4_active_columns = SDR(self.L4_sensory_sp.getColumnDimensions())
        self.L4_sensory_sp.compute(self.vision_SDR, True, self.L4_active_columns)

        if self.metrics_on:
            self.L4_sp_info.addData(self.L4_active_columns)

        return


    def pool_movement(self):
        self.L6a_active_columns = SDR(self.L6a_location_sp.getColumnDimensions())
        self.L6a_location_sp.compute(self.movement_SDR, True, self.L6a_active_columns)

        if self.metrics_on:
            self.L6a_location_sp_info.addData(self.L6a_active_columns)

        return


    def temporal_object(self):
        self.L23_object_tm.activateDendrites(
            learn=True,
            externalPredictiveInputsActive = self.L4_sensory_tm.getActiveCells(),
            externalPredictiveInputsWinners = self.L4_sensory_tm.getWinnerCells()
        )
        self.L23_object_tm.activateCells(self.L4_active_columns, learn=True)
        if self.metrics_on:
            self.L23_object_tm_info.addData(self.L23_object_tm.getActiveCells().flatten())
        return


    def temporal_senses(self):
        self.L4_sensory_tm.activateDendrites(
            learn=True
        )
        self.L4_sensory_tm.activateCells(self.L4_active_columns, learn=True)
        if self.metrics_on:
            self.L4_sensory_tm_info.addData(self.L4_sensory_tm.getActiveCells().flatten())
        return


    def temporal_senses_motion_context(self):
        self.L4_sensory_tm.activateDendrites(
            learn=True,
            externalPredictiveInputsActive=self.L6a_location_tm.getActiveCells(),
            externalPredictiveInputsWinners=self.L6a_location_tm.getWinnerCells()
        )
        self.L4_predictive_cells = self.L4_sensory_tm.getPredictiveCells()
        self.L4_sensory_tm.activateCells(self.L4_active_columns, learn=True)
        if self.metrics_on:
            self.L4_sensory_tm_info.addData(self.L4_sensory_tm.getActiveCells().flatten())
        return

    def temporal_location(self):
        self.L6a_location_tm.activateDendrites(learn=True)
        self.L6a_location_tm.activateCells(self.L6a_active_columns, learn=True)
        if self.metrics_on:
            self.L6a_location_tm_info.addData(self.L6a_location_tm.getActiveCells().flatten())
        return

    def temporal_location_sensory_context(self):
        self.L6a_location_tm.activateDendrites(
            learn=True,
            externalPredictiveInputsActive=self.L4_sensory_tm.getActiveCells(),
            externalPredictiveInputsWinners = self.L4_sensory_tm.getWinnerCells()
        )
        self.L6a_predictive_cells = self.L6a_location_tm.getPredictiveCells()
        self.L6a_location_tm.activateCells(self.L6a_active_columns, learn=True,)
        if self.metrics_on:
            self.L6a_location_tm_info.addData(self.L6a_location_tm.getActiveCells().flatten())
        return


    def find_most_active_neuron(self, tm_info):
        self.cells_freq = tm_info.activationFrequency.activationFrequency
        #index = np.argmax(self.cells_freq)
        self.most_active_cells = np.argpartition(self.cells_freq,-1)[-1:]

        return

    def track_most_active_neuron(self, animal, tm):
        self.cells_active = tm.getActiveCells().sparse

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

        return

    def contextual_memory(self, tm_from, tm_to, active_columns_to, metrics_to):
        tm_to.activateDendrites(
            learn=True,
            externalPredictiveInputsActive=tm_from.getActiveCells(),
            externalPredictiveInputsWinners = tm_from.getWinnerCells()
        )
        tm_to.activateCells(active_columns_to, learn=True,)
        if self.metrics_on:
            metrics_to.addData(tm_to.getActiveCells().flatten())
        return