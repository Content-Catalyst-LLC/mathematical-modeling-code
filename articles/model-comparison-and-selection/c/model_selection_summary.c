#include <math.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    const char *id;
    const char *family;
    double calibration_rmse;
    double validation_rmse;
    int parameter_count;
    double interpretability;
    double robustness;
    double decision_relevance;
} Candidate;

double score(Candidate model) {
    return model.validation_rmse
        + 0.08 * (double)model.parameter_count
        - 0.35 * model.interpretability
        - 0.40 * model.robustness
        - 0.35 * model.decision_relevance;
}

int main(void) {
    Candidate models[] = {
        {"baseline_naive", "baseline", 2.90, 3.05, 0, 0.95, 0.72, 0.55},
        {"linear_trend", "statistical", 1.80, 2.10, 2, 0.88, 0.70, 0.68},
        {"logistic_growth", "mechanistic", 1.25, 1.42, 3, 0.76, 0.82, 0.86},
        {"stochastic_shock", "stochastic", 1.05, 1.60, 6, 0.58, 0.88, 0.90},
        {"high_flex_curve", "flexible", 0.45, 2.75, 9, 0.35, 0.40, 0.52}
    };
    const int n = 5;
    double best_score = INFINITY;
    const char *best_id = "";

    printf("model_id,comparison_score,overfit_gap\n");

    for (int i = 0; i < n; ++i) {
        double current_score = score(models[i]);
        double overfit_gap = models[i].validation_rmse - models[i].calibration_rmse;
        printf("%s,%.6f,%.6f\n", models[i].id, current_score, overfit_gap);
        if (current_score < best_score) {
            best_score = current_score;
            best_id = models[i].id;
        }
    }

    fprintf(stderr, "selected_model=%s comparison_score=%.6f\n", best_id, best_score);
    return EXIT_SUCCESS;
}
