from .subhalo import data as subhalo_data
import pandas as pd

class data:
    def __init__(self, file_path: str, snap_num: int) -> None:
        print('Access subhalo_as_dataframe data')
        self.__file_path = file_path
        self.__snap_num = snap_num

    def access(self):
        subhalo = subhalo_data(self.__file_path, self.__snap_num).access()

        x = []
        y = []
        z = []

        x_velocity = []
        y_velocity = []
        z_velocity = []

        stellar_mass = []
        gas_mass = []
        tracer_mass = []

        subhalo_stellar_length = []
        subhalo_gas_length = []
        subhalo_tracer_length = []


        record_count = len(subhalo.data['SubhaloMass'])

        for i in range(record_count):
            x.append(subhalo.data['SubhaloPos'][i][0])
            y.append(subhalo.data['SubhaloPos'][i][1])
            z.append(subhalo.data['SubhaloPos'][i][2])
            x_velocity.append(subhalo.data['SubhaloVel'][i][0])
            y_velocity.append(subhalo.data['SubhaloVel'][i][1])
            z_velocity.append(subhalo.data['SubhaloVel'][i][2])
            stellar_mass.append(subhalo.data['SubhaloMassType'][i][4])
            gas_mass.append(subhalo.data['SubhaloMassType'][i][0])
            tracer_mass.append(subhalo.data['SubhaloMassType'][i][6])
            subhalo_stellar_length.append(subhalo.data['SubhaloLenType'][i][4])
            subhalo_gas_length.append(subhalo.data['SubhaloLenType'][i][0])
            subhalo_tracer_length.append(subhalo.data['SubhaloLenType'][i][6])
        
        data_structure = {'X': x,
                          'Y': y,
                          'Z': z,
                          'X_velocity': x_velocity,
                          'Y_velocity': y_velocity,
                          'Z_velocity': z_velocity,
                          'Mass': subhalo.data['SubhaloMass'],
                          'StellarMass': stellar_mass,
                          'GasMass': gas_mass,
                          'TracerMass': tracer_mass,
                          'SubhaloLength': subhalo.data['SubhaloLen'],
                          'SubhaloStellarLength': subhalo_stellar_length,
                          'SubhaloGasLength': subhalo_gas_length,
                          'SubhaloTracerLength': subhalo_tracer_length}
        
        return pd.DataFrame(data_structure)