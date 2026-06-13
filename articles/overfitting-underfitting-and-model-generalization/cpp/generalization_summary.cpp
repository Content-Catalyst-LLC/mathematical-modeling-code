#include <iomanip>
#include <iostream>
#include <limits>
#include <string>
#include <vector>

struct Candidate {
    std::string id;
    std::string family;
    double training_rmse;
    double validation_rmse;
    int parameter_count;
    double complexity;
    double interpretability;
};

double score(const Candidate& model) {
    return model.validation_rmse
        + 0.20 * model.complexity
        + 0.08 * static_cast<double>(model.parameter_count)
        - 0.20 * model.interpretability;
}

std::string classify(const Candidate& model) {
    const double gap = model.validation_rmse - model.training_rmse;
    if (model.training_rmse >= 3.0 && model.validation_rmse >= 3.0) {
        return "likely_underfit";
    }
    if (gap >= 1.0 && model.training_rmse <= 1.0) {
        return "likely_overfit";
    }
    if (model.validation_rmse <= 1.5 && gap <= 0.6) {
        return "generalizes_reasonably";
    }
    return "requires_review";
}

int main() {
    std::vector<Candidate> models = {
        {"constant_baseline", "baseline", 3.40, 3.55, 0, 0.05, 0.95},
        {"linear_trend", "statistical", 1.95, 2.10, 2, 0.25, 0.88},
        {"logistic_growth", "mechanistic", 1.20, 1.38, 3, 0.45, 0.78},
        {"regularized_curve", "regularized", 0.95, 1.44, 5, 0.62, 0.66},
        {"high_flex_curve", "flexible", 0.28, 2.85, 10, 0.95, 0.30}
    };

    double best_score = std::numeric_limits<double>::infinity();
    std::string best_id;

    std::cout << "model_id,generalization_score,overfit_gap,classification\n";
    for (const auto& model : models) {
        const double current_score = score(model);
        const double gap = model.validation_rmse - model.training_rmse;
        std::cout << std::fixed << std::setprecision(6)
                  << model.id << "," << current_score << "," << gap << "," << classify(model) << "\n";
        if (current_score < best_score) {
            best_score = current_score;
            best_id = model.id;
        }
    }

    std::cerr << "selected_for_review=" << best_id << " generalization_score=" << best_score << "\n";
    return 0;
}
