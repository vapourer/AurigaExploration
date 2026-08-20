import pandas as pd
import data_access
from data_access import *
from .stellar_particle_by_subhalo import data as particles_by_subhalo_data

class data:
    def __init__(self, file_path: str) -> None:
        print('Generate stellar_particle_by_subhalo_all output')
        self.__file_path = file_path

    def output(self) -> None:
        snap_num = 25

        particles_by_subhalo = particles_by_subhalo_data(self.__file_path, snap_num).output()

        particles_by_subhalo.to_csv(f'./output/halo_6/stellar_particles_by_subhalo/StellarParticlesBySubhalo_{snap_num}.csv')