package main

import (
	"fmt"
	"os"
)

type Artifact struct {
	Name     string
	Path     string
	Required bool
}

func exists(path string) bool {
	_, err := os.Stat(path)
	return err == nil
}

func main() {
	artifacts := []Artifact{
		{"README", "README.md", true},
		{"metadata", "article-metadata.yml", true},
		{"Makefile", "Makefile", true},
		{"data folder", "data", true},
		{"docs folder", "docs", true},
		{"schemas folder", "schemas", false},
		{"canvas manifest", "canvas/canvas_manifest.json", false},
	}

	fmt.Println("artifact,path,required,exists")
	for _, artifact := range artifacts {
		fmt.Printf("%s,%s,%t,%t\n", artifact.Name, artifact.Path, artifact.Required, exists(artifact.Path))
	}
}
