#include <stdio.h>

int main(void) {
    double a = 120.0, b = 1.5, da = 4.0, db = 0.03;
    double ca = da * b;
    double cb = a * db;
    printf("contribution_from_a=%f\n", ca);
    printf("contribution_from_b=%f\n", cb);
    printf("total_derivative=%f\n", ca + cb);
    return 0;
}
