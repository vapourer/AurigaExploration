import pandas as pd
from .merger_tree import data as merger_tree_data

class data:
    def __init__(self, tree_file_path: str, snap_num: int) -> None:
        print('Access merger_tree_as_dataframe data')
        self.__tree_directory = tree_file_path
        self.__snap_num = snap_num

    def access(self):
        tree = merger_tree_data(self.__tree_directory, self.__snap_num).access()

        stellar_mass = []
        gas_mass = []
        tracer_mass = []

        stellar_half_mass_radius = []
        gas_half_mass_radius = []
        tracer_half_mass_radius = []

        record_count = len(tree.data['SnapNum'])

        for i in range(record_count):
            stellar_mass.append(tree.data['SubhaloMassType'][i][4])
            gas_mass.append(tree.data['SubhaloMassType'][i][0])
            tracer_mass.append(tree.data['SubhaloMassType'][i][6])
            stellar_half_mass_radius.append(tree.data['SubhaloHalfmassRadType'][i][4])
            gas_half_mass_radius.append(tree.data['SubhaloHalfmassRadType'][i][0])
            tracer_half_mass_radius.append(tree.data['SubhaloHalfmassRadType'][i][6])
        
        data_structure = {'SnapshotNumber': tree.data["SnapNum"],
                          'FirstProgenitor': tree.data["FirstProgenitor"],
                          'NextProgenitor': tree.data["NextProgenitor"],
                          'Descendant': tree.data["Descendant"],
                          'Redshift': tree.data["Redshift"],
                          'Time': tree.data["Time"],
                          'SubhaloNumber': tree.data["SubhaloNumber"],
                          'StellarMass': stellar_mass,
                          'GasMass': gas_mass,
                          'TracerMass': tracer_mass,
                          'StellarHalfMassRadius': stellar_half_mass_radius,
                          'GasHalfMassRadius': gas_half_mass_radius,
                          'TracerHalfMassRadius': tracer_half_mass_radius}
        
        return pd.DataFrame(data_structure), tree