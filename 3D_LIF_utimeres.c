#include <stdio.h>
#include <stdlib.h>
#include <omp.h>
#include <string.h>

#define PI 3.1415926535897

int dim_x=256,dim_z;
const double mu=1;

typedef struct node {
	short int x,y,z;
	float sigma;
	struct node * next;
} node_t;

void push(node_t ** head, node_t A) {
	node_t * new_node;
	new_node = malloc(sizeof(node_t));

	new_node->x = A.x;
	new_node->y = A.y;
	new_node->z = A.z;
	new_node->sigma=A.sigma;
	new_node->next = *head;
	*head = new_node;
}


double *LIF(double *U, double *U_, node_t **ConMatrix)
{
	int i;
	node_t *A;
	#pragma omp parallel for private(i,A) 
	for(i=0; i<dim_x*dim_x*dim_z; i++)
	{
		A=ConMatrix[i];
		if(A==NULL)
			U_[i]=0;
		else
		{
			double S=0;
			double count=0;
			while(A!=NULL)
			{
				S+=A->sigma*(U[A->x*dim_x*dim_z + A->y*dim_z + A->z]-U[i]);
				count++;
				A=A->next;
			}
			U_[i]=mu-U[i]-1.0/count*S;
		}
	}
	return U_;
}

int main(int argc, char** argv)
{
	if(argc!=5)
	{
		printf("Wrong Input!\nUsage: ./3d_LIF input_file z_dimention seed output_directory\n");
		exit(1);
	}
	dim_z=atoi(argv[2]);
	const double u_th=0.98;
	node_t **ConMatrix=malloc(dim_x*dim_x*dim_z*sizeof(node_t));
	FILE *fp,*fout;
	fp=fopen(argv[1],"r"); 
	short int i,j,k,r;
	int tt=0;

        char str[100];
	sprintf(str,"./%s_%d/data/%05d.dat",argv[4],atoi(argv[3]),tt);
        fout=fopen(str,"w");
	//CONECTIVITY MATRIX SETUP
	printf(".\n");
	for(i=0;i<dim_x;i++)
	{
		for(j=0;j<dim_x;j++)
		{
			for(k=0;k<dim_z;k++)
			{
				ConMatrix[i*dim_x*dim_z + j*dim_z + k]=NULL;
			}
		}
	}
	printf(".\n");
	r=1;
	while(r>0)
	{
		node_t A;
		r=fscanf(fp, "%hd", &i);
		r=fscanf(fp, "%hd", &j);
		r=fscanf(fp, "%hd", &k);
		r=fscanf(fp, "%hd", &A.x);
		r=fscanf(fp, "%hd", &A.y);
		r=fscanf(fp, "%hd", &A.z);
		r=fscanf(fp, "%f",&A.sigma);
		push(&ConMatrix[i*dim_x*dim_z + j*dim_z + k],A);       
	}
	printf("Initialization Completed.\n");
	//INITIALIZATION OF U	
	double *U,*U_,dt=0.01;
	int *Omega;
	U=malloc(dim_x*dim_x*dim_z*sizeof(double));
	Omega=malloc(dim_x*dim_x*dim_z*sizeof(int));

	srand(atoi(argv[3]));
	for(i=0;i<dim_x;i++)
	{
		for(j=0;j<dim_x;j++)
		{
			for(k=0;k<dim_z;k++)
			{
				if (ConMatrix[i*dim_x*dim_z + j*dim_z + k]!=NULL)
					U[i*dim_x*dim_z + j*dim_z + k]=0.98*rand()/RAND_MAX;
				else
					U[i*dim_x*dim_z + j*dim_z + k]=-1;
				Omega[i*dim_x*dim_z + j*dim_z + k]=0;
			}
		}
	}
	//MAIN PROGRAM
	U_=malloc(dim_x*dim_x*dim_z*sizeof(double));
	
	for(tt=0;tt<=10000;tt++)
	{
		U_=LIF(U,U_,ConMatrix);
		#pragma omp parallel for private(i,j,k)
		for(i=0;i<dim_x;i++) //loop unrolling like LIF()
		{
			for(j=0;j<dim_x;j++)
			{
				for(k=0;k<dim_z;k++)
				{
					U[i*dim_x*dim_z + j*dim_z + k]+=dt*U_[i*dim_x*dim_z + j*dim_z + k];
					if (U[i*dim_x*dim_z + j*dim_z + k]>=u_th)
					{
						U[i*dim_x*dim_z + j*dim_z + k]=0;
						if (tt>=1000) Omega[i*dim_x*dim_z + j*dim_z + k]+=1;
					}
				}
			}
		}
		if(tt>9000)
		{
			if (fout!=NULL) fclose(fout);
			char str[100];
			sprintf(str,"./%s_%d/data/%05d.dat",argv[4],atoi(argv[3]),tt);
			fout=fopen(str,"w");
			for(i=0;i<dim_x;i++)
			{
				for(j=0;j<dim_x;j++)
				{
					for(k=0;k<dim_z;k++)
					{
						if(U[i*dim_x*dim_z + j*dim_z + k]!=-1)
							fprintf(fout,"%d\t%d\t%d\t%lf\t%lf\n",i,j,k,U[i*dim_x*dim_z + j*dim_z + k],Omega[i*dim_x*dim_z + j*dim_z + k]*2.0*PI/(tt/100.0-10.0));
					}
				}
			}
		}
	}
	printf("%s DONE\n",argv[4]);
	return 0;
}
