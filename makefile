CC = gcc
#The -Ofast might not work with older versions of gcc; in that case, use -O2
CFLAGS = -lm -pthread -march=native -Wall -funroll-loops -Ofast -Wno-unused-result
#CFLAGS = -lm -pthread -march=native -Wall -funroll-loops -Ofast -Wno-unused-result -DDEBUG

all: bivec

bivec : bivec.c
	$(CC) bivec.c -o bivec $(CFLAGS)

clean:
	rm -rf bivec
