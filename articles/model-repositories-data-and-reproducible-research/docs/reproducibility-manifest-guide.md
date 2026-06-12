# Reproducibility Manifest Guide

A reproducibility manifest records what is needed to regenerate repository outputs.

## Recommended fields

- article or model name;
- run timestamp;
- repository version or commit;
- software and platform context;
- input files and schemas;
- configuration and parameter files;
- random seeds;
- commands or workflow targets;
- output paths;
- output hashes;
- validation status;
- limitations and intended-use notes.

## Principle

A model result should be traceable from output back to code, data, configuration, and environment.
