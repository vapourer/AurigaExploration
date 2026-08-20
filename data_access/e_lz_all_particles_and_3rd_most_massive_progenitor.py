import numpy as np
from .disc import data as disc_data
import auriga_public.auriga_public as ap

class data:
    def __init__(self, output_file_path: str, list_file_path: str, snap_num: int, part_type: int, halo: str) -> None:
        print('Access e_lz_all_particles_and_3rd_most_massive_progenitor data')
        self.__output_file_path = output_file_path
        self.__list_directory = list_file_path
        self.__snap_num = snap_num
        self.__part_type = part_type
        self.__halo = halo

    def access(self):
        snapobj, _ = disc_data(self.__output_file_path, self.__snap_num, self.__part_type).access()

        mdata = ap.util.read_starparticle_mergertree_data_hdf5(self.__snap_num, self.__list_directory, self.__halo)

        first_prog = np.array(sorted(set(list(mdata['Exsitu']['PeakMassIndex']))))

        nstars_in_subhalo = np.zeros(len(first_prog))
        for i, pid in enumerate(first_prog):
            nstars_in_subhalo[i] = np.sum( (mdata['Exsitu']['PeakMassIndex']==pid) & (mdata['Exsitu']['AccretedFlag']==0))

        nsort = np.argsort(nstars_in_subhalo)[::-1]
        nstars_in_subhalo = nstars_in_subhalo[nsort].astype('int')
        first_prog = first_prog[nsort]

        index = 2
        index_firstprog, = np.where( ( mdata['Exsitu']['PeakMassIndex'] == first_prog[index] ) \
                                    & (mdata['Exsitu']['AccretedFlag'] == 0) )
        
        id_index_prog, = np.where( np.in1d( snapobj.data['ParticleIDs'],
                                           mdata['Exsitu']['ParticleIDs'][index_firstprog] ) )
        
        potential = snapobj.data['Potential']
        kinetic_energy = np.sum(snapobj.data['Velocities']**2, axis=1)

        orbital_energy = potential + 0.5 * kinetic_energy
        orbital_energy /= 1e5
        orbital_energy -= orbital_energy.max()
        Lz = np.cross( snapobj.data['Coordinates'], (snapobj.data['Velocities'] ) )[:,0]
        Lz *= np.sign(np.nanmedian(Lz))

        index, = np.where((ap.util.r(snapobj) < 0.1) & (ap.util.r(snapobj) > 0.0))

        return Lz, index, orbital_energy, id_index_prog