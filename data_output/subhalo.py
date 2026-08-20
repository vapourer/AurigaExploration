import data_access
from data_access import *

class data:
    def __init__(self, file_path: str, snap_num: int) -> None:
        print('Generate subhalo output')
        self.__file_path = file_path
        self.__snap_num = snap_num

    def output(self) -> None:

        sub_object = data_access.subhalo_as_dataframe.data(self.__file_path, self.__snap_num).access()

        print()
        print('sub_object')
        print(f'Type: {type(sub_object)}')
        # print(sub_object.data)
        print(sub_object)
        print()
        # print(f'Group_R_Crit200 array length: {len(sub_object.data["Group_R_Crit200"])}')
        print(f'X array length: {len(sub_object["X"])}')
        print(f'Y array length: {len(sub_object["Y"])}')
        print(f'Z array length: {len(sub_object["Z"])}')
        print(f'X_velocity array length: {len(sub_object["X_velocity"])}')
        print(f'Y_velocity array length: {len(sub_object["Y_velocity"])}')
        print(f'Z_velocity array length: {len(sub_object["Z_velocity"])}')
        print(f'SubhaloLength array length: {len(sub_object["SubhaloLength"])}')
        print(f'SubhaloStellarLength array length: {len(sub_object["SubhaloStellarLength"])}')
        print(f'SubhaloGasLength array length: {len(sub_object["SubhaloGasLength"])}')
        print(f'SubhaloTracerLength array length: {len(sub_object["SubhaloTracerLength"])}')
        print(f'Mass array length: {len(sub_object["Mass"])}')
        print(f'StellarMass array length: {len(sub_object["StellarMass"])}')
        print(f'GasMass array length: {len(sub_object["GasMass"])}')
        print(f'TracerMass array length: {len(sub_object["TracerMass"])}')
        print()

        sub_object.to_csv(f'./output/halo_6/subhalos/SubhalosWithLengths_{self.__snap_num}.csv')
