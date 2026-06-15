#include <cmath>
#include <iomanip>
#include <iostream>
#include <vector>

double population(double t){ return 100.0 * std::exp(0.01 * t); }
double population_rate(double t){ return 0.01 * population(t); }
double affluence(double t){ return 2.0 * std::exp(0.02 * t); }
double affluence_rate(double t){ return 0.02 * affluence(t); }

int main(){
  std::vector<double> ts={0.0,5.0,10.0,20.0};
  std::cout<<std::fixed<<std::setprecision(12);
  std::cout<<"rule,model_structure,t,derivative_value,component_a,component_b,warning\n";
  for(double t:ts){
    double a=population_rate(t)*affluence(t);
    double b=population(t)*affluence_rate(t);
    std::cout<<"product_rule,impact = population * affluence,"<<t<<","<<a+b<<","<<a<<","<<b<<",\n";
  }
}
