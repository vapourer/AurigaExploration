import numpy as np
import pandas as pd
from .disc_specify_radius import data as disc_data
from .starparticle_mergertree import data as starparticle_mergertree_data
import auriga_public.auriga_public as ap

class data:
    def __init__(self,
                 output_file_path: str,
                 list_file_path: str,
                 snap_num: int,
                 part_type: int,
                 halo: str,
                 radius: float) -> None:
        
        print('Access spatial_distribution_accreted_stars_by_PeakMassIndex data')
        self.__output_file_path = output_file_path
        self.__list_directory = list_file_path
        self.__snap_num = snap_num
        self.__part_type = part_type
        self.__halo = halo
        self.__radius = radius

    def access(self):
        bounded_disc, _, _, _, _, _ = disc_data(self.__output_file_path, self.__snap_num, self.__part_type, self.__radius).access()        
        _, exsitu = starparticle_mergertree_data(self.__list_directory, self.__snap_num, self.__halo).access()

        reduced_disc_exsitu_particles = set(exsitu["ParticleID"]).intersection(set(bounded_disc['ParticleID']))
        bounded_disc_exsitu = bounded_disc[bounded_disc['ParticleID'].isin(reduced_disc_exsitu_particles)]
        reduced_exsitu = exsitu[(exsitu["ParticleID"].isin(reduced_disc_exsitu_particles)) & (exsitu['AccretedFlag'] == 0)]

        peak_mass_indices = set(reduced_exsitu['PeakMassIndex'])        

        bounded_disc_exsitu_merged = pd.merge(bounded_disc_exsitu, reduced_exsitu, on='ParticleID', how='inner')

        return bounded_disc_exsitu_merged, peak_mass_indices
