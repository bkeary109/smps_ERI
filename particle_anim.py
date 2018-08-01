import numpy as np
import matplotlib
import matplotlib.pylab as plt
import datetime
import matplotlib.animation as animation
from matplotlib.ticker import FormatStrFormatter

smps_file = "2018_07_25_14_46_24_smps.txt"

plottime1 = "17:40"  ## Format: "HH:MM"
plottime2 = "19:45"  ## Format: "HH:MM"

part_sizes = np.genfromtxt(smps_file, delimiter = '\t', skip_header = 26, usecols = xrange(112,177))

size_list = []
num_row = 0
with open(smps_file) as f:
    for row in f:
        if num_row != 25:
            pass
        else:
            size_list.append(row.split('\t')[112:177])
        num_row = num_row + 1
size_list = np.asarray(size_list).astype('float')

time_list = []
num_row = 0
with open(smps_file) as f:
    for row in f:
        if num_row < 26:
            pass
        else:
            time_list.append(row.split('\t')[2])
        num_row = num_row + 1

time_len = np.shape(time_list)
new_time = []

for i in xrange(0,time_len[0]):
    val = time_list[i]
    x = datetime.datetime.strptime(val, '%H:%M:%S')
    new_time.append(x)

time_arr = np.asarray(new_time)

cleantime = []
for elem in time_arr:
    cleantime.append(elem.strftime('%H:%M'))
cleantime = np.asarray(cleantime)

time_len = np.shape(cleantime)[0]
for i in xrange(0, time_len):
    if cleantime[i] == plottime1:
	plotfirst = i
	break
for j in xrange(0, time_len):
    if cleantime[j] == plottime2:
	plotlast = j
	break


fig,ax = plt.subplots()
plt.xlim(40,430)
plt.xlabel('Diameter (nm)')
plt.ylabel('Concentration')

ax.set_xscale('log')
plt.tick_params(axis='x', which='both', length = 5)
ax.xaxis.set_minor_formatter(FormatStrFormatter("%d"))
ax.xaxis.set_major_formatter(FormatStrFormatter("%d"))
for tick in ax.xaxis.get_major_ticks():
    tick.label.set_fontsize(9)
for tick in ax.xaxis.get_minor_ticks():
    tick.label.set_fontsize(9)
plt.ticklabel_format(style='sci', axis = 'y', scilimits = (0,4))

imgs = []
for i in xrange(plotfirst,plotlast):
    img, = plt.plot(size_list[0], part_sizes[i,:], 'o', color = 'b')
    title = plt.text(250, 2.5E6, cleantime[i], fontsize = 20)
    imgs.append([img, title])

ani = animation.ArtistAnimation(fig, imgs, interval = 300, blit = True, repeat_delay = 2000)
plt.show()

ani.save("particlesize.html")
