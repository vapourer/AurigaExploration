import matplotlib.pyplot as plt
import data_access
from data_access import *

class plot:
    def __init__(self, output_file_path: str, list_file_path: str, snap_num: int, part_type: int, halo: str) -> None:
        print('New spatial_distribution_accreted_stars plot')
        self.__output_file_path = output_file_path
        self.__list_file_path = list_file_path
        self.__snap_num = snap_num
        self.__part_type = part_type
        self.__halo = halo

    def create(self) -> None:        
        prog_star_positions, snapfb_thisprog, c_index, isort2 \
            = data_access.spatial_distribution_accreted_stars.data(self.__output_file_path,
                                                                   self.__list_file_path,
                                                                   self.__snap_num,
                                                                   self.__part_type,
                                                                   self.__halo).access()

        pcolors = ( snapfb_thisprog[c_index[isort2]] - snapfb_thisprog.min() ) \
            / ( snapfb_thisprog.max() - snapfb_thisprog.min() )

        _, ax = plt.subplots(1, 3, figsize=(9, 3))
        ax[0].scatter( prog_star_positions[:,1]*1e3, prog_star_positions[:,2]*1e3, c=pcolors, s=5., marker='.',
                      linewidth=0, cmap=plt.get_cmap('viridis'), alpha=0.2 )
        
        ax[1].scatter( prog_star_positions[:,1]*1e3, prog_star_positions[:,0]*1e3, c=pcolors, s=5., marker='.',
                      linewidth=0, cmap=plt.get_cmap('viridis'), alpha=0.2 )
        
        ax[2].scatter( prog_star_positions[:,2]*1e3, prog_star_positions[:,0]*1e3, c=pcolors, s=5., marker='.',
                      linewidth=0, cmap=plt.get_cmap('viridis'), alpha=0.2 )
        
        plt.savefig(f'./output/{self.__halo}/original_plots/SpatialDistributionAccretedStars_{self.__snap_num}.png')