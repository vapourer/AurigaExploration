import numpy as np
import pandas as pd
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
        
        print('New tracer_behaviour plot')  
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
        stellar_tracer_masses = []
        gas_tracer_masses = []
        stellar_tracer_counts = []
        gas_tracer_counts = []

        become_dwarf_galaxy = False
        become_larger_than_dwarf_galaxy = False

        for snapshot_number in snapshot_numbers:
            grouped_by_snapshot_number[snapshot_number] = snapshots_grouped[snapshots_grouped['SnapshotNumber'] == snapshot_number]

            subhalo_number = grouped_by_snapshot_number[snapshot_number]['SubhaloNumber'].iloc[0]

            subhalos = data_access.subhalo_as_dataframe.data(self.__output_file_path, snapshot_number).access()
            subhalos_preceding = subhalos[0:subhalo_number]
            subhalo = subhalos.iloc[subhalo_number]

            stellar_particles_start = np.sum(subhalos[0:subhalo_number]['SubhaloStellarLength'])
            stellar_particles_end = stellar_particles_start + subhalo['SubhaloStellarLength']

            gas_particles_start = np.sum(subhalos[0:subhalo_number]['SubhaloGasLength'])
            gas_particles_end = gas_particles_start + subhalo['SubhaloGasLength']
            
            tracer_particles_start = np.sum(subhalos[0:subhalo_number]['SubhaloTracerLength'])
            tracer_particles_end = tracer_particles_start + subhalo['SubhaloTracerLength']

            stellar_disc = data_access.snapshot_raw_as_dataframe.data(self.__output_file_path, snapshot_number, self.__part_type).access()
            gas_disc = data_access.gas_snapshot_dataframe.data(self.__output_file_path, snapshot_number).access()
            tracer_disc = data_access.tracer_snapshot_dataframe.data(self.__output_file_path, snapshot_number).access()

            stellar_particles = stellar_disc[int(stellar_particles_start):int(stellar_particles_end)]
            gas_particles = gas_disc[int(gas_particles_start):int(gas_particles_end)]
            tracer_particles = tracer_disc[int(tracer_particles_start):int(tracer_particles_end)]

            stellar_particle_ids_with_tracers = set(stellar_particles['ParticleID']).intersection(set(tracer_particles['TracerParentID']))
            gas_particle_ids_with_tracers = set(gas_particles['ParticleID']).intersection(set(tracer_particles['TracerParentID']))

            stellar_tracer_particles = stellar_particles[stellar_particles['ParticleID'].isin(stellar_particle_ids_with_tracers)]
            gas_tracer_particles = gas_particles[gas_particles['ParticleID'].isin(gas_particle_ids_with_tracers)]

            # breakpoint()

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
                    if subhalo_number > 0:
                        larger_than_dwarf_galaxy_redshift = grouped_by_snapshot_number[snapshot_number]['Redshift'].iloc[0]

                    become_larger_than_dwarf_galaxy = True

            if subhalo_number > 0:
                redshift.append(grouped_by_snapshot_number[snapshot_number]['Redshift'].iloc[0])

                stellar_mass = (10**10) * np.max(grouped_by_snapshot_number[snapshot_number]['StellarMass']) / h
                gas_mass = (10**10) * np.max(grouped_by_snapshot_number[snapshot_number]['GasMass']) / h
                stellar_masses.append(stellar_mass)
                gas_masses.append(gas_mass)
                combined_masses.append(stellar_mass + gas_mass)

                stellar_tracer_masses.append(np.sum(stellar_tracer_particles['Mass']))
                gas_tracer_masses.append(np.sum(gas_tracer_particles['Mass']))
                stellar_tracer_counts.append(len(stellar_tracer_particles['ParticleID']))
                gas_tracer_counts.append(len(gas_tracer_particles['ParticleID']))

        data_structure = {'Redshift': redshift,
                          'StellarMass': stellar_masses,
                          'GasMass': gas_masses,
                          'CombinedMass': combined_masses,
                          'StellarTracerMass': stellar_tracer_masses,
                          'GasTracerMass': gas_tracer_masses,
                          'StellarTracerCount': stellar_tracer_counts,
                          'GasTracerCount': gas_tracer_counts}
                
        data = pd.DataFrame(data_structure)
        data.to_csv(f'./output/halo_6/tracer_behaviour/TracerBehaviourAgainstRedshift_{self.__peak_mass_index}.csv')

        # plt.plot(redshift, stellar_masses, label='Stellar mass', color='b')
        # plt.plot(redshift, gas_masses, label='Gas mass', color='y')
        plt.plot(redshift, stellar_tracer_masses, label='Stellar tracer mass', color='b')
        plt.plot(redshift, gas_tracer_masses, label='Gas tracer mass', color='y')
        plt.axvline(dwarf_galaxy_redshift, 0, 1, linestyle='--', color='g', alpha=0.4, label='Stellar mass reached $10^7_{\odot}$')        

        if larger_than_dwarf_galaxy_redshift > 0:
            plt.axvline(larger_than_dwarf_galaxy_redshift, 0, 1, linestyle='--', color='r', alpha=0.4, label='Stellar mass exceeded $10^9_{\odot}$')

        plt.gca().invert_xaxis()
        plt.xlabel('Redshift')
        plt.ylabel('Mass (in solar masses)')
        plt.legend()
        plt.title(f'Tracer behaviours against redshift for peak mass index {self.__peak_mass_index}')
        plt.savefig(f'./output/halo_6/tracer_behaviour/TracerBehaviourAgainstRedshift_{self.__peak_mass_index}.png')


 
        