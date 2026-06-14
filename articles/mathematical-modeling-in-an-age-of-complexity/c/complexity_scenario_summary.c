#include <stdio.h>
#include <stdlib.h>

typedef struct {
    const char *key;
    const char *scenario_name;
    double stress_level;
    double interdependence_level;
    double uncertainty_level;
    double resilience_score;
    double equity_score;
    double adaptability_score;
} ComplexityScenario;

double fragility_score(ComplexityScenario s) {
    return 0.35 * s.stress_level +
           0.30 * s.interdependence_level +
           0.25 * s.uncertainty_level +
           0.10 * (1.0 - s.adaptability_score);
}

double robust_value(ComplexityScenario s) {
    double f = fragility_score(s);
    return 0.40 * s.resilience_score +
           0.30 * s.equity_score +
           0.30 * s.adaptability_score -
           0.20 * f;
}

int main(void) {
    ComplexityScenario scenarios[] = {
        {"baseline", "Baseline stress", 0.35, 0.45, 0.40, 0.72, 0.68, 0.65},
        {"compound_shock", "Compound shock", 0.78, 0.70, 0.72, 0.48, 0.52, 0.55},
        {"cascading_failure", "Cascading failure", 0.88, 0.86, 0.75, 0.32, 0.40, 0.42},
        {"adaptive_pathway", "Adaptive pathway", 0.65, 0.68, 0.70, 0.66, 0.70, 0.82}
    };

    printf("key,stress_level,interdependence_level,uncertainty_level,resilience_score,equity_score,adaptability_score,fragility_score,robust_value\n");

    for (int i = 0; i < 4; ++i) {
        printf("%s,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f\n",
               scenarios[i].key,
               scenarios[i].stress_level,
               scenarios[i].interdependence_level,
               scenarios[i].uncertainty_level,
               scenarios[i].resilience_score,
               scenarios[i].equity_score,
               scenarios[i].adaptability_score,
               fragility_score(scenarios[i]),
               robust_value(scenarios[i]));
    }

    fprintf(stderr, "complexity_scenario_summary complete\n");
    return EXIT_SUCCESS;
}
