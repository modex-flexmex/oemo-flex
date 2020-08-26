"""
Run this script from the root directory of the datapackage to update
or create meta data.
"""
import logging
import os

from oemof.tools.logger import define_logging
from oemof.tabular.datapackage import building
from oemoflex.helpers import setup_experiment_paths


name = 'FlexMex1_4a'

basepath = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
exp_paths = setup_experiment_paths(name, basepath)

logpath = define_logging(
    logpath=exp_paths.results_postprocessed,
    logfile='oemoflex.log'
)


def main():
    r"""Infer the metadata of the datapackage"""
    logging.info("Inferring the metadata of the datapackage")
    building.infer_metadata(
        package_name=name,
        foreign_keys={
            'bus': [
                'heat-shortage',
                'heat-excess',
                'wind-onshore',
                'wind-offshore',
                'solar-pv',
                'electricity-shortage',
                'electricity-curtailment',
                'electricity-demand',
                'heat-demand',
            ],
            'profile': [
                'wind-onshore',
                'wind-offshore',
                'solar-pv',
                'electricity-demand',
                'heat-demand',
            ],
            'chp': [
                'ch4-bpchp',
            ],
        },
        path=exp_paths.data_preprocessed
    )


if __name__ == '__main__':
    main()