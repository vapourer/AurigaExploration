import data_access
from data_access import *

class data:
    def __init__(self, file_path: str, snap_num: int) -> None:
        print('Generate subhalo_to_csv output')
        self.__file_path = file_path
        self.__snap_num = snap_num

    def output(self) -> None:
        sub_object = data_access.subhalo_as_dataframe.data(self.__file_path, self.__snap_num).access()

        # header = 'Index,'
        # header += 'X,'
        # header += 'Y,'
        # header += 'Z,'
        # header += 'Velocity_X,'
        # header += 'Velocity_Y,'
        # header += 'Velocity_Z,'
        # header += 'Mass,'
        # header += 'StellarMass,'
        # header += 'GasMass,'
        # header += 'TracerMass\n'
        
        # records = [header]
        # record_count = len(sub_object["Mass"])

        # for i in range(record_count):
        #     record = f'{str(i)},'
        #     record += f'{sub_object["X"][i]},'
        #     record += f'{sub_object["Y"][i]},'
        #     record += f'{sub_object["Z"][i]},'
        #     record += f'{sub_object["X_velocity"][i]},'
        #     record += f'{sub_object["Y_velocity"][i]},'
        #     record += f'{sub_object["Z_velocity"][i]},'
        #     record += f'{sub_object["Mass"][i]},'
        #     record += f'{sub_object["StellarMass"][i]},'
        #     record += f'{sub_object["GasMass"][i]},'
        #     record += f'{sub_object["TracerMass"][i]}\n'
        #     records.append(record)                

        # with open(f'./output/halo_6/subhalos/Subhalos_{self.__snap_num}.csv', 'w') as file:
        #     file.writelines(records)

        sub_object.to_csv(f'./output/halo_6/subhalos/Subhalos_{self.__snap_num}.csv')