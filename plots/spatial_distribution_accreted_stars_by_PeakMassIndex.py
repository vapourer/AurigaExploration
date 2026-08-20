import numpy as np
import pandas as pd

class data:
    def __init__(self,
                 bounded_disc_exsitu: pd.DataFrame, peak_mass_index: int) -> None:

        print('New spatial_distribution_accreted_stars_by_PeakMassIndex plot helper class')
        self.__bounded_disc_exsitu = bounded_disc_exsitu
        self.__peak_mass_index = peak_mass_index

    def process(self) -> None:
        
        indexed_disc = self.__bounded_disc_exsitu[self.__bounded_disc_exsitu['PeakMassIndex'] == self.__peak_mass_index]
        
        prog_star_positions = np.array([indexed_disc['X'], indexed_disc['Y'], indexed_disc['Z']])
        snapfb_thisprog = indexed_disc['BoundFirstTime']

        return prog_star_positions, snapfb_thisprog
        
