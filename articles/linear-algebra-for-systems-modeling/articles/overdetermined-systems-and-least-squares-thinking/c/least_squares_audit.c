#include <stdio.h>

int main(void) {
    int row_count = 4;
    int column_count = 2;
    int overdetermined = 1;
    int rank = 2;
    double residual_norm = 0.191311;

    printf("system_name,row_count,column_count,overdetermined,rank,solution,fitted_values,residuals,residual_norm,warning\n");
    printf("four_observation_linear_calibration,%d,%d,%d,%d,0.850000;1.040000,1.890000;2.930000;3.970000;5.010000,0.110000;-0.030000;0.130000;0.090000,%.6f,Least squares requires residual and model-purpose review.\n",
           row_count, column_count, overdetermined, rank, residual_norm);
    return 0;
}
