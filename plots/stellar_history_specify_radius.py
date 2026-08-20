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
                 halo: str,
                 radius: float) -> None:
        
        print('New stellar_history_specify_radius plot')
        self.__output_file_path = output_file_path
        self.__list_directory = list_file_path
        self.__tree_directory = tree_file_path
        self.__snap_num = snap_num
        self.__part_type = part_type
        self.__halo = halo
        self.__radius = radius

    def create(self) -> None:
        disc_final, halo_centre, bulk_velocity, xdir, ydir, zdir = data_access.disc_specify_radius.data(self.__output_file_path,
                                                          self.__snap_num,
                                                          self.__part_type,
                                                          self.__radius).access()
        
        insitu, exsitu = data_access.starparticle_mergertree.data(self.__list_directory,
                                                                  self.__snap_num,
                                                                  self.__halo).access()

        reduced_disc_insitu_particles = set(insitu["ParticleID"]).intersection(set(disc_final['ParticleID']))
        reduced_disc_exsitu_particles = set(exsitu["ParticleID"]).intersection(set(disc_final['ParticleID']))

        tree = data_access.merger_tree.data(self.__tree_directory, self.__snap_num).access()

        snapshots = tree.data['SnapNum']
        snapshots = np.sort(np.fromiter(set(snapshots), np.int32))

        for snapshot_number in snapshots:
            snapshot = data_access.snapshot_raw.data(self.__output_file_path, snapshot_number, self.__part_type).access()        

            snapshot = data_access.snapshot_centred_to_latest.data(snapshot,
                                                                halo_centre,
                                                                bulk_velocity,
                                                                xdir,
                                                                ydir,
                                                                zdir).access()
            
            snapshot_insitu = snapshot[snapshot['ParticleID'].isin(reduced_disc_insitu_particles)]
            snapshot_exsitu = snapshot[snapshot['ParticleID'].isin(reduced_disc_exsitu_particles)]
        
            n, xedges, yedges = np.histogram2d(snapshot_insitu['Z'], snapshot_insitu['Y'],
                                            bins=(500,500))

            xbin = 0.5 * (xedges[:-1] + xedges[1:])
            ybin = 0.5 * (yedges[:-1] + yedges[1:])
            xc, yc = np.meshgrid(xbin, ybin)

            _, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 4.5), tight_layout=True)

            ax1.contourf( xc, yc, np.log10(n.T), cmap='gray')

            n, xedges, yedges = np.histogram2d(snapshot_exsitu['Z'], snapshot_exsitu['Y'],
                                            bins=(500,500))
            
            ax1.contourf( xc, yc, np.log10(n.T), cmap='hot')
        
            n, xedges, yedges = np.histogram2d(snapshot_insitu['Z'], snapshot_insitu['X'],
                                               bins=(500,500))
            
            ax2.contourf( xc, yc, np.log10(n.T), cmap='gray')

            n, xedges, yedges = np.histogram2d(snapshot_exsitu['Z'], snapshot_exsitu['X'],
                                               bins=(500,500))
            
            ax2.contourf( xc, yc, np.log10(n.T), cmap='hot')

            ax1.set_axis_off()
            ax2.set_axis_off()

            if snapshot_number < 10:
                three_digit = '00' + str(snapshot_number)
            elif snapshot_number >= 10 and snapshot_number < 100:
                three_digit = '0' + str(snapshot_number)
            else:
                three_digit = str(snapshot_number)

            plt.savefig(f'./output/plots/history/History_{three_digit}.png')        
        
