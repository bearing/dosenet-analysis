#pearson correlation

import numpy
from bokeh.plotting import figure, show, output_file, save
from bokeh.io import export_svgs

#data_avg.py: code to average data and graph averaged data
from data_avg import data_average, avg_graph

class correlation:
    def _init_(self):
        pass

    data_avger = data_average()
    avg_grapher = avg_graph()

    def input(self):
        self.u1 = 'https://radwatch.berkeley.edu/sites/default/files/dosenet/etch_roof_weather.csv' #input('csv url1: ')
        self.c1 = 4 #int(input('column # for csv1: '))
        self.csv1 = self.data_avger.get_csv(self.u1)
        self.f1 = self.csv1[0][self.c1-1]
        self.u2 = 'https://radwatch.berkeley.edu/sites/default/files/dosenet/etch_roof.csv' #input('csv url2: ')
        self.c2 = 4 #int(input('column # for csv2: '))
        self.csv2 = self.data_avger.get_csv(self.u2)
        self.f2 = self.csv2[0][self.c2-1]
        print(self.f2)
        self.type = 'html' #input('file type (svg/html): ')
        self.start = 1523137415 #float(input('start (epoch): '))
        self.stop = 1525428315 #float(input('stop: '))
        self.error = 'Y' #input('error? (Y/N): ')
        interval_input = input('comma separated intervals in secs: ')
        interval_input = interval_input.strip(' ')
        str_intervals = interval_input.split(',')
        intervals = [int(i) for i in str_intervals]
        return intervals

    def pearson_calc(self, x, y):
        a = numpy.average(x)
        b = numpy.average(y)
        X = numpy.sum([(i - a)**2 for i in x])
        Y = numpy.sum([(i - b)**2 for i in y])
        XY = numpy.sum([(i - a)*(j - b) for i,j in zip(x,y)])
        coefficient = XY/(X*Y)**0.5
        return coefficient

    def averager_runner(self, interval):
        if self.f1 == 'cpm':
            points1 = self.data_avger.avg_main(self.csv1, self.start, self.stop, interval, self.c1, 1)
        else:
            points1 = self.data_avger.avg_main(self.csv1, self.start, self.stop, interval, self.c1, 0)
        if self.f2 == 'cpm':
            points2 = self.data_avger.avg_main(self.csv2, self.start, self.stop, interval, self.c2, 1)
        else:
            points2 = self.data_avger.avg_main(self.csv2, self.start, self.stop, interval, self.c2, 0)
        avg_points1_data = [i[1] for i in points1]
        avg_points2_data = [i[1] for i in points2]
        r = self.pearson_calc(avg_points1_data, avg_points2_data)
        return points1, points2, r

    def coefficient_plot(self, intervals, coefficients):
        x_labels = [str(i) for i in intervals]
        coefficients.reverse()
        plotting = figure(plot_width = 1000, plot_height = 1000, x_range = x_labels, tools="pan,wheel_zoom,box_zoom,reset")
        plotting.vbar(x = x_labels, top = coefficients, width = 0.3)
        if self.type == 'html':
            output_file('correlation_'+self.f1+'_vs_'+self.f2+'.html')
        else:
            a = 'correlation_'+self.f1+'_vs_'+self.f2+".svg"
            plotting.output_backend = "svg"
            export_svgs(plotting, filename=a)
        save(plotting)

    def main(self):
        intervals = self.input()
        i = len(intervals)
        coefficients = []
        while i > 0:
            avg_points1, avg_points2, coef = self.averager_runner(intervals[i-1])
            coefficients.append(coef)
            print('Coefficient for '+str(intervals[i-1])+' second interval: '+str(coef))
            name = self.f1+'_vs_'+self.f2+'_'+str(intervals[i-1])+'s'
            self.avg_grapher.graph_main(avg_points1, avg_points2, self.error, name, self.type, 1)
            i -= 1
        self.coefficient_plot(intervals, coefficients)

pearson_run = correlation()
pearson_run.main()
