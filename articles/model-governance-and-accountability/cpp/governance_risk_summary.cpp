#include <iomanip>
#include <iostream>
#include <string>
#include <vector>

struct GovernanceRiskCase {
    std::string key;
    std::string model_name;
    double error_risk;
    double uncertainty_level;
    double consequence_level;
    double scope_misuse_risk;
    double accountability_gap;
};

double governance_risk_score(const GovernanceRiskCase& c) {
    return 0.20 * c.error_risk +
           0.20 * c.uncertainty_level +
           0.25 * c.consequence_level +
           0.20 * c.scope_misuse_risk +
           0.15 * c.accountability_gap;
}

std::string review_class(double score) {
    if (score >= 0.70) {
        return "escalation_required";
    }
    if (score >= 0.55) {
        return "governance_review_required";
    }
    return "standard_monitoring";
}

int main() {
    std::vector<GovernanceRiskCase> cases = {
        {"infrastructure_risk", "Infrastructure risk prioritization model", 0.38, 0.56, 0.82, 0.42, 0.24},
        {"public_health_demand", "Public health demand model", 0.50, 0.68, 0.86, 0.48, 0.32},
        {"supply_chain_resilience", "Supply chain resilience model", 0.36, 0.52, 0.65, 0.40, 0.22},
        {"ai_triage_support", "AI-assisted triage support model", 0.62, 0.72, 0.95, 0.70, 0.55}
    };

    std::cout << "key,error_risk,uncertainty_level,consequence_level,scope_misuse_risk,accountability_gap,governance_risk_score,review_class\n";
    for (const auto& c : cases) {
        const double score = governance_risk_score(c);
        std::cout << std::fixed << std::setprecision(6)
                  << c.key << ","
                  << c.error_risk << ","
                  << c.uncertainty_level << ","
                  << c.consequence_level << ","
                  << c.scope_misuse_risk << ","
                  << c.accountability_gap << ","
                  << score << ","
                  << review_class(score) << "\n";
    }

    return 0;
}
