#include <cmath>
#include <iostream>
#include <string>
#include <vector>

struct Record {
  std::string parameter;
  double baseline;
  double lower;
  double upper;
  std::string status;
  std::string warning;
};

int main() {
  std::vector<Record> records = {
    {"growth_rate",0.35,0.20,0.50,"sensitive","conclusion may depend on growth-rate assumptions"},
    {"carrying_capacity",100.0,75.0,125.0,"sensitive","capacity scale affects final stock interpretation"},
    {"initial_stock",10.0,5.0,20.0,"stable","output variation is limited across this synthetic range"}
  };
  std::cout << "parameter_name,baseline_value,lower_bound,upper_bound,status,warning\n";
  for (const auto& r : records) {
    std::cout << r.parameter << "," << r.baseline << "," << r.lower << "," << r.upper << "," << r.status << "," << r.warning << "\n";
  }
}
