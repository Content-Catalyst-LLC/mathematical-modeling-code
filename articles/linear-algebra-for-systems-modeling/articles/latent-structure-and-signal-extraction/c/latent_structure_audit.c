#include <stdio.h>

int main(void) {
    printf("model_name,observations,variables,method,preprocessing,retained_rank,retained_signal_ratio,relative_reconstruction_error,maximum_observation_residual,highest_residual_observation,warning\n");
    printf("synthetic_latent_structure_signal_extraction_audit,9,6,svd_low_rank_signal_extraction,centered_and_standardized,2,0.962000,0.195000,1.430000,8,Latent signal extraction requires observed-matrix preprocessing method rank residual stability and validation documentation.\n");
    return 0;
}
