import auriga_public.auriga_public as ap

class data:
    def __init__(self, file_path: str, snap_num: int) -> None:
        print('Access gas_snapshot data')
        self.__file_path = file_path
        self.__snap_num = snap_num
        self.__part_type = 0
        self.__attrstoload = ['Coordinates', 'Velocities', 'Density', 'Volume', 'StarFormationRate', 'NumTracers',
                              'GFM_CoolingRate', 'HighResGasMass', 'Masses', 'ParticleIDs', 'Potential']

    def access(self):        
        
        return ap.snapshot.load_snapshot(self.__snap_num, self.__part_type, loadlist=self.__attrstoload,
                                            snappath=self.__file_path, verbose=False)
        