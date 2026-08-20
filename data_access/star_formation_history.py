from .snapshot import data as snapshot_data
import auriga_public.auriga_public as ap

class data:
    def __init__(self, file_path: str, snap_num: int, part_type: int) -> None:
        print('Access star_formation_history data')
        self.__file_path = file_path
        self.__snap_num = snap_num
        self.__part_type = part_type

    def access(self):
        snapobj, _, _, _, _, _, _ = snapshot_data(self.__file_path, self.__snap_num, self.__part_type).access()
        ages = ap.util.GetLookbackTimeFromScaleFactor_Flat(snapobj.data['GFM_StellarFormationTime'],
                                                           snapobj.hubbleparam, snapobj.omega0, snapobj.omegalambda)
        
        return snapobj, ages