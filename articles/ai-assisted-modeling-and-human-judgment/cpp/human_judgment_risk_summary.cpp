#include <iomanip>
#include <iostream>
#include <string>
#include <vector>

struct HumanJudgmentCase {
    std::string key;
    std::string judgment_point;
    std::string decision_context;
    double evidence_strength;
    double uncertainty_level;
    double consequence_level;
    double automation_bias_risk;
    double accountability_clarity;
};

double judgment_risk_score(const HumanJudgmentCase& item) {
    return 0.25 * (1.0 - item.evidence_strength) +
           0.25 * item.uncertainty_level +
           0.25 * item.consequence_level +
           0.15 * item.automation_bias_risk +
           0.10 * (1.0 - item.accountability_clarity);
}

std::string review_class(double score) {
    if (score >= 0.65) {
        return "escalation_required";
    }
    if (score >= 0.50) {
        return "human_review_required";
    }
    return "standard_review";
}

int main() {
    std::vector<HumanJudgmentCase> cases = {
        {"problem_frame", "problem framing", "public infrastructure stress model", 0.72, 0.58, 0.80, 0.45, 0.70},
        {"data_fit", "data fitness judgment", "using administrative records", 0.62, 0.66, 0.75, 0.50, 0.65},
        {"model_use", "approved use decision", "moving from exploratory to decision support", 0.68, 0.70, 0.88, 0.72, 0.55},
        {"public_summary", "communication approval", "publishing model results", 0.76, 0.62, 0.82, 0.60, 0.72}
    };

    std::cout << "key,evidence_strength,uncertainty_level,consequence_level,automation_bias_risk,accountability_clarity,judgment_risk_score,review_class\n";
    for (const auto& item : cases) {
        const double score = judgment_risk_score(item);
        std::cout << std::fixed << std::setprecision(6)
                  << item.key << ","
                  << item.evidence_strength << ","
                  << item.uncertainty_level << ","
                  << item.consequence_level << ","
                  << item.automation_bias_risk << ","
                  << item.accountability_clarity << ","
                  << score << ","
                  << review_class(score) << "\n";
    }

    return 0;
}
