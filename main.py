import matplotlib
import argparse
import plots
from plots import *
import data_output
from data_output import *

def plot_or_output_data() -> int:
    print('0\tCancel')
    print('1\tPlot')
    print('2\tOutput data')

    try:
        return int(input())
    except:
        return -1
    
def plot() -> None:
    print()
    print('Select plot')
    print('0  Cancel')
    print()
    print('Original plots (from tutorial)')
    print('1  Star formation history')
    print('2  Disc')
    print('3  Rotation curve')
    print('4  Rotation curves with dark matter')
    print('5  Satellites within R200 - mass against distance')
    print('6  Satellites within R200 with stars and gases separated - mass against distance')
    print('7  Solar mass against redshift')
    print('8  Dark matter mass evolution')
    print('9  Point of maximum mass and dark matter loss')
    print('10 Spatial distribution of accreted stars')
    print('11 Accreted star particles and those bound in satellite galaxies')
    print('12 E-Lz all particles and 3rd most massive progenitor')
    print()
    print('New plots (for R200, assign negative radius)')
    print('13 Disc with specified radius')
    print('14 insitu stellar history within specified radius (multiple plots)')
    print('15 Stellar history within specified radius (multiple plots)')
    print('16 Spatial distributions of accreted stars (multiple plots)')
    print('17 Various halo_6 disc plots showing exsitu elements (multiple plots)')
    print('18 Particle history for specific peak mass index (multiple plots)')
    print('19 Stellar mass against redshift for specific peak mass index')
    print('20 Gas mass against redshift for specific peak mass index')
    print('21 Stellar and gas masses against redshift for specific peak mass index')
    print('22 Stellar mass against stellar half mass radius for specific peak mass index')
    print('23 In-situ stellar mass against redshift')
    print('24 Tracer behaviour by peak mass index')

    selected_plot = 0

    try:
        selected_plot = int(input())
    except:
        print('Incorrect entry')

    if selected_plot == 0:
        None
    elif selected_plot == 1:
        plots.star_formation_history.plot(output_file_path, snapshot, part_type, halo_path).create()
    elif selected_plot == 2:
        plots.disc.plot(output_file_path, snapshot, part_type, halo_path).create()
    elif selected_plot == 3:
        plots.rotation_curve.plot(output_file_path, snapshot, part_type, halo_path).create()
    elif selected_plot == 4:
        plots.rotation_curves_with_dark_matter.plot(output_file_path, snapshot, part_type, halo_path).create()
    elif selected_plot == 5:
        plots.satellites_within_r200.plot(output_file_path, snapshot, halo_path).create()
    elif selected_plot == 6:
        plots.satellites_within_r200_stars_and_gases.plot(output_file_path, snapshot, halo_path).create()
    elif selected_plot == 7:
        plots.solar_mass_redshift.plot(tree_file_path, snapshot, halo_path).create()
    elif selected_plot == 8:
        plots.dark_matter_mass_evolution.plot(tree_file_path, snapshot, halo_path).create()
    elif selected_plot == 9:
        plots.maximum_mass_dark_matter_lost.plot(output_file_path, tree_file_path, snapshot, halo_path).create()
    elif selected_plot == 10:
        plots.spatial_distribution_accreted_stars.plot(output_file_path, list_file_path, snapshot, part_type, halo_path).create()
    elif selected_plot == 11:
        plots.accreted_star_particles_and_those_bound_in_satellite_galaxies.plot(output_file_path, list_file_path, snapshot, part_type, halo_path).create()
    elif selected_plot == 12:
        plots.e_lz_all_particles_and_3rd_most_massive_progenitor.plot(output_file_path, list_file_path, snapshot, part_type, halo_path).create()
    elif selected_plot == 13:
        print('Enter radius in Mpc')
        radius = float(input())
        plots.disc_specify_radius.plot(output_file_path, snapshot, part_type, radius, halo_path).create()
    elif selected_plot == 14:
        print('Enter radius in Mpc')
        radius = float(input())
        plots.insitu_stellar_history_specify_radius.plot(output_file_path, list_file_path, tree_file_path, snapshot, part_type, halo_path, radius).create()
    elif selected_plot == 15:
        print('Enter radius in Mpc')
        radius = float(input())
        plots.stellar_history_specify_radius.plot(output_file_path, list_file_path, tree_file_path, snapshot, part_type, halo_path, radius).create()
    elif selected_plot == 16:
        print('Enter radius in Mpc')
        radius = float(input())
        plots.spatial_distribution_accreted_stars_all.plot(output_file_path, list_file_path, snapshot, part_type, halo_path, radius).create()
    elif selected_plot == 17:
        print('Enter radius in Mpc')
        radius = float(input())
        plots.disc_show_exsitu_elements_specify_radius.plot(output_file_path, list_file_path, snapshot, part_type, radius).create()
    elif selected_plot == 18:
        print('Enter radius in Mpc')
        radius = float(input())
        print('Enter peak mass index')
        peak_mass_index = int(input())
        plots.particle_history_by_peak_mass_index.plot(output_file_path, list_file_path, tree_file_path, snapshot, part_type, halo_path, radius, peak_mass_index).create()
    elif selected_plot == 19:
        print('Enter radius in Mpc')
        radius = float(input())
        print('Enter peak mass index')
        peak_mass_index = int(input())
        plots.stellar_mass_against_redshift.plot(output_file_path, list_file_path, tree_file_path, snapshot, part_type, halo_path, radius, peak_mass_index).create()
    elif selected_plot == 20:
        print('Enter radius in Mpc')
        radius = float(input())
        print('Enter peak mass index')
        peak_mass_index = int(input())
        plots.gas_mass_against_redshift.plot(output_file_path, list_file_path, tree_file_path, snapshot, part_type, halo_path, radius, peak_mass_index).create()
    elif selected_plot == 21:
        print('Enter radius in Mpc')
        radius = float(input())
        print('Enter peak mass index')
        peak_mass_index = int(input())
        plots.stellar_gas_masses_against_redshift.plot(output_file_path, list_file_path, tree_file_path, snapshot, part_type, halo_path, radius, peak_mass_index).create()
    elif selected_plot == 22:
        print('Enter radius in Mpc')
        radius = float(input())
        print('Enter peak mass index')
        peak_mass_index = int(input())
        plots.stellar_mass_against_radius.plot(output_file_path, list_file_path, tree_file_path, snapshot, part_type, halo_path, radius, peak_mass_index).create()
    elif selected_plot == 23:
        print('Enter radius in Mpc')
        radius = float(input())
        plots.insitu_stellar_mass_against_redshift.plot(output_file_path, list_file_path, tree_file_path, snapshot, part_type, halo_path, radius).create()
    elif selected_plot == 24:
        print('Enter radius in Mpc')
        radius = float(input())
        print('Enter peak mass index')
        peak_mass_index = int(input())
        plots.tracer_behaviour.plot(output_file_path, list_file_path, tree_file_path, snapshot, part_type, halo_path, radius, peak_mass_index).create()        
    else:
        print('Unknown request')       

    

def output_data() -> None:
    print()
    print('Select data extraction')
    print('0  Cancel')
    print()
    print('Initial exploration')
    print('1  Radii of star particles')
    print('2  Disc')
    print('3  Disc with specified radius')
    print('4  Satellites within R200')
    print('5  Satellites within R200 with stars and gases separated - mass against distance')
    print('6  Merger tree to csv')
    print('7  Subhalo')
    print('8  Star particle / merger tree data')
    print('9  Stellar history with specified radius')
    print('10 Subhalos to csv')
    print('11 Spatial distributions of accreted stars')
    print()
    print('Supporting data (for R200, assign negative radius)')
    print('12 ParticleID grouped by PeakMassIndex with specified radius')
    print('13 Comparison of star particle / merger tree data with actual merger tree')
    print('14 Search on merger tree for subhalos')
    print('15 Search on merger tree for subhalos by peak mass index')
    print('16 Search on merger tree for subhalos by peak mass index; then find related exsitu particles')
    print('17 Stellar information by peak mass index')
    print('18 Particle history by peak mass index')
    print('19 Obtain sub halo masses from particle histories, by peak mass index')
    print('20 Subhalo by snapshot number and index')
    print('21 All subhalo files as csv, from minimum snapshot number')
    print('22 Snapshots and subhalos, identified from merger tree using peak mass index')
    print('23 More merger tree analysis')
    print('24 Stellar masses and other historical information from merger tree')
    print('25 Disc csv including gas tracer fields')
    print('26 Disc csv with gas fields')
    print('27 Gas by peak mass index')
    print('28 Subhalo disc check')
    print('29 Stellar particles by subhalo')
    print('30 Gas particles by subhalo')
    print('31 Tracer particles by subhalo')
    print('32 More merger tree analysis')
    print('33 More subhalo analysis')
    print('34 Gas history with specified radius')

    selected_data = 0

    try:
        selected_data = int(input())
    except:
        print('Incorrect entry')

    if selected_data == 0:
        None
    elif selected_data == 1:
        data_output.star_particle_radii.data(output_file_path, snapshot, part_type).output()
    elif selected_data == 2:
        data_output.disc.data(output_file_path, snapshot, part_type).output()
    elif selected_data == 3:
        print('Enter radius in Mpc')
        radius = float(input())
        data_output.disc_specify_radius.data(output_file_path, snapshot, part_type, halo_path, radius).output()
    elif selected_data == 4:
        data_output.satellites_within_r200.data(output_file_path, snapshot).output()
    elif selected_data == 5:
        data_output.satellites_within_r200_stars_and_gases.data(output_file_path, snapshot).output()
    elif selected_data == 6:
        data_output.merger_tree.data(tree_file_path, snapshot).output()
    elif selected_data == 7:
        data_output.subhalo.data(output_file_path, snapshot).output()
    elif selected_data == 8:
        data_output.starparticle_mergertree.data(list_file_path, snapshot, halo_path).output()
    elif selected_data == 9:
        print('Enter radius in Mpc')
        radius = float(input())
        data_output.stellar_history_specify_radius.data(output_file_path, list_file_path, snapshot, part_type, halo_path, radius).output()
    elif selected_data == 10:
        data_output.subhalo_to_csv.data(output_file_path, snapshot).output()
    elif selected_data == 11:
        print('Enter radius in Mpc')
        radius = float(input())
        data_output.spatial_distribution_accreted_stars_by_PeakMassIndex.data(output_file_path, list_file_path, snapshot, part_type, halo_path, radius).output()
    elif selected_data == 12:
        print('Enter radius in Mpc')
        radius = float(input())
        data_output.group_by_peak_mass_index.data(output_file_path, list_file_path, snapshot, part_type, halo_path, radius).output()
    elif selected_data == 13:
        print('Enter radius in Mpc')
        radius = float(input())
        print('Enter peak mass index')
        peak_mass_index = int(input())
        data_output.starparticle_mergertree_comparison.data(output_file_path, list_file_path, tree_file_path, snapshot, part_type, halo_path, radius, peak_mass_index).output()
    elif selected_data == 14:
        print('Enter radius in Mpc')
        radius = float(input())
        data_output.merger_tree_subhalo_search.data(output_file_path, list_file_path, tree_file_path, snapshot, part_type, radius).output()
    elif selected_data == 15:
        print('Enter radius in Mpc')
        radius = float(input())
        print('Enter peak mass index')
        peak_mass_index = int(input())
        data_output.merger_tree_subhalo_search_by_peak_mass_index.data(output_file_path, list_file_path, tree_file_path, snapshot, part_type, halo_path, radius, peak_mass_index).output()
    elif selected_data == 16:
        print('Enter radius in Mpc')
        radius = float(input())
        print('Enter peak mass index')
        peak_mass_index = int(input())
        data_output.merger_tree_back_to_particles.data(output_file_path, list_file_path, tree_file_path, snapshot, part_type, halo_path, radius, peak_mass_index).output()
    elif selected_data == 17:
        print('Enter radius in Mpc')
        radius = float(input())
        print('Enter peak mass index')
        peak_mass_index = int(input())
        data_output.stellar_info_by_peak_mass_index.data(output_file_path, list_file_path, tree_file_path, snapshot, part_type, halo_path, radius, peak_mass_index).output()
    elif selected_data == 18:
        print('Enter radius in Mpc')
        radius = float(input())
        print('Enter peak mass index')
        peak_mass_index = int(input())
        data_output.particle_history.data(output_file_path, list_file_path, tree_file_path, snapshot, part_type, halo_path, radius, peak_mass_index).output()
    elif selected_data == 19:
        print('Enter radius in Mpc')
        radius = float(input())
        print('Enter peak mass index')
        peak_mass_index = int(input())
        data_output.masses_from_particle_history.data(output_file_path, list_file_path, tree_file_path, snapshot, part_type, halo_path, radius, peak_mass_index).output()
    elif selected_data == 20:
        print('Enter snapshot number')
        input_snapshot = int(input())
        print('Enter sub halo index')
        subhalo_index = int(input())
        data_output.subhalo_by_ID.data(output_file_path, input_snapshot, subhalo_index).output()
    elif selected_data == 21:
        print('Enter minimum snapshot number')
        input_snapshot = int(input())
        data_output.subhalo_files_by_snapshot_number.data(output_file_path, input_snapshot).output()
    elif selected_data == 22:
        print('Enter radius in Mpc')
        radius = float(input())
        print('Enter peak mass index')
        peak_mass_index = int(input())
        data_output.snapshot_subhalo_from_merger_tree.data(output_file_path, list_file_path, tree_file_path, snapshot, part_type, halo_path, radius, peak_mass_index).output()
    elif selected_data == 23:
        data_output.subhalos_by_snapshot_from_merger_tree.data(tree_file_path, snapshot).output()
    elif selected_data == 24:
        print('Enter radius in Mpc')
        radius = float(input())
        print('Enter peak mass index')
        peak_mass_index = int(input())
        data_output.stellar_masses_navigate_merger_tree.data(output_file_path, list_file_path, tree_file_path, snapshot, part_type, halo_path, radius, peak_mass_index).output()
    elif selected_data == 25:
        data_output.tracer_snapshot.data(output_file_path, snapshot).output()
    elif selected_data == 26:
        data_output.gas_snapshot.data(output_file_path, snapshot).output()
    elif selected_data == 27:
        print('Enter radius in Mpc')
        radius = float(input())
        print('Enter peak mass index')
        peak_mass_index = int(input())
        data_output.gas_by_peak_mass_index.data(output_file_path, list_file_path, tree_file_path, snapshot, part_type, halo_path, radius, peak_mass_index).output()
    elif selected_data == 28:
        data_output.subhalo_disc_check.data(output_file_path, snapshot, part_type).output()
    elif selected_data == 29:
        data_output.stellar_particle_by_subhalo_all.data(output_file_path).output()
    elif selected_data == 30:
        data_output.gas_particle_by_subhalo_all.data(output_file_path).output()
    elif selected_data == 31:
        data_output.tracer_particle_by_subhalo_all.data(output_file_path).output()
    elif selected_data == 32:
        data_output.merger_tree_navigation_analysis.data(tree_file_path, snapshot).output()
    elif selected_data == 33:
        print('Enter snapshot number')
        input_snapshot = int(input())
        data_output.subhalos_by_snapshot.data(output_file_path, input_snapshot).output()
    elif selected_data == 34:
        print('Enter subhalo number')
        subhalo = int(input())
        print('Enter radius in Mpc')
        radius = float(input())
        data_output.gas_history_specify_radius.data(output_file_path, tree_file_path, snapshot, part_type, halo_path, subhalo, radius).output()
    else:
        print('Unknown request')

    # file_path: str, tree_file_path: str, snap_num: int,
    #              part_type: int, halo: str, subhalo_id: int, radius: float

    
            

# matplotlib.use('QtAgg')
print()
print(f'Backend: {matplotlib.get_backend()}')
print()

parser = argparse.ArgumentParser()
parser.add_argument("--halo", type=int, default=6)
parser.add_argument("--snapshot", type=int, default=251)
parser.add_argument("--part_type", type=int, default=4)
args = parser.parse_args()

halo = args.halo
snapshot = args.snapshot
part_type = args.part_type

# breakpoint()

print(f'halo: {halo}')
print(f'snapshot: {snapshot}')
print(f'part_type: {part_type}')
print()

print('Loading data from')

data_path = '/mnt/scratch/users/arirgran/level4/RerunsHighFreqStellarSnaps/'
halo_path = f'halo_{halo}'
output_path = 'output'
list_path = 'lists/accretedstardata/'
tree_path = 'mergertrees/'

print(f'halo path: {halo_path}')

output_paths = [data_path, halo_path + '/', output_path]
output_file_path = ''.join(output_paths)
print(f'output file path: {output_file_path}')

list_paths = [data_path, list_path]
list_file_path = ''.join(list_paths)
print(f'list file path: {list_file_path}')

tree_paths = [data_path, tree_path, halo_path + '/']
tree_file_path = ''.join(tree_paths)
print(f'tree file path: {tree_file_path}')
print()

plot_or_print = plot_or_output_data()

if plot_or_print == 0:
    print('Cancelled')
elif plot_or_print == 1:
    plot()
elif plot_or_print == 2:
    output_data()
else:
    print('Unknown request')
