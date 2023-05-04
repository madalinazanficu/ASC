#include <stdio.h>
#include <stdlib.h>

void free_matrix(double **matrix) {
	free(*matrix);
	*matrix = NULL;
}

void print_matrix(double *matrix, int N) {
	for (int i = 0; i < N; i++) {
		for (int j = 0; j < N; j++) {
			printf("%lf ", matrix[i * N + j]);
		}
		printf("\n");
	}
	printf("\n");
}