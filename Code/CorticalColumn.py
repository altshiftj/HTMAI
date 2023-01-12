import numpy as np
import math
import csv
import htm

from htm.algorithms import SpatialPooler as SP
from htm.algorithms import TemporalMemory as TM
import htm.bindings.encoders as enc
from htm.bindings.sdr import *

from Code.helpers.encode_helper import *
from Code.helpers.neural_activity_to_csv import *

RECORD_ACTIVITY_INTERVAL = 100

class CorticalColumn:
    """
    Class Cortical Column defines an object which creates encoded SDRs from sensory input
    and carries out the operation of Spatial Pooling and Temporal Memory on the SDRs.
    """

    def __init__(self, vision, number_of_columns, layer_depth):
        self.thought_count = 0

        number_of_columns = number_of_columns
        layer_depth = layer_depth

        # region Encoders

        # SDR composed of encoded ray's angle, as well as the feedback it senses and sends back
        ray_encoding_width = 64 * 64
        self.vision_SDR = htm.SDR([ray_encoding_width])

        # Encoded feedforward input from movement
        movement_encoding_width = 64 * 64
        self.movement_SDR = htm.SDR([movement_encoding_width])

        # Ray Angle encoder parameters
        angle_enc_param = rdse_encoder_parameters(
            # region Angle Encoder Parameters
            active_bits=0,
            category=0,
            radius=0,
            resolution=6,
            seed=1,
            size=ray_encoding_width,
            sparsity=0.004,
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
            size=ray_encoding_width,
            sparsity=0.004,
            # endregion
        )

        l1_distance_enc_param = rdse_encoder_parameters(
            # region Linear Speed Encoder Parameters
            active_bits=0,
            category=0,
            radius=0,
            resolution=50,
            seed=3,
            size=movement_encoding_width,
            sparsity=0.004,
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
            size=movement_encoding_width,
            sparsity=0.004,
            # endregion
        )

        # Animal change in head direction encoder
        ang_velocity_enc_param = rdse_encoder_parameters(
            # region Anglular Velocity Encoder Parameters
            active_bits=0,
            category=0,
            radius=0,
            resolution=1,
            seed=5,
            size=movement_encoding_width,
            sparsity=0.004,
            # endregion
        )

        # Ray Angle and Length Encoders
        self.ray_angle_encoder = rdse_encoder(angle_enc_param)
        self.ray_feedback_encoder = rdse_encoder(color_enc_param)

        # Turn and Speed Encoders
        self.l1_distance_encoder = rdse_encoder(l1_distance_enc_param)
        self.linear_speed_encoder = rdse_encoder(linear_speed_enc_param)
        self.angular_velocity_encoder = rdse_encoder(ang_velocity_enc_param)

        self.location_enc_info = Metrics([self.movement_SDR.size], 999999999)
        self.vision_enc_info = Metrics([self.vision_SDR.size], 999999999)
        # endregion

        # region Spatial Pooler

        self.L23_active_columns = SDR(number_of_columns)
        self.L4_active_columns = SDR(number_of_columns)
        self.L6a_active_columns = SDR(number_of_columns)

        # L23 object layer spatial pooler
        self.L23_sp = SP(
            # region L23_sp Parameters
            inputDimensions=[number_of_columns * layer_depth],
            columnDimensions=(number_of_columns,),
            potentialRadius=(number_of_columns * layer_depth),
            potentialPct=.85,
            globalInhibition=True,
            localAreaDensity=8 / 256,
            # numActiveColumnsPerInhArea=1,
            # stimulusThreshold=0,
            synPermConnected=0.14,
            synPermActiveInc=0.04,
            synPermInactiveDec=0.006,
            boostStrength=3,
            # minPctOverlapDutyCycle=0,
            # dutyCyclePeriod=0,
            # spVerbosity=0,
            wrapAround=False,
            seed=6,
            # endregion
        )

        # L4 sensory layer spatial pooler
        self.L4_sp = SP(
            # region L4_sp Parameters
            inputDimensions=(self.vision_SDR.size,),
            columnDimensions=(number_of_columns,),
            potentialRadius=ray_encoding_width,
            potentialPct=.85,
            globalInhibition=True,
            localAreaDensity=12 / 256,
            # numActiveColumnsPerInhArea=0,
            # stimulusThreshold=0,
            synPermConnected=0.14,
            synPermActiveInc=0.04,
            synPermInactiveDec=0.006,
            # minPctOverlapDutyCycle=0,
            # dutyCyclePeriod=0,32
            boostStrength=3,
            # spVerbosity=0,
            wrapAround=False,
            seed=7,
            # endregion
        )

        # L6a motion layer
        self.L6a_sp = SP(
            # region L6a_sp Parameters
            inputDimensions=(self.movement_SDR.size,),
            columnDimensions=(number_of_columns,),
            potentialRadius=movement_encoding_width,
            potentialPct=.85,
            globalInhibition=True,
            localAreaDensity=12 / 256,
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

        # Spatial pooler metrics
        self.L23_sp_info = Metrics(self.L23_sp.getColumnDimensions(), 999999999)
        self.L4_sp_info = Metrics(self.L4_sp.getColumnDimensions(), 999999999)
        self.L6a_sp_info = Metrics(self.L6a_sp.getColumnDimensions(), 999999999)
        # endregion

        # region Temporal Memory

        self.L23_predictive_cells = 0
        self.L4_predictive_cells = 0
        self.L6a_predictive_cells = 0

        self.L23_active_segments = 0
        self.L4_active_segments = 0
        self.L6a_active_segments = 0

        # L23 object layer temporal memory
        self.L23_tm = TM(
            # region L23_tm Parameters
            columnDimensions=self.L23_sp.getColumnDimensions(),
            cellsPerColumn=layer_depth,
            maxSegmentsPerCell=64,
            maxSynapsesPerSegment=32,
            maxNewSynapseCount=16,
            activationThreshold=6,
            minThreshold=5,
            initialPermanence=0.51,
            connectedPermanence=0.6,
            permanenceIncrement=0.1,
            permanenceDecrement=0.02,
            predictedSegmentDecrement=0.006,
            externalPredictiveInputs=(number_of_columns * layer_depth),
            checkInputs=1,
            seed=9,
            # endregion
        )

        # L4 sensory layer temporal memory
        self.L4_tm = TM(
            # region L4_tm Parameters
            columnDimensions=self.L4_sp.getColumnDimensions(),
            cellsPerColumn=layer_depth,
            maxSegmentsPerCell=64,
            maxSynapsesPerSegment=32,
            maxNewSynapseCount=16,
            activationThreshold=13,
            minThreshold=10,
            initialPermanence=0.51,
            connectedPermanence=0.6,
            permanenceIncrement=0.1,
            permanenceDecrement=0.02,
            predictedSegmentDecrement=0.01,
            externalPredictiveInputs=(number_of_columns * layer_depth),
            checkInputs=1,
            seed=10,
            # endregion
        )

        # L6a motion layer temporal memory
        self.L6a_tm = TM(
            # region L6a_tm Parameters
            columnDimensions=self.L6a_sp.getColumnDimensions(),
            cellsPerColumn=layer_depth,
            maxSegmentsPerCell=64,
            maxSynapsesPerSegment=32,
            maxNewSynapseCount=16,
            activationThreshold=13,
            minThreshold=10,
            initialPermanence=0.51,
            connectedPermanence=0.6,
            permanenceIncrement=0.1,
            permanenceDecrement=0.02,
            predictedSegmentDecrement=0.01,
            externalPredictiveInputs=(number_of_columns * layer_depth),
            checkInputs=1,
            seed=11,
            # endregion
        )

        # Temporal Memory metrics
        self.L23_tm_info = Metrics([self.L23_tm.numberOfCells()], 999999999)
        self.L4_tm_info = Metrics([self.L4_tm.numberOfCells()], 999999999)
        self.L6a_tm_info = Metrics([self.L6a_tm.numberOfCells()], 999999999)
        # endregion

    def vision_code(self, vision):
        """Function encode_vision encodes the orientation and feedback of each ray in vision into SDRs"""

        # Clear the previous vision SDR list
        encoded_vision = []

        # Encode rays and add to vision SDR list
        for ray in vision:
            # Encode ray angles and feedback
            ray_angle_SDR = self.ray_angle_encoder.encode(int(ray.degree_ego_angle))
            ray_length_SDR = self.ray_feedback_encoder.encode(ray.color_num)

            # Create ray SDR whose size is the sum of the sizes of angle and feedback SDRs
            ray_SDR = htm.SDR(ray_angle_SDR.size)

            # Make ray SDR represent both ray angle and feedback via concatentation
            ray_SDR.union(ray_length_SDR, ray_angle_SDR)

            # Add ray SDR to list of SDRs representing vision
            encoded_vision.append(ray_SDR)

        # Make vision SDR a concatenation of all ray SDRs
        self.vision_SDR.union(encoded_vision)

        # Record metrics of the vision SDR
        self.vision_enc_info.addData(self.vision_SDR)

        return

    def encode_vision_no_mets(self, vision):
        """Function encode_vision encodes the orientation and feedback of each ray in vision into SDRs"""

        # Clear the previous vision SDR list
        encoded_vision = []

        # Encode rays and add to vision SDR list
        for ray in vision:
            # Encode ray angles and feedback
            ray_angle_SDR = self.ray_angle_encoder.encode(int(ray.degree_ego_angle))
            ray_length_SDR = self.ray_feedback_encoder.encode(ray.color_num)

            # Create ray SDR whose size is the sum of the sizes of angle and feedback SDRs
            ray_SDR = htm.SDR(ray_angle_SDR.size)

            # Make ray SDR represent both ray angle and feedback via concatentation
            ray_SDR.union(ray_length_SDR, ray_angle_SDR)

            # Add ray SDR to list of SDRs representing vision
            encoded_vision.append(ray_SDR)

        # Make vision SDR a concatenation of all ray SDRs
        self.vision_SDR.union(encoded_vision)

        return

    def encode_movement(self, motions):
        """Function encode_movement encodes the 2D distance travelled and change in head direction of an animal into SDRs"""
        encoded_movement = []

        l1_distance_SDR = self.l1_distance_encoder.encode(motions[0])
        encoded_movement.append(l1_distance_SDR)

        # Create an SDR the of encoded distance moved
        linear_move_SDR = self.linear_speed_encoder.encode(motions[1])
        encoded_movement.append(linear_move_SDR)

        # Create an SDR the of encoded change in head direction
        angular_move_SDR = self.angular_velocity_encoder.encode(motions[2])
        encoded_movement.append(angular_move_SDR)

        # Make movement SDR a concatenation of move and head direction SDRs
        self.movement_SDR.union(encoded_movement)

        # Record metrics of the movement SDR
        self.location_enc_info.addData(self.movement_SDR)

        return

    def encode_movement_no_mets(self, motions):
        """Function encode_movement encodes the 2D distance travelled and change in head direction of an animal into SDRs"""
        encoded_movement = []

        l1_distance_SDR = self.l1_distance_encoder.encode(motions[0])
        encoded_movement.append(l1_distance_SDR)

        # Create an SDR the of encoded distance moved
        linear_move_SDR = self.linear_speed_encoder.encode(motions[1])
        encoded_movement.append(linear_move_SDR)

        # Create an SDR the of encoded change in head direction
        angular_move_SDR = self.angular_velocity_encoder.encode(motions[2])
        encoded_movement.append(angular_move_SDR)

        # Make movement SDR a concatenation of move and head direction SDRs
        self.movement_SDR.value =self.movement_SDR.union(encoded_movement)

        return

    def pool(self, pooler, active_columns, input_SDR, learning, metrics):
        """Function pool computes active columns of a temporal layer"""
        pooler.compute(input_SDR, learning, active_columns)
        metrics.addData(active_columns)

        return

    def feedforward_memory(self, tm, active_columns, learning, metrics_to):
        """Function feedforward_memory recieves a temporal memory layer, its active columns, whether it learns or not
        and if metrics are to be recorded, and computes the current active and predictive cells"""
        tm.activateDendrites(learn=learning)

        if tm == self.L23_tm:
            self.L23_predictive_cells = tm.getPredictiveCells()
            self.L23_active_segments = tm.getActiveSegments()
        elif tm == self.L4_tm:
            self.L4_predictive_cells = tm.getPredictiveCells()
            self.L4_active_segments = tm.getActiveSegments()
        elif tm == self.L6a_tm:
            self.L6a_predictive_cells = tm.getPredictiveCells()
            self.L6a_active_segments = tm.getActiveSegments()

        tm.activateCells(active_columns, learn=learning)
        metrics_to.addData(tm.getActiveCells().flatten())

        return

    def feedback_memory(self, tm_from, tm_to, active_columns_to, learning, metrics_to):
        """Function feedback_memory takes active cells from one layer and sends it activity to another layer.
        The to_layer is therefore receving feedback from another layer's activation"""

        # Activate dendrites of the neurons in a temporal layer
        tm_to.activateDendrites(
            learn=learning,
            externalPredictiveInputsActive=tm_from.getActiveCells(),
            externalPredictiveInputsWinners=tm_from.getWinnerCells()
        )

        if tm_to == self.L23_tm:
            self.L23_predictive_cells = tm_to.getPredictiveCells()
            self.L23_active_segments = tm_to.getActiveSegments()
        elif tm_to == self.L4_tm:
            self.L4_predictive_cells = tm_to.getPredictiveCells()
            self.L4_active_segments = tm_to.getActiveSegments()
        elif tm_to == self.L6a_tm:
            self.L6a_predictive_cells = tm_to.getPredictiveCells()
            self.L6a_active_segments = tm_to.getActiveSegments()

        # Calculate the active cells of a temporal layer based on the current active columns and dendrite segments
        tm_to.activateCells(active_columns_to, learn=learning)

        # Add metrics data to the layer's metric object
        metrics_to.addData(tm_to.getActiveCells().flatten())

        return

    def feedforward_motion(self, motions, learning):
        self.encode_movement(motions)

        self.pool(self.L6a_sp, self.L6a_active_columns, self.movement_SDR, learning, self.L6a_sp_info)

        #self.feedforward_memory(self.L6a_tm, self.L6a_active_columns, learning, self.L6a_tm_info)

    def feedforward_vision(self, vision, learning):
        self.vision_code(vision)

        self.pool(self.L4_sp, self.L4_active_columns, self.vision_SDR, learning, self.L4_sp_info)

        self.feedforward_memory(self.L4_tm, self.L4_active_columns, learning, self.L4_tm_info)

    def feedforward_object(self, learning):
        self.pool(self.L23_sp, self.L23_active_columns, self.L4_tm.getActiveCells(), learning, self.L23_sp_info)
        self.feedforward_memory(self.L23_tm, self.L23_active_columns, learning, self.L23_tm_info)

    def initialize(self, vision, motions):
        self.thought_count+=1
        create_neural_activity_csv()

        # Encode movement of the animal
        self.feedforward_motion(motions, False)
        self.feedforward_vision(vision, False)

    def process(self, vision, motions, learning):
        """Function process takes all actions of a cortical column and condenses its possible actions into one function
        in a specific order."""
        self.thought_count += 1

        self.feedforward_motion(motions, learning)
        self.feedback_memory(self.L6a_tm, self.L4_tm, self.L4_active_columns, learning, self.L4_tm_info)

        self.feedforward_vision(vision, learning)
        self.feedback_memory(self.L4_tm, self.L6a_tm, self.L6a_active_columns, learning, self.L6a_tm_info)

        self.feedforward_object(learning)
        self.feedback_memory(self.L23_tm, self.L4_tm, self.L4_active_columns, learning, self.L4_tm_info)

        if self.thought_count % RECORD_ACTIVITY_INTERVAL == 0:
            self.record_activity()
        return

    def record_activity(self):
        write_neural_activity_csv(self.L23_tm, 'L23', self.thought_count, self.L23_predictive_cells, self.L23_active_segments)
        write_neural_activity_csv(self.L4_tm, 'L4', self.thought_count, self.L4_predictive_cells, self.L4_active_segments)
        write_neural_activity_csv(self.L6a_tm, 'L6a', self.thought_count, self.L6a_predictive_cells, self.L6a_active_segments)

    def cc_feedback(self, cc_from, learning):
        self.feedback_memory(cc_from.L23_tm, self.L23_tm, self.L23_active_columns, learning, self.L23_tm_info)

        return
