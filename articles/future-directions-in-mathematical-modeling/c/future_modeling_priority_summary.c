#include <stdio.h>
#include <stdlib.h>

typedef struct { const char *key; double complexity, maturity, governance, uncertainty, judgment; } Direction;

double priority(Direction d) {
    return 0.25*d.complexity + 0.20*d.maturity + 0.20*d.governance + 0.20*d.uncertainty + 0.15*d.judgment;
}

const char *review_class(Direction d) {
    double s = priority(d);
    if (d.governance >= 0.85 || d.judgment >= 0.90) return "governance_priority";
    if (d.uncertainty >= 0.85) return "uncertainty_priority";
    if (s >= 0.78) return "strategic_priority";
    return "monitor";
}

int main(void) {
    Direction rows[] = {
        {"hybrid_models",0.88,0.70,0.74,0.72,0.80},
        {"ai_assistance",0.82,0.78,0.90,0.76,0.92},
        {"digital_twins",0.86,0.75,0.88,0.70,0.84},
        {"uncertainty_workflows",0.90,0.72,0.82,0.92,0.86},
        {"participatory_modeling",0.78,0.62,0.86,0.68,0.94}
    };
    printf("key,complexity_relevance,technical_maturity,governance_need,uncertainty_pressure,human_judgment_need,future_priority_score,review_class\n");
    for (int i = 0; i < 5; ++i) {
        printf("%s,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%s\n", rows[i].key, rows[i].complexity, rows[i].maturity, rows[i].governance, rows[i].uncertainty, rows[i].judgment, priority(rows[i]), review_class(rows[i]));
    }
    fprintf(stderr, "future_modeling_priority_summary complete\n");
    return EXIT_SUCCESS;
}
