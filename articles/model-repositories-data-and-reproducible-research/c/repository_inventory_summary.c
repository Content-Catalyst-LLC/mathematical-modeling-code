#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>

int exists(const char *path) {
    struct stat buffer;
    return stat(path, &buffer) == 0;
}

int main(void) {
    const char *names[] = {"README", "metadata", "Makefile", "data folder", "docs folder", "schemas folder", "canvas manifest"};
    const char *paths[] = {"README.md", "article-metadata.yml", "Makefile", "data", "docs", "schemas", "canvas/canvas_manifest.json"};
    int required[] = {1, 1, 1, 1, 1, 0, 0};
    int count = 7;

    printf("artifact,path,required,exists\n");
    for (int i = 0; i < count; ++i) {
        printf("%s,%s,%s,%s\n", names[i], paths[i], required[i] ? "true" : "false", exists(paths[i]) ? "true" : "false");
    }

    fprintf(stderr, "c repository_inventory_summary complete\n");
    return EXIT_SUCCESS;
}
