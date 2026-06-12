#include <filesystem>
#include <iostream>
#include <string>
#include <vector>

struct Artifact {
    std::string name;
    std::string path;
    bool required;
};

int main() {
    std::vector<Artifact> artifacts = {
        {"README", "README.md", true},
        {"metadata", "article-metadata.yml", true},
        {"Makefile", "Makefile", true},
        {"data folder", "data", true},
        {"docs folder", "docs", true},
        {"schemas folder", "schemas", false},
        {"canvas manifest", "canvas/canvas_manifest.json", false}
    };

    std::cout << "artifact,path,required,exists\n";
    for (const auto& item : artifacts) {
        std::cout << item.name << ","
                  << item.path << ","
                  << (item.required ? "true" : "false") << ","
                  << (std::filesystem::exists(item.path) ? "true" : "false") << "\n";
    }

    return 0;
}
