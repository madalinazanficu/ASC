// TODO
// Inumtirea matricelor

#include <math.h>
#include <stddef.h>
#include <stdio.h>
#include <stdint.h>     // provides int8_t, uint8_t, int16_t etc.
#include <stdlib.h>
#include <sys/time.h>

#define N 1500
double a[N][N], b[N][N], c[N][N];

int main(int argc, char* argv[])
{
    
    int i,j,k;
    int bi;
    int bj;
    int bk;
    int blockSize=50; 
    struct timeval start, end;
    float elapsed;

    if(argc > 2)
    {
        printf("apelati cu %s <n>\n", argv[0]);
        return -1;
    }
    if(argc == 2)
        blockSize = atoi(argv[1]);

    srand (0); //to repeat experiment
    //srand ( time ( NULL)); // if you want random seed


    //reset c matrix and initialize a and b matrix
    for (i=0;i<N;i++){
        for (j=0;j<N;j++){
            c[i][j] = 0.0;
            a[i][j] = (double)rand()/RAND_MAX*2.0-1.0; //double in range -1 to 1
            b[i][j] = (double)rand()/RAND_MAX*2.0-1.0; //double in range -1 to 1
        }
    }
    
    gettimeofday(&start, NULL);
    
    // TODO: implementati i-k-j folosind optimizari
    for(i=0; i<N; i++) {
        double *orig_pa = &a[i][0];
        for(k=0; k<N; k++) {
            double *pa = orig_pa;
            double *pb = &b[k][0];
            for(j=0; j<N; j++) {
                //c[i][j] += a[i][k]*b[k][j];
                c[i][j] += *pa * *pb;
                pa++;
                pb++;
            }
        }
    }

    gettimeofday(&end, NULL);

    elapsed = ((end.tv_sec - start.tv_sec)*1000000.0f + end.tv_usec - start.tv_usec)/1000000.0f;

    printf("TIME (i-k-j optimize): %12f\n", elapsed);
    return 0;
}

