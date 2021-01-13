import sys
import os
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import random

fig,ax= plt.subplots(3,5,figsize=(15,10))

x=[]
y=[]
u=[]

start = int(sys.argv[1].replace('.png',''))
i = 0
for fnum in range(start,start+280,20):
	fname = str(fnum)+'.dat'
	
	sequence_containing_x_vals=[]
	sequence_containing_y_vals=[]
	sequence_containing_z_vals=[]
	sequence_containing_u_vals=[]
	
	with open('data/'+fname) as fin:            
		print(fname)
		for line in fin.readlines():
			line=line.split()
			if line[2]=='18':
				x.append(255-int(line[0]))
				y.append(int(line[1]))
				u.append(float(line[3]))
	im=ax[int(i/5)][i%5].scatter(y,x,s=1.5,c=u,cmap='hot',vmin=0, vmax=1,marker='s',linewidths=0)
	ax[int(i/5)][i%5].set_title('t = '+str(fnum/100)+' t.u.')
	ax[int(i/5)][i%5].tick_params('both',labelsize=14)
	ax[int(i/5)][i%5].set_xlim(25,250)
	ax[int(i/5)][i%5].set_xticks(np.arange(50, 251, 100))
	ax[int(i/5)][i%5].set_ylim(25,250)
	ax[int(i/5)][i%5].set_yticks(np.arange(50, 251, 100))

	fontsize1=18
	ax[int(i/5)][i%5].set_xlabel('i',fontsize=fontsize1)
	ax[int(i/5)][i%5].set_ylabel('j',fontsize=fontsize1)
	ax[int(i/5)][i%5].label_outer()

	#ax[int(i/5)][i%5].arrow(224,250,-50,-50, head_width=10, head_length=10, fc='k', ec='k')

	ax[int(i/5)][i%5].set_aspect('equal')
	i+=1

fontsize=18
cbar_ax = fig.add_axes([0.1, 0.95, 0.8, 0.02])
fig.colorbar(im, cax=cbar_ax, orientation='horizontal')
cbar_ax.tick_params(labelsize=16) 
cbar_ax.xaxis.set_label_position('top')
cbar_ax.set_xlabel("$u_{ij19}$",labelpad=10,fontsize=fontsize)

ax[-1, -1].axis('off')
plt.savefig('grid_view.png')
plt.close(fig)
