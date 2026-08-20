import numpy as np
from .disc import data as disc_data
import auriga_public.auriga_public as ap

class data:
    def __init__(self, output_file_path: str, list_file_path: str, snap_num: int, part_type: int, halo: str) -> None:
        print('Access accreted_star_particles_and_those_bound_in_satellite_galaxies data')
        self.__output_file_path = output_file_path
        self.__list_directory = list_file_path
        self.__snap_num = snap_num
        self.__part_type = part_type
        self.__halo = halo

    def access(self):
        snapobj, _ = disc_data(self.__output_file_path, self.__snap_num, self.__part_type).access()
        
        mdata = ap.util.read_starparticle_mergertree_data_hdf5(self.__snap_num, self.__list_directory, self.__halo)

        index_accreted, = np.where((mdata['Exsitu']['AccretedFlag']==0))
        id_index, = np.where( np.in1d( snapobj.data['ParticleIDs'], mdata['Exsitu']['ParticleIDs'][index_accreted] ) )
        prog_star_positions = snapobj.data['Coordinates'][id_index]
        prog_star_velocities = snapobj.data['Velocities'][id_index]
        radii_accreted = np.sqrt( np.sum(prog_star_positions**2, axis=1) )
        radial_velocities_accreted = np.sum(prog_star_positions * prog_star_velocities, axis=1) / radii_accreted

        index_insat, = np.where((mdata['Exsitu']['AccretedFlag']==1))
        id_index, = np.where( np.in1d( snapobj.data['ParticleIDs'], mdata['Exsitu']['ParticleIDs'][index_insat] ) )
        prog_star_positions = snapobj.data['Coordinates'][id_index]
        prog_star_velocities = snapobj.data['Velocities'][id_index]
        radii_insat = np.sqrt( np.sum(prog_star_positions**2, axis=1) )
        radial_velocities_insat = np.sum(prog_star_positions * prog_star_velocities, axis=1) / radii_insat

        return radii_accreted, radial_velocities_accreted, radii_insat, radial_velocities_insat