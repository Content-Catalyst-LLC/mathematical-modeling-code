#include <stdio.h>
#include <stdlib.h>

typedef struct {
    const char *key;
    const char *option_name;
    double projected_benefit;
    double total_cost;
    double feasibility;
    double equity_score;
    double uncertainty_width;
    double public_risk;
} PolicyOption;

double public_value_score(PolicyOption option) {
    double budget_penalty = option.total_cost > 40.0 ? 14.0 : 0.0;
    return option.projected_benefit
        + 18.0 * option.feasibility
        + 24.0 * option.equity_score
        - option.total_cost
        - 0.22 * option.uncertainty_width
        - 30.0 * option.public_risk
        - budget_penalty;
}

int main(void) {
    PolicyOption options[] = {
        {"baseline", "Maintain current services", 42.0, 18.0, 0.86, 0.52, 18.0, 0.42},
        {"targeted_prevention", "Targeted prevention program", 68.0, 32.0, 0.74, 0.78, 22.0, 0.30},
        {"broad_expansion", "Broad service expansion", 81.0, 49.0, 0.58, 0.69, 28.0, 0.34},
        {"adaptive_pathway", "Adaptive pathway with monitoring triggers", 73.0, 38.0, 0.70, 0.82, 16.0, 0.24}
    };

    printf("key,projected_benefit,total_cost,equity_score,public_risk,public_value_score,budget_violation\n");

    for (int i = 0; i < 4; ++i) {
        const char *budget_violation = options[i].total_cost > 40.0 ? "true" : "false";
        printf("%s,%.3f,%.3f,%.3f,%.3f,%.6f,%s\n",
               options[i].key,
               options[i].projected_benefit,
               options[i].total_cost,
               options[i].equity_score,
               options[i].public_risk,
               public_value_score(options[i]),
               budget_violation);
    }

    fprintf(stderr, "policy_option_summary complete\n");
    return EXIT_SUCCESS;
}
