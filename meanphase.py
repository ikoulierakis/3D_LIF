import cv2
import numpy as np
import os
import sys
import matplotlib.pyplot as plt
import imutils
from matplotlib.ticker import FormatStrFormatter


fig,ax= plt.subplots(1,2)

x=[]
y=[]
u=[]
cut_level=170

with open(sys.argv[1]) as fin:
    for line in fin.readlines():
        line=line.split()
        if line[2]=='18':
            x.append(255-int(line[0]))
            y.append(int(line[1]))
            u.append(float(line[4]))
im=ax[0].scatter(y,x,s=0.5,c=u,cmap='copper',marker='s',linewidths=0)
ax[0].plot([0,255], [cut_level,cut_level], 'k--', lw=0.3)

ax[0].arrow(50,30,50,50, head_width=10, head_length=10, fc='g', ec='g')

y1=[]
u1=[]
t=[]
for tt in range(80020,85001,20):
    print("\r{}".format(tt),end='')
    x=[]
    y=[]
    u=[]
    with open('data/'+str(tt)+'.dat','r') as fin:
        for line in fin.readlines():
            line=line.split()
            if line[2]=='18':
                x.append(255-int(line[0]))
                y.append(int(line[1]))
                u.append(float(line[3]))
        y1.append([y[i] for i in range(len(y)) if x[i]==cut_level])
        u1.append([u[i] for i in range(len(y)) if x[i]==cut_level])
        t.append([tt/100]*len(y1[0]))
im1=ax[1].scatter(y1,t,s=2,c=u1,cmap='plasma',marker='s',linewidths=0)
ax[0].set_xlabel('i',fontsize=16)
ax[0].set_ylabel('j',fontsize=16)
ax[0].set_xlim(50,255)
ax[0].set_xlim(25,250)
ax[0].label_outer()
ax[1].set_xlabel('i',fontsize=16)
ax[1].set_ylabel('time',fontsize=16,labelpad=-20)
ax[1].set_yticks([800,850])
fig.subplots_adjust(right=0.98,left=0.12)

cbar_ax = fig.add_axes([0.10, 0.85, 0.4, 0.05])
fig.colorbar(im, orientation='horizontal',cax=cbar_ax)
cbar_ax.xaxis.set_label_position('top')
cbar_ax.set_xlabel("$\omega_{i,j,19}$",labelpad=10,fontsize=16)

cbar_ax1 = fig.add_axes([0.60, 0.85, 0.35, 0.05])
fig.colorbar(im1, orientation='horizontal',cax=cbar_ax1)
cbar_ax1.xaxis.set_label_position('top')
cbar_ax1.set_xlabel("$u_{i,175,19}$",labelpad=10,fontsize=16)

ax[0].set_aspect('equal', 'box')
ax[1].set_aspect(1./ax[1].get_data_ratio())

plt.sca(ax[1])
#plt.yticks([min(u1),max(u1)])
plt.sca(ax[0])
plt.xlim([0,255])
plt.ylim([0,255])

label_pos=840
ax[0].text(-70,200,'a)',fontsize=18,fontweight='bold')
ax[1].text(40,label_pos,'b)',fontsize=18,fontweight='bold')
ax[1].set_ylim([800, 850])
#ax[1].yaxis.set_major_formatter(FormatStrFormatter('%.2f'))

#fig.tight_layout()

plt.savefig('lif_meanphase_slices_layer18.png')
plt.show()
