#pearson correlation

import numpy
from bokeh.plotting import figure, show, output_file, save
from bokeh.io import export_svgs

#data_avg.py: code to average data and graph averaged data
from data_avg import data_average, avg_graph

class pearson:
    def _init_(self):
        pass

    data_avger = data_average()
    avg_grapher = avg_graph()

    def input(self):
        self.u1 = 'https://radwatch.berkeley.edu/sites/default/files/dosenet/etch_roof.csv' #input('csv url1: ')
        self.c1 = 4 #int(input('column # for csv1: '))
        self.f1 = self.data_avger.get_csv(self.u1)[0][self.c1-1]
        self.u2 = 'https://radwatch.berkeley.edu/sites/default/files/dosenet/etch_roof_adc.csv' #input('csv url2: ')
        self.c2 = 4 #int(input('column # for csv2: '))
        self.f2 = self.data_avger.get_csv(self.u2)[0][self.c2-1]
        self.type = 'html' #input('file type (svg/html): ')
        self.start = 1525337415 #float(input('start (epoch): '))
        self.stop = 1525368315 #float(input('stop: '))
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
        print('coefficient')
        print(coefficient)
        return coefficient

    def averager_runner(self, interval):
        self.points1 = self.data_avger.avg_main(self.csv1, self.start, self.stop, interval, self.c1)
        self.points2 = self.data_avger.avg_main(self.csv2, self.start, self.stop, interval, self.c2)
        print('avged')
        self.points1, self.points2 = self.avg_grapher.data_align(self.points1, self.points2)
        r = self.pearson_calc(self.points1[1], self.points2[1])
        return r

    def main(self):
        intervals = self.input()
        i = len(intervals)
        coefficients = []
        self.csv1 = self.data_avger.get_csv(self.u1)
        self.csv2 = self.data_avger.get_csv(self.u2)
        while i > 0:
            coef = self.averager_runner(intervals[i-1])
            coefficients.append(coef)
            name = self.f1+'_vs_'+self.f2+'_'+str(intervals[i-1])+'s'
            self.avg_grapher.graph(self.points1, self.points2, self.error, name, self.type, 1)
            i -= 1
        print('main: almost done')
        x_labels = [str(i) for i in intervals]
        plot = figure(plot_width = 1000, plot_height = 1000, x_range = x_labels, tools="pan,wheel_zoom,box_zoom,reset")
        plot.vbar(x = x_labels, top = coefficients, width = 0.7)
        show(plot)
        if self.type == 'html':
            output_file('correlation_'+self.f1+'_vs_'+self.f2+'.html')
        else:
            a = 'correlation_'+self.f1+'_vs_'+self.f2+".svg"
            plot.output_backend = "svg"
            export_svgs(plot, filename=a)
        save(plot)

pearson_run = pearson()
pearson_run.main()
#k = self.data_avger.avg_main('https://radwatch.berkeley.edu/sites/default/files/dosenet/etch_roof.csv', 1525337415, 1525368315, 100, 4)
#j = self.data_avger.avg_main('https://radwatch.berkeley.edu/sites/default/files/dosenet/etch_roof_adc.csv', 1525337415, 1525368315, 100, 4)
