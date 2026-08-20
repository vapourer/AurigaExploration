import data_access
from data_access import *

class data:
    def __init__(self, file_path: str, snap_num: int, part_type: int) -> None:
        print('Generate disc output')
        self.__file_path = file_path
        self.__snap_num = snap_num
        self.__part_type = part_type

    def output(self) -> None:
        snapobj, _ = data_access.disc.data(self.__file_path, self.__snap_num,
                                                                       self.__part_type).access()
        
        print()
        print('snapobj')
        print(f'Type: {type(snapobj)}')
        print(snapobj.data)
        print()
        print(f'Coordinates array length: {len(snapobj.data["Coordinates"])}')
        print(f'GFM_InitialMass array length: {len(snapobj.data["GFM_InitialMass"])}')
        print(f'GFM_StellarFormationTime array length: {len(snapobj.data["GFM_StellarFormationTime"])}')
        print(f'Masses array length: {len(snapobj.data["Masses"])}')
        print(f'ParticleIDs array length: {len(snapobj.data["ParticleIDs"])}')
        print(f'Potential array length: {len(snapobj.data["Potential"])}')
        print(f'Velocities array length: {len(snapobj.data["Velocities"])}')
        print(f'radius array length: {len(snapobj.data["radius"])}')
        print()

        field_names = ['X', 'Y', 'Z', 'X_Velocity', 'Y_Velocity', 'Z_Velocity', 'GFM_StellarFormationTime', 'GFM_InitialMass',
                       'Masses', 'ParticleIDs', 'Potential']
        
        field_names = ','.join(field_names)
        print(field_names)

        for i in range(10):
            print(f'{snapobj.data["Coordinates"][i][0]}, \
                    {snapobj.data["Coordinates"][i][1]}, \
                    {snapobj.data["Coordinates"][i][2]}, \
                    {snapobj.data["Velocities"][i][0]}, \
                    {snapobj.data["Velocities"][i][1]}, \
                    {snapobj.data["Velocities"][i][2]}, \
                    {snapobj.data["GFM_StellarFormationTime"][i]}, \
                    {snapobj.data["GFM_InitialMass"][i]}, \
                    {snapobj.data["Masses"][i]}, \
                    {snapobj.data["ParticleIDs"][i]}, \
                    {snapobj.data["Potential"][i]}')

        print()

