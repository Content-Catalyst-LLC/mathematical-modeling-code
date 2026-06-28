#include <math.h>
#include <stdio.h>

int main(void) {
    int row_count = 3;
    int column_count = 3;
    int rank = 3;
    int nullity = 0;
    double input_norm = 120.415946;
    double output_norm = 152.750205;
    double amplification_ratio = output_norm / input_norm;

    printf("system_name,row_count,column_count,input_state,output_state,rank,nullity,input_norm,output_norm,amplification_ratio,warning\n");
    printf("three_component_system_response,%d,%d,100.000000;60.000000;30.000000,126.000000;75.500000;42.000000,%d,%d,%.6f,%.6f,%.6f,Matrix action requires row meanings column meanings units scaling and sensitivity review.\n",
           row_count, column_count, rank, nullity, input_norm, output_norm, amplification_ratio);
    return 0;
}
