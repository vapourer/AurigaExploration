import numpy as np
import pandas as pd
import uuid
import data_access
from data_access import *

class data:
    def __init__(self, file_path: str, snap_num: int) -> None:
        print('Generate tracer_particle_by_subhalo output')
        self.__file_path = file_path
        self.__snap_num = snap_num

    def output(self) -> None:
        sub_object = data_access.subhalo_as_dataframe.data(self.__file_path, self.__snap_num).access()
        tracer_snapshot = data_access.tracer_snapshot_dataframe.data(self.__file_path, self.__snap_num).access()

        non_fuzz = sub_object["SubhaloTracerLength"].sum()
        particles = tracer_snapshot["TracerID"][0:non_fuzz]
        parents = tracer_snapshot["TracerParentID"][0:non_fuzz]
        
        index = []
        subhalo_id = []
        subhalo_number = []
        particle = []
        parent = []

        counter = 0
        subhalo = 0
        subhalo_start = 0
        # subhalo_end = sub_object["SubhaloTracerLength"].iloc[0]

        for length in sub_object["SubhaloTracerLength"]:

            subhalo_end = subhalo_start + length      

            subhalo_particles = particles[subhalo_start:subhalo_end]
            subhalo_parents = parents[subhalo_start:subhalo_end]
            particle_count = len(subhalo_particles)

            id = str(uuid.uuid4())

            for i in range(particle_count):

                index.append(counter)
                subhalo_number.append(subhalo)
                subhalo_id.append(id)
                particle.append(subhalo_particles.iloc[i])
                parent.append(subhalo_parents.iloc[i])

                counter += 1

            subhalo_start = subhalo_end
            subhalo += 1
            # subhalo_end = subhalo_start + length

        data_structure = {'TracerID': particle,
                          'TracerParentID': parent,
                          'SubhaloNumber': subhalo_number,
                          'SubhaloID': subhalo_id}
        
        return pd.DataFrame(data_structure) 

        header = 'Index,'
        header += 'TracerID,'
        header += 'TracerParentID,'
        header += 'SubhaloID\n'
        records = [header]

        for i in index:
            record = f'{i},'
            record += f'{particle[i]},'
            record += f'{parent[i]},'
            record += f'{subhalo_id[i]}\n'
            records.append(record)                

        with open(f'./output/halo_6/tracer_particles_by_subhalo/TracerParticlesBySubhalo_{self.__snap_num}.csv', 'w') as file:
            file.writelines(records)            
        