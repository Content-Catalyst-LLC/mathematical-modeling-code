#include <math.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
  double growth_rate;
  double carrying_capacity;
  double initial_stock;
  double time_step;
  double horizon;
} ModelParameters;

typedef struct {
  double model_time;
  double stock;
} ModelState;

static ModelState step_logistic(ModelParameters p, ModelState s){
  double dx = p.growth_rate * s.stock * (1.0 - s.stock / p.carrying_capacity);
  ModelState next = {s.model_time + p.time_step, s.stock + p.time_step * dx};
  return next;
}

int main(void){
  ModelParameters p = {0.35, 100.0, 10.0, 0.25, 20.0};
  ModelState s = {0.0, p.initial_stock};
  while(s.model_time < p.horizon){
    s = step_logistic(p, s);
  }
  printf("model_use,growth_rate,carrying_capacity,initial_stock,time_step,horizon,final_time,final_stock,warning\n");
  printf("governance_review,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.12f,Typed records improve structural review but do not prove empirical validity.\n", p.growth_rate, p.carrying_capacity, p.initial_stock, p.time_step, p.horizon, s.model_time, s.stock);
  return EXIT_SUCCESS;
}
