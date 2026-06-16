#include <iostream>
#include <string>
#include <vector>

struct Record {
  std::string recordType;
  std::string name;
  std::string roleOrProcess;
  std::string evidenceOrRequirement;
  std::string status;
  std::string warning;
};

int main() {
  std::vector<Record> records = {
    {"mechanism_record","stock_flow_accumulation","stock changes through inflow and outflow","synthetic teaching example","review","flows must represent real processes"},
    {"mechanism_record","balancing_feedback","state-dependent adjustment limits growth","formal teaching example","review","feedback parameters require evidence"},
    {"formal_record","differential_equation","dxdt=f","process interpretation required","review","rate equation needs mechanism meaning"},
    {"claim_record","mechanistic","organized process produces behavior","process evidence required","review","scope depends on assumptions"},
    {"claim_record","exploratory","investigates possible behavior","scenario assumptions required","active","not a confirmed mechanism or forecast"}
  };
  std::cout << "record_type,name,role_or_process,evidence_or_requirement,status,warning\n";
  for (const auto& r : records) {
    std::cout << r.recordType << "," << r.name << "," << r.roleOrProcess << "," << r.evidenceOrRequirement << "," << r.status << "," << r.warning << "\n";
  }
}
