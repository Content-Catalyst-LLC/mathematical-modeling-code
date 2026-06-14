#include <stdio.h>
#include <stdlib.h>

typedef struct {
    const char *key;
    const char *model_name;
    const char *intended_use;
    double severity;
    double likelihood;
    double detectability_gap;
    double uncertainty_level;
    double equity_concern;
    double accountability_gap;
} ModelRiskCase;

double ethical_risk_score(ModelRiskCase item) {
    return 1.8 * item.severity +
           1.3 * item.likelihood +
           1.2 * item.detectability_gap +
           1.1 * item.uncertainty_level +
           1.5 * item.equity_concern +
           1.6 * item.accountability_gap;
}

const char *review_class(double score) {
    if (score >= 6.0) {
        return "high_ethics_review_required";
    }
    if (score >= 4.0) {
        return "governance_review_required";
    }
    return "standard_review";
}

int main(void) {
    ModelRiskCase cases[] = {
        {"exploratory_model", "Exploratory planning model", "learning and scenario discussion", 0.35, 0.35, 0.25, 0.60, 0.30, 0.25},
        {"allocation_model", "Resource allocation model", "prioritizing scarce resources", 0.85, 0.55, 0.55, 0.65, 0.75, 0.70},
        {"public_dashboard", "Public risk dashboard", "communicating population risk", 0.70, 0.50, 0.45, 0.80, 0.55, 0.60},
        {"automated_score", "Automated scoring model", "triggering institutional action", 0.90, 0.60, 0.70, 0.60, 0.80, 0.85}
    };

    printf("key,severity,likelihood,detectability_gap,uncertainty_level,equity_concern,accountability_gap,ethical_risk_score,review_class\n");

    for (int i = 0; i < 4; ++i) {
        double score = ethical_risk_score(cases[i]);
        printf("%s,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%s\n",
               cases[i].key,
               cases[i].severity,
               cases[i].likelihood,
               cases[i].detectability_gap,
               cases[i].uncertainty_level,
               cases[i].equity_concern,
               cases[i].accountability_gap,
               score,
               review_class(score));
    }

    fprintf(stderr, "model_ethics_risk_summary complete\n");
    return EXIT_SUCCESS;
}
