import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import data_access
from data_access import *

class plot:
    def __init__(self,
                 output_file_path: str, 
                 list_file_path: str,
                 snap_num: int,
                 part_type: int,
                 radius: float) -> None:
        
        print('New disc_show_exsitu_elements_specify_radius plots')
        self.__output_file_path = output_file_path
        self.__list_directory = list_file_path
        self.__snap_num = snap_num
        self.__part_type = part_type
        self.__halo = 'halo_6'
        self.__radius = radius

    def create(self) -> None:
        disc, _, _, _, _, _ = data_access.disc_specify_radius.data(self.__output_file_path,
                                                          self.__snap_num,
                                                          self.__part_type,
                                                          self.__radius).access()
        
        insitu, exsitu = data_access.starparticle_mergertree.data(self.__list_directory,
                                                                  self.__snap_num,
                                                                  self.__halo).access()

        reduced_disc_insitu_particles = set(insitu["ParticleID"]).intersection(set(disc['ParticleID']))
        reduced_disc_exsitu_particles = set(exsitu["ParticleID"]).intersection(set(disc['ParticleID']))

        reduced_disc_insitu = disc[disc['ParticleID'].isin(reduced_disc_insitu_particles)]
        reduced_disc_exsitu = disc[disc['ParticleID'].isin(reduced_disc_exsitu_particles)]

        reduced_exsitu = exsitu[exsitu['ParticleID'].isin(reduced_disc_exsitu_particles)]

        if self.__snap_num < 10:
            three_digit = '00' + str(self.__snap_num)
        elif self.__snap_num >= 10 and self.__snap_num < 100:
            three_digit = '0' + str(self.__snap_num)
        else:
            three_digit = str(self.__snap_num)

        face_file = f'./output/{self.__halo}/disc/DiscShowExsitu_{three_digit}_face.png'
        edge_file = f'./output/{self.__halo}/disc/DiscShowExsitu_{three_digit}_edge.png'

        self.__full_plot(reduced_disc_insitu, reduced_disc_exsitu, face_file, edge_file)

        face_file = f'./output/{self.__halo}/disc/ExsituOnly_{three_digit}_face.png'
        edge_file = f'./output/{self.__halo}/disc/ExsituOnly_{three_digit}_edge.png'

        self.__exsitu_plot(reduced_disc_exsitu, face_file, edge_file)

        reduced_disc_exsitu = pd.merge(reduced_disc_exsitu, reduced_exsitu, on='ParticleID', how='inner')
        peak_mass_indices = np.array([377, 918, 23050, 36275, 36900, 37138, 37333, 135236, 188717, 190063])

        exsitu_columns = reduced_disc_exsitu.columns
        exsitu_selected = [pd.DataFrame(columns=exsitu_columns)]

        for peak_mass_index in peak_mass_indices:
            current_disc = reduced_disc_exsitu[reduced_disc_exsitu["PeakMassIndex"] == peak_mass_index]

            face_file = f'./output/{self.__halo}/disc/DiscShowExsitu_{three_digit}_{peak_mass_index}_face.png'
            edge_file = f'./output/{self.__halo}/disc/DiscShowExsitu_{three_digit}_{peak_mass_index}_edge.png'
            self.__full_plot(reduced_disc_insitu, current_disc, face_file, edge_file, index=peak_mass_index)

            face_file = f'./output/{self.__halo}/disc/ExsituOnly_{three_digit}_{peak_mass_index}_face.png'
            edge_file = f'./output/{self.__halo}/disc/ExsituOnly_{three_digit}_{peak_mass_index}_edge.png'
            self.__exsitu_plot(current_disc, face_file, edge_file, index=peak_mass_index)

            exsitu_selected.append(current_disc)

        exsitu_selected = pd.concat(exsitu_selected)

        face_file = f'./output/{self.__halo}/disc/DiscShowExsituSelected_{three_digit}_face.png'
        edge_file = f'./output/{self.__halo}/disc/DiscShowExsituSelected_{three_digit}_edge.png'

        self.__full_plot(reduced_disc_insitu, exsitu_selected, face_file, edge_file, selected=True)

        face_file = f'./output/{self.__halo}/disc/ExsituSelectedOnly_{three_digit}_face.png'
        edge_file = f'./output/{self.__halo}/disc/ExsituSelectedOnly_{three_digit}_edge.png'

        self.__exsitu_plot(exsitu_selected, face_file, edge_file,  selected=True)

    def __full_plot(self, disc_insitu: pd.DataFrame, disc_exsitu: pd.DataFrame, face_file: str, edge_file: str, selected=False, index=None):

        gray_map = plt.cm.get_cmap('gray')
        gray_map_reversed = gray_map.reversed()

        n, xedges, yedges = np.histogram2d(disc_insitu['Z']*1e3, disc_insitu['Y']*1e3, bins=(500,500))

        xbin = 0.5 * (xedges[:-1] + xedges[1:])
        ybin = 0.5 * (yedges[:-1] + yedges[1:])
        xc, yc = np.meshgrid(xbin, ybin)

        _, ax = plt.subplots(figsize=(9, 9))

        plt.contourf( xc, yc, np.log10(n.T), cmap=gray_map_reversed)

        n, xedges, yedges = np.histogram2d(disc_exsitu['Z']*1e3, disc_exsitu['Y']*1e3, bins=(500,500))            
        plt.contourf( xc, yc, np.log10(n.T), cmap='hot')

        np.set_printoptions(threshold=1000)

        plot_title = 'Face on disc plot with insitu and exsitu particles separated'

        if index:
            plot_title += f' (PeakMassIndex = {index})'

        if selected:
            plot_title = 'Face on disc plot with insitu and selected exsitu particles separated'        

        plt.title(plot_title)

        ax.set_xlabel('kpc')
        ax.set_ylabel('kpc')

        plt.savefig(face_file)
        plt.close()

        _, ax = plt.subplots(figsize=(9, 9))
        
        n, xedges, yedges = np.histogram2d(disc_insitu['Z']*1e3, disc_insitu['X']*1e3, bins=(500,500))            
        plt.contourf( xc, yc, np.log10(n.T), cmap=gray_map_reversed)

        n, xedges, yedges = np.histogram2d(disc_exsitu['Z']*1e3, disc_exsitu['X']*1e3, bins=(500,500))            
        plt.contourf( xc, yc, np.log10(n.T), cmap='hot')

        plot_title = 'Edge on disc plot with insitu and exsitu particles separated'

        if index:
            plot_title += f' (PeakMassIndex = {index})'

        if selected:
            plot_title = 'Edge on disc plot with insitu and selected exsitu particles separated'        

        plt.title(plot_title)

        ax.set_xlabel('kpc')
        ax.set_ylabel('kpc')

        plt.savefig(edge_file)
        plt.close()

    def __exsitu_plot(self, disc_exsitu: pd.DataFrame, face_file: str, edge_file: str, selected=False, index=None):

        n, xedges, yedges = np.histogram2d(disc_exsitu['Z']*1e3, disc_exsitu['Y']*1e3, bins=(500,500))

        xbin = 0.5 * (xedges[:-1] + xedges[1:])
        ybin = 0.5 * (yedges[:-1] + yedges[1:])
        xc, yc = np.meshgrid(xbin, ybin)

        _, ax = plt.subplots(figsize=(9, 9))
                    
        plt.contourf( xc, yc, np.log10(n.T), cmap='hot')

        plot_title = 'Face on disc plot with exsitu particles only'

        if index:
            plot_title += f' (PeakMassIndex = {index})'

        if selected:
            plot_title = 'Face on disc plot with selected exsitu particles only'        

        plt.title(plot_title)

        ax.set_xlabel('kpc')
        ax.set_ylabel('kpc')

        plt.savefig(face_file)
        plt.close()

        _, ax = plt.subplots(figsize=(9, 9))

        n, xedges, yedges = np.histogram2d(disc_exsitu['Z']*1e3, disc_exsitu['X']*1e3, bins=(500,500))            
        plt.contourf( xc, yc, np.log10(n.T), cmap='hot')

        plot_title = 'Edge on disc plot with exsitu particles only'

        if index:
            plot_title += f' (PeakMassIndex = {index})'

        if selected:
            plot_title = 'Edge on disc plot with selected exsitu particles only'        

        plt.title(plot_title)

        ax.set_xlabel('kpc')
        ax.set_ylabel('kpc')     

        plt.savefig(edge_file)
        plt.close()
