import pandas as pd
from .snapshot import data as snapshot_data
import auriga_public.auriga_public as ap

class data:
    def __init__(self, file_path: str, snap_num: int, part_type: int, radius: float) -> None:
        print('Access disc_specify_radius data')
        self.__file_path = file_path
        self.__snap_num = snap_num
        self.__part_type = part_type
        self.__radius = radius

    def access(self):
        snapshot, _, halo_centre, bulk_velocity, xdir, ydir, zdir = snapshot_data(self.__file_path, self.__snap_num, self.__part_type).access()
        
        x = []
        y = []
        z = []

        x_velocity = []
        y_velocity = []
        z_velocity = []

        for i in range(len(snapshot.data['Coordinates'])):
            x.append(snapshot.data['Coordinates'][i][0])
            y.append(snapshot.data['Coordinates'][i][1])
            z.append(snapshot.data['Coordinates'][i][2])
            x_velocity.append(snapshot.data['Velocities'][i][0])
            y_velocity.append(snapshot.data['Velocities'][i][1])
            z_velocity.append(snapshot.data['Velocities'][i][2])
        
        data_structure = {'X': x,
                          'Y': y,
                          'Z': z,
                          'X_velocity': x_velocity,
                          'Y_velocity': y_velocity,
                          'Z_velocity': z_velocity,
                          'GFM_StellarFormationTime': snapshot.data['GFM_StellarFormationTime'],
                          'GFM_InitialMass': snapshot.data['GFM_InitialMass'],
                          'Mass': snapshot.data['Masses'],
                          'ParticleID': snapshot.data['ParticleIDs'],
                          'Potential': snapshot.data['Potential'],
                          'Radius': snapshot.data['radius'],
                          'InitialMass': snapshot.data['GFM_InitialMass']}
        
        data_frame = pd.DataFrame(data_structure)

        if not self.__radius < 0:
            data_frame = data_frame[data_frame['Radius'] <= self.__radius]

        return data_frame, halo_centre, bulk_velocity, xdir, ydir, zdir