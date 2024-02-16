import logging
import os

import dask.dataframe as ddf
import numpy as np
import pandas as pd

import src.algorithms.distributions
import src.elements.s3_parameters as s3p


class Readings:

    def __init__(self, s3_parameters: s3p.S3Parameters):
        """

        :param s3_parameters:
        """

        self.__s3_parameters = s3_parameters

        self.__distributions = src.algorithms.distributions.Distributions()

        self.__meta = {0.1: float, 0.25: float, 0.5: float, 0.75: float, 0.9: float}
        self.__rename = {0.1: 'lower_decile', 0.25: 'lower_quartile', 0.5: 'median',
                         0.75: 'upper_quartile', 0.9: 'upper_decile'}

    def __calculations(self, frame: ddf.DataFrame) -> pd.DataFrame:

        computations: ddf.DataFrame = frame[['sequence_id', 'date', 'measure']].groupby(
            by=['sequence_id', 'date']).apply(self.__distributions.quantiles, meta=self.__meta)
        calculations: pd.DataFrame = computations.compute(scheduler='processes')

        return calculations

    def __structure(self, blob: pd.DataFrame):

        data = blob.copy()
        data.reset_index(drop=False, inplace=True)
        data.rename(columns=self.__rename)

        logging.log(level=logging.INFO, msg=data.head())

    def exc(self, s3_keys: list):
        """

        :param s3_keys:
        :return:
        """

        strings = [os.path.dirname(s3_key) for s3_key in s3_keys]
        paths = np.unique(np.array(strings))
        nodes = [f's3://{self.__s3_parameters.bucket_name}/{path}/*.csv' for path in paths]

        for node in nodes:

            frame: ddf.DataFrame = ddf.read_csv(node)
            calculations = self.__calculations(frame=frame)
            self.__structure(blob=calculations)
