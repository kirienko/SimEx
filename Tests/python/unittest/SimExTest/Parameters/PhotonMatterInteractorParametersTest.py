""" :module: Test module hosting the test for the SingFELPhotonDiffractorParameter class."""
##########################################################################
#                                                                        #
# Copyright (C) 2016-2018 Carsten Fortmann-Grote                         #
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

import os
import shutil

# Include needed directories in sys.path.
import unittest

from SimEx.Parameters.AbstractCalculatorParameters import AbstractCalculatorParameters
from SimEx.Parameters.PhotonMatterInteractorParameters import PhotonMatterInteractorParameters

from TestUtilities.TestUtilities import generateTestFilePath


class PhotonMatterInteractorParametersTest(unittest.TestCase):
    """
    Test class for the PhotonMatterInteractorParameters class.
    """

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        """ Tearing down the test class. """
        pass

    def setUp(self):
        """ Setting up a test. """
        self.__files_to_remove = []
        self.__dirs_to_remove = []

    def tearDown(self):
        """ Tearing down a test. """
        for f in self.__files_to_remove:
            if os.path.isfile(f):
                os.remove(f)
        for d in self.__dirs_to_remove:
            if os.path.isdir(d):
                shutil.rmtree(d)

    def testDefaultConstruction(self):
        """ Testing the default construction of the class using a dictionary. """

        # Attempt to construct an instance of the class.
        parameters = PhotonMatterInteractorParameters()

        self.assertIsInstance(parameters, PhotonMatterInteractorParameters)

        self.assertEqual(parameters.rotation, [1,0,0,0])
        self.assertFalse(parameters.calculate_Compton)
        self.assertEqual(parameters.number_of_trajectories, 1)

        self.assertEqual(parameters._AbstractCalculatorParameters__cpus_per_task_default, 1)

    def testShapedConstruction(self):
        """ Testing the default construction of the class using a dictionary. """

        # Attempt to construct an instance of the class.
        parameters = PhotonMatterInteractorParameters(
            rotation=[-0.5, 0.5, 0.5, 0.5],
            calculate_Compton=True,
            number_of_trajectories=100
            )

        self.assertEqual(parameters.rotation, [-0.5, 0.5, 0.5, 0.5])
        self.assertTrue(parameters.calculate_Compton)
        self.assertEqual(parameters.number_of_trajectories, 100)

    def testConstructionFaultyInput(self):
        """ Test the exceptions risen on faulty parameter input. """

        self.assertRaises( PhotonMatterInteractorParameters, rotation=2.0)
        self.assertRaises( PhotonMatterInteractorParameters, rotation=[])
        self.assertRaises( PhotonMatterInteractorParameters, rotation=[1.0, 0, 0])
        self.assertRaises( PhotonMatterInteractorParameters, rotation=[1, 'O', 'O', 'P' ])



if __name__ == '__main__':
    unittest.main()
