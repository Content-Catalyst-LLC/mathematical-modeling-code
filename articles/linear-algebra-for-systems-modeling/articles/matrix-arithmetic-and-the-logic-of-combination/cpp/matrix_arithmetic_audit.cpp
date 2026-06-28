#include <iostream>

int main() {
    bool compatible_shape = true;
    double output_entry_sum = 3.95;

    std::cout << "operation_name,matrix_shape,compatible_shape,output_entry_sum,warning\n";
    std::cout << "baseline_plus_weighted_intervention_and_stress,3x3,"
              << compatible_shape << "," << output_entry_sum
              << ",Shape compatibility is not enough; semantic compatibility must be documented.\n";
    return 0;
}
