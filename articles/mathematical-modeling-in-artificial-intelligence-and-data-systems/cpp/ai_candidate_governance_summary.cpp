#include <iomanip>
#include <iostream>
#include <string>
#include <vector>

struct ModelCandidate {
    std::string key;
    std::string model_name;
    double validation_score;
    double calibration_error;
    double subgroup_error_gap;
    double drift_score;
    double interpretability_score;
    double privacy_risk;
    double deployment_criticality;
};

double governance_score(const ModelCandidate& candidate) {
    const double penalty =
        1.8 * candidate.calibration_error +
        1.5 * candidate.subgroup_error_gap +
        1.2 * candidate.drift_score +
        1.4 * candidate.privacy_risk +
        0.7 * candidate.deployment_criticality -
        0.5 * candidate.interpretability_score;
    return candidate.validation_score - penalty;
}

bool requires_review(const ModelCandidate& candidate) {
    return candidate.calibration_error > 0.08 ||
           candidate.subgroup_error_gap > 0.12 ||
           candidate.drift_score > 0.20 ||
           candidate.privacy_risk > 0.15 ||
           candidate.interpretability_score < 0.50;
}

int main() {
    std::vector<ModelCandidate> candidates = {
        {"baseline_logistic", "Baseline logistic model", 0.76, 0.050, 0.080, 0.120, 0.920, 0.080, 0.62},
        {"tree_ensemble", "Tree ensemble", 0.83, 0.070, 0.140, 0.180, 0.620, 0.130, 0.70},
        {"neural_model", "Neural model", 0.86, 0.095, 0.190, 0.240, 0.380, 0.180, 0.82},
        {"constrained_model", "Constrained calibrated model", 0.81, 0.035, 0.060, 0.100, 0.780, 0.090, 0.66}
    };

    std::cout << "key,validation_score,calibration_error,subgroup_error_gap,drift_score,privacy_risk,governance_score,requires_review\n";
    for (const auto& candidate : candidates) {
        std::cout << std::fixed << std::setprecision(6)
                  << candidate.key << ","
                  << candidate.validation_score << ","
                  << candidate.calibration_error << ","
                  << candidate.subgroup_error_gap << ","
                  << candidate.drift_score << ","
                  << candidate.privacy_risk << ","
                  << governance_score(candidate) << ","
                  << (requires_review(candidate) ? "true" : "false") << "\n";
    }

    return 0;
}
