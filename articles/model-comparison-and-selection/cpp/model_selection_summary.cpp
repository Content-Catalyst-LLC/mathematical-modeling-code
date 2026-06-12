#include <iomanip>
#include <iostream>
#include <limits>
#include <string>
#include <vector>

struct Candidate {
    std::string id;
    std::string family;
    double calibration_rmse;
    double validation_rmse;
    int parameter_count;
    double interpretability;
    double robustness;
    double decision_relevance;
};

double score(const Candidate& model) {
    return model.validation_rmse
        + 0.08 * static_cast<double>(model.parameter_count)
        - 0.35 * model.interpretability
        - 0.40 * model.robustness
        - 0.35 * model.decision_relevance;
}

int main() {
    std::vector<Candidate> models = {
        {"baseline_naive", "baseline", 2.90, 3.05, 0, 0.95, 0.72, 0.55},
        {"linear_trend", "statistical", 1.80, 2.10, 2, 0.88, 0.70, 0.68},
        {"logistic_growth", "mechanistic", 1.25, 1.42, 3, 0.76, 0.82, 0.86},
        {"stochastic_shock", "stochastic", 1.05, 1.60, 6, 0.58, 0.88, 0.90},
        {"high_flex_curve", "flexible", 0.45, 2.75, 9, 0.35, 0.40, 0.52}
    };

    double best_score = std::numeric_limits<double>::infinity();
    std::string best_id;

    std::cout << "model_id,comparison_score,overfit_gap\n";
    for (const auto& model : models) {
        const double current_score = score(model);
        const double gap = model.validation_rmse - model.calibration_rmse;
        std::cout << std::fixed << std::setprecision(6)
                  << model.id << "," << current_score << "," << gap << "\n";
        if (current_score < best_score) {
            best_score = current_score;
            best_id = model.id;
        }
    }

    std::cerr << "selected_model=" << best_id << " comparison_score=" << best_score << "\n";
    return 0;
}
