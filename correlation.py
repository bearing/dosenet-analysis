#pearson correlation calculator and grapher

import numpy
from bokeh.plotting import figure, show, output_file, save
from bokeh.io import export_svgs

#data_avg.py: code to average data and graph averaged data
from data_avg import data_average, avg_graph

class correlation:
    def _init_(self):
        pass

    #initialize classes from data_avg.py
    data_avger = data_average()
    avg_grapher = avg_graph()

    def input(self): #to get input from users
        self.u1 = input('csv url1: ')
        self.csv1 = self.data_avger.get_csv(self.u1)
        self.c1 = int(input('column # for csv1: '))
        if len(self.csv1[0]) < self.c1:
            print('Error: column number')
            raise SystemExit(0)
        self.f1 = self.csv1[0][self.c1-1]
        self.u2 = input('csv url2: ')
        self.csv2 = self.data_avger.get_csv(self.u2)
        self.c2 = int(input('column # for csv2: '))
        if len(self.csv1[0]) < self.c1:
            print('Error: column number')
            raise SystemExit(0)
        self.f2 = self.csv2[0][self.c2-1]
        self.type = input('file type (svg/html): ')
        self.start = float(input('start (epoch): '))
        self.stop = float(input('stop: '))
        if self.stop < self.start:
            print('Error: stop time less than start time')
            raise SystemExit(0)
        self.error = input('error? (Y/N): ')
        interval_input = input('comma separated integer intervals in secs: ')
        interval_input = interval_input.strip(' ')
        str_intervals = interval_input.split(',')
        intervals = [int(i) for i in str_intervals]
        intervals = sorted(intervals)
        return intervals

    def pearson_calc(self, x, y): #actual correlation calculator
        a = numpy.average(x)
        b = numpy.average(y)
        X = numpy.sum([(i - a)**2 for i in x])
        Y = numpy.sum([(i - b)**2 for i in y])
        XY = numpy.sum([(i - a)*(j - b) for i,j in zip(x,y)])
        coefficient = XY/(X*Y)**0.5
        return coefficient

    def averager_runner(self, interval): #runs the averager class from data_avg.py and pearson_calc function
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

    def coefficient_plot(self, intervals, coefficients): #plots correlation coefficents based on interval of averaging
        x_labels = [str(i) for i in intervals] #x-axis labels
        coefficients.reverse() #reverse order of coefficients in list to match up with labels
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
        intervals = self.input() #receives input
        i = len(intervals)
        coefficients = []
        while i > 0: #run through averagers and graphers for each interval
            avg_points1, avg_points2, coef = self.averager_runner(intervals[i-1])
            coefficients.append(coef)
            print('Coefficient for '+str(intervals[i-1])+' second interval: '+str(coef))
            name = self.f1+'_vs_'+self.f2+'_'+str(intervals[i-1])+'s'
            #graph data v data plots by using graph_main method
            self.avg_grapher.graph_main(avg_points1, avg_points2, self.error, name, self.type, 1, [name, self.f1, self.f2], coef)
            i -= 1
        self.coefficient_plot(intervals, coefficients)

pearson_run = correlation()
pearson_run.main()
