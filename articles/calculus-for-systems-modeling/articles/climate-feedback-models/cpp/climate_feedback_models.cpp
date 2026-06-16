#include <cmath>
#include <iostream>

double one_box(double forcing, double feedback, double heat_capacity, double time){
  double equilibrium = forcing / feedback;
  return equilibrium * (1.0 - std::exp(-(feedback / heat_capacity) * time));
}

int main(){
  double forcing=3.7, c=8.0;
  std::cout << "time,weak_feedback,baseline_feedback,strong_feedback\n";
  for(int t=0;t<=100;t+=10){
    std::cout << t << "," << one_box(forcing,0.9,c,t) << "," << one_box(forcing,1.2,c,t) << "," << one_box(forcing,1.6,c,t) << "\n";
  }
}
