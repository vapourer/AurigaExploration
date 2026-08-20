import numpy as np
import auriga_public.auriga_public as ap

class data:
    def __init__(self, output_file_path: str, tree_file_path: str, snap_num: int) -> None:
        print('Access maximum_mass_dark_matter_lost data')
        self.__output_file_path = output_file_path
        self.__tree_directory = tree_file_path
        self.__snap_num = snap_num

    def access(self):
        subobj = ap.subhalos.subfind(self.__snap_num, directory=self.__output_file_path + '/',
                                     loadlist=['SubhaloPos', 'Group_R_Crit200'])
        
        r200 = subobj.data['Group_R_Crit200'][0]

        treeobj = ap.mergertree.load_mergertree(0, 0, self.__snap_num, directory=self.__tree_directory, base='trees_sf1_')
        
        result = treeobj.GetObjectHistoryFromSubhaloID(0, self.__snap_num, 0,
                                                       ['SubhaloMassType', 'Redshift', 'SubhaloPos'])

        main_pos = result['SubhaloPos']
        distance = np.sqrt( np.sum( (subobj.data['SubhaloPos']-main_pos[0,:])**2, axis=1) )
        ii, = np.where( (distance <= r200) & (distance > 0) )

        nsubhalos = len(ii)
        fraction_lost = np.zeros(nsubhalos)
        
        for i, isub in enumerate(range(nsubhalos)):
            result = treeobj.GetObjectHistoryFromSubhaloID(isub, self.__snap_num, 0,
                                                           ['SubhaloMassType', 'SubhaloPos', 'Redshift'],
                                                           mainprogonly=True)
            
            dmmass = result['SubhaloMassType'][:,:,1]
            maxdmmass = np.nanmax(dmmass)
            fraction_lost[i] = 1 - (dmmass[0] / maxdmmass)

        return distance[ii], fraction_lost