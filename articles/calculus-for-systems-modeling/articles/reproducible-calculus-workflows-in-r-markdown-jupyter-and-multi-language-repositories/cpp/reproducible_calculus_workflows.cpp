#include <iostream>
#include <string>
#include <vector>

struct Artifact {
  std::string name;
  std::string type;
  std::string path;
  std::string origin;
  std::string role;
  std::string warning;
};

int main() {
  std::vector<Artifact> artifacts = {
    {"parameter_records","csv","data/parameter_records.csv","source","documents parameter names values units sources and ranges","Parameter records do not prove empirical correctness."},
    {"model_outputs","csv","outputs/tables/model_outputs.csv","generated","stores computed trajectory or summary outputs","Generated outputs require diagnostics and interpretation limits."},
    {"diagnostics","json","outputs/json/diagnostics.json","generated","records validation convergence and warning status","Diagnostics should remain attached to interpretation."},
    {"governance_queue","markdown","outputs/reports/governance_queue.md","generated","collects warnings requiring human review","Governance queues support judgment but do not replace it."}
  };

  std::cout << "artifact_name,artifact_type,path,source_or_generated,review_role,warning\n";
  for (const auto& a : artifacts) {
    std::cout << a.name << "," << a.type << "," << a.path << "," << a.origin << "," << a.role << "," << a.warning << "\n";
  }
}
