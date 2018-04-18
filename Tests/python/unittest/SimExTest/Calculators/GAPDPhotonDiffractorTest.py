""" Test module for the GAPDPhotonDiffractor."""
##########################################################################
#                                                                        #
# Copyright (C) 2015-2018 Carsten Fortmann-Grote                         #
# Contact: Carsten Fortmann-Grote <carsten.grote@xfel.eu>                #
#                                                                        #
# This file is part of simex_platform.                                   #
# simex_platform is free software: you can redistribute it and/or modify #
# it under the terms of the GNU General Public License as published by   #
# the Free Software Foundation, either version 3 of the License, or      #
# (at your option) any later version.                                    #
#                                                                        #
# simex_platform is distributed in the hope that it will be useful,      #
# but WITHOUT ANY WARRANTY; without even the implied warranty of         #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          #
# GNU General Public License for more details.                           #
#                                                                        #
# You should have received a copy of the GNU General Public License      #
# along with this program.  If not, see <http://www.gnu.org/licenses/>.  #
#                                                                        #
##########################################################################

import h5py
import os, sys
import shutil
import unittest

# Import the class to test.
from SimEx.Calculators.AbstractPhotonDiffractor import AbstractPhotonDiffractor
#from SimEx.Calculators.GAPDPhotonDiffractor import GAPDPhotonDiffractor
#from SimEx.Parameters.GAPDPhotonDiffractorParameters import GAPDPhotonDiffractorParameters
#from SimEx.Parameters.PhotonBeamParameters import PhotonBeamParameters
#from SimEx.Parameters.DetectorGeometry import DetectorGeometry, DetectorPanel
#from SimEx.Utilities.Units import electronvolt, joule, meter, radian
from TestUtilities import TestUtilities

class GAPDPhotonDiffractorTest(unittest.TestCase):
    """
    Test class for the GAPDPhotonDiffractor class.
    """

    @classmethod
    def setUpClass(cls):
        """ Setting up the test class. """
        pass

    @classmethod
    def tearDownClass(cls):
        """ Tearing down the test class. """
        files_to_remove = ['tmp.beam', 'tmp.geom']
        for f in files_to_remove:
            if os.path.isfile(f):
                os.remove(f)

    def setUp(self):
        """ Setting up a test. """
        self.__files_to_remove = []
        self.__dirs_to_remove = []
        self.__sample = TestUtilities.generateTestFilePath("2nip.pdb")

    def tearDown(self):
        """ Tearing down a test. """
        for f in self.__files_to_remove:
            if os.path.isfile(f):
                os.remove(f)
        for d in self.__dirs_to_remove:
            if os.path.isdir(d):
                shutil.rmtree(d)

    def notestShapedConstruction(self):
        """ Testing the construction of the class with parameters. """

        # Setup parameters.
        parameters=GAPDPhotonDiffractorParameters(sample=self.__sample)

        # Construct the object.
        diffractor = GAPDPhotonDiffractor(parameters=parameters, input_path=None)

        # Check type.
        self.assertIsInstance(diffractor, GAPDPhotonDiffractor)
        self.assertIsInstance(diffractor, AbstractPhotonDiffractor)

    def notestConstructionWithPropInput(self):
        """ Check that beam parameters can be taken from a given propagation output file."""


        parameters = GAPDPhotonDiffractorParameters(
                sample=self.__sample,
                detector_geometry=TestUtilities.generateTestFilePath("simple.geom"),
                beam_parameters=None,
                number_of_diffraction_patterns=1,
                )

        diffractor = GAPDPhotonDiffractor(
                parameters=parameters,
                input_path=TestUtilities.generateTestFilePath("prop_out_0000001.h5"),
                output_path="diffr",
                )

        # Set spectrum type to tophat otherwise calculation will never finish.
        diffractor.parameters.beam_parameters.photon_energy_spectrum_type="tophat"

        # Check that beam parameters have been updated from prop output.
        self.assertAlmostEqual( diffractor.parameters.beam_parameters.photon_energy.m_as(electronvolt) , 4972.8402471221643, 5 )

    def notestBackengineWithPropInput(self):
        """ Check that beam parameters can be taken from a given propagation output file."""

        self.__dirs_to_remove.append("diffr")

        parameters = GAPDPhotonDiffractorParameters(
                sample=self.__sample,
                detector_geometry=TestUtilities.generateTestFilePath("simple.geom"),
                beam_parameters=None,
                number_of_diffraction_patterns=1,
                )

        diffractor = GAPDPhotonDiffractor(
                parameters=parameters,
                input_path=TestUtilities.generateTestFilePath("prop_out_0000001.h5"),
                output_path="diffr",
                )

        # Set spectrum type to tophat otherwise calculation will never finish.
        diffractor.parameters.beam_parameters.photon_energy_spectrum_type="tophat"

        # Check that beam parameters have been updated from prop output.
        diffractor.backengine()

    def notestBackengineSinglePattern(self):
        """ Check we can run pattern_sim with a minimal set of parameter. """

        # Ensure cleanup.
        self.__dirs_to_remove.append("diffr")

        # Get parameters.
        parameters = GAPDPhotonDiffractorParameters(sample=self.__sample,
                detector_geometry=TestUtilities.generateTestFilePath("simple.geom"),
                number_of_diffraction_patterns=1)

        # Get calculator.
        diffractor = GAPDPhotonDiffractor(parameters=parameters, input_path=None, output_path='diffr')

        # Run backengine
        status = diffractor.backengine()

        # Check return code.
        self.assertEqual(status, 0)

        # Check output dir was created.
        self.assertTrue( os.path.isdir( diffractor.output_path ) )

        # Check pattern was written.
        self.assertIn( "diffr_out_0000001.h5" , os.listdir( diffractor.output_path ))

    def notestBackengineMultiplePatterns(self):
        """ Check we can run pattern_sim with a minimal set of parameter. """

        # Ensure cleanup.
        self.__dirs_to_remove.append("diffr")

        # Get parameters.
        parameters = GAPDPhotonDiffractorParameters(sample=self.__sample,
                detector_geometry=TestUtilities.generateTestFilePath("simple.geom"),
                number_of_diffraction_patterns=2)

        # Get calculator.
        diffractor = GAPDPhotonDiffractor(parameters=parameters, input_path=None, output_path='diffr')

        # Run backengine
        status = diffractor.backengine()

        # Check return code.
        self.assertEqual(status, 0)

        # Check output dir was created.
        self.assertTrue( os.path.isdir( diffractor.output_path ) )

        # Check pattern was written.
        self.assertIn( "diffr_out-1.h5" , os.listdir( diffractor.output_path ))
        self.assertIn( "diffr_out-2.h5" , os.listdir( diffractor.output_path ))

    def notestBackengine(self):
        # Get calculator.

        # Ensure cleanup.
        self.__dirs_to_remove.append("diffr")

        # Setup parameters.
        beam_parameters = PhotonBeamParameters(
            photon_energy=4.96e3*electronvolt,
            photon_energy_relative_bandwidth=0.01,
            beam_diameter_fwhm=2e-6*meter,
            divergence=2e-6*radian,
            pulse_energy=1e-3*joule,
            photon_energy_spectrum_type='tophat')

        self.assertIsInstance(beam_parameters, PhotonBeamParameters)

        geometry = DetectorGeometry(
                panels=DetectorPanel(
                    ranges={"fast_scan_min" : 0,
                        "fast_scan_max" : 63,
                        "slow_scan_min" : 0,
                        "slow_scan_max" : 63},
                    pixel_size=220.0e-6*meter,
                    photon_response=1.0,
                    distance_from_interaction_plane=0.1*meter,
                    corners={"x" : -32, "y": -32},
                    saturation_adu=1e4,
                    )
                )

        sys.stdout.flush()
        parameters = GAPDPhotonDiffractorParameters(sample=self.__sample,
                        beam_parameters=beam_parameters,
                        detector_geometry=geometry,
                        number_of_diffraction_patterns=10)


        diffractor = GAPDPhotonDiffractor(parameters=parameters, input_path=None, output_path='diffr')

        # Run backengine
        status = diffractor.backengine()

        # Check return code.
        self.assertEqual(status, 0)

        # Check output dir was created.
        output_path = "%s" % diffractor.output_path
        self.assertTrue(os.path.isdir(output_path))

        # Check pattern was written.
        self.assertIn("diffr_out-1.h5" , os.listdir(output_path))

    def testBackengineGPU(self):
        """ Check a backengine calculation with openCL enabled. """

        # Ensure cleanup.
        self.__dirs_to_remove.append("diffr")
        self.__files_to_remove.append("diffr.h5")

        # Clean up to make sure no old files mess things up.
        self.tearDown()

        beam_parameters = PhotonBeamParameters(
            photon_energy=4.96e3*electronvolt,
            photon_energy_relative_bandwidth=0.01,
            beam_diameter_fwhm=2e-6*meter,
            divergence=2e-6*radian,
            pulse_energy=1e-3*joule,
            photon_energy_spectrum_type='tophat'
            )

        geometry = DetectorGeometry(
                panels=DetectorPanel(
                    ranges={"fast_scan_min" : 0,
                        "fast_scan_max" : 63,
                        "slow_scan_min" : 0,
                        "slow_scan_max" : 63},
                    pixel_size=220.0e-6*meter,
                    photon_response=1.0,
                    distance_from_interaction_plane=0.1*meter,
                    corners={"x" : -32, "y": -32},
                    saturation_adu=1e4,
                    )
                )

        parameters = GAPDPhotonDiffractorParameters(sample=self.__sample,
                        beam_parameters=beam_parameters,
                        detector_geometry=geometry,
                        number_of_diffraction_patterns=10,
                        use_gpu=True)


        # Get calculator.
        diffractor = GAPDPhotonDiffractor(parameters=parameters, input_path=None, output_path='diffr')

        # Run backengine
        status = diffractor.backengine()

        # Check return code.
        self.assertEqual(status, 0)

        output_path = "%s" % diffractor.output_path
        # Check output dir was created.
        self.assertTrue(os.path.isdir(output_path))

        # Check pattern was written.
        diffractor.saveH5()
        self.assertIn("diffr_out_0000001.h5" , os.listdir(output_path))

    def notestSaveH5(self):
        """ Check that saveh5() creates correct filenames. """

        # Ensure cleanup.
        self.__dirs_to_remove.append("diffr")
        self.__files_to_remove.append("diffr.h5")

        # Setup beam parameters.
        beam_parameters = PhotonBeamParameters(photon_energy=5e3*electronvolt,
                pulse_energy=2e-3*joule,
                photon_energy_relative_bandwidth=1e-3,
                photon_energy_spectrum_type="tophat",
                beam_diameter_fwhm=3e-6*meter,
                )

        geometry = DetectorGeometry(
                panels=DetectorPanel(
                    ranges={"fast_scan_min" : 0,
                        "fast_scan_max" : 63,
                        "slow_scan_min" : 0,
                        "slow_scan_max" : 63},
                    pixel_size=220.0e-6*meter,
                    photon_response=1.0,
                    distance_from_interaction_plane=0.1*meter,
                    corners={"x" : -32, "y": -32},
                    saturation_adu=1e4,
                    )
                )

        # Get parameters.
        parameters = GAPDPhotonDiffractorParameters(sample=self.__sample,
                detector_geometry=geometry,
                beam_parameters=beam_parameters,
                number_of_diffraction_patterns=2)

        # Get calculator.
        diffractor = GAPDPhotonDiffractor(parameters=parameters, input_path=None, output_path='diffr')

        # Run backengine
        status = diffractor.backengine()

        # Check return code.
        self.assertEqual(status, 0)

        # Check output dir was created.
        self.assertTrue( os.path.isdir( diffractor.output_path ) )

        # Save correctly.
        diffractor.saveH5()

        # Check output file was created.
        self.assertTrue( os.path.isfile( diffractor.output_path ) )

        # Check pattern was written.
        self.assertIn( "diffr_out_0000001.h5" , os.listdir( "diffr" ))
        self.assertIn( "diffr_out_0000002.h5" , os.listdir( "diffr" ))

        # Open linked h5 file.
        with h5py.File(diffractor.output_path, 'r') as h5:
            self.assertIn("data" , list(h5.keys()))
            self.assertIn("0000001" , list(h5["data"].keys()))
            self.assertIn("0000002" , list(h5["data"].keys()))
            self.assertIn("data" , list(h5["data/0000001"].keys()))
            self.assertIn("data" , list(h5["data/0000002"].keys()))

            self.assertIn("params" , list(h5.keys()))
            self.assertIn("beam" , list(h5["params"].keys()))
            self.assertIn("photonEnergy" , list(h5["params/beam"].keys()))
            self.assertIn("focusArea" , list(h5["params/beam"].keys()))

        # Check metafile was created.
        self.assertIn( os.path.split(diffractor.output_path)[-1], os.listdir( os.path.dirname( diffractor.output_path) ) )

    def notestBackengineWithBeamParametersObject(self):
        """ Check beam parameter logic if they are set as parameters. """

        # Ensure cleanup.
        self.__dirs_to_remove.append("diffr")

        # Setup beam parameters.
        beam_parameters = PhotonBeamParameters(
                photon_energy=16.0e3*electronvolt,
                photon_energy_relative_bandwidth=0.001,
                pulse_energy=2.0e-3*joule,
                beam_diameter_fwhm=100e-9*meter,
                divergence=None,
                photon_energy_spectrum_type="tophat",
                )

        # Get parameters.
        parameters = GAPDPhotonDiffractorParameters(sample=self.__sample,
                detector_geometry=TestUtilities.generateTestFilePath("simple.geom"),
                beam_parameters=beam_parameters,
                number_of_diffraction_patterns=2,
                )

        # Get calculator.
        diffractor = GAPDPhotonDiffractor(parameters=parameters, input_path=None, output_path='diffr')

        # Run backengine
        status = diffractor.backengine()

        # Check return code.
        self.assertEqual(status, 0)

    def notestBackengineWithBeamAndGeometry(self):
        """ Check geom parameter logic if they are set as parameters. """

        # Ensure cleanup.
        self.__dirs_to_remove.append("diffr")

        # Setup beam parameters.
        beam_parameters = PhotonBeamParameters(
                photon_energy=16.0e3*electronvolt,
                photon_energy_relative_bandwidth=0.001,
                pulse_energy=2.0e-3*joule,
                beam_diameter_fwhm=100e-9*meter,
                divergence=None,
                photon_energy_spectrum_type="tophat",
                )

        geometry = DetectorGeometry(panels=DetectorPanel(
                                                         ranges={"fast_scan_min" : 0,
                                                             "fast_scan_max" : 63,
                                                             "slow_scan_min" : 0,
                                                             "slow_scan_max" : 63},
                                                         pixel_size=220.0e-6*meter,
                                                         photon_response=1.0,
                                                         distance_from_interaction_plane=0.1*meter,
                                                         corners={"x" : -32, "y": -32},
                                                         saturation_adu=1e4,
                                                        )
                                    )
        # Get parameters.
        parameters = GAPDPhotonDiffractorParameters(sample=self.__sample,
                detector_geometry=geometry,
                beam_parameters=beam_parameters,
                number_of_diffraction_patterns=2,
                )

        # Get calculator.
        diffractor = GAPDPhotonDiffractor(parameters=parameters, input_path=None, output_path='diffr')

        # Run backengine
        status = diffractor.backengine()

        # Check return code.
        self.assertEqual(status, 0)

if __name__ == '__main__':
    unittest.main()
