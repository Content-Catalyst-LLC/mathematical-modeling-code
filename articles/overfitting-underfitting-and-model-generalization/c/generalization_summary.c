#include <math.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    const char *id;
    const char *family;
    double training_rmse;
    double validation_rmse;
    int parameter_count;
    double complexity;
    double interpretability;
} Candidate;

double score(Candidate model) {
    return model.validation_rmse
        + 0.20 * model.complexity
        + 0.08 * (double)model.parameter_count
        - 0.20 * model.interpretability;
}

const char *classify(Candidate model) {
    double gap = model.validation_rmse - model.training_rmse;
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

int main(void) {
    Candidate models[] = {
        {"constant_baseline", "baseline", 3.40, 3.55, 0, 0.05, 0.95},
        {"linear_trend", "statistical", 1.95, 2.10, 2, 0.25, 0.88},
        {"logistic_growth", "mechanistic", 1.20, 1.38, 3, 0.45, 0.78},
        {"regularized_curve", "regularized", 0.95, 1.44, 5, 0.62, 0.66},
        {"high_flex_curve", "flexible", 0.28, 2.85, 10, 0.95, 0.30}
    };
    const int n = 5;
    double best_score = INFINITY;
    const char *best_id = "";

    printf("model_id,generalization_score,overfit_gap,classification\n");

    for (int i = 0; i < n; ++i) {
        double current_score = score(models[i]);
        double gap = models[i].validation_rmse - models[i].training_rmse;
        printf("%s,%.6f,%.6f,%s\n", models[i].id, current_score, gap, classify(models[i]));
        if (current_score < best_score) {
            best_score = current_score;
            best_id = models[i].id;
        }
    }

    fprintf(stderr, "selected_for_review=%s generalization_score=%.6f\n", best_id, best_score);
    return EXIT_SUCCESS;
}
