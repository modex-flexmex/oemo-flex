import os

import pandas as pd

from oemof.tools.logger import define_logging
from oemoflex.preprocessing import (
    create_default_elements, update_shortage, update_load, update_wind_onshore,
    update_wind_offshore, update_solar_pv, update_nuclear_st, update_ch4_gt, update_link,
    create_electricity_demand_profiles, create_wind_onshore_profiles, create_wind_offshore_profiles,
    create_solar_pv_profiles)
from oemoflex.helpers import setup_experiment_paths, check_if_csv_dirs_equal


name = 'FlexMex1_2d'

# Get paths
basepath = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
exp_paths = setup_experiment_paths(name, basepath)

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
    scalars = pd.read_csv(
        os.path.join(exp_paths['data_raw'], 'Scalars.csv'),
        header=0,
        na_values=['not considered', 'no value']
    )

    # Filter out only scenario-related input parameters
    scalars = scalars.loc[scalars['Scenario'].isin([name, 'FlexMex1', 'ALL']), :]

    # Prepare oemof.tabular input CSV files
    create_default_elements(
        os.path.join(exp_paths.data_preprocessed, 'elements'),
        select_components=[
            'ch4-gt',
            'electricity-curtailment',
            'electricity-demand',
            'electricity-shortage',
            'electricity-transmission',
            'solar-pv',
            'uranium-nuclear-st',
            'wind-offshore',
            'wind-onshore'
        ]
    )

    # update elements
    update_ch4_gt(exp_paths.data_preprocessed, scalars)
    update_link(exp_paths.data_preprocessed, scalars)
    update_load(exp_paths.data_preprocessed, scalars)
    update_nuclear_st(exp_paths.data_preprocessed, scalars)
    update_shortage(exp_paths.data_preprocessed, scalars)
    update_solar_pv(exp_paths.data_preprocessed, scalars)
    update_wind_offshore(exp_paths.data_preprocessed, scalars)
    update_wind_onshore(exp_paths.data_preprocessed, scalars)

    # create sequences
    create_electricity_demand_profiles(exp_paths.data_raw, exp_paths.data_preprocessed)
    create_solar_pv_profiles(exp_paths.data_raw, exp_paths.data_preprocessed)
    create_wind_offshore_profiles(exp_paths.data_raw, exp_paths.data_preprocessed)
    create_wind_onshore_profiles(exp_paths.data_raw, exp_paths.data_preprocessed)

    # compare with previous data
    previous_path = os.path.join(os.path.split(exp_paths.data_preprocessed)[0] + '_default', 'data')
    new_path = exp_paths.data_preprocessed
    #check_if_csv_dirs_equal(new_path, previous_path)


if __name__ == '__main__':
    main()
