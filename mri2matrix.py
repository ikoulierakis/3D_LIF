import cv2
import sys 
import os
import numpy as np

N=int(sys.argv[4])
sigma_max=float(sys.argv[3])
print(sigma_max)
dim_z=int(sys.argv[2])
dir=sys.argv[1]
images=os.listdir(dir)
os.chdir(dir)
matrix=np.empty([256,256,int(sys.argv[2])])
for im in images:
	image_np=cv2.imread(im,0)
	index= int(im.replace('.png','').split('-')[1])
	if index<=dim_z: matrix[:,:,index-1]=image_np/255.0
mean=np.mean([ h for h in matrix.reshape(256*256*dim_z,1) if h>0])
matrix=matrix/mean*sigma_max
mean=np.mean([ h for h in matrix.reshape(256*256*dim_z,1) if h>0])
print(mean)
with open(dir[:-1]+'_'+str(N)+'_'+str(sigma_max)+'.dat','w') as f:
	for i in range(256):
		print("\r>> i={}".format(i),end='')
		for j in range(256):
			for k in range(dim_z):		
				if k<dim_z-1 and matrix[i,j,k]>=0.01:
					if matrix[i,j,k+1]>=0.01: 
						line=str(i)+'\t'
						line=line+str(j)+'\t'
						line=line+str(k)+'\t'
						line=line+str(i)+'\t'
						line=line+str(j)+'\t'
						line=line+str(k+1)+'\t'    
						line=line+'%.10f'%(matrix[i,j,k]*matrix[i,j,k+1])+'\n'
						f.write(line)

				if k>0 and matrix[i,j,k]>=0.001:
					if matrix[l,m,k-1]>=0.01: 
						line=str(i)+'\t'
						line=line+str(j)+'\t'
						line=line+str(k)+'\t'
						line=line+str(i)+'\t'
						line=line+str(j)+'\t'
						line=line+str(k-1)+'\t'    
						line=line+'%.10f'%(matrix[i,j,k]*matrix[i,j,k-1])+'\n'
						f.write(line)

				for l in range(max(0,i-N),min(i+N+1,256)):
					for m in range(max(0,j-N),min(j+N+1,256)):			
						#for n in range(max(0,k-int(N/5)),min(k+int(N/5)+1,dim_z)):
						if matrix[i,j,k]>=0.001:
							if matrix[l,m,k]>=0.01 and (i!=l or j!=m): 
								line=str(i)+'\t'
								line=line+str(j)+'\t'
								line=line+str(k)+'\t'
								line=line+str(l)+'\t'
								line=line+str(m)+'\t'
								line=line+str(k)+'\t'    
								line=line+'%.10f'%(matrix[i,j,k]*matrix[l,m,k])+'\n'
								f.write(line)
print('')
