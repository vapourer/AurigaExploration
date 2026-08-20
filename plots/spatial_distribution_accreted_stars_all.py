import matplotlib.pyplot as plt
from .spatial_distribution_accreted_stars_by_PeakMassIndex import data as spatial_distribution_data
import data_access
from data_access import *

class plot:
    def __init__(self,
                 output_file_path: str,
                 list_file_path: str,
                 snap_num: int,
                 part_type: int,
                 halo: str,
                 radius: float) -> None:

        print('New spatial_distribution_accreted_stars_all plots')
        self.__output_file_path = output_file_path
        self.__list_file_path = list_file_path
        self.__snap_num = snap_num
        self.__part_type = part_type
        self.__halo = halo
        self.__radius = radius

    def create(self) -> None:
        
        bounded_disc_exsitu, peak_mass_indices = data_access.spatial_distribution_accreted_stars_by_PeakMassIndex.data(self.__output_file_path,
                                                                              self.__list_file_path,
                                                                              self.__snap_num,
                                                                              self.__part_type,
                                                                              self.__halo,
                                                                              self.__radius).access()
        
        for index in peak_mass_indices:
        
            prog_star_positions, snapfb_thisprog = spatial_distribution_data(bounded_disc_exsitu, index).process()

            if len(set(snapfb_thisprog)) > 1:
                pcolors = ( snapfb_thisprog - snapfb_thisprog.min() ) \
                    / ( snapfb_thisprog.max() - snapfb_thisprog.min() )
            else:
                pcolors = snapfb_thisprog

            _, ax = plt.subplots(1, 3, figsize=(9, 3))
            ax[0].scatter( prog_star_positions[1]*1e3, prog_star_positions[2]*1e3, c=pcolors, s=5., marker='.', linewidth=0, cmap=plt.get_cmap('viridis'), alpha=0.2 )
                
            ax[1].scatter( prog_star_positions[1]*1e3, prog_star_positions[0]*1e3, c=pcolors, s=5., marker='.', linewidth=0, cmap=plt.get_cmap('viridis'), alpha=0.2 )
                
            ax[2].scatter( prog_star_positions[2]*1e3, prog_star_positions[0]*1e3, c=pcolors, s=5., marker='.', linewidth=0, cmap=plt.get_cmap('viridis'), alpha=0.2 )

            plt.suptitle(f'Satellite with peak mass index {index} (scales in kpc)')
                
            plt.savefig(f'./output/{self.__halo}/spatial_distribution/SpatialDistributionAccretedStars_{self.__snap_num}_{index}.png')