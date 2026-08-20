import numpy as np
import pandas as pd
import data_access
from data_access import *

class data:
    def __init__(self,
                 output_file_path: str, 
                 list_file_path: str,
                 tree_file_path: str,
                 snap_num: int,
                 part_type: int,
                 halo: str,
                 radius: float) -> None:
        
        print('New halo_6_selected_exsitu_groups_histories plot')
        self.__output_file_path = output_file_path
        self.__list_directory = list_file_path
        self.__tree_directory = tree_file_path
        self.__snap_num = snap_num
        self.__part_type = part_type
        self.__halo = halo
        self.__radius = radius

    def output(self):
        disc, _, _, _, _, _ = data_access.disc_specify_radius.data(self.__output_file_path,
                                                          self.__snap_num,
                                                          self.__part_type,
                                                          self.__radius).access()
        
        insitu, exsitu = data_access.starparticle_mergertree.data(self.__list_directory,
                                                                  self.__snap_num,
                                                                  self.__halo).access()
        
        tree, _ = data_access.merger_tree_as_dataframe.data(self.__tree_directory, self.__snap_num).access()

        # snapshots = tree.data['SnapNum']
        # snapshots = np.sort(np.fromiter(set(snapshots), np.int32))

        reduced_disc_insitu_particles = set(insitu["ParticleID"]).intersection(set(disc['ParticleID']))
        reduced_disc_exsitu_particles = set(exsitu["ParticleID"]).intersection(set(disc['ParticleID']))

        reduced_disc_insitu = disc[disc['ParticleID'].isin(reduced_disc_insitu_particles)]
        reduced_disc_exsitu = disc[disc['ParticleID'].isin(reduced_disc_exsitu_particles)]

        reduced_exsitu = exsitu[exsitu['ParticleID'].isin(reduced_disc_exsitu_particles)]

        reduced_disc_exsitu = pd.merge(reduced_disc_exsitu, reduced_exsitu, on='ParticleID', how='inner')
        peak_mass_indices = np.array([377, 918, 23050, 36275, 36900, 37138, 37333, 188717, 190063])

        exsitu_columns = reduced_disc_exsitu.columns
        exsitu_selected = [pd.DataFrame(columns=exsitu_columns)]