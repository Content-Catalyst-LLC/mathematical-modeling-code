#include <stdio.h>

int main(void) {
    int compatible_shape = 1;
    double output_entry_sum = 3.95;

    printf("operation_name,matrix_shape,compatible_shape,output_entry_sum,warning\n");
    printf("baseline_plus_weighted_intervention_and_stress,3x3,%d,%.4f,Shape compatibility is not enough; semantic compatibility must be documented.\n",
           compatible_shape, output_entry_sum);
    return 0;
}
