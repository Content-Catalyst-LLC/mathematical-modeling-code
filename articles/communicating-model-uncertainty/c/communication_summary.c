#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    const char *key;
    const char *layer;
    const char *audience;
    const char *status;
} CommunicationRecord;

double priority(CommunicationRecord record) {
    double score = strcmp(record.status, "active") == 0 ? 1.0 : 5.0;

    if (
        strcmp(record.layer, "decision_threshold") == 0 ||
        strcmp(record.layer, "governance") == 0 ||
        strcmp(record.layer, "model_limit") == 0
    ) {
        score += 2.0;
    }

    if (
        strcmp(record.audience, "public") == 0 ||
        strcmp(record.audience, "decision_maker") == 0
    ) {
        score += 1.0;
    }

    return score;
}

int main(void) {
    CommunicationRecord records[] = {
        {"central_result", "result", "decision_maker", "active"},
        {"uncertainty_range", "uncertainty", "public", "review"},
        {"threshold_risk", "decision_threshold", "decision_maker", "review"},
        {"structural_limit", "model_limit", "technical_reviewer", "review"},
        {"use_limit", "governance", "future_user", "review"}
    };

    printf("key,communication_layer,audience,status,priority\n");

    for (int i = 0; i < 5; ++i) {
        printf("%s,%s,%s,%s,%.2f\n", records[i].key, records[i].layer, records[i].audience, records[i].status, priority(records[i]));
    }

    fprintf(stderr, "communication_summary complete\n");
    return EXIT_SUCCESS;
}
