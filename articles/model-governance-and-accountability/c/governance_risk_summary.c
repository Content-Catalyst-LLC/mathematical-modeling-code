#include <stdio.h>
#include <stdlib.h>

typedef struct {
    const char *key;
    const char *model_name;
    double error_risk;
    double uncertainty_level;
    double consequence_level;
    double scope_misuse_risk;
    double accountability_gap;
} GovernanceRiskCase;

double governance_risk_score(GovernanceRiskCase c) {
    return 0.20 * c.error_risk +
           0.20 * c.uncertainty_level +
           0.25 * c.consequence_level +
           0.20 * c.scope_misuse_risk +
           0.15 * c.accountability_gap;
}

const char *review_class(double score) {
    if (score >= 0.70) {
        return "escalation_required";
    }
    if (score >= 0.55) {
        return "governance_review_required";
    }
    return "standard_monitoring";
}

int main(void) {
    GovernanceRiskCase cases[] = {
        {"infrastructure_risk", "Infrastructure risk prioritization model", 0.38, 0.56, 0.82, 0.42, 0.24},
        {"public_health_demand", "Public health demand model", 0.50, 0.68, 0.86, 0.48, 0.32},
        {"supply_chain_resilience", "Supply chain resilience model", 0.36, 0.52, 0.65, 0.40, 0.22},
        {"ai_triage_support", "AI-assisted triage support model", 0.62, 0.72, 0.95, 0.70, 0.55}
    };

    printf("key,error_risk,uncertainty_level,consequence_level,scope_misuse_risk,accountability_gap,governance_risk_score,review_class\n");

    for (int i = 0; i < 4; ++i) {
        double score = governance_risk_score(cases[i]);
        printf("%s,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%s\n",
               cases[i].key,
               cases[i].error_risk,
               cases[i].uncertainty_level,
               cases[i].consequence_level,
               cases[i].scope_misuse_risk,
               cases[i].accountability_gap,
               score,
               review_class(score));
    }

    fprintf(stderr, "governance_risk_summary complete\n");
    return EXIT_SUCCESS;
}
