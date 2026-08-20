import numpy as np
from .disc import data as disc_data
import auriga_public.auriga_public as ap

class data:
    def __init__(self, output_file_path: str, list_file_path: str, snap_num: int, part_type: int, halo: str) -> None:
        print('Access spatial_distribution_accreted_stars data')
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
            nstars_in_subhalo[i] = np.sum( (mdata['Exsitu']['PeakMassIndex']==pid) \
                                          & (mdata['Exsitu']['AccretedFlag']==0))            

        nsort = np.argsort(nstars_in_subhalo)[::-1]
        nstars_in_subhalo = nstars_in_subhalo[nsort].astype('int')

        first_prog = first_prog[nsort]

        index = 2
        index_firstprog, = np.where( ( mdata['Exsitu']['PeakMassIndex'] == first_prog[index] ) \
                                    & (mdata['Exsitu']['AccretedFlag'] == 0) )
        
        id_index_prog, = np.where( np.in1d( snapobj.data['ParticleIDs'],
                                           mdata['Exsitu']['ParticleIDs'][index_firstprog] ) )
        
        prog_star_positions = snapobj.data['Coordinates'][id_index_prog]

        snapfb_thisprog = mdata['Exsitu']['BoundFirstTime'][index_firstprog]
        c_index, = np.where( np.in1d(mdata['Exsitu']['ParticleIDs'][index_firstprog], snapobj.data['ParticleIDs']) )

        isort2 = np.argsort(mdata['Exsitu']['ParticleIDs'][ index_firstprog ][c_index])

        return prog_star_positions, snapfb_thisprog, c_index, isort2