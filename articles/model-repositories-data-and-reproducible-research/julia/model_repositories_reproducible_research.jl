# Julia workflow for model repositories, data, and reproducible research.
# Dependency-light: Base + standard libraries only.

using Printf
using Dates
using SHA

struct ExpectedArtifact
    artifact::String
    path::String
    required::Bool
    purpose::String
end

function sha_for_file(path::String)
    if !isfile(path)
        return "not_applicable"
    end
    return bytes2hex(open(sha256, path))
end

function main()
    artifacts = [
        ExpectedArtifact("README", "README.md", true, "Project overview"),
        ExpectedArtifact("metadata", "article-metadata.yml", true, "Article metadata"),
        ExpectedArtifact("Makefile", "Makefile", true, "Workflow targets"),
        ExpectedArtifact("data folder", "data", true, "Data and metadata"),
        ExpectedArtifact("docs folder", "docs", true, "Documentation"),
        ExpectedArtifact("schemas folder", "schemas", false, "Validation schemas")
    ]

    println("repository_inventory_run=", Dates.now())
    println("artifact,path,required,exists,sha256")

    for item in artifacts
        exists_flag = isfile(item.path) || isdir(item.path)
        hash_value = sha_for_file(item.path)
        @printf("%s,%s,%s,%s,%s\n", item.artifact, item.path, item.required, exists_flag, hash_value)
    end
end

main()
