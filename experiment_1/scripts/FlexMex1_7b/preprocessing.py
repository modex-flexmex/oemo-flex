import os

from oemof.tools.logger import define_logging
from oemoflex.preprocessing import (
    create_default_data, update_electricity_shortage, update_electricity_demand,
    update_ch4_gt, update_wind_onshore, update_wind_offshore, update_solar_pv,
    update_electricity_bev, create_electricity_bev_profiles,
    create_electricity_demand_profiles,
    create_wind_onshore_profiles, create_wind_offshore_profiles, create_solar_pv_profiles)
from oemoflex.helpers import setup_experiment_paths, load_scalar_input_data, check_if_csv_dirs_equal


name = 'FlexMex1_7b'

# Get paths
exp_paths = setup_experiment_paths(name)

exp_paths.data_preprocessed = os.path.join(exp_paths.data_preprocessed, 'data')

logpath = define_logging(
    logpath=exp_paths.results_postprocessed,
    logfile='oemoflex.log'
)

if not os.path.exists(exp_paths.data_preprocessed):
    for subdir in ['elements', 'sequences']:
        os.makedirs(os.path.join(exp_paths.data_preprocessed, subdir))


def main():
    # Load common input parameters
    scalars = load_scalar_input_data()

    # Filter out only scenario-related input parameters
    scalars = scalars.set_index(['Region', 'Parameter'])
    overwrite_scalars = scalars.loc[scalars['Scenario'] == 'FlexMex1UC5_7_8', :]
    scalars = scalars.loc[scalars['Scenario'].isin([name, 'FlexMex1', 'ALL']), :]

    scalars.update(overwrite_scalars)
    scalars = scalars.reset_index()

    # Prepare oemof.tabular input CSV files
    create_default_data(
        exp_paths.data_preprocessed,
        select_components=[
            'electricity-shortage',
            'electricity-curtailment',
            'electricity-demand',
            'electricity-bev',
            'ch4-gt',
            'wind-offshore',
            'wind-onshore',
            'solar-pv',
        ]
    )

    # update elements
    update_electricity_shortage(exp_paths.data_preprocessed, scalars)
    update_electricity_demand(exp_paths.data_preprocessed, scalars)
    update_wind_onshore(exp_paths.data_preprocessed, scalars)
    update_wind_offshore(exp_paths.data_preprocessed, scalars)
    update_solar_pv(exp_paths.data_preprocessed, scalars)
    update_electricity_bev(exp_paths.data_preprocessed, scalars)
    update_ch4_gt(exp_paths.data_preprocessed, scalars)

    # create sequences
    create_electricity_demand_profiles(exp_paths.data_raw, exp_paths.data_preprocessed)
    create_wind_onshore_profiles(exp_paths.data_raw, exp_paths.data_preprocessed)
    create_wind_offshore_profiles(exp_paths.data_raw, exp_paths.data_preprocessed)
    create_solar_pv_profiles(exp_paths.data_raw, exp_paths.data_preprocessed)
    create_electricity_bev_profiles(exp_paths.data_raw, exp_paths.data_preprocessed)

    # compare with previous data
    previous_path = os.path.join(
        os.path.split(exp_paths.data_preprocessed)[0] + '_default', 'data'
    )
    new_path = exp_paths.data_preprocessed
    check_if_csv_dirs_equal(new_path, previous_path)


if __name__ == '__main__':
    main()
