import numpy as np
import auriga_public.auriga_public as ap

class data:
    def __init__(self, file_path: str, snap_num: int) -> None:
        print('Access satellites data')
        self.__file_path = file_path
        self.__snap_num = snap_num

    def access(self):
        attrstoload = ['SubhaloMass', 'SubhaloPos', 'SubhaloVel', 'SubhaloMassType', 'Group_R_Crit200']

        subobj = ap.subhalos.subfind(self.__snap_num, directory=self.__file_path + '/', loadlist=attrstoload)

        main_pos = subobj.data['SubhaloPos'][0]
        print()
        print(f'main_pos = {main_pos}')
        print()
        distance = np.sqrt( np.sum( (subobj.data['SubhaloPos']-main_pos)**2, axis=1) )

        mass = subobj.data['SubhaloMassType'][:,1]
        r200 = subobj.data['Group_R_Crit200'][0]

        return distance, r200, mass, subobj