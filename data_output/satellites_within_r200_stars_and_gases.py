import numpy as np
import matplotlib.pyplot as plt
import data_access
from data_access import *

class data:
    def __init__(self, file_path: str, snap_num: int) -> None:
        print('New satellites_within_r200_stars_and_gases output')
        self.__file_path = file_path
        self.__snap_num = snap_num

    def output(self) -> None:
        (distance,
         distance_star,
         distance_gas,
         r200,
         mass,
         smass,
         gmass) = data_access.satellites_within_r200_stars_and_gases.data(self.__file_path,
                                                                          self.__snap_num).access()
        
        print(f'r200 = {r200}')
        print()

        print(f'distance ({len(distance)})')
        print(distance)
        print()

        print(f'mass ({len(mass)})')
        print(mass)
        print()

        print(f'distance_star ({len(distance_star)})')
        print(distance_star)
        print()

        print(f'smass ({len(smass)})')
        print(smass)
        print()

        print(f'distance_gas ({len(distance_gas)})')
        print(distance_gas)
        print()

        print(f'gmass ({len(gmass)})')
        print(gmass)
        print()

