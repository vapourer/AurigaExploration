import pandas as pd
from .snapshot_raw import data as raw_snapshot_data

class data:
    def __init__(self, file_path: str, snap_num: int, part_type: int) -> None:
        print('Access snapshot_raw_as_dataframe data')
        self.__file_path = file_path
        self.__snap_num = snap_num
        self.__part_type = part_type

    def access(self) -> pd.DataFrame:

        raw_snapshot = raw_snapshot_data(self.__file_path, self.__snap_num, self.__part_type).access()

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
        
        data_structure = {'X': x,
                          'Y': y,
                          'Z': z,
                          'X_velocity': x_velocity,
                          'Y_velocity': y_velocity,
                          'Z_velocity': z_velocity,
                          'StellarFormationTime': raw_snapshot.data['GFM_StellarFormationTime'],
                          'Mass': raw_snapshot.data['Masses'],
                          'ParticleID': raw_snapshot.data['ParticleIDs'],
                          'Potential': raw_snapshot.data['Potential'],
                          'InitialMass': raw_snapshot.data['GFM_InitialMass']} 
        
        return pd.DataFrame(data_structure)  