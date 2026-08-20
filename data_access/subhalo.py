import auriga_public.auriga_public as ap

class data:
    def __init__(self, file_path: str, snap_num: int) -> None:
        print('Access subhalo data')
        self.__file_path = file_path
        self.__snap_num = snap_num

    def access(self):
        
        attrstoload = ['SubhaloMass', 'SubhaloPos', 'SubhaloVel', 'SubhaloMassType', 'Group_R_Crit200', 'SubhaloLen', 'SubhaloLenType']
        return ap.subhalos.subfind(self.__snap_num, directory=self.__file_path + '/', loadlist=attrstoload)
       