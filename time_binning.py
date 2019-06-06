"""This file takes a URL as a command line argument and saves the data
from the URL, then it bins the data by time and produces consistent
timestamps for the data points.
"""
__author__ = 'Sagnik Bhattacharya (github.com/sagnibak)'
import numpy as np
import pandas as pd
import argparse
from time import time
from datetime import datetime
from math import isnan
import os


START_TIME = 1447986433  # (not) HARD-CODED VALUE
TIME_INTERVAL = 2400  # seconds (40 minutes), (not) HARD-CODED VALUE


class Bin(object):
    def __init__(self, start_time, end_time, items=None):
        self.start_time = start_time
        self.end_time = end_time
        if items:
            self.items = list(items)
        else:
            self.items = None

    def store(self, value):
        if isnan(value):
            value = 0.
        if self.items:
            self.items.append(value)
        else:
            self.items = [value]

    def average(self):
        if not self.items:
            return float('nan')
        return sum(self.items) / len(self.items)

    def has_time(self, time_):
        """
        >>> a = Bin(100., 150.)
        >>> a.has_time(22)
        False
        >>> a.has_time(100.)
        True
        >>> a.has_time(149.999)
        True
        >>> a.has_time(150.)
        False
        >>> a.has_time(200)
        False
        """
        return self.start_time <= time_ < self.end_time

    def to_list(self):
        """
        >>> a = Bin(100, 150, [100., 200., 250, 200., 0.])
        >>> a.to_list()
        [100, 150.0]
        >>> a.store(float('nan'))
        >>> a.to_list()
        [100, 125.0]
        """
        return [self.start_time, self.average()]

    def __str__(self):
        return f'Start time: {self.start_time} | End time: {self.end_time} | Items: {self.items}'


def store_in_bins(data: np.array):
    """Averages data over `time_interval` and makes
    all timestamps uniform.

    :param data:  Nx2 dimensional Numpy array with N
                  data points and accompanying unix timestamps
    :return:      Mx2 dimensional Pandas DataFrame with M
                  binned data points and accompanying unix
                  timestamps
    """
    n_bins = (int(time()) - START_TIME) // TIME_INTERVAL

    bins = np.empty((n_bins,), dtype=Bin)
    result_bins = np.empty((n_bins, 2), dtype=np.float)

    # make bins and store the values in the right bins
    last_idx = data.shape[0] - 1  # this makes the algorithm run in O(n) time instead of O(n^2)
    for i in range(n_bins):  # loops M times
        bins[i] = Bin(start_time=START_TIME + i * TIME_INTERVAL,
                      end_time=START_TIME + (i + 1) * TIME_INTERVAL)

        while bins[i].has_time(data[last_idx, 0]):
            bins[i].store(data[last_idx, 1])
            last_idx -= 1

    for idx, time_bin in enumerate(bins):
        result_bins[idx] = time_bin.to_list()

    df = pd.DataFrame(result_bins, columns=['unix_time', 'value'])

    return df


def run_binner(url: str, col_name: str):
    try:
        df = pd.read_csv(url, sep=',')
    except ValueError as ve:
        if isinstance(url, pd.DataFrame):
            df = url
        else:
            raise ValueError('Cannot handle this data!')

    timestamps = df['deviceTime_unix'].astype(float)
    data = df[col_name].astype(float)

    df = pd.DataFrame(data={'timestamps': timestamps, 'data': data})
    # make sure dataframe is sorted in descending order
    dg = df.sort_values(by='timestamps', axis=0, ascending=False)

    return store_in_bins(dg.values)


def main():
    global START_TIME, TIME_INTERVAL

    # command line arguments
    parser = argparse.ArgumentParser(description='Download data and bin it by time.')
    parser.add_argument('url', help='URL where you want to get data from')
    parser.add_argument('-c', '--col_name', help='name of the column from where data needs to be binned')
    parser.add_argument('-s', '--save_dir', help='directory where binned data should be saved')
    parser.add_argument('-i', '--time_interval', help='time interval to average data over', type=int)
    parser.add_argument('-t', '--start_time', help='date and to begin collecting data from (24-hour time format)',
                        metavar='YYYY-MM-DD HH:mm:ss', type=str)
    args = parser.parse_args()

    print(f'Getting data from {args.url}')
    if not args.save_dir:
        args.save_dir = 'binned_data'
    print(f'Binned data will be saved in the directory {args.save_dir}')
    if args.time_interval:
        TIME_INTERVAL = args.time_interval
    if args.start_time:
        START_TIME = int(datetime.strptime(args.start_time, '%Y-%m-%d %H:%M:%S').timestamp())

    df_to_save = run_binner(args.url, args.col_name)
    df_to_save.to_csv(os.path.join(args.save_dir, f'ws_data_{args.col_name}_{TIME_INTERVAL}.csv'),
                      index=False, na_rep='nan')


if __name__ == '__main__':
    main()
