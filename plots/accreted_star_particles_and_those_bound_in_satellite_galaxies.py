import matplotlib.pyplot as plt
import data_access
from data_access import *

class plot:
    def __init__(self,
                 output_file_path: str,
                 list_file_path: str,
                 snap_num: int,
                 part_type: int,
                 halo: str) -> None:
        
        print('New accreted_star_particles_and_those_bound_in_satellite_galaxies plot')
        self.__output_file_path = output_file_path
        self.__list_file_path = list_file_path
        self.__snap_num = snap_num
        self.__part_type = part_type
        self.__halo = halo

    def create(self) -> None:
        (radii_accreted,
        radial_velocities_accreted,
        radii_insat,
        radial_velocities_insat) \
        = data_access.accreted_star_particles_and_those_bound_in_satellite_galaxies.data(self.__output_file_path,
                                                                                         self.__list_file_path,
                                                                                         self.__snap_num,
                                                                                         self.__part_type,
                                                                                         self.__halo).access()

        _, ax = plt.subplots(1, 1, figsize=(6, 4.5), tight_layout=True)
        ax.scatter( radii_accreted, radial_velocities_accreted, c='r', s=5, marker='.', linewidth=0, alpha=0.2 )
        ax.scatter( radii_insat, radial_velocities_insat, c='b', s=5, marker='.', linewidth=0, alpha=0.2 )
        plt.savefig(f'./output/{self.__halo}/original_plots/AccretedStarParticlesAndThoseBoundInSatelliteGalaxies_{self.__snap_num}.png')
