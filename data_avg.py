#code to average data and graph data

import csv
import urllib.request
import codecs
import numpy as np
import datetime

from bokeh.plotting import figure, show, output_file, save
from bokeh.models import LinearAxis, Range1d

class data_average:
    def _init_(self):
        pass

    def get_csv(self, url):
        csv_file = urllib.request.urlopen(url)
        data = csv.reader(codecs.iterdecode(csv_file, 'utf-8'))
        data_list = []
        for row in data:
            data_list.append(row)
        return data_list

    def avg_main(self, url, sec_start, sec_stop, avg_over_time, column):
        sec_stop = float(sec_stop)
        sec_start = float(sec_start)
        csv_data = np.array(self.get_csv(url))
        csv_data = np.delete(csv_data, (0), axis=0)
        time_data = csv_data[:,2].astype(float)
        bin_number = int((sec_stop - sec_start)/avg_over_time)
        early = sec_start
        late = early + avg_over_time
        avgd_data_points = []
        while bin_number > 0:
            to_be_avged = []
            index_list= list(np.where(np.logical_and(time_data >= float(early) , time_data < float(late))))
            counter = index_list[0].size
            if counter == 0:
                early = late
                late += avg_over_time
                bin_number -= 1
            upper_bound = index_list[-1]
            to_be_avged = []
            errors = []
            while counter > 0:
                b1 = csv_data[upper_bound - counter - 1, column-1]
                b = [float(n) for n in b1]
                c1 = csv_data[upper_bound - counter - 1, -1]
                c = [float(n) for n in c1]
                to_be_avged.append(b)
                errors.append(c)
                counter -= 1
            avg_time = (early+late)/2
            bin_avg = np.average(to_be_avged)
            error_avg = np.average(errors)
            avgd_data_points.append([avg_time,bin_avg,error_avg])
            early = late
            late += avg_over_time
            print(bin_number)
            bin_number += -1
        return avgd_data_points

class avg_graph:
    def _init_(self):
        pass

    def graph(self, points, error, to_do):
        plot = figure(plot_width = 1000, plot_height = 1000, tools="pan,wheel_zoom,box_zoom,reset")
        i = len(points)

        while i > 0:
            print(i)
            plot.circle(x=points[i-1][0], y=points[i-1][1])
            i -= 1

        i = len(points)
        if error == 'Y':
            while i > 0:
                print(i)
                plot.vbar(x=points[i-1][0],top=points[i-1][2], bottom = 0, width = 1, color = "red")
                i -= 1

        if to_do == 'Y':
            show(plot)
        else:
            output_file(to_do+'.html')
            save(plot)

a = str(input('csv url: '))
b = int(input('start time (sec since epoch): '))
c = int(input('stop time: '))
d = int(input('# of sec to avg over: '))
e = int(input('column of csv to avg: '))
f = str(input('plot with error? (Y/N): '))
g = str(input('save or show (save: file name, show: Y): '))

print('Progress:')
avger = data_average()
final_data_list = avger.avg_main(a, b, c, d, e)

grapher = avg_graph()
grapher.graph(final_data_list, f, g)
print('Finished')
