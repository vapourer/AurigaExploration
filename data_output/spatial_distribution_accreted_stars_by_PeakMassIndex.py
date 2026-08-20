import pandas as pd
import data_access
from data_access import *
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
        
        print('Generate spatial_distribution_accreted_stars_by_PeakMassIndex output')
        self.__output_file_path = output_file_path
        self.__list_directory = list_file_path
        self.__snap_num = snap_num
        self.__part_type = part_type
        self.__halo = halo
        self.__radius = radius

    def output(self):
        bounded_disc, _, _, _, _, _ = data_access.disc_specify_radius.data(self.__output_file_path, self.__snap_num, self.__part_type, self.__radius).access()

        print()
        print(f'bounded_disc {(type(bounded_disc))}')
        print(f'Length: {len(bounded_disc["ParticleID"])}')
        print(f'ParticleID field is unique: {bounded_disc["ParticleID"].is_unique}')
        print(bounded_disc)
        print()
        
        _, exsitu = data_access.starparticle_mergertree.data(self.__list_directory, self.__snap_num, self.__halo).access()

        print()
        print(f'exsitu {(type(exsitu))}')
        print(f'Length: {len(exsitu["ParticleID"])}')
        print(exsitu)
        print()

        reduced_disc_exsitu_particles = set(exsitu["ParticleID"]).intersection(set(bounded_disc['ParticleID']))

        bounded_disc_exsitu = bounded_disc[bounded_disc['ParticleID'].isin(reduced_disc_exsitu_particles)]

        reduced_exsitu = exsitu[exsitu["ParticleID"].isin(reduced_disc_exsitu_particles)]

        print()
        print(f'bounded_disc_exsitu {(type(bounded_disc_exsitu))}')
        print(f'Length: {len(bounded_disc_exsitu["ParticleID"])}')
        print(bounded_disc_exsitu)
        print()

        print()
        print(f'reduced_exsitu {(type(reduced_exsitu))}')
        print(f'Length: {len(reduced_exsitu["ParticleID"])}')
        print(reduced_exsitu)
        print()

        grouped_by_peak_mass_index = exsitu.groupby(['PeakMassIndex']).count()

        print()
        print(f'grouped_by_peak_mass_index {(type(grouped_by_peak_mass_index))}')
        print(f'{len(grouped_by_peak_mass_index)} rows')
        print(grouped_by_peak_mass_index)
        print()

        # pd.set_option('display.max_rows', None)
        # pd.set_option('display.max_columns', None)
        # pd.set_option('display.width', None)

        reduced_grouped_by_peak_mass_index = reduced_exsitu.groupby(['PeakMassIndex']).count()

        print()
        print(f'reduced_grouped_by_peak_mass_index {(type(reduced_grouped_by_peak_mass_index))}')
        print(f'{len(reduced_grouped_by_peak_mass_index)} rows')
        print(reduced_grouped_by_peak_mass_index)
        print()
        
        bounded_disc_exsitu_merged = pd.merge(bounded_disc_exsitu, reduced_exsitu, on='ParticleID', how='inner')
        
        print()
        print(f'bounded_disc_exsitu_combined {(type(bounded_disc_exsitu_merged))}')
        print(f'{len(bounded_disc_exsitu_merged)} rows')
        print(bounded_disc_exsitu_merged)
        print()