#include <stdio.h>
#include <stdlib.h>

static double bounded_update(double stock, double inflow, double demand, double losses, double capacity) {
    double next = stock + inflow - demand - losses;
    if (next < 0.0) return 0.0;
    if (next > capacity) return capacity;
    return next;
}

int main(void) {
    double stock = 80.0;
    const double capacity = 100.0;
    const double inflow = 5.0;
    const double demand = 6.0;
    const double control_action = 1.5;
    const double loss_rate = 0.015;
    const int periods = 60;
    double total_shortage = 0.0;

    printf("period,stock,inflow,effective_demand,control_action,losses,shortage\n");
    for (int period = 0; period <= periods; ++period) {
        double effective_demand = demand - control_action;
        if (effective_demand < 0.0) effective_demand = 0.0;

        double losses = loss_rate * stock;
        double shortage = effective_demand + losses - (stock + inflow);
        if (shortage < 0.0) shortage = 0.0;

        printf("%d,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f\n", period, stock, inflow, effective_demand, control_action, losses, shortage);
        total_shortage += shortage;
        stock = bounded_update(stock, inflow, effective_demand, losses, capacity);
    }

    fprintf(stderr, "c final_stock=%.6f total_shortage=%.6f\n", stock, total_shortage);
    return EXIT_SUCCESS;
}
