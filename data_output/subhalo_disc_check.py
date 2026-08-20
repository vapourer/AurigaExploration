import numpy as np
import data_access
from data_access import *

class data:
    def __init__(self, file_path: str, snap_num: int, part_type: int) -> None:
        print('Generate subhalo_disc_check output')
        self.__file_path = file_path
        self.__snap_num = snap_num
        self.__part_type = part_type

    def output(self) -> None:

        sub_object = data_access.subhalo_as_dataframe.data(self.__file_path, self.__snap_num).access()

        stellar_snapshot = data_access.snapshot_raw_as_dataframe.data(self.__file_path, self.__snap_num, self.__part_type).access()        
        gas_snapshot = data_access.gas_snapshot_dataframe.data(self.__file_path, self.__snap_num).access()
        tracer_snapshot = data_access.tracer_snapshot_dataframe.data(self.__file_path, self.__snap_num).access()
        
        subhalo_count = len(sub_object["Mass"])

        first_stellar_subhalo_length = sub_object["SubhaloStellarLength"].iloc[0]
        second_stellar_subhalo_length = sub_object["SubhaloStellarLength"].iloc[1]

        first_gas_subhalo_length = sub_object["SubhaloGasLength"].iloc[0]
        second_gas_subhalo_length = sub_object["SubhaloGasLength"].iloc[1]

        first_tracer_subhalo_length = sub_object["SubhaloTracerLength"].iloc[0]
        second_tracer_subhalo_length = sub_object["SubhaloTracerLength"].iloc[1]
        
        print()
        print(f'Subhalo length: {subhalo_count}')
        print(f'Stellar snapshot length: {len(stellar_snapshot["ParticleID"])} records')
        print(f'Gas snapshot length: {len(gas_snapshot["ParticleID"])} records')
        print(f'Tracer snapshot length: {len(tracer_snapshot["TracerID"])} records')
        print(f'First stellar subhalo length = {first_stellar_subhalo_length}')
        print(f'Second stellar subhalo length = {second_stellar_subhalo_length}')
        print(f'First gas subhalo length = {first_gas_subhalo_length}')
        print(f'Second gas subhalo length = {second_gas_subhalo_length}')
        print(f'First tracer subhalo length = {first_tracer_subhalo_length}')
        print(f'Second tracer subhalo length = {second_tracer_subhalo_length}')
        print(f'First overall subhalo length = {sub_object["SubhaloLength"].iloc[0]}')
        print(f'Second overall subhalo length = {sub_object["SubhaloLength"].iloc[1]}')
        print()



        first_subhalo_first_stellar_particle = stellar_snapshot['ParticleID'].iloc[0]
        first_subhalo_last_stellar_particle = stellar_snapshot['ParticleID'].iloc[first_stellar_subhalo_length - 1]
        second_subhalo_first_stellar_particle = stellar_snapshot['ParticleID'].iloc[first_stellar_subhalo_length]
        second_subhalo_last_stellar_particle = stellar_snapshot['ParticleID'].iloc[first_stellar_subhalo_length + second_stellar_subhalo_length - 1]

        first_subhalo_first_gas_particle = stellar_snapshot['ParticleID'].iloc[0]
        first_subhalo_last_gas_particle = stellar_snapshot['ParticleID'].iloc[first_gas_subhalo_length - 1]
        second_subhalo_first_gas_particle = stellar_snapshot['ParticleID'].iloc[first_gas_subhalo_length]
        second_subhalo_last_gas_particle = stellar_snapshot['ParticleID'].iloc[first_gas_subhalo_length + second_gas_subhalo_length - 1]


        first_subhalo_first_tracer_particle = stellar_snapshot['ParticleID'].iloc[0]
        first_subhalo_last_tracer_particle = stellar_snapshot['ParticleID'].iloc[first_tracer_subhalo_length - 1]
        second_subhalo_first_tracer_particle = stellar_snapshot['ParticleID'].iloc[first_tracer_subhalo_length]
        second_subhalo_last_tracer_particle = stellar_snapshot['ParticleID'].iloc[first_tracer_subhalo_length + second_tracer_subhalo_length - 1]


        print(f'first_subhalo_first_stellar_particle = {first_subhalo_first_stellar_particle}')
        print(f'first_subhalo_last_stellar_particle = {first_subhalo_last_stellar_particle}')
        print(f'second_subhalo_first_stellar_particle = {second_subhalo_first_stellar_particle}')
        print(f'second_subhalo_last_stellar_particle = {second_subhalo_last_stellar_particle}')
        print()

        print(f'first_subhalo_first_gas_particle = {first_subhalo_first_gas_particle}')
        print(f'first_subhalo_last_gas_particle = {first_subhalo_last_gas_particle}')
        print(f'second_subhalo_first_gas_particle = {second_subhalo_first_gas_particle}')
        print(f'second_subhalo_last_gas_particle = {second_subhalo_last_gas_particle}')
        print()

        print(f'first_subhalo_first_tracer_particle = {first_subhalo_first_tracer_particle}')
        print(f'first_subhalo_last_tracer_particle = {first_subhalo_last_tracer_particle}')
        print(f'second_subhalo_first_tracer_particle = {second_subhalo_first_tracer_particle}')
        print(f'second_subhalo_last_tracer_particle = {second_subhalo_last_tracer_particle}')
        print()

        print(f'Sum of stellar subhalo lengths = {sub_object["SubhaloStellarLength"].sum()} ')
        print(f'Sum of gas subhalo lengths = {sub_object["SubhaloGasLength"].sum()} ')
        print(f'Sum of tracer subhalo lengths = {sub_object["SubhaloTracerLength"].sum()} ')
        print()




