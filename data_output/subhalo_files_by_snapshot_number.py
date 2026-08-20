from .subhalo_to_csv import data as subhalo_data

class data:

    def __init__(self, file_path: str, snap_num: int) -> None:
        print('Generate subhalo_files_by_snapshot_number output')
        self.__file_path = file_path
        self.__snap_num = snap_num
        self.__max_snap_num = 251

    def output(self) -> None:

        for snapshot in range(self.__snap_num, self.__max_snap_num + 1):
                subhalo_data(self.__file_path, snapshot).output()
