from zplot import *
import sys
from subprocess import call



def get_ymax(coll_list, t):
    ymax = 0

    for c in coll_list:
        ymax = ymax if t.getmax(c) < ymax else t.getmax(c)

    ymax = ymax + ymax * 0.3

    round_ymax = 0
    round_scale = 10 if ymax < 100 else 100

    while round_ymax < ymax:
        round_ymax += round_scale

    #print(round_ymax)

    return round_ymax

#data_file='memtable.hit.64.dat'

if len(sys.argv) < 3:
    print("./plot.py memtable.hit.dat")
    sys.exit()

#data_file='test.dat'
data_file=sys.argv[1]
print(data_file)

ctype = 'eps' #if len(sys.argv) < 2 else sys.argv[1]
#ctype = 'pdf'

t = table(file=data_file)
t.dump()
#ymax = round(get_ymax(['count'], t),-1)
ymax = get_ymax(['count'],t)

#global_ymax=int(sys.argv[2])
global_ymax=ymax
print(ymax)

#ymax=sys.argv[2]
c = canvas(ctype, title=data_file, dimensions=['2.5in', '1.85in'])
d = drawable(canvas=c, xrange=[0,42], yrange=[-1,global_ymax],
            #coord=[0,25]
            # dimensions=['3in','1.85in']
            )

# background: green, with a yellow vertical grid
#c.box(coord=[[0,0],[300,140]], fill=True, fillcolor='darkgreen', linewidth=0)
#grid(drawable=d, y=False, xrange=[90,101], xstep=1, linecolor='yellow',
 #    linedash=[2,2])

options = [('skip_list', 'solid', 0.5, 'pink'),
            ('cuckoo', 'dline1', 0.5, 'black'),
            ('prefix_hash', 'solid', 0.5, 'green'),
            ('hash_linkedlist', 'solid', 0.5, 'purple'),
            ('toss_async', 'solid', 0.5, 'blue'),
            ('toss_sync', 'solid', 0.5, 'skyblue'),
]

xm = []
w='mrep="%s"' % "cuckoo"
for x, y in t.query(select='thread,line', where=w):
    y = str(float(y) + 0.5)
    xm.append((x, y))

#ym = [ymax // 1000000,ymax]
ym = []
#ym.append((ymax // 1000 , global_ymax))
ym.append((global_ymax,global_ymax*1000))

axis(drawable=d, style='box',
#   xauto=[1,15,1],
    title=data_file,
    ytitle="IOPS",
	#ytitleshift=[20,0],
    xtitle="Threads",
    xmanual=xm,
    yauto=[0, ymax, ymax/5],
	ylabelfontsize=7,
#    ymanual=ym,
    domajortics=False,
    #xaxisposition=0,
    linewidth=0.5, xlabelfontsize=8.0, doxlabels=True,
    )
#xlabelformat='\'%s',
#   xlabelshift=[0,-30],linecolor='black', xlabelfontcolor='black')'
p = plotter()
L = legend()

for opt, ftype, fsize, color in options:
    w = 'mrep="%s"' % opt
    st = table(table=t, where=w)

	#if opt == "prefix_hash" :
		#opt="hash_skiplist"
    barargs = {'drawable':d, 'table':st, 'xfield': 'line', 'yfield': 'count',
                'fill': True, 'barwidth': 0.8, 'fillsize': fsize,
                'fillstyle': ftype, 'fillcolor': color,
                'legendtext': opt,'legend' : L}

    p.verticalbars(**barargs)

    L.draw (c, coord=[d.left() + 5, d.top() -6], style='right', skipnext=4, skipspace=45, fontsize=8, height=5, hspace=2)

c.render()
#
#
#call(["mv", _title + ".eps", "figure"])
call(["open", data_file + "." + ctype])

