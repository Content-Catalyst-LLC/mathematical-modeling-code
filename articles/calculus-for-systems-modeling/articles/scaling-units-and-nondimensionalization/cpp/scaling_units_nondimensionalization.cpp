#include <iostream>
#include <string>
#include <vector>

struct Record {
  std::string recordType;
  std::string name;
  std::string value;
  std::string unit;
  std::string interpretation;
  std::string warning;
};

int main() {
  std::vector<Record> records = {
    {"unit_record","population_stock","40","state units","synthetic teaching value","synthetic value do not treat as empirical measurement"},
    {"unit_record","carrying_capacity","100","state units","synthetic teaching capacity","capacity scale controls normalized interpretation"},
    {"unit_record","growth_rate","0.35","per time unit","synthetic teaching rate","rate units must match the time variable"},
    {"scale_record","stock_scale","100","state units","carrying capacity used to normalize population stock","changing the scale changes dimensionless stock"},
    {"nondimensional_record","scaled_stock","0.4","dimensionless","population stock as fraction of carrying capacity","dimensionless form depends on documented scale"}
  };

  std::cout << "record_type,name,value,unit,interpretation,warning\n";
  for (const auto& r : records) {
    std::cout << r.recordType << "," << r.name << "," << r.value << "," << r.unit << "," << r.interpretation << "," << r.warning << "\n";
  }
}
