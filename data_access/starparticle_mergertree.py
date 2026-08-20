import numpy as np
import pandas as pd
import auriga_public.auriga_public as ap

class data:
    def __init__(self, list_file_path: str, snap_num: int, halo: str) -> None:
        print('Access starparticle_mergertree data')
        self.__list_directory = list_file_path
        self.__snap_num = snap_num
        self.__halo = halo

    def access(self):

        starparticle_mergertree_data = ap.util.read_starparticle_mergertree_data_hdf5(self.__snap_num, self.__list_directory, self.__halo)

        insitu = pd.DataFrame({'ParticleID': starparticle_mergertree_data['Insitu']['ParticleIDs']})

        exsitu_data_structure = {'ParticleID': starparticle_mergertree_data['Exsitu']['ParticleIDs'],
                                 'PeakMassIndex': starparticle_mergertree_data['Exsitu']['PeakMassIndex'],
                                 'BoundFirstTime': starparticle_mergertree_data['Exsitu']['BoundFirstTime'],
                                 'AccretedFlag': starparticle_mergertree_data['Exsitu']['AccretedFlag'],
                                 'BirthSubhaloIndex': starparticle_mergertree_data['Exsitu']['BirthSubhaloindex'],
                                 'BirthSnapshot': starparticle_mergertree_data['Exsitu']['BirthSnap'],
                                 'RootIndex': starparticle_mergertree_data['Exsitu']['RootIndex']}

        return insitu, pd.DataFrame(exsitu_data_structure)
