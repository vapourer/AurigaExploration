import numpy as np
import pandas as pd
from .snapshot_raw import data as raw_data
import auriga_public.auriga_public as ap

class data:
    def __init__(self, snapshot: raw_data, halo_centre: np.ndarray, bulk_velocity: np.ndarray,
                 xdir: np.ndarray, ydir: np.ndarray, zdir: np.ndarray) -> None:
        
        print('Access snapshot_centred_to_latest data')
        self.__snapshot = snapshot
        self.__halo_centre = halo_centre
        self.__bulk_velocity = bulk_velocity
        self.__xdir = xdir
        self.__ydir = ydir
        self.__zdir = zdir

    def access(self):
        
        centred_halo = ap.util.CentreOnHalo(self.__snapshot, self.__halo_centre)
        ap.util.remove_bulk_velocity(centred_halo, self.__bulk_velocity)
        ap.util.rotateto(centred_halo, self.__xdir, dir2=self.__ydir, dir3=self.__zdir)

        x = []
        y = []
        z = []

        x_velocity = []
        y_velocity = []
        z_velocity = []

        for i in range(len(centred_halo.data['Coordinates'])):
            x.append(centred_halo.data['Coordinates'][i][0])
            y.append(centred_halo.data['Coordinates'][i][1])
            z.append(centred_halo.data['Coordinates'][i][2])
            x_velocity.append(centred_halo.data['Velocities'][i][0])
            y_velocity.append(centred_halo.data['Velocities'][i][1])
            z_velocity.append(centred_halo.data['Velocities'][i][2])
        
        data_structure = {'X': x,
                          'Y': y,
                          'Z': z,
                          'X_velocity': x_velocity,
                          'Y_velocity': y_velocity,
                          'Z_velocity': z_velocity,
                          'GFM_StellarFormationTime': centred_halo.data['GFM_StellarFormationTime'],
                          'GFM_InitialMass': centred_halo.data['GFM_InitialMass'],
                          'Mass': centred_halo.data['Masses'],
                          'ParticleID': centred_halo.data['ParticleIDs'],
                          'Potential': centred_halo.data['Potential']}
        
        return pd.DataFrame(data_structure)