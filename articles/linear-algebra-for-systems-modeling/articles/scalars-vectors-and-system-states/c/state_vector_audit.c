#include <math.h>
#include <stdio.h>

double determinant_2x2(double a, double b, double c, double d) {
    return a * d - b * c;
}

int main(void) {
    double a = 0.80, b = 0.15, c = 0.20, d = 0.90;
    double trace = a + d;
    double det = determinant_2x2(a, b, c, d);
    double disc = trace * trace - 4.0 * det;
    double root = sqrt(disc);
    double lambda1 = (trace + root) / 2.0;
    double lambda2 = (trace - root) / 2.0;
    double dominant = fabs(lambda1) > fabs(lambda2) ? fabs(lambda1) : fabs(lambda2);
    printf("model_name,rank,determinant,dominant_eigenvalue,warning\n");
    printf("two_component_transition_model,2,%.6f,%.6f,Matrix interpretation depends on entry meaning and scale.\n", det, dominant);
    return 0;
}
