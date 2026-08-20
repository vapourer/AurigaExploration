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
                 radius: float) -> None:
        
        print('New insitu_stellar_mass_against_redshift plot')  
        self.__output_file_path = output_file_path
        self.__list_directory = list_file_path
        self.__tree_directory = tree_file_path
        self.__snap_num = snap_num
        self.__part_type = part_type
        self.__halo = halo 
        self.__radius = radius     

    def create(self) -> None:

        h = 0.6777

        disc_final, _, _, _, _, _ = data_access.disc_specify_radius.data(self.__output_file_path,
                                                          self.__snap_num,
                                                          self.__part_type,
                                                          self.__radius).access()
        
        tree, _ = data_access.merger_tree_as_dataframe.data(self.__tree_directory, self.__snap_num).access()
        redshift_for_snapshot = tree[['SnapshotNumber', 'Redshift']]
        
        redshift_for_snapshot_unique = {}

        for snapshot in redshift_for_snapshot['SnapshotNumber']:
            if not snapshot in redshift_for_snapshot_unique.keys():
                redshift_for_snapshot_unique[snapshot] = redshift_for_snapshot['Redshift'].iloc[0]

        insitu, _ = data_access.starparticle_mergertree.data(self.__list_directory,
                                                                  self.__snap_num,
                                                                  self.__halo).access()
        
        reduced_disc_insitu_particles = set(insitu["ParticleID"]).intersection(set(disc_final['ParticleID']))

        insitu_redshift = []
        insitu_mass = []

        dwarf_galaxy_redshift = -1
        larger_than_dwarf_galaxy_redshift = -1

        reached_dwarf_galaxy_redshift = False
        exceeded_dwarf_galaxy_redshift = False
        
        for snapshot_number in range(5, 251):
            disc = data_access.snapshot_raw_as_dataframe.data(self.__output_file_path, snapshot_number, self.__part_type).access()
            reduced_disc_insitu = disc[disc['ParticleID'].isin(reduced_disc_insitu_particles)]

            mass = (10**10) * sum(reduced_disc_insitu['Mass']) / h

            breakpoint()
            
            redshift = redshift_for_snapshot_unique[snapshot_number]

            insitu_redshift.append(redshift)
            insitu_mass.append(mass)

            if not reached_dwarf_galaxy_redshift:
                if mass > 10**7 and mass < 10**9:
                    dwarf_galaxy_redshift = redshift
                    reached_dwarf_galaxy_redshift = True

            if reached_dwarf_galaxy_redshift and not exceeded_dwarf_galaxy_redshift:
                if mass > 10**9:
                    larger_than_dwarf_galaxy_redshift = redshift
                    exceeded_dwarf_galaxy_redshift = True        

        plt.plot(insitu_redshift, insitu_mass)
        plt.axvline(dwarf_galaxy_redshift, 0, 1, linestyle='--', color='g', alpha=0.4, label='Reached $10^7_{\odot}$')        

        if larger_than_dwarf_galaxy_redshift > 0:
            plt.axvline(larger_than_dwarf_galaxy_redshift, 0, 1, linestyle='--', color='r', alpha=0.4, label='Exceeded $10^9_{\odot}$')

        plt.gca().invert_xaxis()
        plt.xlabel('Redshift')
        plt.ylabel('Stellar mass (in solar masses)')
        plt.legend()
        plt.title(f'Stellar mass against redshift for in-situ particles')
        plt.savefig(f'./output/halo_6/stellar_mass_histories/InsituMassRedshift.png')


 
        