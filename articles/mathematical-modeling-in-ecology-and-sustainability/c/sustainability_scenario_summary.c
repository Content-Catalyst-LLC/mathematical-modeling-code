#include <stdio.h>
#include <stdlib.h>

typedef struct {
    const char *key;
    const char *scenario_name;
    double initial_stock;
    double growth_rate;
    double carrying_capacity;
    double extraction;
    double climate_stress;
    int years;
    double minimum_stock;
} ResourceScenario;

typedef struct {
    double final_stock;
    double minimum_observed_stock;
    double minimum_resilience_margin;
    int threshold_breach;
} Evaluation;

Evaluation evaluate(ResourceScenario scenario) {
    double stock = scenario.initial_stock;
    double effective_growth = scenario.growth_rate * (1.0 - scenario.climate_stress);
    double min_stock = stock;
    double min_margin = stock - scenario.minimum_stock;

    for (int year = 0; year < scenario.years; ++year) {
        double regeneration = effective_growth * stock * (1.0 - stock / scenario.carrying_capacity);
        stock = stock + regeneration - scenario.extraction;
        if (stock < 0.0) {
            stock = 0.0;
        }
        if (stock < min_stock) {
            min_stock = stock;
        }
        double margin = stock - scenario.minimum_stock;
        if (margin < min_margin) {
            min_margin = margin;
        }
    }

    Evaluation result = {stock, min_stock, min_margin, min_stock < scenario.minimum_stock};
    return result;
}

int main(void) {
    ResourceScenario scenarios[] = {
        {"baseline", "Baseline managed use", 420.0, 0.24, 800.0, 36.0, 0.04, 25, 250.0},
        {"high_extraction", "High extraction pressure", 420.0, 0.24, 800.0, 64.0, 0.04, 25, 250.0},
        {"climate_stress", "Climate stress with lower regeneration", 420.0, 0.24, 800.0, 42.0, 0.22, 25, 250.0},
        {"restoration_pathway", "Restoration and reduced extraction", 420.0, 0.28, 860.0, 24.0, 0.03, 25, 250.0},
        {"adaptive_management", "Adaptive use with monitoring trigger", 420.0, 0.25, 820.0, 32.0, 0.08, 25, 250.0}
    };

    printf("key,final_stock,minimum_observed_stock,minimum_resilience_margin,threshold_breach\n");

    for (int i = 0; i < 5; ++i) {
        Evaluation eval = evaluate(scenarios[i]);
        printf("%s,%.6f,%.6f,%.6f,%s\n",
               scenarios[i].key,
               eval.final_stock,
               eval.minimum_observed_stock,
               eval.minimum_resilience_margin,
               eval.threshold_breach ? "true" : "false");
    }

    fprintf(stderr, "sustainability_scenario_summary complete\n");
    return EXIT_SUCCESS;
}
