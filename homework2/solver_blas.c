/*
 * Tema 2 ASC
 * 2023 Spring
 */
#include "utils.h"
#include <cblas.h>


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

/* 
 * Add your BLAS implementation here
 */
double* my_solver(int N, double *A, double *B) {
	printf("BLAS SOLVER\n");

	// Requested operation: C = A * B * At + Bt * Bt

	double alpha = 1;
	double beta = 1;

	// AB = A * B
	double *AB = malloc(N * N * sizeof(double));
	for (int i = 0; i < N * N; i++) {
		AB[i] = B[i];
	}

	blas_dtrmm(CblasLeft, CblasUpper, CblasNoTrans, CblasNonUnit, N, N, alpha, A, N, beta, AB);

	// ABAt devine AB = AB * At
	blas_dtrmm(CblasRight, CblasLower, CblasTrans, CblasNonUnit, N, N, alpha, A, N, beta, AB);

	// BtBt = Bt * Bt
	double *BtBt = malloc(N * N * sizeof(double));
	blas_dgemm(CblasTrans, CblasTrans, N, N, N, alpha, B, N, B, N, beta, BtBt, N);


	// ABAt + BtBt
	double *C = malloc(N * N * sizeof(double));
	for (int i = 0; i < N; i++) {
		for (int j = 0; j < N; j++) {
			C[i * N + j] = AB[i * N + j] + BtBt[i * N + j];
		}
	}

	free_matrix(&AB);
	free_matrix(&BtBt);

	return C;
}

/*
	TODO: delete main
*/

int main() {

	int N = 3;

	double A1[3][3] = {{1.0, 2.0, 3.0}, {0.0, 4.0, 5.0}, {0.0, 0.0, 6.0}};
	double B1[3][3] = {{1.0, 2.0, 3.0}, {4.0, 5.0, 6.0}, {7.0, 8.0, 9.0}};


	double *A = &A1[0][0];
	double *B = &B1[0][0];


	double *C = my_solver(N, A, B);
	if (C == NULL) {
		printf("C is NULL\n");
	} else {
		print_matrix(C, N);
		free(C);
	}

	return 0;
}
