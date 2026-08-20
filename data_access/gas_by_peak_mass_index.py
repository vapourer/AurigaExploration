import pandas as pd
from .tracer_snapshot_dataframe import data as tracer_snapshot_data
from .exsitu_particles_by_peak_mass_index import data as exsitu_particles_data
from .navigate_merger_tree import data as navigate_merger_tree_data
from .snapshot_raw_as_dataframe import data as stellar_snapshot_data
from .gas_snapshot_dataframe import data as gas_snapshot_data

class data:
    def __init__(self,
                 output_file_path: str,
                 list_file_path: str,
                 tree_file_path: str,
                 snap_num: int,
                 part_type: int,
                 halo: int,
                 radius: float,                 
                 peak_mass_index: int) -> None:
        
        print('Access gas_by_peak_mass_index data')
        self.__output_file_path = output_file_path
        self.__list_directory = list_file_path
        self.__tree_directory = tree_file_path
        self.__snap_num = snap_num
        self.__part_type = part_type
        self.__halo = halo 
        self.__radius = radius
        self.__peak_mass_index = peak_mass_index
        self.__tracer_part_type = 6
        self.__gas_part_type = 0
        
            

    def access(self) -> None:
        exsitu_by_peak_mass_index = exsitu_particles_data(self.__output_file_path,
                                                          self.__list_directory,
                                                          self.__snap_num,
                                                          self.__part_type,
                                                          self.__halo,
                                                          self.__radius,
                                                          self.__peak_mass_index).access()
        
        tracer_snapshot = tracer_snapshot_data(self.__output_file_path, self.__snap_num).access()

        exsitu_tracers_by_peak_mass_index = pd.merge(exsitu_by_peak_mass_index, tracer_snapshot, left_on='ParticleID', right_on='TracerParentID', how='inner')

        snapshots_grouped, snapshot_numbers = navigate_merger_tree_data(self.__output_file_path,
                                                                                    self.__list_directory,
                                                                                    self.__tree_directory,
                                                                                    self.__snap_num,
                                                                                    self.__part_type,
                                                                                    self.__halo,
                                                                                    self.__radius,
                                                                                    self.__peak_mass_index).access()
        
        header = 'Index,'
        header += 'Snapshot,'
        header += 'GasParticleCount,'
        header += 'GasTotalMass,'
        header += 'StellarParticleCount,'
        header += 'StellarMassFromTracers\n'
        records = [header]

        index = 0
        
        for snapshot_number in snapshot_numbers:
            # tracer_snapshot = tracer_snapshot_data(self.__output_file_path, snapshot_number).access()
            gas_snapshot = gas_snapshot_data(self.__output_file_path, snapshot_number).access()
            stellar_snapshot = stellar_snapshot_data(self.__output_file_path, snapshot_number, self.__part_type).access()

            print(f'Snapshot {snapshot_number}')

            gas_snapshot = pd.merge(exsitu_tracers_by_peak_mass_index, gas_snapshot, left_on='TracerParentID', right_on='ParticleID', how='inner')
            gas_particle_count = len(gas_snapshot["TracerID"])
            gas_mass = sum(gas_snapshot["Mass"])

            print(f'{gas_particle_count} gas particles')

            stellar_snapshot = pd.merge(exsitu_tracers_by_peak_mass_index, stellar_snapshot, left_on='TracerParentID', right_on='ParticleID', how='inner')
            stellar_particle_count = len(stellar_snapshot["TracerID"])
            stellar_mass = sum(stellar_snapshot["Mass"])

            print(f'{stellar_particle_count} stellar particles')

            record = f'{index},'
            record += f'{snapshot_number},'
            record += f'{gas_particle_count},'
            record += f'{gas_mass},'
            record += f'{stellar_particle_count},'
            record += f'{stellar_mass}\n'
            records.append(record)

            index += 1
            
        with open(f'./output/halo_6/gas/ParticleTypesByTracer{self.__peak_mass_index}.csv', 'w') as file:
            file.writelines(records)



        
        return exsitu_tracers_by_peak_mass_index