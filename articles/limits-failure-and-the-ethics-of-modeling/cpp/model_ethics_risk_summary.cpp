#include <iomanip>
#include <iostream>
#include <string>
#include <vector>

struct ModelRiskCase {
    std::string key;
    std::string model_name;
    std::string intended_use;
    double severity;
    double likelihood;
    double detectability_gap;
    double uncertainty_level;
    double equity_concern;
    double accountability_gap;
};

double ethical_risk_score(const ModelRiskCase& item) {
    return 1.8 * item.severity +
           1.3 * item.likelihood +
           1.2 * item.detectability_gap +
           1.1 * item.uncertainty_level +
           1.5 * item.equity_concern +
           1.6 * item.accountability_gap;
}

std::string review_class(double score) {
    if (score >= 6.0) {
        return "high_ethics_review_required";
    }
    if (score >= 4.0) {
        return "governance_review_required";
    }
    return "standard_review";
}

int main() {
    std::vector<ModelRiskCase> cases = {
        {"exploratory_model", "Exploratory planning model", "learning and scenario discussion", 0.35, 0.35, 0.25, 0.60, 0.30, 0.25},
        {"allocation_model", "Resource allocation model", "prioritizing scarce resources", 0.85, 0.55, 0.55, 0.65, 0.75, 0.70},
        {"public_dashboard", "Public risk dashboard", "communicating population risk", 0.70, 0.50, 0.45, 0.80, 0.55, 0.60},
        {"automated_score", "Automated scoring model", "triggering institutional action", 0.90, 0.60, 0.70, 0.60, 0.80, 0.85}
    };

    std::cout << "key,severity,likelihood,detectability_gap,uncertainty_level,equity_concern,accountability_gap,ethical_risk_score,review_class\n";
    for (const auto& item : cases) {
        const double score = ethical_risk_score(item);
        std::cout << std::fixed << std::setprecision(6)
                  << item.key << ","
                  << item.severity << ","
                  << item.likelihood << ","
                  << item.detectability_gap << ","
                  << item.uncertainty_level << ","
                  << item.equity_concern << ","
                  << item.accountability_gap << ","
                  << score << ","
                  << review_class(score) << "\n";
    }

    return 0;
}
