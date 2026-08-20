import auriga_public.auriga_public as ap

class data:
    def __init__(self, file_path: str, snap_num: int, part_type: int) -> None:
        print('Access snapshot data')
        self.__file_path = file_path
        self.__snap_num = snap_num
        self.__part_type = part_type

    def access(self):
        attrstoload = ['Coordinates', 'Velocities', 'GFM_StellarFormationTime', 'GFM_InitialMass',
                       'Masses', 'ParticleIDs', 'Potential']

        snapshot = ap.snapshot.load_snapshot(self.__snap_num, self.__part_type, loadlist=attrstoload,
                                            snappath=self.__file_path, verbose=False)
        
        subhalo = ap.subhalos.subfind(self.__snap_num, directory=self.__file_path + '/',
                                     loadlist=['SubhaloPos', 'Group_R_Crit200'])
        
        halo_centre = subhalo.data['SubhaloPos'][0]
        
        snapshot = ap.util.CentreOnHalo(snapshot, halo_centre)

        bulk_velocity = ap.util.calculate_bulk_velocity(snapshot, idx=None,
                                                        radialcut=0.1*subhalo.data['Group_R_Crit200'][0])
        
        ap.util.remove_bulk_velocity(snapshot, bulk_velocity)
        snapshot = ap.util.apply_mask(snapshot, stars=True, radialcut=subhalo.data['Group_R_Crit200'][0])

        xdir, ydir, zdir = ap.util.align_galaxy(snapshot, idx=None, radialcut=0.1*subhalo.data['Group_R_Crit200'][0] )
        ap.util.rotateto(snapshot, xdir, dir2=ydir, dir3=zdir)

        return snapshot, subhalo, halo_centre, bulk_velocity, xdir, ydir, zdir