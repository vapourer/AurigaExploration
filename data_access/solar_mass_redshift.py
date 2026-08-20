import auriga_public.auriga_public as ap

class data:
    def __init__(self, tree_file_path: str, snap_num: int) -> None:
        print('Access solar_mass_redshift data')
        self.__tree_directory = tree_file_path
        self.__snap_num = snap_num

    def access(self):
        treeobj = ap.mergertree.load_mergertree(0, 0, self.__snap_num,
                                                directory=self.__tree_directory, base='trees_sf1_')
        
        return treeobj.GetObjectHistoryFromSubhaloID(0, self.__snap_num, 0,
                                                     ['SubhaloMassType', 'Redshift', 'SubhaloPos'])