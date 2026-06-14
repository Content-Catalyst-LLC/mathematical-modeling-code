#include <stdio.h>
#include <stdlib.h>

typedef struct {
    const char *key;
    const char *name;
    double expected_stock;
    double lower_bound;
    double upper_bound;
    double burden;
    double consequence_if_wrong;
} DecisionOption;

double decision_score(DecisionOption option) {
    double threshold_penalty = option.lower_bound < 45.0 ? 8.0 : 0.0;
    return option.expected_stock - 0.8 * option.burden - 1.2 * option.consequence_if_wrong - threshold_penalty;
}

int main(void) {
    DecisionOption options[] = {
        {"no_action", "No immediate action", 52.0, 38.0, 66.0, 1.0, 9.0},
        {"monitoring", "Formal monitoring", 54.0, 42.0, 68.0, 3.0, 6.0},
        {"moderate_intervention", "Moderate intervention", 60.0, 50.0, 72.0, 5.0, 4.0},
        {"strong_intervention", "Strong intervention", 68.0, 58.0, 78.0, 8.0, 2.0}
    };

    printf("key,option_name,decision_score,threshold_margin,robustness_class\n");

    for (int i = 0; i < 4; ++i) {
        const char *class_name = options[i].lower_bound >= 45.0 ? "robust" : "fragile";
        printf("%s,%s,%.3f,%.3f,%s\n", options[i].key, options[i].name, decision_score(options[i]), options[i].expected_stock - 45.0, class_name);
    }

    fprintf(stderr, "decision_summary complete\n");
    return EXIT_SUCCESS;
}
