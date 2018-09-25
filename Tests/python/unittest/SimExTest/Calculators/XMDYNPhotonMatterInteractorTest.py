""" Test module for the XMDYNPhotonMatterInteractor. """
##########################################################################
#                                                                        #
# Copyright (C) 2015 - 2018 Carsten Fortmann-Grote                       #
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
import numpy
import os
import shutil
import unittest

# Import the class to test.
from SimEx.Calculators.XMDYNPhotonMatterInteractor import XMDYNPhotonMatterInteractor
from TestUtilities import TestUtilities

class XMDYNPhotonMatterInteractorTest(unittest.TestCase):
    """
    Test class for the XMDYNPhotonMatterInteractor class.
    """

    @classmethod
    def setUpClass(cls):
        """ Setting up the test class. """
        cls.input_h5 = TestUtilities.generateTestFilePath('prop_out_0000001.h5')
        cls.input_xmdyn_dir = TestUtilities.generateTestFilePath('xmdyn_run')

    @classmethod
    def tearDownClass(cls):
        """ Tearing down the test class. """

    def setUp(self):
        """ Setting up a test. """
        self.__files_to_remove = []
        self.__dirs_to_remove = []

    def tearDown(self):
        """ Tearing down a test. """
        # Clean up.
        for f in self.__files_to_remove:
            if os.path.isfile(f):
                os.remove(f)
        for p in self.__dirs_to_remove:
            if os.path.isdir(p):
                shutil.rmtree(p)

    def testConstructionWithDict(self):
        """ Testing the construction of the class with a parameter dictionary. """

        # Setup pmi parameters.
        pmi_parameters = {'number_of_trajectories' : 1,
                          'number_of_steps'        : 100,
                         }

        interactor = XMDYNPhotonMatterInteractor(
                parameters=pmi_parameters,
                output_path='pmi_out',
                input_path=TestUtilities.generateTestFilePath('prop_out_0000001.5'),
                sample_path=TestUtilities.generateTestFilePath('sample.h5'),
                )

        self.assertIsInstance(interactor, XMDYNPhotonMatterInteractor)

    def testConstructionWithParametersNoProp(self):
        """ Testing the construction of the class with a parameter dictionary without propagation input. """
        input_path = PhotonBeamParameters(
                photon_energy = 8.6e3*electronvolt,
                pulse_energy=1.5e-3*joule,
                relative_bandwidth=1e-4,
                divergence=1.0e-3*rad,
                )

         # Setup pmi parameters.
        pmi_parameters = PhotonMatterInteractionParameters(
                number_of_trajectories=1,
                )

        interactor = XMDYNPhotonMatterInteractor(
                parameters=pmi_parameters,
                output_path='pmi_out',
                input_path=input_path,
                sample_path=TestUtilities.generateTestFilePath('sample.h5'),
                )

        self.assertIsInstance(interactor, XMDYNPhotonMatterInteractor)


    def testConstructionWithParameters(self):
        """ Testing the construction of the class with a parameter object. """

        # Setup pmi parameters.
        pmi_parameters = PhotonMatterInteractionParameters(
                number_of_trajectories=1,
                )

        interactor = XMDYNPhotonMatterInteractor(parameters=pmi_parameters,
                                                     output_path='pmi_out',
                                                     input_path=TestUtilities.generateTestFilePath('prop_out_0000001.h5'),
                                                     sample_path=TestUtilities.generateTestFilePath('sample.h5'),
                                                     )

        self.assertIsInstance(interactor, XMDYNPhotonMatterInteractor)

    def testBackengineDefaultPaths(self):
        """ Check that the backengine method works correctly. """

        # Prepare input.
        shutil.copytree( TestUtilities.generateTestFilePath('prop_out'), os.path.abspath( 'prop' ) )
        self.__dirs_to_remove.append( 'prop' )
        self.__dirs_to_remove.append( 'pmi' )

        parameters = PhotonMatterInteractionParameters(number_of_trajectories=1)
        test_interactor = XMDYNPhotonMatterInteractor(
                parameters=parameters,
                input_path=None,
                output_path=None,
                sample_path=TestUtilities.generateTestFilePath('sample.h5') )

        # Call backengine
        status = test_interactor.backengine()

        # Check that the backengine returned zero.
        self.assertEqual(status, 0)

        # Check we have generated the expected output.
        self.assertIn( 'pmi_out_0000001.h5' , os.listdir( test_interactor.output_path ) )

    def testBackengine(self):
        """ Check that the backengine method works correctly. """


        # Clean up.
        self.__dirs_to_remove.append('pmi')

        # Get test instance.
        pmi_parameters = {'number_of_trajectories' : 1,
                          'number_of_steps'        : 100,
                         }

        test_interactor = XMDYNPhotonMatterInteractor(parameters=pmi_parameters,
                                                          input_path=self.input_h5,
                                                          output_path='pmi',
                                                          sample_path = TestUtilities.generateTestFilePath('sample.h5') )

        # Call backengine
        status = test_interactor.backengine()

        # Check that the backengine returned zero.
        self.assertEqual(status, 0)

        # Check we have generated the expected output.
        self.assertTrue( 'pmi_out_0000001.h5' in os.listdir( test_interactor.output_path ) )

    def testLoadPDBFile(self):
        """ Check that the sample can be taken from a pdb directly. """

        # Clean up.
        self.__dirs_to_remove.append('pmi')

        # Get test instance.
        pmi_parameters = {'number_of_trajectories' : 10,
                          'number_of_steps'        : 100,
                         }

        pmi = XMDYNPhotonMatterInteractor(parameters=pmi_parameters,
                                              input_path=self.input_h5,
                                              output_path='pmi',
                                              sample_path=TestUtilities.generateTestFilePath('2nip.pdb') )

        # Call backengine
        status = pmi.backengine()

        self.assertEqual(status, 0 )

    def testIssue53(self):
        """ Check that xmdyn_demo writes the Nph variable according to bugfix 53."""

        # Clean up.
        self.__dirs_to_remove.append('pmi')

        # Get test instance.
        pmi_parameters = {'number_of_trajectories' : 10,
                          'number_of_steps'        : 100,
                         }

        pmi = XMDYNPhotonMatterInteractor(parameters=pmi_parameters,
                                              input_path=self.input_h5,
                                              output_path='pmi',
                                              sample_path=TestUtilities.generateTestFilePath('2nip.pdb') )

        # Call backengine
        status = pmi.backengine()

        h5 = h5py.File('pmi/pmi_out_0000001.h5')
        Nph = h5['/data/snp_0000001/Nph']

        self.assertEqual(Nph.shape, (1,))

    def testRotationNone(self):
        """ Check that by default no rotation is applied and that random rotation has an effect."""

        # Clean up.
        self.__dirs_to_remove.append('pmi')

        # Get test instance.
        pmi_parameters = {'number_of_trajectories' : 1,
                          'number_of_steps'        : 100,
                         }

        test_interactor = XMDYNPhotonMatterInteractor(parameters=pmi_parameters,
                                                          input_path=self.input_h5,
                                                          output_path='pmi',
                                                          sample_path = TestUtilities.generateTestFilePath('sample.h5') )

        # Call backengine
        status = test_interactor.backengine()

        # Check that the backengine returned zero.
        self.assertEqual(status, 0)

        # Check we have generated the expected output.
        # Check rotation angle.
        with h5py.File( os.path.join(test_interactor.output_path, 'pmi_out_0000001.h5'), 'r') as h5:
            angle = h5['data/angle'].value
            self.assertEqual( angle[0,0], 0. )
            self.assertEqual( angle[0,1], 0. )
            self.assertEqual( angle[0,2], 0. )
            self.assertEqual( angle[0,3], 0. )

            # Get atom positions.
            atom_positions = h5['data/snp_0000001/r'].value

        # Now do same calculation again.
        test_interactor.backengine()

        # Get atom positions from new calculation.
        with h5py.File( os.path.join(test_interactor.output_path, 'pmi_out_0000001.h5'), 'r') as h5:
            new_atom_positions = h5['data/snp_0000001/r'].value

        # They should coincide since no rotation has been applied.
        self.assertAlmostEqual( 1e10*numpy.linalg.norm(atom_positions - new_atom_positions), 0.0, 7 )

    def testRotationRandom(self):
        """ Check that by default no rotation is applied and that random rotation has an effect."""

        # Clean up.
        self.__dirs_to_remove.append('pmi')

        # Get test instance.
        pmi_parameters = {'number_of_trajectories' : 1,
                          'number_of_steps'        : 100,
                          'random_rotation'        : True,
                         }

        test_interactor = XMDYNPhotonMatterInteractor(parameters=pmi_parameters,
                                                          input_path=self.input_h5,
                                                          output_path='pmi',
                                                          sample_path = TestUtilities.generateTestFilePath('sample.h5') )

        # Call backengine
        status = test_interactor.backengine()

        # Check that the backengine returned zero.
        self.assertEqual(status, 0)

        # Check we have generated the expected output.
        # Check rotation angle.
        with h5py.File( os.path.join(test_interactor.output_path, 'pmi_out_0000001.h5'), 'r') as h5:
            angle = h5['data/angle'].value[0]

            # Check we have a non-zero rotation.
            self.assertNotEqual( numpy.linalg.norm(angle), 0.)

    def test_write_to_s2e_h5(self):
        """ Test writing to s2e formatted hdf5. """

        self.__files_to_remove.append('pmi')
        # Construct with load path.
        pmi = XMDYNPhotonMatterInteractor(load_from_path=TestUtilities.generateTestFilePath('xmdyn_run'), output_path = 'pmi')

        # Write to h5.
        pmi.saveH5()

        # Check.
        self.assertTrue( os.path.isfile(pmi.output_path))

        # Check groups.
        expected_groups = [
            'data',
            'history',
            'info',
            'misc',
            'params',
            'version',
            ]

        expected_data_groups = [
                    'snp_0000001',
                    'snp_0000002',
                    'snp_0000003',
                    ]

        expected_snapshot_groups = [
                    'Sq_bound',
                    'Sq_free',
                    'Sq_halfQ',
                    'T',
                    'Z',
                    'ff',
                    'halfQ',
                    'r',
                    'xyz',
                    ]

        with h5py.File(pmi.output_path, 'r') as h5:
            present_groups = h5.keys()
            for expected_group in expected_groups:
                self.assertIn(expected_group, present_groups)

            present_groups = h5['data'].keys()
            for expected_group in expected_data_groups:
                self.assertIn(expected_group, present_groups)

            present_groups = h5['data/snp_0000001'].keys()
            for expected_group in expected_snapshot_groups:
                self.assertIn(expected_group, present_groups)

        # Check data shapes.
        # Since this is a single-species calculation, there should be only one row in ff.
        self.assertEqual(h5['data/snp_0000001/ff'].value.shape[0], 1)


    def test_load_snapshot_from_dir(self):
        """ Test loading a xmdyn snapshot from a directory that contains xmdyn output. """

        pmi = XMDYNPhotonMatterInteractor(load_from_path=TestUtilities.generateTestFilePath('xmdyn_run'), output_path = 'pmi')

        snapshot = pmi.f_load_snp_from_dir(os.path.join(self.input_xmdyn_dir, 'snp', '1280'.zfill(8)))

        self.assertIsInstance(snapshot, dict)

        expected_keys = ['Z',
                'T',
                'uid',
                'r',
                'v',
                'm',
                'q',
                'f0',
                'Q',
                ]

        present_keys = snapshot.keys()
        for k in expected_keys:
            self.assertIn(k, present_keys)


if __name__ == '__main__':
    unittest.main()

