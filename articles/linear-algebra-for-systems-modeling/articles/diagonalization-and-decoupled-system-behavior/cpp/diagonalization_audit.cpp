#include <iostream>

int main() {
    std::cout << "system_name,matrix_entries,eigenvector_matrix,diagonal_matrix,reconstruction_error_frobenius,spectral_radius,dominant_eigenvalue,stability_classification,warning\n";
    std::cout << "two_mode_diagonalization_audit,0.796667;0.123333;0.246667;0.673333,1.000000;1.000000;1.000000;-2.000000,0.920000;0.000000;0.000000;0.550000,0.000000,0.920000,0.920000,all_modes_decay_discrete_time,Diagonalization decouples representation not necessarily real system.\n";
    return 0;
}
