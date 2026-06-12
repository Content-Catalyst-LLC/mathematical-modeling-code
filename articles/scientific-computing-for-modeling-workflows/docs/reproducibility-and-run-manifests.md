# Reproducibility and Run Manifests

A run manifest records the computational context that produced model outputs.

## Minimum fields

- article or model name;
- run timestamp;
- command or script;
- software versions;
- platform information;
- input files;
- configuration values;
- random seeds;
- output file paths;
- output hashes;
- validation or smoke-check status.

## Principle

A modeling result that cannot be rerun or traced cannot be responsibly audited.
