from .snapshot import data as snapshot_data
import auriga_public.auriga_public as ap

class data:
    def __init__(self, file_path: str, snap_num: int, part_type: int) -> None:
        print('Access disc data')
        self.__file_path = file_path
        self.__snap_num = snap_num
        self.__part_type = part_type

    def access(self):

        snapshot, subhalo, _, _, _, _, _ = snapshot_data(self.__file_path, self.__snap_num, self.__part_type).access()
        return snapshot, subhalo
