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
        
        print('Generate stellar_history_specify_radius output')
        self.__output_file_path = output_file_path
        self.__list_directory = list_file_path
        self.__snap_num = snap_num
        self.__part_type = part_type
        self.__halo = halo
        self.__radius = radius

    def output(self) -> None:
        disc_final, _, _, _, _, _ = data_access.disc_specify_radius.data(self.__output_file_path,
                                                          self.__snap_num,
                                                          self.__part_type,
                                                          self.__radius).access()
        
        insitu, exsitu = data_access.starparticle_mergertree.data(self.__list_directory,
                                                                  self.__snap_num,
                                                                  self.__halo).access()

        print()
        print(f'disc_final ParticleID count = {len(disc_final["ParticleID"])}')
        print(f'insitu ParticleID count = {len(insitu["ParticleID"])}')
        print(f'exsitu ParticleID count = {len(exsitu["ParticleID"])}')
        print(f'exsitu PeakMassIndex count = {len(exsitu["PeakMassIndex"])}')
        print()

        reduced_disc_insitu_particles = set(insitu["ParticleID"]).intersection(set(disc_final['ParticleID']))
        reduced_disc_exsitu_particles = set(exsitu["ParticleID"]).intersection(set(disc_final['ParticleID']))

        print(f'reduced_disc_insitu_particles count = {len(reduced_disc_insitu_particles)}')
        print(f'reduced_disc_exsitu_particles count = {len(reduced_disc_exsitu_particles)}')
        print()
        
        grouped_by_peak_mass_index = exsitu.groupby(['PeakMassIndex']).count()

        print()
        print(f'grouped_by_peak_mass_index ({len(grouped_by_peak_mass_index)} records)')
        print(grouped_by_peak_mass_index)
        print()

        grouped_by_peak_mass_index_desc = grouped_by_peak_mass_index.sort_values(by='PeakMassIndex', ascending=False)
        print('grouped_by_peak_mass_index_desc')
        print(grouped_by_peak_mass_index_desc)
        print()
