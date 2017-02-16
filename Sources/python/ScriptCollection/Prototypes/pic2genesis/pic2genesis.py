##########################################################################
#                                                                        #
# Copyright (C) 2016 Carsten Fortmann-Grote, Ashutosh Sharma             #
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

""" :module pic2genesis: Script to convert openpmd output from picongpu to a genesis beam.dat file. """

import numpy
import h5py
import sys, os

from scipy.constants import m_e, c

def pic2genesis( pic_file_name):
    """ Utility to extract particle data from openPMD and write into genesis distribution file.
    
    :params pic_file_name: Filename of openpmd input data file.
    """
    
    #  Check path.
    if not os.path.isfile(pic_file_name):
        raise RuntimeError("%s is not a file." % (pic_file_name))
        
    # Check if input is native or openPMD.
    with h5py.File( pic_file_name, 'r' ) as h5_handle:

        timestep = h5_handle['data'].keys()[-1]

        h5_positions = '/data/%s/particles/e/position/' % (timestep)
        h5_momenta = '/data/%s/particles/e/momentum/' % (timestep)

        x_data = h5_handle[h5_positions]['x'].value
        x_data_unit = h5_handle[h5_positions]['x'].attrs['unitSI']
        x = x_data*x_data_unit

        y_data = h5_handle[h5_positions]['y'].value
        y_data_unit = h5_handle[h5_positions]['y'].attrs['unitSI']
        y = y_data*y_data_unit

        z_data = h5_handle[h5_positions]['z'].value
        z_data_unit = h5_handle[h5_positions]['z'].attrs['unitSI']
        z = z_data*z_data_unit

        px_data = h5_handle[h5_momenta]['x'].value
        px_data_unit = h5_handle[h5_momenta]['x'].attrs['unitSI']
        px = px_data*px_data_unit
        


        py_data = h5_handle[h5_momenta]['y'].value
        py_data_unit = h5_handle[h5_momenta]['y'].attrs['unitSI']
        py = py_data*py_data_unit

        pz_data = h5_handle[h5_momenta]['z'].value
        pz_data_unit = h5_handle[h5_momenta]['z'].attrs['unitSI']
        pz = pz_data*pz_data_unit
        
        # Convert to xprime, yprime.
        xprime = numpy.arctan(px/py)
        zprime = numpy.arctan(pz/py)            
        
        # Calculate particle charge.
        charge_group = h5_handle['/data/%d/particles/e/charge/' %(timestep)]

        charge_value = charge_group.attrs['value']
        charge_unit = charge_group.attrs['unitSI']
        charge = charge_value * charge_unit # 1e in As
        
        # Get number of particles and total charge.
        particle_patches = h5_handle['/data/%d/particles/e/particlePatches/numParticles' %(timestep)].value
        total_number_of_electrons = numpy.sum( particle_patches )
        total_charge = total_number_of_electrons * charge

        # Calculate momentum
        psquare = px**2 + py**2 + pz**2
        #gamma = numpy.sqrt( 1. + psquare/((m_e*c)**2))
        P = numpy.sqrt(psquare/((m_e*c)**2))
        
        h5_handle.close()
        
        return numpy.vstack([ x, xprime, z, zprime, y/c, P]).transpose(),  total_charge

if __name__ == "__main__":
    data, charge = pic2genesis(sys.argv[1])
    # Setup header for distribution file.
    comments = "? "
    size = data.shape[0]
    header = "VERSION = 1.0\nSIZE = %d\nCHARGE = %7.6E\nCOLUMNS X XPRIME Y YPRIME T P" % (size, charge)

    numpy.savetxt( fname='beam.dist', X=data, header=header, comments=comments)

