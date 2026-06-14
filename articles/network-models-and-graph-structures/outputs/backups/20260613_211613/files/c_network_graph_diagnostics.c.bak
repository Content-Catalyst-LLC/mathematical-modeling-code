#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int source;
    int target;
    double weight;
} Edge;

int main(void) {
    const int node_count = 7;
    const int edge_count = 10;

    Edge edges[10] = {
        {0, 6, 0.95},
        {0, 4, 0.90},
        {1, 6, 0.70},
        {2, 0, 0.60},
        {3, 6, 0.50},
        {3, 2, 0.65},
        {4, 6, 0.80},
        {5, 6, 0.75},
        {1, 5, 0.55},
        {0, 1, 0.85}
    };

    int in_degree[7] = {0};
    int out_degree[7] = {0};
    double weighted_out[7] = {0.0};

    for (int i = 0; i < edge_count; ++i) {
        out_degree[edges[i].source] += 1;
        in_degree[edges[i].target] += 1;
        weighted_out[edges[i].source] += edges[i].weight;
    }

    printf("node,in_degree,out_degree,total_degree,weighted_out\n");
    for (int node = 0; node < node_count; ++node) {
        printf("%d,%d,%d,%d,%.6f\n", node + 1, in_degree[node], out_degree[node], in_degree[node] + out_degree[node], weighted_out[node]);
    }

    fprintf(stderr, "c node_count=%d edge_count=%d\n", node_count, edge_count);
    return EXIT_SUCCESS;
}
