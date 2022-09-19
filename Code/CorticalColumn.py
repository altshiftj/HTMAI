import numpy as np
import math
import csv
import htm
from htm.algorithms import SpatialPooler as SP
from htm.algorithms import TemporalMemory as TM
import htm.bindings.encoders as enc
from htm.bindings.sdr import *

from helpers.display_SDR import *
from helpers.encode_helper import *


class CorticalColumn:
    """
    Class Cortical Column defines an object which creates encoded SDRs from sensory objects
    and carries out the operation of Spatial Pooling and Temporal Memory on the SDRs.
    """

    def __init__(self, vision):
        #region Initialize
        self.number_of_columns = 256                            # Number of minicolumns in each layer
        self.layer_depth = 32                                   # Number of neurons per minicolumn

        # SDR composed of encoded ray's angle, as well as the feedback it senses and sends back
        self.ray_encoding_width = 64*64
        vision_encoding_width = self.ray_encoding_width*len(vision)
        self.vision_SDR = htm.SDR([vision_encoding_width])
        self.encoded_vision = []                                # Encoded feedforward input from the eye, list of encoded ray SDRs representing animal vision

        # Encoded feedforward input from movement
        self.location_encoding_width = 64 * 64
        self.location_SDR = htm.SDR([self.location_encoding_width])
        self.encoded_location = []

        # Encoded feedforward input from movement
        self.orientation_encoding_width = 64 * 64
        self.orientation_SDR = htm.SDR([self.orientation_encoding_width])
        self.encoded_orientation = []

        self.L23_active_columns = SDR(self.number_of_columns)
        self.L4_active_columns = SDR(self.number_of_columns)
        self.L5a_active_columns = SDR(self.number_of_columns)
        self.L5b_active_columns = SDR(self.number_of_columns)
        self.L6a_active_columns = SDR(self.number_of_columns)
        self.L6b_active_columns = SDR(self.number_of_columns)
        #endregion

        # region Encoders
        # Ray Angle encoder parameters
        angle_enc_param = rdse_encoder_parameters(
            # region Angle Encoder Parameters
            active_bits=0,
            category=0,
            radius=0,
            resolution=6,
            seed=1,
            size=int(self.ray_encoding_width/2),
            sparsity=0.02,
            # endregion
        )

        # Ray Feedback encoder parameters
        color_enc_param = rdse_encoder_parameters(
            # region Color Encoder Parameters
            active_bits=0,
            category=0,
            radius=0,
            resolution=1,
            seed=2,
            size=int(self.ray_encoding_width/2),
            sparsity=0.02,
            # endregion
        )

        l1_distance_enc_param = rdse_encoder_parameters(
            # region Linear Speed Encoder Parameters
            active_bits=0,
            category=0,
            radius=0,
            resolution=30,
            seed=3,
            size=int(self.location_encoding_width / 2),
            sparsity=0.02,
            # endregion
        )

        # Animal change in distance encoder
        linear_speed_enc_param = rdse_encoder_parameters(
            # region Linear Speed Encoder Parameters
            active_bits=0,
            category=0,
            radius=0,
            resolution=1,
            seed=4,
            size=int(self.location_encoding_width / 2),
            sparsity=0.02,
            # endregion
        )

        l1_ang_enc_param = rdse_encoder_parameters(
            # region Anglular Velocity Encoder Parameters
            active_bits=0,
            category=0,
            radius=0,
            resolution=15,
            seed=5,
            size=int(self.orientation_encoding_width / 2),
            sparsity=0.02,
            # endregion
        )

        # Animal change in head direction encoder
        ang_velocity_enc_param = rdse_encoder_parameters(
            # region Anglular Velocity Encoder Parameters
            active_bits=0,
            category=0,
            radius=0,
            resolution=1,
            seed=6,
            size=int(self.orientation_encoding_width / 2),
            sparsity=0.02,
            # endregion
        )

        # Ray Angle and Length Encoders
        self.ray_angle_encoder = rdse_encoder(angle_enc_param)                  # Encoder to encode a ray's angle using encoder parameters defined above
        self.ray_feedback_encoder = rdse_encoder(color_enc_param)               # Encoder to encode a ray's feedback using encoder paramters defined above
        self.vision_enc_info = Metrics([self.vision_SDR.size], 999999999)                    # Metric information of the vision SDR

        # Turn and Speed Encoders
        self.l1_distance_encoder = rdse_encoder(l1_distance_enc_param)
        self.linear_speed_encoder = rdse_encoder(linear_speed_enc_param)        # Encoder to encode an animals speed using encoder paramters defined above
        self.l1_angle_encoder = rdse_encoder(l1_ang_enc_param)
        self.angular_velocity_encoder = rdse_encoder(ang_velocity_enc_param)    # Encoder to encode an animals head turning speed using encoder paramters defined above
        
        self.location_enc_info = Metrics([self.location_SDR.size], 999999999)                    # Metric information of the movement SDR
        self.orientation_enc_info = Metrics([self.orientation_SDR.size], 999999999)
        # endregion

        # region Spatial Pooler
        # L23 object layer spatial pooler
        self.L23_sp = SP(
            # region L23_sp Parameters
            inputDimensions=[self.number_of_columns*self.layer_depth],
            columnDimensions=[self.number_of_columns],
            potentialRadius=(self.number_of_columns*self.layer_depth),
            potentialPct=.85,
            globalInhibition=True,
            localAreaDensity=0.0625,
            #numActiveColumnsPerInhArea=1,
            # stimulusThreshold=0,
            synPermConnected=0.14,
            synPermActiveInc=0.04,
            synPermInactiveDec=0.006,
            boostStrength=3,
            # minPctOverlapDutyCycle=0,
            # dutyCyclePeriod=0,
            # spVerbosity=0,
            wrapAround=False,
            seed=7,
            # endregion
        )

        # L4 sensory layer spatial pooler
        self.L4_sp = SP(
            # region L4_sp Parameters
            inputDimensions=[self.vision_SDR.size],
            columnDimensions=[self.number_of_columns],
            potentialRadius=2*self.ray_encoding_width,
            potentialPct=.85,
            globalInhibition=True,
            localAreaDensity=0.0625,
            # numActiveColumnsPerInhArea=0,
            # stimulusThreshold=0,
            synPermConnected=0.14,
            synPermActiveInc=0.04,
            synPermInactiveDec=0.006,
            # minPctOverlapDutyCycle=0,
            # dutyCyclePeriod=0,
            boostStrength=3,
            # spVerbosity=0,
            wrapAround=False,
            seed=8,
            # endregion
        )

        self.L5a_sp = SP(
            # region L5a_sp Parameters
            inputDimensions=[self.number_of_columns*self.layer_depth],
            columnDimensions=[self.number_of_columns],
            potentialRadius=int(self.number_of_columns*self.layer_depth),
            potentialPct=.85,
            globalInhibition=True,
            localAreaDensity=0.0625,
            # numActiveColumnsPerInhArea=0,
            # stimulusThreshold=0,
            synPermConnected=0.14,
            synPermActiveInc=0.04,
            synPermInactiveDec=0.006,
            # minPctOverlapDutyCycle=0,
            # dutyCyclePeriod=0,
            boostStrength=3,
            # spVerbosity=0,
            wrapAround=False,
            seed=9,
            # endregion
        )

        self.L5b_sp = SP(
            # region L5b_sp Parameters
            inputDimensions=[self.number_of_columns*self.layer_depth],
            columnDimensions=[self.number_of_columns],
            potentialRadius=int(self.number_of_columns*self.layer_depth),
            potentialPct=.85,
            globalInhibition=True,
            localAreaDensity=0.0625,
            # numActiveColumnsPerInhArea=0,
            # stimulusThreshold=0,
            synPermConnected=0.14,
            synPermActiveInc=0.04,
            synPermInactiveDec=0.006,
            # minPctOverlapDutyCycle=0,
            # dutyCyclePeriod=0,
            boostStrength=3,
            # spVerbosity=0,
            wrapAround=False,
            seed=10,
            # endregion
        )

        # L6a motion layer
        self.L6a_sp = SP(
            # region L6a_sp Parameters
            inputDimensions=[self.orientation_SDR.size],
            columnDimensions=[self.number_of_columns],
            potentialRadius=int(self.orientation_encoding_width),
            potentialPct=.85,
            globalInhibition=True,
            localAreaDensity=0.0625,
            # numActiveColumnsPerInhArea=0,
            # stimulusThreshold=0,
            synPermConnected=0.14,
            synPermActiveInc=0.04,
            synPermInactiveDec=0.006,
            # minPctOverlapDutyCycle=0,
            # dutyCyclePeriod=0,
            boostStrength=3,
            # spVerbosity=0,
            wrapAround=False,
            seed=11,
            # endregion
        )

        self.L6b_sp = SP(
            # region L6b_sp Parameters
            inputDimensions=[self.location_SDR.size],
            columnDimensions=[self.number_of_columns],
            potentialRadius=int(self.location_encoding_width),
            potentialPct=.85,
            globalInhibition=True,
            localAreaDensity=0.0625,
            # numActiveColumnsPerInhArea=0,
            # stimulusThreshold=0,
            synPermConnected=0.14,
            synPermActiveInc=0.04,
            synPermInactiveDec=0.006,
            # minPctOverlapDutyCycle=0,
            # dutyCyclePeriod=0,
            boostStrength=3,
            # spVerbosity=0,
            wrapAround=False,
            seed=12,
            # endregion
        )

        # Spatial pooler metrics
        self.L23_sp_info = Metrics(self.L23_sp.getColumnDimensions(), 999999999)
        self.L4_sp_info = Metrics(self.L4_sp.getColumnDimensions(), 999999999)
        self.L5a_sp_info = Metrics(self.L5a_sp.getColumnDimensions(), 999999999)
        self.L5b_sp_info = Metrics(self.L5b_sp.getColumnDimensions(), 999999999)
        self.L6a_sp_info = Metrics(self.L6a_sp.getColumnDimensions(), 999999999)
        self.L6b_sp_info = Metrics(self.L6b_sp.getColumnDimensions(), 999999999)
        # endregion

        # region Temporal Memory
        # L23 object layer temporal memory
        self.L23_tm = TM(
            # region L23_tm Parameters
            columnDimensions=self.L23_sp.getColumnDimensions(),
            cellsPerColumn=self.layer_depth,
            maxSegmentsPerCell=64,
            maxSynapsesPerSegment=32,
            maxNewSynapseCount=16,
            activationThreshold=9,
            minThreshold=5,
            initialPermanence=0.21,
            connectedPermanence=0.14,
            permanenceIncrement=0.1,
            permanenceDecrement=0.1,
            predictedSegmentDecrement=0.0006,
            externalPredictiveInputs=(self.number_of_columns * self.layer_depth),
            checkInputs=1,
            seed=13,
            # endregion
        )

        # L4 sensory layer temporal memory
        self.L4_tm = TM(
            # region L4_tm Parameters
            columnDimensions=self.L4_sp.getColumnDimensions(),
            cellsPerColumn=self.layer_depth,
            maxSegmentsPerCell=64,
            maxSynapsesPerSegment=32,
            maxNewSynapseCount=16,
            activationThreshold=9,
            minThreshold=5,
            initialPermanence=0.21,
            connectedPermanence=0.14,
            permanenceIncrement=0.1,
            permanenceDecrement=0.1,
            predictedSegmentDecrement=0.0006,
            externalPredictiveInputs=(self.number_of_columns * self.layer_depth),
            checkInputs=1,
            seed = 14,
            # endregion
        )

        # L6a motion layer temporal memory
        self.L5a_tm = TM(
            # region L5a_tm Parameters
            columnDimensions=self.L5a_sp.getColumnDimensions(),
            cellsPerColumn=self.layer_depth,
            maxSegmentsPerCell=64,
            maxSynapsesPerSegment=32,
            maxNewSynapseCount=16,
            activationThreshold=9,
            minThreshold=5,
            initialPermanence=0.21,
            connectedPermanence=0.14,
            permanenceIncrement=0.1,
            permanenceDecrement=0.1,
            predictedSegmentDecrement=0.0006,
            externalPredictiveInputs=(self.number_of_columns * self.layer_depth),
            checkInputs=1,
            seed=15,
            # endregion
        )

        # L6a motion layer temporal memory
        self.L5b_tm = TM(
            # region L5b_tm Parameters
            columnDimensions=self.L5b_sp.getColumnDimensions(),
            cellsPerColumn=self.layer_depth,
            maxSegmentsPerCell=64,
            maxSynapsesPerSegment=32,
            maxNewSynapseCount=16,
            activationThreshold=9,
            minThreshold=5,
            initialPermanence=0.21,
            connectedPermanence=0.14,
            permanenceIncrement=0.1,
            permanenceDecrement=0.1,
            predictedSegmentDecrement=0.0006,
            externalPredictiveInputs=(self.number_of_columns * self.layer_depth),
            checkInputs=1,
            seed=16,
            # endregion
        )

        # L6a motion layer temporal memory
        self.L6a_tm = TM(
            # region L6a_tm Parameters
            columnDimensions=self.L6a_sp.getColumnDimensions(),
            cellsPerColumn=self.layer_depth,
            maxSegmentsPerCell=64,
            maxSynapsesPerSegment=32,
            maxNewSynapseCount=16,
            activationThreshold=9,
            minThreshold=5,
            initialPermanence=0.21,
            connectedPermanence=0.14,
            permanenceIncrement=0.1,
            permanenceDecrement=0.1,
            predictedSegmentDecrement=0.0006,
            externalPredictiveInputs=(self.number_of_columns * self.layer_depth),
            checkInputs=1,
            seed = 17,
            # endregion
        )

        self.L6b_tm = TM(
            # region L6b_tm Parameters
            columnDimensions=self.L6b_sp.getColumnDimensions(),
            cellsPerColumn=self.layer_depth,
            maxSegmentsPerCell=64,
            maxSynapsesPerSegment=32,
            maxNewSynapseCount=16,
            activationThreshold=9,
            minThreshold=5,
            initialPermanence=0.21,
            connectedPermanence=0.14,
            permanenceIncrement=0.1,
            permanenceDecrement=0.1,
            predictedSegmentDecrement=0.0006,
            externalPredictiveInputs=(self.number_of_columns * self.layer_depth),
            checkInputs=1,
            seed=18,
            # endregion
        )

        # Temporal Memory metrics
        self.L23_tm_info = Metrics([self.L23_tm.numberOfCells()], 999999999)
        self.L4_tm_info = Metrics([self.L4_tm.numberOfCells()], 999999999)
        self.L5a_tm_info = Metrics([self.L5a_tm.numberOfCells()], 999999999)
        self.L5b_tm_info = Metrics([self.L5b_tm.numberOfCells()], 999999999)
        self.L6a_tm_info = Metrics([self.L6a_tm.numberOfCells()], 999999999)
        self.L6b_tm_info = Metrics([self.L6b_tm.numberOfCells()], 999999999)
        # endregion

    def encode_vision(self, vision):
        """Function encode_vision encodes the orientation and feedback of each ray in vision into SDRs"""

        # Clear the previous vision SDR list
        self.encoded_vision.clear()

        # Encode rays and add to vision SDR list
        for ray in vision:

            # Encode ray angles and feedback
            ray_angle_SDR = self.ray_angle_encoder.encode(int(ray.degree_ego_angle))
            ray_length_SDR = self.ray_feedback_encoder.encode(ray.color_num)

            # Create ray SDR whose size is the sum of the sizes of angle and feedback SDRs
            ray_SDR = htm.SDR(self.ray_angle_encoder.size+self.ray_feedback_encoder.size)

            # Make ray SDR represent both ray angle and feedback via concatentation
            ray_SDR.concatenate(ray_length_SDR, ray_angle_SDR)

            # Add ray SDR to list of SDRs representing vision
            self.encoded_vision.append(ray_SDR)

        # Make vision SDR a concatenation of all ray SDRs
        self.vision_SDR.concatenate(self.encoded_vision)

        # Record metrics of the vision SDR
        self.vision_enc_info.addData(self.vision_SDR)

        return

    def encode_location(self, l1_distance, linear_move):
        """Function encode_movement encodes the 2D distance travelled and change in head direction of an animal into SDRs"""
        self.encoded_location.clear()

        l1_distance_SDR = self.l1_distance_encoder.encode(l1_distance)
        self.encoded_location.append(l1_distance_SDR)

        # Create an SDR the of encoded distance moved
        linear_move_SDR = self.linear_speed_encoder.encode(linear_move)
        self.encoded_location.append(linear_move_SDR)

        # Make movement SDR a concatenation of move and head direction SDRs
        self.location_SDR.concatenate(self.encoded_location)

        # Record metrics of the movement SDR
        self.location_enc_info.addData(self.location_SDR)

        return

    def encode_orientation(self, l1_angle, angular_turn):
        """Function encode_movement encodes the 2D distance travelled and change in head direction of an animal into SDRs"""
        self.encoded_orientation.clear()

        l1_angle_SDR = self.l1_angle_encoder.encode(l1_angle)
        self.encoded_orientation.append(l1_angle_SDR)

        # Create an SDR the of encoded change in head direction
        angular_move_SDR = self.angular_velocity_encoder.encode(angular_turn)
        self.encoded_orientation.append(angular_move_SDR)

        self.orientation_SDR.concatenate(self.encoded_orientation)

        # Record metrics of the movement SDR
        self.orientation_enc_info.addData(self.orientation_SDR)

        return

    def pool(self, pooler, active_columns, input_SDR, learning, metrics):
        """Function pool computes active columns of a temporal layer"""
        pooler.compute(input_SDR, learning, active_columns)
        metrics.addData(active_columns)

        return

    def feedforward_memory(self, tm, active_columns, learning, metrics_to):
        """Function feedforward_memory recieves a temporal memory layer, its active columns, whether it learns or not
        and if metrics are to be recorded, and computes the current active and predictive cells cells """
        tm.activateDendrites(learn=learning)
        tm.activateCells(active_columns, learn=learning)
        metrics_to.addData(tm.getActiveCells().flatten())

        return

    def feedback_memory(self, tm_from, tm_to, active_columns_to, learning, metrics_to):
        """Function feedback_memory takes active cells from one layer and sends it activity to another layer.
        The to_layer is therefore receving feedback from another layer's activation"""

        #Activate dendrites of the neurons in a temporal layer
        tm_to.activateDendrites(
            learn=learning,
            externalPredictiveInputsActive=tm_from.getActiveCells(),
            externalPredictiveInputsWinners=tm_from.getWinnerCells()
        )

        # Calculate the active cells of a temporal layer based on the current active columns and dendrite segments
        tm_to.activateCells(active_columns_to, learn=learning)

        # Add metrics data to the layer's metric object
        metrics_to.addData(tm_to.getActiveCells().flatten())

        return

    def initialize(self, vision, l1_distance, linear_motion, l1_angle, angular_motion):
        # Encode movement of the animal
        self.encode_orientation(l1_angle, angular_motion)
        self.pool(self.L6a_sp, self.L6a_active_columns, self.orientation_SDR, False, self.L6a_sp_info)
        self.feedforward_memory(self.L6a_tm, self.L6a_active_columns, False, self.L6a_tm_info)

        self.encode_location(l1_distance, linear_motion)
        # Pool the movement encoding
        self.pool(self.L6b_sp, self.L6b_active_columns, self.location_SDR, False, self.L6b_sp_info)
        # Feedforward movement input into temporal memory layer L6a
        self.feedforward_memory(self.L6b_tm, self.L6b_active_columns, False, self.L6b_tm_info)

        # Encode sensory vision of the animal eye
        self.encode_vision(vision)
        # Pool vision encoding
        self.pool(self.L4_sp, self.L4_active_columns, self.vision_SDR, False, self.L4_sp_info)
        # Feedforward sensory input into temporal memory layer L4
        self.feedforward_memory(self.L4_tm, self.L4_active_columns, False, self.L4_tm_info)

    def process(self, vision, l1_distance, linear_motion, l1_angle, angular_motion, learning):
        """Function process takes all actions of a cortical column, and condenses its possible actions into one function
        in a specific order."""

        # Encode movement of the animal
        self.encode_orientation(l1_angle, angular_motion)
        # Pool the movement encoding
        self.pool(self.L6a_sp, self.L6a_active_columns, self.orientation_SDR, learning, self.L6a_sp_info)
        
        # Feedforward movement input into temporal memory layer L6a
        self.feedforward_memory(self.L6a_tm, self.L6a_active_columns, learning, self.L6a_tm_info)

        # Feedback from L6a motion layer activation to L4 sensory layer
        self.feedback_memory(self.L6a_tm, self.L4_tm, self.L4_active_columns, learning, self.L4_tm_info)

        # Encode sensory vision of the animal eye
        self.encode_vision(vision)
        # Pool vision encoding
        self.pool(self.L4_sp, self.L4_active_columns, self.vision_SDR, learning, self.L4_sp_info)
        # Feedforward sensory input into temporal memory layer L4
        self.feedforward_memory(self.L4_tm, self.L4_active_columns, learning, self.L4_tm_info)

        # Feedback from L4 sensory layer activation to L6a motion layer
        self.feedback_memory(self.L4_tm, self.L6a_tm, self.L6a_active_columns, learning, self.L6a_tm_info)

        # Pool L4 sensory activation to L2/3 input
        self.pool(self.L23_sp, self.L23_active_columns, self.L4_tm.getActiveCells(), learning, self.L23_sp_info)
        # Pool L4 sensory input into temporal memory layer L2/3
        self.feedforward_memory(self.L23_tm, self.L23_active_columns, learning, self.L23_tm_info)

        # Feedback from L2/3 object layer activation to L4 sensory layer
        self.feedback_memory(self.L23_tm, self.L4_tm, self.L4_active_columns, learning, self.L4_tm_info)

        self.encode_location(l1_distance,linear_motion)
        self.pool(self.L6b_sp, self.L6b_active_columns, self.location_SDR, learning, self.L6b_sp_info)
        self.feedforward_memory(self.L6b_tm, self.L6b_active_columns, learning, self.L6b_tm_info)

        # Feedback from L6b object layer activation to L5b sensory layer
        self.feedback_memory(self.L6b_tm, self.L5b_tm, self.L5b_active_columns, learning, self.L5b_tm_info)

        # Pool L23 sensory activation to L5b input
        self.pool(self.L5b_sp, self.L5b_active_columns, self.L23_tm.getActiveCells(), learning, self.L5b_sp_info)
        # Pool L23 sensory input into temporal memory layer L5b
        self.feedforward_memory(self.L5b_tm, self.L5b_active_columns, learning, self.L5b_tm_info)

        # Feedback from L5b object layer activation to L6b sensory layer
        self.feedback_memory(self.L5b_tm, self.L6b_tm, self.L6b_active_columns, learning, self.L6b_tm_info)

        # Pool L5b sensory activation to L5a input
        self.pool(self.L5a_sp, self.L5a_active_columns, self.L5b_tm.getActiveCells(), learning, self.L5a_sp_info)
        # Pool L5b sensory input into temporal memory layer L5a
        self.feedforward_memory(self.L5a_tm, self.L5a_active_columns, learning, self.L5a_tm_info)

        return

    def cc_feedback(self, cc_from):
        self.feedback_memory(cc_from.L23_tm, self.L23_tm, self.L23_active_columns, learning, self.L23_tm_info)
        self.feedback_memory(cc_from.L5a_tm, self.L5a_tm, self.L5a_active_columns, learning, self.L5a_tm_info)