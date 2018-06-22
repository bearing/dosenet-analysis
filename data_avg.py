#General averaging code
import csv
import urllib.request
import codecs
import numpy as np
import datetime
from datetime import timedelta

class data_average:
    def _init_(self):
        pass

    #get csv file from url
    def get_csv(url):
        csv_file = urllib.request.urlopen(url)
        data = csv.reader(codecs.iterdecode(csv_file, 'utf-8'))
        data_list = []
        for row in data:
            data_list.append(row)
        return data_list

    #to average data
    def average(url, start_time, stop_time, avg_over_time, column):
        csv_data = np.array(self.get_csv(url))
        sec_start = datetime.datetime(start_time).timestamp()
        sec_stop = datetime.datetime(stop_time).timestamp()
        counter = int((sec_stop - sec_start)/avg_over_time) # num of times  program will take an avg
        early = start_time # lower bound
        sec_added = datetime.timedelta(seconds = avg_over_time) # allows the addition of seconds to datetime to get another datetime
        late = start_time + sec_added # upper bound
        avgd_data_points = []
        while counter>0:
            index_list = np.where(np.logical_and(csv_data[:][0] >= early, csv_data[:][0] < late)) #finds the indices of the needed datetime values
            index_list_size = np.shape(index_list)[1] #finds number of elements in index_list
            counter2 = index_list_size
            to_be_avged = {}
            while index_list_size>=0:
                a = csv_data[index_list[0][index_list_size]][column-1]
                to_be_avged.append(a)
                index_list_size += -1
            bin_avg = np.average(to_be_avged)
            avgd_data_points.append(bin_avg)
            early = late
            late += sec_added
            counter += -1
        return avgd_data_points
