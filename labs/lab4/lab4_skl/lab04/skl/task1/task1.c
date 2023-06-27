#include <math.h>
#include <stddef.h>
#include <stdio.h>
#include <stdint.h>     // provides int8_t, uint8_t, int16_t etc.
#include <stdlib.h>

struct particle
{
    int8_t v_x, v_y, v_z;
};

int main(int argc, char* argv[])
{
    if(argc < 2)
    {
        printf("apelati cu %s <n>\n", argv[0]);
        return -1;
    }

    long n = atol(argv[1]);

    // TODO
    // alocati dinamic o matrice de n x n elemente de tip struct particle
    // verificati daca operatia a reusit
    struct particle *vect = (struct particle*)malloc(n * n * sizeof(struct particle));
    if (vect == NULL) {
        printf("Alocarea nu a reusit\n");
        return -1;
    }
  

    // TODO
    // populati matricea alocata astfel:
    // *liniile pare contin particule cu toate componentele vitezei pozitive
    //   -> folositi modulo 128 pentru a limita rezultatului lui rand()
    // *liniile impare contin particule cu toate componentele vitezi negative
    //   -> folositi modulo 129 pentru a limita rezultatului lui rand()
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            if (i % 2 == 0) {
                vect[i * n + j].v_x = rand() % 128;
                vect[i * n + j].v_y = rand() % 128;
                vect[i * n + j].v_z = rand() % 128;
            }
            else {
                vect[i * n + j].v_x = -rand() % 129;
                vect[i * n + j].v_y = -rand() % 129;
                vect[i * n + j].v_z = -rand() % 129;
            }
        }
    }

    // TODO
    // scalati vitezele tuturor particulelor cu 0.5
    //   -> folositi un cast la int8_t* pentru a parcurge vitezele fara
    //      a fi nevoie sa accesati individual componentele v_x, v_y, si v_z
    for (int i = 0; i < n * n; i++) {
        int8_t* v = (int8_t*)&vect[i];
        for (int j = 0; j < 3; j++) {
            v[j] = v[j] / 2;
        }
    }

    // compute max particle speed
    float max_speed = 0.0f;
    for(long i = 0; i < n * n; ++i)
    {
        float speed = sqrt(vect[i].v_x * vect[i].v_x +
                           vect[i].v_y * vect[i].v_y +
                           vect[i].v_z * vect[i].v_z);
        if(max_speed < speed) max_speed = speed;
    }

    // print result
    printf("viteza maxima este: %f\n", max_speed);

    free(vect);

    return 0;
}

