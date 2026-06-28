#include <stdio.h>
#include <math.h>

double determinant3x3(double m[3][3]) {
    return m[0][0]*(m[1][1]*m[2][2] - m[1][2]*m[2][1])
         - m[0][1]*(m[1][0]*m[2][2] - m[1][2]*m[2][0])
         + m[0][2]*(m[1][0]*m[2][1] - m[1][1]*m[2][0]);
}

int main(void) {
    double matrix[3][3] = {
        {1.0, 0.0, 0.5},
        {0.0, 1.0, 0.5},
        {0.0, 0.0, 1.0}
    };

    double det = determinant3x3(matrix);
    int rank = fabs(det) > 1e-10 ? 3 : 2;
    int ambient_dimension = 3;
    int vector_count = 3;
    int spans = rank == ambient_dimension ? 1 : 0;
    int independent = rank == vector_count ? 1 : 0;
    int basis = spans && independent;

    printf("vector_set_name,ambient_dimension,vector_count,rank,spans_ambient_space,linearly_independent,is_basis_for_ambient_space,warning\n");
    printf("candidate_system_basis,3,3,%d,%d,%d,%d,A basis claim is mathematical not proof of real-world adequacy.\n", rank, spans, independent, basis);
    return 0;
}
