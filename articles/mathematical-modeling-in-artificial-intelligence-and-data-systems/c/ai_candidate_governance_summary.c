#include <stdio.h>
#include <stdlib.h>

typedef struct {
    const char *key;
    const char *model_name;
    double validation_score;
    double calibration_error;
    double subgroup_error_gap;
    double drift_score;
    double interpretability_score;
    double privacy_risk;
    double deployment_criticality;
} ModelCandidate;

double governance_score(ModelCandidate candidate) {
    double penalty =
        1.8 * candidate.calibration_error +
        1.5 * candidate.subgroup_error_gap +
        1.2 * candidate.drift_score +
        1.4 * candidate.privacy_risk +
        0.7 * candidate.deployment_criticality -
        0.5 * candidate.interpretability_score;
    return candidate.validation_score - penalty;
}

int requires_review(ModelCandidate candidate) {
    return candidate.calibration_error > 0.08 ||
           candidate.subgroup_error_gap > 0.12 ||
           candidate.drift_score > 0.20 ||
           candidate.privacy_risk > 0.15 ||
           candidate.interpretability_score < 0.50;
}

int main(void) {
    ModelCandidate candidates[] = {
        {"baseline_logistic", "Baseline logistic model", 0.76, 0.050, 0.080, 0.120, 0.920, 0.080, 0.62},
        {"tree_ensemble", "Tree ensemble", 0.83, 0.070, 0.140, 0.180, 0.620, 0.130, 0.70},
        {"neural_model", "Neural model", 0.86, 0.095, 0.190, 0.240, 0.380, 0.180, 0.82},
        {"constrained_model", "Constrained calibrated model", 0.81, 0.035, 0.060, 0.100, 0.780, 0.090, 0.66}
    };

    printf("key,validation_score,calibration_error,subgroup_error_gap,drift_score,privacy_risk,governance_score,requires_review\n");

    for (int i = 0; i < 4; ++i) {
        printf("%s,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%s\n",
               candidates[i].key,
               candidates[i].validation_score,
               candidates[i].calibration_error,
               candidates[i].subgroup_error_gap,
               candidates[i].drift_score,
               candidates[i].privacy_risk,
               governance_score(candidates[i]),
               requires_review(candidates[i]) ? "true" : "false");
    }

    fprintf(stderr, "ai_candidate_governance_summary complete\n");
    return EXIT_SUCCESS;
}
