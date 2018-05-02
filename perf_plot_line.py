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
c = canvas(ctype, title=data_file, dimensions=['3.6in', '2.8in'])
d = drawable(canvas=c, xrange=[0,40], yrange=[-1,global_ymax],
            coord=[50,40]
            # dimensions=['3in','1.85in']
            )

# background: green, with a yellow vertical grid
#c.box(coord=[[0,0],[300,140]], fill=True, fillcolor='darkgreen', linewidth=0)
#grid(drawable=d, y=False, xrange=[90,101], xstep=1, linecolor='yellow',
 #    linedash=[2,2])

options = [('skip_list', 'diamond', 0.8, 'pink', True),
            ('cuckoo', 'triangle', 1, 'skyblue', True),
            #('prefix_hash', 'hline', 0.5, 'green', False),
            #('hash_linkedlist', 'xline', 0.5, 'purple',False),
            ('toss_async', 'star', 0.5, 'black',False),
            ('toss_sync', 'vline', 0.5, 'gray',False),
            ('toss_ccuck', 'vline', 0.5, 'red',False),
]

xm = []
#w='mrep="%s"' % "cuckoo"
w='mrep="%s"' % "skip_list"
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

for opt, symbstyle, linewidth, color, symbfill in options:
    w = 'mrep="%s"' % opt
    st = table(table=t, where=w)

    lineargs = {'drawable':d, 'table':st, 'xfield': 'line2', 'yfield': 'count',
				'linecolor':color, 'linewidth':linewidth, 'symbstyle': symbstyle,
				'symbfill':symbfill,
				#'linedash':linedash,
                'legendtext': opt,'legend' : L}

  #  p.verticalbars(**barargs)
    p.line(**lineargs)
	#p.line(**lineargs)

    L.draw (c, coord=[d.left() + 5, d.top() -6], style='right', skipnext=4, skipspace=45, fontsize=8, height=5, hspace=2)

c.render()
#
#
#call(["mv", _title + ".eps", "figure"])
call(["open", data_file + "." + ctype])

