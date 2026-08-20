import pandas as pd
import uuid
import data_access
from data_access import *

class data:
    def __init__(self, file_path: str, snap_num: int) -> None:
        print('Generate stellar_particle_by_subhalo output')
        self.__file_path = file_path
        self.__snap_num = snap_num
        self.__part_type = 4

    def output(self) -> None:
        sub_object = data_access.subhalo_as_dataframe.data(self.__file_path, self.__snap_num).access()
        stellar_snapshot = data_access.snapshot_raw_as_dataframe.data(self.__file_path, self.__snap_num, self.__part_type).access()

        non_fuzz = sub_object["SubhaloStellarLength"].sum()
        particles = stellar_snapshot["ParticleID"][0:non_fuzz]
        x_positions = stellar_snapshot["X"][0:non_fuzz]
        y_positions = stellar_snapshot["Y"][0:non_fuzz]
        z_positions = stellar_snapshot["Z"][0:non_fuzz]
        x_velocities = stellar_snapshot["X_velocity"][0:non_fuzz]
        y_velocities = stellar_snapshot["Y_velocity"][0:non_fuzz]
        z_velocities = stellar_snapshot["Z_velocity"][0:non_fuzz]
        stellar_formation_times = stellar_snapshot["StellarFormationTime"][0:non_fuzz]
        masses = stellar_snapshot["Mass"][0:non_fuzz]
        potentials = stellar_snapshot["Potential"][0:non_fuzz]
        initial_masses = stellar_snapshot["InitialMass"][0:non_fuzz]
        
        index = []
        subhalo_id = []
        subhalo_number = []
        particle = []
        mass = []
        x = []
        y = []
        z = []
        x_velocity = []
        y_velocity = []
        z_velocity = []
        stellar_formation_time = []
        initial_mass = []
        potential = []

        counter = 0
        subhalo = 0
        subhalo_start = 0
        # subhalo_end = sub_object["SubhaloStellarLength"].iloc[0]

        for length in sub_object["SubhaloStellarLength"]:

            subhalo_end = subhalo_start + length

            subhalo_particles = particles[subhalo_start:subhalo_end]
            subhalo_x_positions = x_positions[subhalo_start:subhalo_end]
            subhalo_y_positions = y_positions[subhalo_start:subhalo_end]
            subhalo_z_positions = z_positions[subhalo_start:subhalo_end]
            subhalo_x_velocities = x_velocities[subhalo_start:subhalo_end]
            subhalo_y_velocities = y_velocities[subhalo_start:subhalo_end]
            subhalo_z_velocities = z_velocities[subhalo_start:subhalo_end]
            subhalo_stellar_formation_times = stellar_formation_times[subhalo_start:subhalo_end]
            subhalo_masses = masses[subhalo_start:subhalo_end]
            subhalo_potentials = potentials[subhalo_start:subhalo_end]
            subhalo_initial_masses = initial_masses[subhalo_start:subhalo_end]
            particle_count = len(subhalo_particles)

            id = str(uuid.uuid4())

            for i in range(particle_count):

                index.append(counter)
                subhalo_number.append(subhalo)
                subhalo_id.append(id)
                particle.append(subhalo_particles.iloc[i])
                x.append(subhalo_x_positions.iloc[i])
                y.append(subhalo_y_positions.iloc[i])
                z.append(subhalo_z_positions.iloc[i])
                x_velocity.append(subhalo_x_velocities.iloc[i])
                y_velocity.append(subhalo_y_velocities.iloc[i])
                z_velocity.append(subhalo_z_velocities.iloc[i])
                mass.append(subhalo_masses.iloc[i])
                stellar_formation_time.append(subhalo_stellar_formation_times.iloc[i])
                initial_mass.append(subhalo_initial_masses.iloc[i])
                potential.append(subhalo_potentials.iloc[i])

                counter += 1

            subhalo_start = subhalo_end
            # subhalo_end = subhalo_start + length
            subhalo += 1

        data_structure = {'Index': index,
                          'ParticleID': particle,
                          'X': x,
                          'Y': y,
                          'Z': z,
                          'X_velocity': x_velocity,
                          'Y_velocity': y_velocity,
                          'Z_velocity': z_velocity,
                          'StellarFormationTime': stellar_formation_time,
                          'Mass': mass,
                          'Potential': potential,
                          'InitialMass': initial_mass,
                          'SubhaloNumber': subhalo_number,
                          'SubhaloID': subhalo_id}
        
        return pd.DataFrame(data_structure) 

        # header = 'Index,'
        # header += 'ParticleID,'
        # header += 'X,'
        # header += 'Y,'
        # header += 'Z,'
        # header += 'X_velocity,'
        # header += 'Y_velocity,'
        # header += 'Z_velocity,'
        # header += 'StellarFormationTime,'
        # header += 'Mass,'
        # header += 'Potential,'
        # header += 'InitialMass,'
        # header += 'SubhaloNumber,'
        # header += 'SubhaloID\n'
        
        # records = [header]

        # for i in index:
        #     record = f'{i},'
        #     record += f'{particle[i]},'
        #     record += f'{x[i]},'
        #     record += f'{y[i]},'
        #     record += f'{z[i]},'
        #     record += f'{x_velocity[i]},'
        #     record += f'{y_velocity[i]},'
        #     record += f'{z_velocity[i]},'
        #     record += f'{stellar_formation_time[i]},'
        #     record += f'{mass[i]},'            
        #     record += f'{potential[i]},'
        #     record += f'{initial_mass[i]},'
        #     record += f'{subhalo_number[i]},'
        #     record += f'{subhalo_id[i]}\n'
        #     records.append(record)                

        # with open(f'./output/halo_6/stellar_particles_by_subhalo/StellarParticlesBySubhalo_{self.__snap_num}.csv', 'w') as file:
        #     file.writelines(records)            
        