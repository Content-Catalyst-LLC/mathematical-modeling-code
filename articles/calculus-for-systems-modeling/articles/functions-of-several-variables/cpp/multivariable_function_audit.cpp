#include <iomanip>
#include <iostream>
#include <vector>
double system_response(double x, double y){ return 3.0*x + 2.0*y + 0.5*x*y; }
bool is_feasible(double x, double y){ return x >= 0.0 && y >= 0.0 && x + y <= 10.0; }
int main(){
  std::vector<std::pair<double,double>> cases = {{2.0,4.0},{8.0,4.0},{6.0,3.0}};
  std::cout << std::fixed << std::setprecision(12);
  std::cout << "x,y,output,feasible,warning\n";
  for(auto pair : cases){
    double x = pair.first, y = pair.second;
    bool feasible = is_feasible(x,y);
    std::cout << x << "," << y << "," << system_response(x,y) << "," << feasible << "," << (feasible ? "" : "Input combination is outside the feasible region.") << "\n";
  }
}
