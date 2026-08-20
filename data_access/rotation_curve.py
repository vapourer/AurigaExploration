import numpy as np
from scipy import stats
from .disc import data as rotated_snapshot_data
import auriga_public.auriga_public as ap

class data:
    def __init__(self, file_path: str, snap_num: int, part_type: int) -> None:
        print('Access rotation_curve data')
        self.__file_path = file_path
        self.__snap_num = snap_num
        self.__part_type = part_type

    def access(self):
        snapobj, subobj = rotated_snapshot_data(self.__file_path, self.__snap_num, self.__part_type).access()

        star_radius = ap.util.r(snapobj)
        Gcosmo = 43.

        isort_stars = np.argsort(star_radius)
        cummass = np.cumsum(snapobj.data['Masses'][isort_stars])
        Vc_stars = np.sqrt( Gcosmo*cummass/star_radius[isort_stars] )
        vbinstars, edges, _ = stats.binned_statistic(star_radius[isort_stars], Vc_stars, statistic='mean', bins=100,
                                                     range=[0., 0.1*subobj.data['Group_R_Crit200'][0]])

        return vbinstars, edges, Gcosmo, subobj, star_radius