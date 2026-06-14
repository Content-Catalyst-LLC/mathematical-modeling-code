#include <iomanip>
#include <iostream>
#include <string>
#include <vector>

struct CommunicationRecord {
    std::string key;
    std::string layer;
    std::string audience;
    std::string status;
};

double priority(const CommunicationRecord& record) {
    double score = record.status == "active" ? 1.0 : 5.0;
    if (record.layer == "decision_threshold" || record.layer == "governance" || record.layer == "model_limit") {
        score += 2.0;
    }
    if (record.audience == "public" || record.audience == "decision_maker") {
        score += 1.0;
    }
    return score;
}

int main() {
    std::vector<CommunicationRecord> records = {
        {"central_result", "result", "decision_maker", "active"},
        {"uncertainty_range", "uncertainty", "public", "review"},
        {"threshold_risk", "decision_threshold", "decision_maker", "review"},
        {"structural_limit", "model_limit", "technical_reviewer", "review"},
        {"use_limit", "governance", "future_user", "review"}
    };

    std::cout << "key,communication_layer,audience,status,priority\n";
    for (const auto& record : records) {
        std::cout << std::fixed << std::setprecision(2)
                  << record.key << "," << record.layer << "," << record.audience << ","
                  << record.status << "," << priority(record) << "\n";
    }

    return 0;
}
