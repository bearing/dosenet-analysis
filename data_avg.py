#code to average data and graph data
#to install dependencies: conda install selenium phantomjs pillow

import csv
import urllib.request
import codecs
import numpy as np
import datetime

from bokeh.plotting import figure, show, output_file, save
from bokeh.models import LinearAxis, Range1d
from bokeh.io import export_svgs

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
                pass
            else:
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

    def graph(self, points, points2, error, to_do, file_type, graph_type):
        if len(points) == 0:
            print('Error - Data1 empty')
            return
        if points2 != False:
            if len(points2) == 0:
                print('Error - Data2 empty')
                return
        if graph_type == 2:
            plot = figure(plot_width = 1000, plot_height = 1000, tools="pan,wheel_zoom,box_zoom,reset", x_axis_type='datetime')
            pointsdata = [i[1] for i in points]
            min_val = 0.25*min(pointsdata)
            max_val = 1.75*max(pointsdata)
            plot.y_range=Range1d(min_val, max_val)
            i = len(points)
            if error == 'Y':
                while i > 0:
                    print(i)
                    a = datetime.datetime.fromtimestamp(points[i-1][0])
                    plot.vbar(x=a, top=points[i-1][1]+points[i-1][2], bottom=points[i-1][1]-points[i-1][2], width = 0.01, color = "red")
                    i -= 1

            i = len(points)
            while i > 0:
                print(i)
                a = datetime.datetime.fromtimestamp(points[i-1][0])
                plot.circle(x=a, y=points[i-1][1])
                i -= 1

            if points2 != False:
                points2data = [i[1] for i in points2]
                min_val2 = 0.25*min(points2data)
                max_val2 = 1.75*max(points2data)
                plot.extra_y_ranges = {'data2': Range1d(start = min_val2, end=max_val2)}
                plot.add_layout(LinearAxis(y_range_name='data2'), 'right')
                i = len(points2)
                if error == 'Y':
                    while i > 0:
                        print(i)
                        a = datetime.datetime.fromtimestamp(points2[i-1][0])
                        plot.vbar(x=a, top=points2[i-1][1]+points2[i-1][2], bottom=points2[i-1][1]-points2[i-1][2], width = 0.01, color = "green", y_range_name='data2')
                        i -= 1

                i = len(points2)
                while i > 0:
                    print(i)
                    a = datetime.datetime.fromtimestamp(points2[i-1][0])
                    plot.triangle(x=a, y=points2[i-1][1], y_range_name='data2', color = 'yellow')
                    i -= 1

        else:
            plot = figure(plot_width = 1000, plot_height = 1000, tools="pan,wheel_zoom,box_zoom,reset")
            i = len(points2)
            if error == 'Y':
                while i > 0:
                    print(i)
                    plot.vbar(x=points[i-1][1], top=points2[i-1][1]+points2[i-1][2], bottom=points2[i-1][1]-points2[i-1][2], width = 0.01, color = "red")
                    plot.hbar(y=points2[i-1][1], left=points[i-1][1]+points[i-1][2], right=points[i-1][1]-points[i-1][2], height = 0.01, color = "green")
                    i -= 1

            i = len(points)
            while i > 0:
                try:
                    print(i)
                    plot.circle(x=points[i-1][1], y=points2[i-1][1], radius = 0.01)
                except:
                    pass
                i -= 1

        if to_do == 'Y':
            show(plot)
        else:
            if file_type == 'html':
                output_file(to_do+'.html')
            else:
                a = to_do+".svg"
                plot.output_backend = "svg"
                export_svgs(plot, filename=a)
            save(plot)

a = str(input('csv url: '))
a2 = str(input('csv2 (url/N): '))
b = int(input('start time (sec since epoch): '))
c = int(input('stop time: '))
d = int(input('# of sec to avg over: '))
e = int(input('column of csv to avg: '))

if a2 != 'N':
    e2 = int(input('column of csv2 to avg: '))
    g = int(input('1) data1 v d2 OR 2) d1,d2 v time (1/2): '))
else:
    g = 2
f = str(input('plot with error? (Y/N): '))
h = str(input('save or show graph (save: file name, show: Y): '))
if h != 'Y':
    j = str(input('output file format? (svg/html): '))
else:
    j = False

print('Progress:')
avger = data_average()
final_data_list = avger.avg_main(a, b, c, d, e)


if a2 != 'N':
    final_data_list2 = avger.avg_main(a2, b, c, d, e2)
else:
    final_data_list2 = False

grapher = avg_graph()
grapher.graph(final_data_list, final_data_list2, f, h, j, g)
print('Finished')
