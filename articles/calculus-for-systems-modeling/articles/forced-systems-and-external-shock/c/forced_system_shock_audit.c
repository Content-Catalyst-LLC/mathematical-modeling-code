#include <math.h>
#include <stdio.h>
#include <stdlib.h>

double restoring_rate(double x, double equilibrium, double recovery_rate){ return -recovery_rate * (x - equilibrium); }
double impulse_shock(double time, double shock_time, double shock_magnitude){ return fabs(time - shock_time) < 1e-12 ? shock_magnitude : 0.0; }

int main(void){
  double baseline = 100.0, forced = 100.0;
  double equilibrium = 100.0, recovery_rate = 0.15, shock_time = 10.0, shock_magnitude = -30.0, dt = 0.1;
  printf("step,time,baseline_state,forced_state,shock_value,absolute_deviation,warning\n");
  for(int step=0; step<=300; step++){
    double time = step * dt;
    double shock = impulse_shock(time, shock_time, shock_magnitude);
    printf("%d,%.6f,%.6f,%.6f,%.6f,%.6f,Shock response depends on forcing form timing magnitude recovery rate and numerical step size.\n", step, time, baseline, forced, shock, fabs(forced-baseline));
    baseline = baseline + dt * restoring_rate(baseline, equilibrium, recovery_rate);
    if(shock != 0.0){ forced = forced + shock; }
    forced = forced + dt * restoring_rate(forced, equilibrium, recovery_rate);
  }
  return EXIT_SUCCESS;
}
