#include <iomanip>
#include <iostream>
#include <vector>

double system_response(double x, double y){ return 3.0*x + 2.0*y + 0.5*x*y; }
double partial_x(double, double y){ return 3.0 + 0.5*y; }
double partial_y(double x, double){ return 2.0 + 0.5*x; }
double cross_partial_xy(double, double){ return 0.5; }
bool is_feasible(double x, double y){ return x >= 0.0 && y >= 0.0 && x + y <= 10.0; }

int main(){
  std::vector<std::pair<double,double>> cases = {{2.0,4.0},{8.0,4.0},{6.0,3.0}};
  std::cout << std::fixed << std::setprecision(12);
  std::cout << "x,y,output,partial_x,partial_y,cross_partial_xy,feasible,warning\n";
  for(auto pair : cases){
    double x = pair.first, y = pair.second;
    bool feasible = is_feasible(x,y);
    std::cout << x << "," << y << "," << system_response(x,y) << "," << partial_x(x,y) << "," << partial_y(x,y) << "," << cross_partial_xy(x,y) << "," << feasible << "," << (feasible ? "" : "Input combination is outside the feasible region.") << "\n";
  }
}
