#include <algorithm>
#include <iomanip>
#include <iostream>
#include <string>
struct Scenario{std::string name; double stock, cap, inflow, demand, loss; int periods;};
int main(){ Scenario s{"cpp_constraint_stress",40,60,3,7,0.05,60}; double total_shortage=0,total_overflow=0,stock=s.stock; for(int p=0;p<=s.periods;++p){ double losses=s.loss*stock; double raw=stock+s.inflow-s.demand-losses; total_shortage += std::max(0.0,-raw); total_overflow += std::max(0.0,raw-s.cap); stock=std::min(s.cap,std::max(0.0,raw)); } std::cout<<std::fixed<<std::setprecision(6)<<"cpp final_stock="<<stock<<" total_shortage="<<total_shortage<<" total_overflow="<<total_overflow<<"\n"; }
