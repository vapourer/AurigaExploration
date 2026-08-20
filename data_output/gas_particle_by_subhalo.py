import numpy as np
import pandas as pd
import uuid
import data_access
from data_access import *

class data:
    def __init__(self, file_path: str, snap_num: int) -> None:
        print('Generate gas_particle_by_subhalo output')
        self.__file_path = file_path
        self.__snap_num = snap_num

    def output(self) -> None:
        sub_object = data_access.subhalo_as_dataframe.data(self.__file_path, self.__snap_num).access()
        gas_snapshot = data_access.gas_snapshot_dataframe.data(self.__file_path, self.__snap_num).access()

        non_fuzz = sub_object["SubhaloGasLength"].sum()
        particles = gas_snapshot["ParticleID"][0:non_fuzz]
        masses = gas_snapshot["Mass"][0:non_fuzz]
        densities = gas_snapshot["Density"][0:non_fuzz]
        volumes = gas_snapshot["Volume"][0:non_fuzz]
        x_positions = gas_snapshot["X"][0:non_fuzz]
        y_positions = gas_snapshot["Y"][0:non_fuzz]
        z_positions = gas_snapshot["Z"][0:non_fuzz]
        x_velocities = gas_snapshot["X_velocity"][0:non_fuzz]
        y_velocities = gas_snapshot["Y_velocity"][0:non_fuzz]
        z_velocities = gas_snapshot["Z_velocity"][0:non_fuzz]
        star_formation_rates = gas_snapshot["StarFormationRate"][0:non_fuzz]
        tracer_counts = gas_snapshot["TracerCount"][0:non_fuzz]
        cooling_rates = gas_snapshot["CoolingRate"][0:non_fuzz]
        potentials = gas_snapshot["Potential"][0:non_fuzz]
        high_res_gas_masses = gas_snapshot["HighResGasMass"][0:non_fuzz]
        
        index = []
        subhalo_id = []
        subhalo_number = []
        particle = []
        mass = []
        density = []
        volume = []
        x = []
        y = []
        z = []
        x_velocity = []
        y_velocity = []
        z_velocity = []
        star_formation_rate = []
        tracer_count = []
        cooling_rate = []
        potential = []
        high_res_gas_mass = []


        counter = 0
        subhalo = 0
        subhalo_start = 0
        # subhalo_end = sub_object["SubhaloGasLength"].iloc[0]

        for length in sub_object["SubhaloGasLength"]:

            subhalo_end = subhalo_start + length          

            subhalo_particles = particles[subhalo_start:subhalo_end]
            subhalo_masses = masses[subhalo_start:subhalo_end]
            subhalo_densities = densities[subhalo_start:subhalo_end]
            subhalo_volumes = volumes[subhalo_start:subhalo_end]
            subhalo_x_positions = x_positions[subhalo_start:subhalo_end]
            subhalo_y_positions = y_positions[subhalo_start:subhalo_end]
            subhalo_z_positions = z_positions[subhalo_start:subhalo_end]
            subhalo_x_velocities = x_velocities[subhalo_start:subhalo_end]
            subhalo_y_velocities = y_velocities[subhalo_start:subhalo_end]
            subhalo_z_velocities = z_velocities[subhalo_start:subhalo_end]
            subhalo_star_formation_rates = star_formation_rates[subhalo_start:subhalo_end]
            subhalo_tracer_counts = tracer_counts[subhalo_start:subhalo_end]
            subhalo_cooling_rates = cooling_rates[subhalo_start:subhalo_end]
            subhalo_potentials = potentials[subhalo_start:subhalo_end]
            subhalo_high_res_gas_masses = high_res_gas_masses[subhalo_start:subhalo_end]
            particle_count = len(subhalo_particles)

            id = str(uuid.uuid4())

            for i in range(particle_count):

                index.append(counter)
                subhalo_number.append(subhalo)
                subhalo_id.append(id)
                particle.append(subhalo_particles.iloc[i])
                mass.append(subhalo_masses.iloc[i])
                density.append(subhalo_densities.iloc[i])
                volume.append(subhalo_volumes.iloc[i])
                x.append(subhalo_x_positions.iloc[i])
                y.append(subhalo_y_positions.iloc[i])
                z.append(subhalo_z_positions.iloc[i])
                x_velocity.append(subhalo_x_velocities.iloc[i])
                y_velocity.append(subhalo_y_velocities.iloc[i])
                z_velocity.append(subhalo_z_velocities.iloc[i])
                star_formation_rate.append(subhalo_star_formation_rates.iloc[i])
                tracer_count.append(subhalo_tracer_counts.iloc[i])
                cooling_rate.append(subhalo_cooling_rates.iloc[i])
                potential.append(subhalo_potentials.iloc[i])
                high_res_gas_mass.append(subhalo_high_res_gas_masses.iloc[i])

                counter += 1

            subhalo_start = subhalo_end
            subhalo += 1
            # subhalo_end = subhalo_start + length

        data_structure = {'Index': index,
                          'ParticleID': particle,
                          'Mass': mass,
                          'Density': density,
                          'Volume': volume,
                          'X': x,
                          'Y': y,
                          'Z': z,
                          'X_velocity': x_velocity,
                          'Y_velocity': y_velocity,
                          'Z_velocity': z_velocity,
                          'StarFormationRate': star_formation_rate,
                          'TracerCount': tracer_count,
                          'CoolingRate': cooling_rate,
                          'Potential': potential,
                          'HighResGasMass': high_res_gas_mass,
                          'SubhaloNumber': subhalo_number,
                          'SubhaloID': subhalo_id}
        
        return pd.DataFrame(data_structure) 

        # header = 'Index,'
        # header += 'ParticleID,'
        # header += 'Mass,'
        # header += 'Density,'
        # header += 'Volume,'
        # header += 'X,'
        # header += 'Y,'
        # header += 'Z,'
        # header += 'X_velocity,'
        # header += 'Y_velocity,'
        # header += 'Z_velocity,'
        # header += 'StarFormationRate,'
        # header += 'TracerCount,'
        # header += 'CoolingRate,'
        # header += 'Potential,'
        # header += 'HighResGasMass,'
        # header += 'SubhaloID\n'
        
        # records = [header]

        # for i in index:
        #     record = f'{i},'
        #     record += f'{particle[i]},'
        #     record += f'{mass[i]},'
        #     record += f'{density[i]},'
        #     record += f'{volume[i]},'
        #     record += f'{x[i]},'
        #     record += f'{y[i]},'
        #     record += f'{z[i]},'
        #     record += f'{x_velocity[i]},'
        #     record += f'{y_velocity[i]},'
        #     record += f'{z_velocity[i]},'
        #     record += f'{star_formation_rate[i]},'
        #     record += f'{tracer_count[i]},'
        #     record += f'{cooling_rate[i]},'
        #     record += f'{potential[i]},'
        #     record += f'{high_res_gas_mass[i]},'
        #     record += f'{subhalo_id[i]}\n'
        #     records.append(record)                

        # with open(f'./output/halo_6/gas_particles_by_subhalo/GasParticlesBySubhalo_{self.__snap_num}.csv', 'w') as file:
        #     file.writelines(records)            
        