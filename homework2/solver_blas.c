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

/* 
 * Add your BLAS implementation here
 */
double* my_solver(int N, double *A, double *B) {
	printf("BLAS SOLVER\n");

	// Requested operation: C = A * B * At + Bt * Bt
	double alpha = 1.0;
	double beta = 1.0;

	// AB = A * B
	double *AB = calloc(N * N, sizeof(double));
	for (int i = 0; i < N * N; i++) {
		AB[i] = B[i];
	}

	cblas_dtrmm(CblasRowMajor, CblasLeft, CblasUpper, CblasNoTrans,
					CblasNonUnit, N, N, alpha, A, N, AB, N);

	// ABAt devine AB = AB * At
	cblas_dtrmm(CblasRowMajor, CblasRight, CblasUpper, CblasTrans,
					CblasNonUnit, N, N, alpha, A, N, AB, N);

	// BtBt = Bt * Bt
	double *BtBt = calloc(N * N, sizeof(double));
	cblas_dgemm(CblasRowMajor, CblasTrans, CblasTrans,
					N, N, N, alpha, B, N, B, N, beta, BtBt, N);

	// C devine AB = AB + BtBt
	cblas_daxpy(N * N, alpha, BtBt, 1, AB, 1);

	free_matrix(&BtBt);

	return AB;
}
