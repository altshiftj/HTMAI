import htm
from htm.algorithms import SpatialPooler as SP
from htm.algorithms import TemporalMemory as TM
from htm.algorithms import Predictor
import htm.bindings.encoders as enc
from htm.bindings.sdr import *
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
        self.angle_encoder = enc.RDSE()
        self.length_encoder = enc.RDSE()
        self.vision_SDR = htm.SDR(1)
        self.spatial_pooler = SP()
        self.active_columns = SDR(1)
        self.thought_count = 0

        # region Encoders
        # Ray Angle and Length encoding parameters
        self.angle_enc_param = rdse_encoder_parameters(
            active_bits=0,
            category=0,
            radius=30,
            resolution=0,
            seed=0,
            size=500,
            sparsity=0.1
        )

        self.length_enc_param = rdse_encoder_parameters(
            active_bits=0,
            category=0,
            radius=100,
            resolution=0,
            seed=0,
            size=750,
            sparsity=0.1
        )

        #Ray Angle and Length Encoders

        self.angle_encoder = rdse_encoder(self.angle_enc_param)
        self.length_encoder = rdse_encoder(self.length_enc_param)
        self.ray_encoding_width = self.length_encoder.size + self.angle_encoder.size

        self.vision_encoding_width = self.ray_encoding_width * len(eye.vision)
        self.enc_info = Metrics([self.vision_encoding_width], 999999999)
        # endregion

        # region Spatial Pooler
        self.spatial_pooler = SP(
            inputDimensions=[self.vision_encoding_width],
            columnDimensions=[100],
            potentialRadius=16,
            potentialPct=0.85,
            globalInhibition=True,
            localAreaDensity=0.1,
            synPermInactiveDec=0.006,
            synPermActiveInc=0.04,
            synPermConnected=0.13,
            boostStrength=3,
            wrapAround=True
        )
        self.sp_info = Metrics(self.spatial_pooler.getColumnDimensions(), 999999999)
        # endregion

        # region Temporal Memory
        self.tm = TM(
            columnDimensions=self.spatial_pooler.getColumnDimensions(),
            cellsPerColumn=5,
            activationThreshold=17,
            initialPermanence=0.21,
            connectedPermanence=self.spatial_pooler.getSynPermConnected(),
            minThreshold=10,
            maxNewSynapseCount=32,
            permanenceIncrement=0.1,
            permanenceDecrement=0.1,
            predictedSegmentDecrement=0.0,
            seed=0,
            maxSegmentsPerCell=128,
            maxSynapsesPerSegment=64,
            checkInputs=0,
            externalPredictiveInputs=0
        )
        self.tm_info = Metrics([self.tm.numberOfCells()], 999999999)
        # endregion

    def encode(self, eye):
        """Function encode encodes the length and orientation of each ray in vision into SDRs"""
        self.encoded_vision.clear()
        for ray in eye.vision:
            ray_length_SDR = self.length_encoder.encode(int(ray.length))
            ray_angle_SDR = self.angle_encoder.encode(int(ray.degree_angle))

            rdse_ray_SDR = htm.SDR(self.ray_encoding_width)
            rdse_ray_SDR.concatenate(ray_length_SDR,ray_angle_SDR)
            self.encoded_vision.append(rdse_ray_SDR)

        self.vision_SDR = htm.SDR(self.vision_encoding_width)
        self.vision_SDR.concatenate(self.encoded_vision)
        self.enc_info.addData( self.vision_SDR )

        return

    def pool(self):

        self.active_columns = SDR(self.spatial_pooler.getColumnDimensions())
        self.spatial_pooler.compute( self.vision_SDR, True, self.active_columns )
        self.sp_info.addData( self.active_columns )


        return

    def temporal(self):

        self.tm.compute(self.active_columns, learn=True)
        self.tm_info.addData( self.tm.getActiveCells().flatten() )

        return

