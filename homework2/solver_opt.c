/*
 * Tema 2 ASC
 * 2023 Spring
 */
#include "utils.h"


void free_matrix(double **matrix) {
	free(*matrix);
	*matrix = NULL;
}

void print_matrix(double *matrix, int N) {
	for (int i = 0; i != N; i++) {
		for (int j = 0; j != N; j++) {
			printf("%lf ", matrix[i * N + j]);
		}
		printf("\n");
	}
	printf("\n");
}

double *get_transpose(double *matrix, int N) {

	double *T = (double*) malloc(N * N * sizeof(double));

	for (int i = 0; i != N; i++) {
		register double *t = T + i * N;
		register double *m = matrix + i;

		for (int j = 0; j < N; j++) {
			// t[i * N + j] = matrix[j * N + i];

			*t = *m;
			t++;
			m += N;

		}
	}

	return T;
}


/* A superior triunghiulara */
double *multiply_superior(double *A, double *B, int N) {

	double *M = (double *)calloc(N * N, sizeof(double));
	for (int i = 0; i != N; i++) {
		for (int k = i; k != N; k++) {
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

/* B inferior triunghiulara */
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
	for (int i = 0; i != N; i++) {
		for (int k = 0; k != N; k++) {
			register double *a = A + i * N + k;
			register double *b = B + k * N;
			register double *m = M + i * N;

			for (int j = 0; j != N; j++) {
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

	// C = A * B * At + Bt * Bt
	double *AB = multiply_superior(A, B, N);
	double *ABAt = multiply_inferior(AB, At, N);
	double *BtBt = multiply_normal(Bt, Bt, N);

	// Add the two matrices
	double *C = (double *)malloc(N * N * sizeof(double));
	for (int i = 0; i != N * N; i++) {
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


/*
	TODO: delete main
*/

// int main() {

// 	int N = 3;

// 	double A1[3][3] = {{1.0, 2.0, 3.0}, {0.0, 4.0, 5.0}, {0.0, 0.0, 6.0}};
// 	double B1[3][3] = {{1.0, 2.0, 3.0}, {4.0, 5.0, 6.0}, {7.0, 8.0, 9.0}};


// 	double *A = &A1[0][0];
// 	double *B = &B1[0][0];


// 	double *C = my_solver(N, A, B);
// 	if (C == NULL) {
// 		printf("C is NULL\n");
// 	} else {
// 		print_matrix(C, N);
// 		free(C);
// 	}

// 	return 0;
// }