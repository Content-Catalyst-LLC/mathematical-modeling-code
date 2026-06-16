#include <iostream>
double regeneration(double stock, double growth_rate, double carrying_capacity){ return growth_rate * stock * (1.0 - stock / carrying_capacity); }
double extraction(double efficiency, double effort, double stock){ return efficiency * effort * stock; }
double natural_stock_step(double stock, double growth_rate, double carrying_capacity, double harvest, double stress, double dt){
  double next = stock + (regeneration(stock, growth_rate, carrying_capacity) - harvest - stress) * dt;
  return next > 0.0 ? next : 0.0;
}
int main(){
  double stock = 80.0;
  double harvest = extraction(0.003, 12.0, stock);
  double next = natural_stock_step(stock, 0.08, 100.0, harvest, 0.25, 0.25);
  std::cout << "scenario_name,regeneration,extraction,next_stock,warning\n";
  std::cout << "baseline_coupled_resource," << regeneration(stock,0.08,100.0) << "," << harvest << "," << next << ",boundary_human_natural_and_governance_assumptions_required\n";
}
