#include <math.h>
#include <stdio.h>
#include <stdlib.h>

int main(void){
  const double initial_state = 80.0, target = 100.0, adjustment_rate = 0.2, delay = 5.0, dt = 0.1;
  const int steps = 300;
  const int delay_steps = (int)round(delay / dt);
  double states[steps + 2];
  states[0] = initial_state;

  printf("step,time,current_state,delayed_state,derivative_value,target,absolute_gap,warning\n");
  for(int step=0; step<=steps; step++){
    double time = step * dt;
    double current = states[step];
    int delayed_index = step - delay_steps;
    double delayed = delayed_index < 0 ? initial_state : states[delayed_index];
    double derivative = adjustment_rate * (target - delayed);
    printf("%d,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,Delayed adjustment depends on delay length history function time step and feedback strength.\n",
      step, time, current, delayed, derivative, target, fabs(current - target));
    states[step + 1] = current + dt * derivative;
  }
  return EXIT_SUCCESS;
}
