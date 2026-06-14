#include <iomanip>
#include <iostream>
#include <string>
#include <vector>

struct Direction { std::string key; double complexity, maturity, governance, uncertainty, judgment; };

double priority(const Direction& d) {
    return 0.25*d.complexity + 0.20*d.maturity + 0.20*d.governance + 0.20*d.uncertainty + 0.15*d.judgment;
}

std::string review_class(const Direction& d) {
    double s = priority(d);
    if (d.governance >= 0.85 || d.judgment >= 0.90) return "governance_priority";
    if (d.uncertainty >= 0.85) return "uncertainty_priority";
    if (s >= 0.78) return "strategic_priority";
    return "monitor";
}

int main() {
    std::vector<Direction> rows = {
        {"hybrid_models",0.88,0.70,0.74,0.72,0.80},
        {"ai_assistance",0.82,0.78,0.90,0.76,0.92},
        {"digital_twins",0.86,0.75,0.88,0.70,0.84},
        {"uncertainty_workflows",0.90,0.72,0.82,0.92,0.86},
        {"participatory_modeling",0.78,0.62,0.86,0.68,0.94}
    };
    std::cout << "key,complexity_relevance,technical_maturity,governance_need,uncertainty_pressure,human_judgment_need,future_priority_score,review_class\n";
    for (const auto& d : rows) {
        std::cout << std::fixed << std::setprecision(6)
                  << d.key << "," << d.complexity << "," << d.maturity << "," << d.governance << ","
                  << d.uncertainty << "," << d.judgment << "," << priority(d) << "," << review_class(d) << "\n";
    }
}
