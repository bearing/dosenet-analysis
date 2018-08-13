#code to average data and graph averaged data
#to install dependencies: conda install selenium phantomjs pillow

import csv, urllib.request, codecs, datetime
import numpy as np

from bokeh.plotting import figure, show, output_file, save
from bokeh.models import LinearAxis, Range1d, ColumnDataSource
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

    def avg_main(self, data_list, sec_start, sec_stop, interval, column, cpm):
        sec_stop = float(sec_stop)
        sec_start = float(sec_start)
        csv_data = np.array(data_list)
        csv_data = np.delete(csv_data, (0), axis=0) #deleting metadata
        time_data = csv_data[:,2].astype(float)
        bin_number = int((sec_stop - sec_start)/interval)
        early = sec_start
        late = early + interval
        avgd_data_points = []
        while bin_number > 0:
            to_be_avged = []
            index_list= list(np.where(np.logical_and(time_data >= float(early) , time_data < float(late))))
            counter = index_list[0].size
            if counter == 0: #if no data, move to next bin
                pass
            else:
                upper_bound = (index_list[0][-1])
                to_be_avged = []
                errors = []
                while counter > 0:
                    b = float(csv_data[upper_bound - counter - 1, column-1])
                    c = float(csv_data[upper_bound - counter - 1, -1]) #account for the cpm error already being averaged over 5min
                    to_be_avged.append(b)
                    errors.append(c)
                    counter -= 1

                avg_time = (early+late)/2
                bin_avg = np.average(to_be_avged)
                if cpm != 0:
                    error_sqd = [5*((i)**2) for i in errors]
                    error_avg = (np.sum(error_sqd))**0.5
                    error_avg = error_avg/(interval/60)
                else:
                    std_dev = np.std(to_be_avged)
                    error_avg = std_dev
                avgd_data_points.append([avg_time,bin_avg,error_avg])
            early = late
            late += interval
            #print(bin_number)
            bin_number += -1
        return avgd_data_points

class avg_graph:
    def _init_(self):
        pass

    def dvt_graph(self, points, points2, error, to_do, file_type): #data v time graph
        plot = figure(plot_width = 1000, plot_height = 1000, tools="pan,wheel_zoom,box_zoom,reset", x_axis_type='datetime')
        pointsdata = [i[1] for i in points]
        min_val = 0.25*min(pointsdata)
        max_val = 1.75*max(pointsdata)
        plot.y_range=Range1d(min_val, max_val)
        i = len(points)
        if points2 == False:
            if error == 'Y':
                while i > 0:
                    #print(i)
                    a = datetime.datetime.fromtimestamp(points[i-1][0])
                    plot.vbar(x=a, top=points[i-1][1]+points[i-1][2], bottom=points[i-1][1]-points[i-1][2], width = 0.01, color = "green")
                    a = datetime.datetime.fromtimestamp(points[i-1][0])
                    plot.circle(x=a, y=points[i-1][1])
                    i -= 1

            else:
                i = len(points)
                while i > 0:
                    #print(i)
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
                    #print(i)
                    a = datetime.datetime.fromtimestamp(points[i-1][0])
                    plot.vbar(x=a, top=points[i-1][1]+points[i-1][2], bottom=points[i-1][1]-points[i-1][2], width = 0.01, color = "green")
                    a = datetime.datetime.fromtimestamp(points[i-1][0])
                    plot.circle(x=a, y=points[i-1][1])
                    a = datetime.datetime.fromtimestamp(points2[i-1][0])
                    plot.vbar(x=a, top=points2[i-1][1]+points2[i-1][2], bottom=points2[i-1][1]-points2[i-1][2], width = 0.01, color = "red", y_range_name='data2')
                    a = datetime.datetime.fromtimestamp(points2[i-1][0])
                    plot.triangle(x=a, y=points2[i-1][1], y_range_name='data2', color = 'orange')
                    i -= 1

            else:
                i = len(points2)
                while i > 0:
                    #print(i)
                    a = datetime.datetime.fromtimestamp(points[i-1][0])
                    plot.circle(x=a, y=points[i-1][1])
                    a = datetime.datetime.fromtimestamp(points2[i-1][0])
                    plot.triangle(x=a, y=points2[i-1][1], y_range_name='data2', color = 'orange')
                    i -= 1

            if to_do == 'Y':
                show(plot)
            else:
                if file_type == 'html':
                    output_file(to_do+'.html')
                else:
                    a = to_do+'.svg'
                    plot.output_backend = 'svg'
                    export_svgs(plot, filename=a)
                save(plot)

    def dvd_graph(self, points, points2, error, to_do, file_type): #data v data graph
        #make sure no gaps in data for either point set
        points_time = {i[0] for i in points}
        points2_time = {i[0] for i in points2}
        point_time_intersection = list(points2_time.intersection(points_time))
        points = [points[list(points_time).index(i)] for i in point_time_intersection]
        points2 = [points2[list(points2_time).index(i)] for i in point_time_intersection]
        plot = figure(plot_width = 1000, plot_height = 1000, tools="pan,wheel_zoom,box_zoom,reset")#, tooltips=ToolTips)
        points_date = [i[0] for i in points]
        point_radius = 10
        i = len(points2)
        if error == 'Y':
            while i > 0:
                #print(i)
                plot.vbar(x=points[i-1][1], top=points2[i-1][1]+points2[i-1][2], bottom=points2[i-1][1]-points2[i-1][2], width = 0.001, color = "red")
                plot.hbar(y=points2[i-1][1], left=points[i-1][1]+points[i-1][2], right=points[i-1][1]-points[i-1][2], height = 0.001, color = "red")
                i -= 1

        i = len(points)
        while i > 0:
            #print(i)
            plot.circle(x=points[i-1][1], y=points2[i-1][1], size = point_radius, color = "blue")
            i -= 1

        if to_do == 'Y':
            show(plot)
        else:
            if file_type == 'html':
                output_file(to_do+'.html')
            else:
                a = to_do+'.svg'
                plot.output_backend = 'svg'
                export_svgs(plot, filename=a)
            save(plot)

    def graph_main(self, points, points2, error, to_do, file_type, graph_type):
        if len(points) == 0:
            #print('Error - CSV 1 empty')
            return
        if points2 != False:
            if len(points2) == 0:
                #print('Error - CSV 2 empty')
                return

        if graph_type == 1:
            self.dvd_graph(points, points2, error, to_do, file_type)
            return

        if graph_type == 2:
            self.dvt_graph(points, points2, error, to_do, file_type)
            return

#function argument info for user input
def user_based_runner():
    a = input('csv url: ')
    a2 = input('csv2 (url/N): ')
    b = int(input('start time (sec since epoch): '))
    c = int(input('stop time: '))
    d = int(input('# of sec to avg over: '))
    e = int(input('column of csv to avg: '))

    if a2 != 'N':
        e2 = int(input('column of csv2 to avg: '))
        g = int(input('1) data1 v d2 OR 2) d1,d2 v time (1/2): '))
    else:
        g = 2
    f = input('plot with error? (Y/N): ')
    h = input('save or show graph (save: file name, show: Y): ')
    if h != 'Y':
        j = input('output file format? (svg/html): ')
    else:
        j = False

    print('Progress:')
    avger = data_average()
    final_data_list = avger.avg_main(self.get_csv(a), b, c, d, e, 0)


    if a2 != 'N':
        final_data_list2 = avger.avg_main(self.get_csv(a2), b, c, d, e2, 0)
    else:
        final_data_list2 = False

    grapher = avg_graph()
    grapher.graph_main(final_data_list, final_data_list2, f, h, j, g)
    print('Finished')
    return

#user_based_runner()
