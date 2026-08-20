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
        
        print('New stellar_gas_masses_against_redshift plot')  
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

        snapshots_grouped, snapshot_numbers = data_access.navigate_merger_tree.data(self.__output_file_path,
                                                                                    self.__list_directory,
                                                                                    self.__tree_directory,
                                                                                    self.__snap_num,
                                                                                    self.__part_type,
                                                                                    self.__halo,
                                                                                    self.__radius,
                                                                                    self.__peak_mass_index).access()

        grouped_by_snapshot_number = {}

        redshift = []
        stellar_masses = []
        gas_masses = []
        combined_masses = []
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
                redshift.append(grouped_by_snapshot_number[snapshot_number]['Redshift'].iloc[0])

                stellar_mass = (10**10) * np.max(grouped_by_snapshot_number[snapshot_number]['StellarMass']) / h
                gas_mass = (10**10) * np.max(grouped_by_snapshot_number[snapshot_number]['GasMass']) / h
                stellar_masses.append(stellar_mass)
                gas_masses.append(gas_mass)
                combined_masses.append(stellar_mass + gas_mass)

        plt.plot(redshift, stellar_masses, label='Stellar mass', color='b')
        plt.plot(redshift, gas_masses, label='Gas mass', color='y')
        plt.plot(redshift, combined_masses, label='Stellar and gas masses combined', color='m')
        plt.axvline(dwarf_galaxy_redshift, 0, 1, linestyle='--', color='g', alpha=0.4, label='Stellar mass reached $10^7_{\odot}$')        

        if larger_than_dwarf_galaxy_redshift > 0:
            plt.axvline(larger_than_dwarf_galaxy_redshift, 0, 1, linestyle='--', color='r', alpha=0.4, label='Stellar mass exceeded $10^9_{\odot}$')

        plt.gca().invert_xaxis()
        plt.xlabel('Redshift')
        plt.ylabel('Mass (in solar masses)')
        plt.legend()
        plt.title(f'Stellar and gas masses against redshift for peak mass index {self.__peak_mass_index}')
        plt.savefig(f'./output/halo_6/stars_and_gas/MassRedshift_{self.__peak_mass_index}.png')


 
        