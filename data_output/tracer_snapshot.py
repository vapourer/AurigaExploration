import pandas as pd
import data_access
from data_access import *

class data:
    def __init__(self, file_path: str, snap_num: int) -> None:
        print('New tracer_snapshot output')
        self.__file_path = file_path
        self.__snap_num = snap_num

    def output(self) -> pd.DataFrame:
        disc = data_access.tracer_snapshot_dataframe.data(self.__file_path, self.__snap_num).access()

        disc.to_csv(f'./output/halo_6/gas/Disc_Tracer_{self.__snap_num}.csv')