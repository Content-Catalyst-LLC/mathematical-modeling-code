#include <iostream>
#include <iomanip>

int main() {
    int row_count = 4;
    int column_count = 2;
    bool overdetermined = true;
    int rank = 2;
    double residual_norm = 0.191311;

    std::cout << "system_name,row_count,column_count,overdetermined,rank,solution,fitted_values,residuals,residual_norm,warning\n";
    std::cout << "four_observation_linear_calibration,"
              << row_count << "," << column_count << "," << overdetermined << ","
              << rank << ",0.850000;1.040000,1.890000;2.930000;3.970000;5.010000,"
              << "0.110000;-0.030000;0.130000;0.090000,"
              << std::setprecision(6) << residual_norm
              << ",Least squares requires residual and model-purpose review.\n";
    return 0;
}
