import numpy as np
from scipy import stats
from .rotation_curve import data as rotation_curve_data
import auriga_public.auriga_public as ap

class data:
    def __init__(self, file_path: str, snap_num: int, part_type: int) -> None:
        print('Access rotation_curves_with_dark_matter data')
        self.__file_path = file_path
        self.__snap_num = snap_num
        self.__part_type = part_type

    def access(self):
        vbinstars, edges, Gcosmo, subobj, _ = rotation_curve_data(self.__file_path,
                                                               self.__snap_num,
                                                               self.__part_type).access()

        snapobj_dm = ap.snapshot.load_snapshot(self.__snap_num, 1, loadlist=['Coordinates', 'Masses'],
                                               snappath=self.__file_path, verbose=False)
        
        snapobj_dm = ap.util.CentreOnHalo(snapobj_dm, subobj.data['SubhaloPos'][0])
        snapobj_dm = ap.util.apply_mask(snapobj_dm, stars=False, radialcut=0.1*subobj.data['Group_R_Crit200'][0])

        dm_radius = ap.util.r(snapobj_dm)
        isort_dm = np.argsort(dm_radius)
        cummass = np.cumsum(snapobj_dm.data['Masses'][isort_dm])
        Vc_dm = np.sqrt( Gcosmo*cummass/dm_radius[isort_dm] )

        vbindm, edges, _ = stats.binned_statistic(dm_radius[isort_dm], Vc_dm, statistic='mean', bins=100,
                                                     range=[0., 0.1*subobj.data['Group_R_Crit200'][0]])
        
        Rbin = 0.5 * (edges[:-1] + edges[1:])
        Vcirc = np.sqrt(vbinstars**2 + vbindm**2)

        return Rbin, vbinstars, vbindm, Vcirc