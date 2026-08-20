import pandas as pd
from .tracer_snapshot import data as raw_snapshot_data

class data:
    def __init__(self, file_path: str, snap_num: int) -> None:
        print('Access tracer_snapshot_dataframe data')
        self.__file_path = file_path
        self.__snap_num = snap_num

    def access(self) -> pd.DataFrame:

        raw_snapshot = raw_snapshot_data(self.__file_path, self.__snap_num).access()
        
        data_structure = {'TracerParentID': raw_snapshot.data['ParentID'],
                          'TracerID': raw_snapshot.data['TracerID']}  
        
        return pd.DataFrame(data_structure)  