#include <math.h>
#include <stdio.h>
#include <stdlib.h>

double smooth_response(double x) {
    return exp(0.2 * x);
}

double kink_response(double x) {
    return fabs(x);
}

double forward_difference(double (*f)(double), double x, double h) {
    return (f(x + h) - f(x)) / h;
}

double backward_difference(double (*f)(double), double x, double h) {
    return (f(x) - f(x - h)) / h;
}

double central_difference(double (*f)(double), double x, double h) {
    return (f(x + h) - f(x - h)) / (2.0 * h);
}

void emit(const char *name, double (*f)(double), double x0) {
    double h_values[] = {1.0, 0.5, 0.25, 0.125, 0.0625};
    for (int i = 0; i < 5; ++i) {
        double h = h_values[i];
        double fwd = forward_difference(f, x0, h);
        double bwd = backward_difference(f, x0, h);
        double cen = central_difference(f, x0, h);
        double gap = fabs(fwd - bwd);
        const char *flag = gap > 0.5 ? "true" : "false";
        printf("%s,%.6f,%.6f,%.12f,%.12f,%.12f,%.12f,%s\n", name, x0, h, fwd, bwd, cen, gap, flag);
    }
}

int main(void) {
    printf("function_name,x0,h,forward,backward,central,one_sided_gap,kink_flag\n");
    emit("smooth_exp_response", smooth_response, 5.0);
    emit("kink_abs_response", kink_response, 0.0);
    return EXIT_SUCCESS;
}
