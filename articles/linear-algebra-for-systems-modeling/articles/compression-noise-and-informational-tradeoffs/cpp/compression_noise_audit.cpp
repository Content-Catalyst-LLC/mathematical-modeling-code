#include <iostream>

int main() {
    std::cout << "model_name,rows,columns,method,preprocessing,retained_rank,retained_energy_ratio,discarded_energy_ratio,compression_ratio,relative_reconstruction_error,maximum_row_residual,highest_residual_row,warning\n";
    std::cout << "synthetic_compression_noise_audit,9,6,svd_low_rank_compression,centered_and_standardized,2,0.962000,0.038000,1.687500,0.195000,1.430000,8,Compression requires retained-rank reconstruction residual weak-signal and validation documentation.\n";
    return 0;
}
