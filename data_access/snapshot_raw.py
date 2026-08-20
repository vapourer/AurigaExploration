import auriga_public.auriga_public as ap

class data:
    def __init__(self, file_path: str, snap_num: int, part_type: int) -> None:
        print('Access snapshot_raw data')
        self.__file_path = file_path
        self.__snap_num = snap_num
        self.__part_type = part_type

    def access(self):
        attrstoload = ['Coordinates', 'Velocities', 'GFM_StellarFormationTime', 'GFM_InitialMass',
                       'Masses', 'ParticleIDs', 'Potential']
        
        return ap.snapshot.load_snapshot(self.__snap_num, self.__part_type, loadlist=attrstoload,
                                            snappath=self.__file_path, verbose=False)
        