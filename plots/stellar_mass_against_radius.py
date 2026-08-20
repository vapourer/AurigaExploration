import numpy as np
import matplotlib.pyplot as plt
import data_access
from data_access import *

class plot:
    def __init__(self,
                 output_file_path: str,
                 list_file_path: str,
                 tree_file_path: str,
                 snap_num: int,
                 part_type: int,
                 halo: int,
                 radius: float,                 
                 peak_mass_index: int) -> None:
        
        print('New stellar_mass_against_radius plot')  
        self.__output_file_path = output_file_path
        self.__list_directory = list_file_path
        self.__tree_directory = tree_file_path
        self.__snap_num = snap_num
        self.__part_type = part_type
        self.__halo = halo 
        self.__radius = radius
        self.__peak_mass_index = peak_mass_index            

    def create(self) -> None:

        h = 0.6777
        c = (299792458 / 1000) / (3.0857 * (10**16))

        snapshots_grouped, snapshot_numbers = data_access.navigate_merger_tree.data(self.__output_file_path,
                                                                                    self.__list_directory,
                                                                                    self.__tree_directory,
                                                                                    self.__snap_num,
                                                                                    self.__part_type,
                                                                                    self.__halo,
                                                                                    self.__radius,
                                                                                    self.__peak_mass_index).access()

        grouped_by_snapshot_number = {}

        radius = []
        mass = []
        dwarf_galaxy_redshift = -1
        larger_than_dwarf_galaxy_redshift = -1

        become_dwarf_galaxy = False
        become_larger_than_dwarf_galaxy = False

        for snapshot_number in snapshot_numbers:
            grouped_by_snapshot_number[snapshot_number] = snapshots_grouped[snapshots_grouped['SnapshotNumber'] == snapshot_number]

            subhalo = grouped_by_snapshot_number[snapshot_number]['SubhaloNumber'].iloc[0]

            if not become_dwarf_galaxy:
                dwarf_galaxy_check = grouped_by_snapshot_number[snapshot_number]['DwarfGalaxy']
                dwarf_galaxy = np.sum(dwarf_galaxy_check) > 0

                if dwarf_galaxy:
                    dwarf_galaxy_redshift = grouped_by_snapshot_number[snapshot_number]['Redshift'].iloc[0]
                    become_dwarf_galaxy = True

            if become_dwarf_galaxy and not become_larger_than_dwarf_galaxy:
                larger_than_dwarf_galaxy_check = grouped_by_snapshot_number[snapshot_number]['GreaterThanDwarf']
                larger_than_dwarf_galaxy = np.sum(larger_than_dwarf_galaxy_check) > 0

                if larger_than_dwarf_galaxy:
                    if subhalo > 0:
                        larger_than_dwarf_galaxy_redshift = grouped_by_snapshot_number[snapshot_number]['Redshift'].iloc[0]

                    become_larger_than_dwarf_galaxy = True

            if subhalo > 0:
                radius.append(c * (10**3) * grouped_by_snapshot_number[snapshot_number]['StellarHalfMassRadius'].iloc[0] / h)
                mass.append((10**10) * np.max(grouped_by_snapshot_number[snapshot_number]['StellarMass']) / h)

        plt.scatter(radius, mass, s=20)
        
        plt.xlabel('Stellar half mass radius (kpc)')
        plt.ylabel('Stellar mass (in solar masses)')

        plt.title(f'Stellar mass against stellar half mass radius for peak mass index {self.__peak_mass_index}')
        plt.savefig(f'./output/halo_6/stellar_mass_histories/MassRadius_{self.__peak_mass_index}.png')


 
        