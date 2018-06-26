"""Script to repeatedly run `time_binning.py` with
different arguments each time.
"""

import os

SECONDS_IN_A_DAY = 60 * 60 * 24


def run_all_binnings(time_interval):
    """Runs `time_binning.py` for all the five
    data types, passing in the argument `time_interval`.
    """
    # os.system(
    #     f'python time_binning.py ~/Downloads/etch_roof_weather.csv -c pressure -s binned_data/ -i {time_interval}')
    # os.system(
    #     f'python time_binning.py ~/Downloads/etch_roof_weather.csv -c temperature -s binned_data/ -i {time_interval}')
    # os.system(
    #     f'python time_binning.py ~/Downloads/etch_roof_weather.csv -c humidity -s binned_data/ -i {time_interval}')
    # os.system(
    #     f'python time_binning.py ~/Downloads/etch_roof_d3s.csv -c cpm -s binned_data/ -i {time_interval}')
    # os.system(
    #     f'python time_binning.py ~/Downloads/etch_roof_adc.csv -c co2_ppm -s binned_data/ -i {time_interval}')
    os.system(
        f'python time_binning.py ~/Downloads/etch_roof.csv -c cpmpg -s binned_data/ -i {time_interval}')


def main():
    for i in range(1, 29):
        run_all_binnings(int((i / 2) * SECONDS_IN_A_DAY))


if __name__ == '__main__':
    main()
