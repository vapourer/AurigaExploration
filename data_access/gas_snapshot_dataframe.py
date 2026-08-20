import pandas as pd
from .gas_snapshot import data as raw_snapshot_data

class data:
    def __init__(self, file_path: str, snap_num: int) -> None:
        print('Access gas_snapshot_dataframe data')
        self.__file_path = file_path
        self.__snap_num = snap_num

    def access(self) -> pd.DataFrame:

        raw_snapshot = raw_snapshot_data(self.__file_path, self.__snap_num).access()

        x = []
        y = []
        z = []

        x_velocity = []
        y_velocity = []
        z_velocity = []

        for i in range(len(raw_snapshot.data['Coordinates'])):
            x.append(raw_snapshot.data['Coordinates'][i][0])
            y.append(raw_snapshot.data['Coordinates'][i][1])
            z.append(raw_snapshot.data['Coordinates'][i][2])
            x_velocity.append(raw_snapshot.data['Velocities'][i][0])
            y_velocity.append(raw_snapshot.data['Velocities'][i][1])
            z_velocity.append(raw_snapshot.data['Velocities'][i][2])
        
        data_structure = {'ParticleID': raw_snapshot.data['ParticleIDs'],
                          'Mass': raw_snapshot.data['Masses'],
                          'Density': raw_snapshot.data['Density'],
                          'Volume': raw_snapshot.data['Volume'],
                          'X': x,
                          'Y': y,
                          'Z': z,
                          'X_velocity': x_velocity,
                          'Y_velocity': y_velocity,
                          'Z_velocity': z_velocity,                          
                          'StarFormationRate': raw_snapshot.data['StarFormationRate'],
                          'TracerCount': raw_snapshot.data['NumTracers'],
                          'CoolingRate': raw_snapshot.data['GFM_CoolingRate'],
                          'Potential': raw_snapshot.data['Potential'],
                          'HighResGasMass': raw_snapshot.data['HighResGasMass']}
        
        return pd.DataFrame(data_structure)  