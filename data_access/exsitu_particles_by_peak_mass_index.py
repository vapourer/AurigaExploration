import numpy as np
import pandas as pd
from .disc_specify_radius import data as disc_data
from .starparticle_mergertree import data as starparticle_mergertree_data
from .merger_tree_as_dataframe import data as merger_tree_as_dataframe_data
import auriga_public.auriga_public as ap

class data:
    text = []

    def __init__(self,
                 output_file_path: str,
                 list_file_path: str,
                 snap_num: int,
                 part_type: int,
                 halo: int,
                 radius: float,                 
                 peak_mass_index: int) -> None:
        
        print('Access exsitu_particles_by_peak_mass_index data')
        self.__output_file_path = output_file_path
        self.__list_directory = list_file_path
        self.__snap_num = snap_num
        self.__part_type = part_type
        self.__halo = halo
        self.__radius = radius
        self.__peak_mass_index = peak_mass_index        

    def access(self):

        bounded_disc, _, _, _, _, _ = disc_data(self.__output_file_path,
                                                          self.__snap_num,
                                                          self.__part_type,
                                                          self.__radius).access()
        
        _, exsitu = starparticle_mergertree_data(self.__list_directory, self.__snap_num, self.__halo).access()

        reduced_disc_exsitu_particles = set(exsitu["ParticleID"]).intersection(set(bounded_disc['ParticleID']))

        reduced_exsitu = exsitu[(exsitu["ParticleID"].isin(reduced_disc_exsitu_particles)) & (exsitu['AccretedFlag'] == 0)]

        return reduced_exsitu[reduced_exsitu['PeakMassIndex'] == self.__peak_mass_index]