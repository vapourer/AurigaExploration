import pandas as pd
import data_access
from data_access import *

class data:
    def __init__(self,
                 output_file_path: str,
                 list_file_path: str,
                 snap_num: int,
                 part_type: int,
                 halo: str,
                 radius: float) -> None:
        
        print('Generate group_by_peak_mass_index output')
        self.__output_file_path = output_file_path
        self.__list_directory = list_file_path
        self.__snap_num = snap_num
        self.__part_type = part_type
        self.__halo = halo
        self.__radius = radius

    def output(self):
        bounded_disc_exsitu, peak_mass_indices = data_access.spatial_distribution_accreted_stars_by_PeakMassIndex.data(self.__output_file_path,
                                                                              self.__list_directory,
                                                                              self.__snap_num,
                                                                              self.__part_type,
                                                                              self.__halo,
                                                                              self.__radius).access()
        
        print()
        print(f'peak_mass_indices ({len(peak_mass_indices)})')
        print(peak_mass_indices)
        print()

        grouped = bounded_disc_exsitu[['PeakMassIndex', 'ParticleID']]
        grouped = grouped.groupby(['PeakMassIndex']).count()

        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)

        print()
        print(f'Particle count grouped by PeakMassIndex ({len(grouped)})')
        print(grouped)
        print()

        grouped = bounded_disc_exsitu[['PeakMassIndex', 'Mass']]
        grouped = grouped.groupby(['PeakMassIndex']).sum()

        print()
        print(f'Total particle mass grouped by PeakMassIndex ({len(grouped)})')
        print(grouped)
        print()

        grouped = grouped.sort_values('Mass', ascending=False)

        print()
        print(f'Total particle mass grouped by PeakMassIndex ordered by mass (descending)')
        print(grouped)
        print()

        grouped = bounded_disc_exsitu[['PeakMassIndex', 'InitialMass']]
        grouped = grouped.groupby(['PeakMassIndex']).sum()

        print()
        print(f'Total particle initial mass grouped by PeakMassIndex ({len(grouped)})')
        print(grouped)
        print()
