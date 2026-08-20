import data_access
from data_access import *

class data:
    def __init__(self, file_path: str, snap_num: int, part_type: int, halo: str, radius: float) -> None:
        print('Generate disc_specify_radius output')
        self.__file_path = file_path
        self.__snap_num = snap_num
        self.__part_type = part_type
        self.__halo = halo
        self.__radius = radius

    def output(self) -> None:
        bounded_disc, _, _, _, _, _ = data_access.disc_specify_radius.data(self.__file_path, self.__snap_num,
                                                            self.__part_type, self.__radius).access()
        
        print(f'Length of bounded_disc: {len(bounded_disc["Radius"])}')

        print('Columns')
        print(bounded_disc.columns)
        print()

        print(f'ParticleID is unique: {bounded_disc["ParticleID"].is_unique}')
        print()
        
        print(bounded_disc)
        print()

        radius_kpc = int(self.__radius * 1000)
        disc_size = f'Within{radius_kpc}kpc'     

        print(f'Total mass = {sum(bounded_disc["Mass"])}')   

        # if self.__radius < 0:
        #     disc_size = 'R200'

        # bounded_disc.to_csv(f'./output/{self.__halo}/disc/Disc_{disc_size}_{self.__snap_num}.csv', index=False)
        
