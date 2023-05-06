/*
 * Tema 2 ASC
 * 2023 Spring
 */
#include "utils.h"


void free_matrix(double **matrix) {
	free(*matrix);
	*matrix = NULL;
}


double *get_transpose(double *matrix, int N) {

	double *T = (double*) malloc(N * N * sizeof(double));

	for (int i = 0; i < N; i++) {
		register double *t = T + i * N;
		register double *m = matrix + i;

		for (int j = 0; j < N; j++) {
			*t = *m;
			t++;
			m += N;

		}
	}

	return T;
}


/* A- Upper triangular matrix */
double *multiply_superior(double *A, double *B, int N) {

	double *M = (double *)calloc(N * N, sizeof(double));

	for (int i = 0; i < N; i++) {
		for (int k = i; k < N; k++) {
			register double *a = A + i * N + k;
			register double *b = B + k * N;
			register double *m = M + i * N;

			for (int j = 0; j < N; j++) {
				*m += *a * *b;
				m++;
				b++;
			}
		}
	}

	return M;
}

/* B - lower triangular matrix */
double *multiply_inferior(double *A, double *B, int N) {

	double *M = (double *)calloc(N * N, sizeof(double));

	for (int i = 0; i < N; i++) {
		for (int k = 0; k < N; k++) {
			register double *a = A + i * N + k;
			register double *b = B + k * N;
			register double *m = M + i * N;

			for (int j = 0; j <= k; j++) {
				*m += *a * *b;
				m++;
				b++;
			}
		}
	}

	return M;
}

double *multiply_normal(double *A, double *B, int N) {

	double *M = (double *)calloc(N * N, sizeof(double));

	for (int i = 0; i < N; i++) {
		for (int k = 0; k < N; k++) {
			register double *a = A + i * N + k;
			register double *b = B + k * N;
			register double *m = M + i * N;

			for (int j = 0; j < N; j++) {
				*m += *a * *b;
				m++;
				b++;
			}
		}
	}

	return M;
}


/*
 * Add your optimized implementation here
 */
double* my_solver(int N, double *A, double* B) {
	printf("OPT SOLVER\n");

	double *At = get_transpose(A, N);
	double *Bt = get_transpose(B, N);

	// Requested operation: C = A * B * At + Bt * Bt
	double *AB = multiply_superior(A, B, N);
	double *ABAt = multiply_inferior(AB, At, N);
	double *BtBt = multiply_normal(Bt, Bt, N);

	// Add the two matrices
	double *C = (double *)malloc(N * N * sizeof(double));
	for (int i = 0; i < N * N; i++) {
		C[i] = ABAt[i] + BtBt[i];
	}

	// Final step : free all auxiliar matrices used
	free_matrix(&At);
	free_matrix(&Bt);
	free_matrix(&AB);
	free_matrix(&ABAt);
	free_matrix(&BtBt);

	return C;	
}
