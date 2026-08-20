import numpy as np
import pandas as pd
import data_access
from data_access import *

class data:
    def __init__(self, file_path: str, snap_num: int) -> None:
        print('Generate subhalos_by_snapshot output')
        self.__file_path = file_path
        self.__snap_num = snap_num

    def output(self) -> None:

        sub_object = data_access.subhalo_as_dataframe.data(self.__file_path, self.__snap_num).access()

        gas_mass = sub_object["GasMass"]
        stellar_mass = sub_object["StellarMass"]   
        subhalo_number = np.arange(len(gas_mass))

        data_structure = {'subhalo_number': subhalo_number, 'gas_mass': gas_mass, 'stellar_mass': stellar_mass}
        gas_mass_indexed = pd.DataFrame(data_structure)

        gas_mass_reduced = gas_mass_indexed[gas_mass_indexed["gas_mass"] > 0]
        gas_mass_ordered = gas_mass_reduced.sort_values(by=['gas_mass'], ascending=False)
        gas_mass_ordered_zero_stellar_mass = gas_mass_ordered[gas_mass_ordered['stellar_mass'] == 0.0]

        print()
        print('gas_mass')
        print(gas_mass)
        print()

        print()
        print('gas_mass_indexed')
        print(gas_mass_indexed)
        print()

        print()
        print('gas_mass_reduced')
        print(gas_mass_reduced)
        print()

        print()
        print('gas_mass_ordered')
        print(gas_mass_ordered)
        print()

        print()
        print('gas_mass_ordered_zero_stellar_mass')
        print(gas_mass_ordered_zero_stellar_mass)
        print()
