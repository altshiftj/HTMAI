import numpy as np
import math
import csv
import htm
from htm.algorithms import SpatialPooler as SP
from htm.algorithms import TemporalMemory as TM
import htm.bindings.encoders as enc
from htm.bindings.sdr import *

from helpers.encode_helper import *


class CorticalColumn:
    """
    Class Cortical Column defines an object which creates encoded SDRs from sensory input
    and carries out the operation of Spatial Pooling and Temporal Memory on the SDRs.

    :param vision           (list): a list of rays representing the animal's vision
    :param cc_width         (int): an integer indicating the number of minicolumns in the cortical column
    :param cc_layer_depth   (int): an integer indicating the number of cells per minicolumn within the cortical column
                                layers
    """

    def __init__(self, vision, cc_width, cc_layer_depth):
        self.column_width = cc_width
        self.layer_depth = cc_layer_depth

        # region Encoders

        # SDR composed of encoded ray's angle, as well as the feedback it senses and sends back
        ray_encoding_width = 64 * 64
        self.vision_SDR = htm.SDR([ray_encoding_width])
        self.encoded_vision = []

        # Encoded feedforward input from movement
        movement_encoding_width = 64 * 64
        self.movement_SDR = htm.SDR([movement_encoding_width])
        self.encoded_movement = []

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

        distance_traveled_enc_param = rdse_encoder_parameters(
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
        speed_enc_param = rdse_encoder_parameters(
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
        angular_velocity_enc_param = rdse_encoder_parameters(
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
        self.vision_enc_info = Metrics([self.vision_SDR.size], 999999999)

        # Turn and Speed Encoders
        self.distance_traveled_encoder = rdse_encoder(distance_traveled_enc_param)
        self.speed_encoder = rdse_encoder(speed_enc_param)
        self.angular_velocity_encoder = rdse_encoder(angular_velocity_enc_param)
        
        self.movement_enc_info = Metrics([self.movement_SDR.size], 999999999)
        # endregion

        # region Spatial Pooler

        self.L23_active_columns = SDR(self.column_width)
        self.L4_active_columns = SDR(self.column_width)
        self.L6a_active_columns = SDR(self.column_width)

        # L23 object layer spatial pooler
        self.L23_sp = SP(
            # region L23_sp Parameters
            inputDimensions=[self.column_width * self.layer_depth],
            columnDimensions=[self.column_width],
            potentialRadius=(self.column_width * self.layer_depth),
            potentialPct=.85,
            globalInhibition=True,
            localAreaDensity=8/256,
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
            seed=6,
            # endregion
        )

        # L4 sensory layer spatial pooler
        self.L4_sp = SP(
            # region L4_sp Parameters
            inputDimensions=[self.vision_SDR.size],
            columnDimensions=[self.column_width],
            potentialRadius=ray_encoding_width,
            potentialPct=.85,
            globalInhibition=True,
            localAreaDensity=12/256,
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
            inputDimensions=[self.movement_SDR.size],
            columnDimensions=[self.column_width],
            potentialRadius=movement_encoding_width,
            potentialPct=.85,
            globalInhibition=True,
            localAreaDensity=12/256,
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
        # L23 object layer temporal memory
        self.L23_tm = TM(
            # region L23_tm Parameters
            columnDimensions=self.L23_sp.getColumnDimensions(),
            cellsPerColumn=self.layer_depth,
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
            externalPredictiveInputs=(self.column_width * self.layer_depth),
            checkInputs=1,
            seed=9,
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
            activationThreshold=13,
            minThreshold=10,
            initialPermanence=0.51,
            connectedPermanence=0.6,
            permanenceIncrement=0.1,
            permanenceDecrement=0.02,
            predictedSegmentDecrement=0.01,
            externalPredictiveInputs=(self.column_width * self.layer_depth),
            checkInputs=1,
            seed = 10,
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
            activationThreshold=13,
            minThreshold=10,
            initialPermanence=0.51,
            connectedPermanence=0.6,
            permanenceIncrement=0.1,
            permanenceDecrement=0.02,
            predictedSegmentDecrement=0.01,
            externalPredictiveInputs=(self.column_width * self.layer_depth),
            checkInputs=1,
            seed = 11,
            # endregion
        )

        # Temporal Memory metrics
        self.L23_tm_info = Metrics([self.L23_tm.numberOfCells()], 999999999)
        self.L4_tm_info = Metrics([self.L4_tm.numberOfCells()], 999999999)
        self.L6a_tm_info = Metrics([self.L6a_tm.numberOfCells()], 999999999)
        # endregion

    def encode_vision(self, vision):
        """
        Function encode_vision encodes the orientation and feedback of each ray in vision into SDRs

        :param vision (list): List of rays representing the animal's vision
        """

        # Clear the previous vision SDR list
        self.encoded_vision.clear()

        # Encode rays and add to vision SDR list
        for ray in vision:

            # Encode ray angles and feedback
            ray_angle_SDR = self.ray_angle_encoder.encode(int(ray.ego_angle))
            ray_feedback_SDR = self.ray_feedback_encoder.encode(ray.color_num)

            # Create ray SDR whose size is the sum of the sizes of angle and feedback SDRs
            ray_SDR = htm.SDR(ray_angle_SDR.size)

            # Make ray SDR represent both ray angle and feedback via concatentation
            ray_SDR.union(ray_feedback_SDR, ray_angle_SDR)

            # Add ray SDR to list of SDRs representing vision
            self.encoded_vision.append(ray_SDR)

        # Make vision SDR a union of all ray SDRs
        self.vision_SDR.union(self.encoded_vision)

        # Record metrics of the vision SDR
        self.vision_enc_info.addData(self.vision_SDR)

        return

    def encode_movement(self, distance_traveled, speed, angular_velocity):
        """
        Function encode_movement encodes the 2D distance travelled and change in head direction of an animal into
        SDRs

        :param distance_traveled    (int): 2D distance travelled by animal
        :param speed                (int): speed of animal
        :param angular_velocity     (int): change in head direction of animal
        """
        self.encoded_movement.clear()

        distance_traveled_SDR = self.distance_traveled_encoder.encode(distance_traveled)
        self.encoded_movement.append(distance_traveled_SDR)

        # Create an SDR the of encoded distance moved
        speed_SDR = self.speed_encoder.encode(speed)
        self.encoded_movement.append(speed_SDR)

        # Create an SDR the of encoded change in head direction
        angular_velocity_SDR = self.angular_velocity_encoder.encode(angular_velocity)
        self.encoded_movement.append(angular_velocity_SDR)

        # Make movement SDR a union of move and head direction SDRs
        self.movement_SDR.union(self.encoded_movement)

        # Record metrics of the movement SDR
        self.movement_enc_info.addData(self.movement_SDR)

        return

    def pool(self, pooler, active_columns, input_SDR, learning, metrics):
        """
        Function pool computes active columns of a temporal layer

        :param pooler           (SpatialPooler): spatial pooler object
        :param active_columns   (SDR): active column output of the spatial pooler
        :param input_SDR        (SDR): input SDR to the spatial pooler layer
        :param learning         (bool): whether the spatial pooler layer uses learning algorithms or not
        :param metrics          (Metrics): metrics object of the spatial pooler layer
        """
        pooler.compute(input_SDR, learning, active_columns)
        metrics.addData(active_columns)

        return

    def feedforward_memory(self, tm, active_columns, learning, metrics_to):
        """
        Function feedforward_memory recieves a temporal memory layer, its active columns, whether it learns or not
        and if metrics are to be recorded, and computes the current active and predictive cells

        :param tm               (TemporalMemory): temporal memory layer
        :param active_columns   (SDR): active columns of the temporal memory layer
        :param learning         (bool): whether the temporal memory layer uses learning algorithms or not
        :param metrics_to       (Metrics): metrics object of the temporal memory layer
        """
        tm.activateDendrites(learn=learning)
        tm.activateCells(active_columns, learn=learning)
        metrics_to.addData(tm.getActiveCells().flatten())

        return


    def feedback_memory(self, tm_from, tm_to, active_columns_to, learning, metrics_to):
        """
        Function feedback_memory takes active cells from one layer and sends it activity to another layer.
        The to_layer is therefore receiving feedback from another layer's activation

        :param tm_from              (TemporalMemory): temporal memory layer sending feedback
        :param tm_to                (TemporalMemory): temporal memory layer receiving feedback
        :param active_columns_to    (SDR): active columns of the layer receiving feedback
        :param learning             (bool): whether the layer receiving feedback uses learning algorithms or not
        :param metrics_to           (Metrics): metrics object of the layer receiving feedback
        """

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


    def initialize(self, vision, distance_traveled, speed, angular_velocity):
        """
        Initializes the cortical layers of the cortical column by processing sensory and motor inputs

        :param vision               (list): list of rays representing the animal's vision
        :param distance_traveled    (int): distance traveled by the animal
        :param speed                (int): speed of the animal
        :param angular_velocity     (int): change in head direction of the animal
        """

        # Encode movement of the animal
        self.encode_movement(distance_traveled, speed, angular_velocity)
        self.pool(self.L6a_sp, self.L6a_active_columns, self.movement_SDR, False, self.L6a_sp_info)
        self.feedforward_memory(self.L6a_tm, self.L6a_active_columns, False, self.L6a_tm_info)

        # Encode sensory vision of the animal eye
        self.encode_vision(vision)
        # Pool vision encoding
        self.pool(self.L4_sp, self.L4_active_columns, self.vision_SDR, False, self.L4_sp_info)
        # Feedforward sensory input into temporal memory layer L4
        self.feedforward_memory(self.L4_tm, self.L4_active_columns, False, self.L4_tm_info)

    def process(self, vision, distance_traveled, speed, angular_motion, learning):
        """
        Function process takes all actions of a cortical column and condenses its possible actions into one function
        in a specific order.

        :param vision               (list): List of rays representing the animal's vision
        :param distance_traveled    (int): Distance traveled by the animal
        :param speed                (int): Speed of the animal
        :param angular_motion       (int): Change in head direction of the animal
        :param learning             (bool): Boolean value indicating whether learning algorithms for spatial pooler and
                                        temporal memory are active
        """

        # Encode movement of the animal
        self.encode_movement(distance_traveled, speed, angular_motion)

        # Pool the movement encoding
        self.pool(self.L6a_sp, self.L6a_active_columns, self.movement_SDR, learning, self.L6a_sp_info)

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

        return

    def cc_feedback(self, cc_from, learning):
        """
        Function cc_feedback takes a cortical column's active cells and uses them as feedback for this column's
        temporal memory object layer - NOT YET IMPLEMENTED

        :param cc_from      (CorticalColumn): cortical column sending feedback
        :param learning     (bool): whether the cortical column uses learning algorithms or not
        """
        self.feedback_memory(cc_from.L23_tm, self.L23_tm, self.L23_active_columns, learning, self.L23_tm_info)

        return