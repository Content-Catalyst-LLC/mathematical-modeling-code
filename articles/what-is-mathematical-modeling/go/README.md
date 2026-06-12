# Go Workflow

This folder may contain both the original `logistic_model.go` from the first scaffold and the upgraded `main.go` from the quality upgrade.

The article-level `Makefile` intentionally runs:

```bash
cd go && go run main.go
```

instead of:

```bash
go run .
```

This preserves the older file without deleting it while avoiding duplicate declarations of `main`, `LogisticModel`, and helper functions.

Future cleanup option: merge the older file into `main.go` or move it into an archived example package.
