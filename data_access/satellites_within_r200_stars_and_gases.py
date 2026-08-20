import numpy as np
from .satellites import data as satellites_data
import auriga_public.auriga_public as ap

class data:
    def __init__(self, file_path: str, snap_num: int) -> None:
        print('Access satellites_within_r200_stars_and_gases data')
        self.__file_path = file_path
        self.__snap_num = snap_num

    def access(self):
        distance, r200, mass, subobj = satellites_data(self.__file_path, self.__snap_num).access()

        smass = subobj.data['SubhaloMassType'][:,4]
        gmass = subobj.data['SubhaloMassType'][:,0]

        distance_index, = np.where( (distance <= r200) & (distance > 0) )
        distance_index_star, = np.where( (distance <= r200) & (distance > 0) & (smass > 0.) )
        distance_index_gas, = np.where( (distance <= r200) & (distance > 0) & (gmass > 0.) ) 

        distance_star = distance[distance_index_star]
        distance_gas = distance[distance_index_gas]
        distance = distance[distance_index]
        
        # smass = smass[distance_index_star]
        smass = mass[distance_index_star]
        # gmass = gmass[distance_index_gas]
        gmass = mass[distance_index_gas]
        mass = mass[distance_index]

        return distance, distance_star, distance_gas, r200, mass, smass, gmass