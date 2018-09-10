#code to average data and graph averaged data
#to install dependencies: conda install selenium phantomjs pillow

import csv, urllib.request, codecs, datetime
import numpy as np

from bokeh.plotting import figure, show, output_file, save, ColumnDataSource
from bokeh.plotting.figure import Figure
from bokeh.models import LinearAxis, Range1d, Label, HoverTool
from bokeh.io import export_svgs
from bokeh.models.annotations import Title

class data_average:
    def _init_(self):
        pass

    def get_csv(self, url):
        try:
            csv_file = urllib.request.urlopen(url)
            data = csv.reader(codecs.iterdecode(csv_file, 'utf-8')) #open csv using url
        except:
            print('Error: unable to access CSV')
            raise SystemExit(0)
        data_list = []
        for row in data:
            data_list.append(row)
        return data_list

    def avg_main(self, data_list, sec_start, sec_stop, interval, column, cpm):
        csv_data = np.array(data_list)
        csv_data = np.delete(csv_data, (0), axis=0) #delete metadata
        time_data = csv_data[:,2].astype(float)
        bin_number = int((sec_stop - sec_start)/interval)
        #if amount of remainder data is greater than 15% of interval, put in a new bin
        if sec_stop - (sec_start + interval*bin_number) > 0.15*interval:
            bin_number += 1
            leftover = True
        else:
            leftover = False
        early = sec_start #starting point of bin
        late = early + interval #ending point of bin
        avgd_data_points = []
        while bin_number > 0: #averaging data in each bin
            to_be_avged = []
            index_list= list(np.where(np.logical_and(time_data >= float(early) , time_data < float(late)))) #find location of data in a bin
            counter = index_list[0].size #determine number of data points
            if counter == 0:
                pass
            else:
                upper_bound = (index_list[0][-1])
                to_be_avged = []
                errors = []
                while counter > 0: #iterate through bin to get data and error
                    b = float(csv_data[upper_bound - counter - 1, column-1])
                    to_be_avged.append(b)
                    if cpm != 0:
                        c = float(csv_data[upper_bound - counter - 1, -1])
                        errors.append(c)
                    counter -= 1
                avg_time = (early+late)/2
                bin_avg = np.average(to_be_avged)
                if len(to_be_avged) == 1:
                    error_avg = 0.05*to_be_avged[0]
                else:
                    #average/calculate error
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
            if leftover == True and bin_number == 2:
                late = sec_stop
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
        plot.y_range=Range1d(min_val, max_val) #set up y-axis
        i = len(points)
        if points2 == False:
            if error == 'Y':
                while i > 0:
                    a = datetime.datetime.fromtimestamp(points[i-1][0])
                    plot.vbar(x=a, top=points[i-1][1]+points[i-1][2], bottom=points[i-1][1]-points[i-1][2], width = 0.01, color = "green")
                    plot.circle(x=a, y=points[i-1][1])
                    i -= 1

            else:
                i = len(points)
                while i > 0:
                    a = datetime.datetime.fromtimestamp(points[i-1][0])
                    plot.circle(x=a, y=points[i-1][1])
                    i -= 1

        if points2 != False:
            points2data = [i[1] for i in points2]
            min_val2 = 0.25*min(points2data)
            max_val2 = 1.75*max(points2data)
            plot.extra_y_ranges = {'data2': Range1d(start = min_val2, end=max_val2)} #set up 2nd y-axis
            plot.add_layout(LinearAxis(y_range_name='data2'), 'right')
            i = len(points2)
            if error == 'Y':
                while i > 0:
                    a = datetime.datetime.fromtimestamp(points[i-1][0])
                    plot.vbar(x=a, top=points[i-1][1]+points[i-1][2], bottom=points[i-1][1]-points[i-1][2], width = 0.01, color = "green")
                    plot.circle(x=a, y=points[i-1][1])
                    a = datetime.datetime.fromtimestamp(points2[i-1][0])
                    plot.vbar(x=a, top=points2[i-1][1]+points2[i-1][2], bottom=points2[i-1][1]-points2[i-1][2], width = 0.01, color = "orange", y_range_name='data2')
                    plot.triangle(x=a, y=points2[i-1][1], y_range_name='data2', color = 'red')
                    i -= 1

            else:
                i = len(points2)
                while i > 0:
                    a = datetime.datetime.fromtimestamp(points[i-1][0])
                    plot.circle(x=a, y=points[i-1][1])
                    a = datetime.datetime.fromtimestamp(points2[i-1][0])
                    plot.triangle(x=a, y=points2[i-1][1], y_range_name='data2', color = 'red')
                    i -= 1

        if to_do == 'Y':
            show(plot)
            return
        else:
            if file_type == 'html':
                output_file(to_do+'.html')
            else:
                a = to_do+'.svg'
                plot.output_backend = 'svg'
                export_svgs(plot, filename=a)
            save(plot)
            return

    def dvd_graph(self, points, points2, error, to_do, file_type, names, coefficient): #data v data graph
        #make sure no gaps in data for either point set
        points_time = {i[0] for i in points}
        points2_time = {i[0] for i in points2}
        point_time_intersection = list(points2_time.intersection(points_time))
        points = [points[list(points_time).index(i)] for i in point_time_intersection]
        points2 = [points2[list(points2_time).index(i)] for i in point_time_intersection]

        plot = figure(plot_width = 1000, plot_height = 1000, tools="pan,wheel_zoom,box_zoom,reset")
        if names != False:
            plot.xaxis.axis_label = (names[1].replace('_',' ')).upper()
            plot.yaxis.axis_label = (names[2].replace('_',' ')).upper()
            plot_title = Title()
            plot_title.text = (names[0].replace('_',' ')).upper()
            plot.title = plot_title
        i = len(points2)
        if error == 'Y':
            #improve h error bar to v error bar width ratio
            pointserror, points2error = [i[2] for i in points], [i[2] for i in points2]
            min_val, max_val, min_val2, max_val2 = 0.25*min(pointserror), 1.75*max(pointserror), 0.25*min(points2error), 1.75*max(points2error)
            points_diff ,points2_diff = max_val - min_val, max_val2 - min_val2
            if points2_diff > points_diff:
                ratio = 1
                ratio2 = points2_diff/points_diff
            else:
                ratio = points_diff/points2_diff
                ratio2 = 1

            while i > 0:
                b1 = plot.vbar(x=points[i-1][1], top=points2[i-1][1]+points2[i-1][2], bottom=points2[i-1][1]-points2[i-1][2], width = 0.0005*ratio, color = "#ff4d4d")
                b2 = plot.hbar(y=points2[i-1][1], left=points[i-1][1]+points[i-1][2], right=points[i-1][1]-points[i-1][2], height = 0.0005*ratio2, color = "#ff4d4d")
                i -= 1

        if coefficient != False:
            coefficient_subtitle = 'Correlation Coefficent: '+''.join(list(str(coefficient))[0:6])
            plot.add_layout(Title(text=coefficient_subtitle, align="left", text_font_size = "12px"), "above")

        i = len(points)
        while i > 0:
            plot.circle(x=points[i-1][1], y=points2[i-1][1], color = "#0052cc", size = 5)
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

    def graph_main(self, points, points2, error, to_do, file_type, graph_type, names, coefficient):
        if len(points) == 0:
            print('Error - CSV 1 empty')
            raise SystemExit(0)
        if points2 != False:
            if len(points2) == 0:
                print('Error - CSV 2 empty')
                raise SystemExit(0)

        if graph_type == 1:
            self.dvd_graph(points, points2, error, to_do, file_type, names, coefficient)
            return

        if graph_type == 2:
            self.dvt_graph(points, points2, error, to_do, file_type)
            return

#to enable user input
def user_based_runner():
    a = input('csv url: ')
    a2 = input('csv2 (url/N): ')
    b = float(int(input('start time (sec since epoch): ')))
    c = float(int(input('stop time: ')))
    if c < b:
        print('Error: stop time less than start time')
        raise SystemExit(0)
    d = float(int(input('# of sec to avg over: ')))

    if a2 != 'N':
        e = int(input('column of csv1 to avg: '))
        e2 = int(input('column of csv2 to avg: '))
        g = int(input('1) data1 v d2 OR 2) d1,d2 v time (1/2): '))
    else:
        e = int(input('column of csv to avg: '))
        g = 2

    f = input('plot with error? (Y/N): ')
    h = input('save or show graph (save: file name, show: Y): ')

    if h != 'Y':
        j = input('output file format? (svg/html): ')
    else:
        j = False

    avger = data_average()
    final_data_list = avger.avg_main(avger.get_csv(a), b, c, d, e, 0)


    if a2 != 'N':
        final_data_list2 = avger.avg_main(avger.get_csv(a2), b, c, d, e2, 0)
    else:
        final_data_list2 = False

    grapher = avg_graph()
    grapher.graph_main(final_data_list, final_data_list2, f, h, j, g, False, False)
    return

#user_based_runner()
