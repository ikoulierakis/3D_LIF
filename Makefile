CC = gcc
CFLAG="-O3 -march=native -openmp"

all: 3D_LIF 3D_LIF_utimeres

lif: 3D_LIF.c
	$(CC) $(CFLAG) $< $(LDFLAGS) -o $@
utimeres:
	$(CC) $(CFLAG) $< $(LDFLAGS) -o $@

clean:
	rm -f 3D_LIF 3D_LIF_utimeres
