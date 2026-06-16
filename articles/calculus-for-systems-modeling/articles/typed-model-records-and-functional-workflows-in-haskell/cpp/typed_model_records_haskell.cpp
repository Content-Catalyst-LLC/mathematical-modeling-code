#include <iomanip>
#include <iostream>
#include <string>

struct ModelParameters {
  double growthRate;
  double carryingCapacity;
  double initialStock;
  double timeStep;
  double horizon;
};

struct ModelState {
  double modelTime;
  double stock;
};

ModelState stepLogistic(const ModelParameters& p, const ModelState& s) {
  const double dx = p.growthRate * s.stock * (1.0 - s.stock / p.carryingCapacity);
  return {s.modelTime + p.timeStep, s.stock + p.timeStep * dx};
}

int main() {
  ModelParameters p{0.35, 100.0, 10.0, 0.25, 20.0};
  ModelState s{0.0, p.initialStock};
  while (s.modelTime < p.horizon) s = stepLogistic(p, s);

  std::cout << std::fixed << std::setprecision(12);
  std::cout << "model_use,growth_rate,carrying_capacity,initial_stock,time_step,horizon,final_time,final_stock,warning\n";
  std::cout << "governance_review," << p.growthRate << "," << p.carryingCapacity << "," << p.initialStock << "," << p.timeStep << "," << p.horizon << "," << s.modelTime << "," << s.stock << ",Typed records improve structural review but do not prove empirical validity.\n";
}
