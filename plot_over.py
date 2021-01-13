import sys
import os
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import random

os.system('mkdir -p over_view/')
ls_files=os.listdir('data/')

for fname in sys.argv[1:]:
	sequence_containing_x_vals=[]
	sequence_containing_y_vals=[]
	sequence_containing_z_vals=[]
	sequence_containing_u_vals=[]

	with open('data/'+fname) as fin:            
		print(fname)
		fig = plt.figure()
		ax = plt.axes()
		# ax.view_init(90,90)

		ax.set_xlim(left=0,right=250)
		ax.set_ylim(bottom=0,top=250)

		plt.title('t='+str(int(fname.replace('.dat',''))/100)+' t.u.')
		x=[]
		y=[]
		u=[]
		for line in fin.readlines():
			line=line.split()
			if line[2]=='18':
				x.append(255-int(line[0]))
				y.append(int(line[1]))
				u.append(float(line[3]))
		im=ax.scatter(y,x,s=1.4,c=u,cmap='hot',vmin=0, vmax=1,marker='s',linewidths=0)
		fig.colorbar(im,ax=ax)
		plt.savefig('over_view/'+fname.replace('.dat','.png'))
		plt.close(fig)
		ax.cla()
