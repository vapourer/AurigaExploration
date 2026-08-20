import pandas as pd
import data_access
from data_access import *
from .gas_particle_by_subhalo import data as particles_by_subhalo_data

class data:
    def __init__(self, file_path: str) -> None:
        print('Generate gas_particle_by_subhalo_all output')
        self.__file_path = file_path

    def output(self) -> None:
        snap_num = 251

        particles_by_subhalo = particles_by_subhalo_data(self.__file_path, snap_num).output()

        particles_by_subhalo.to_csv(f'./output/halo_6/gas_particles_by_subhalo/GasParticlesBySubhalo_{snap_num}.csv')