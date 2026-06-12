# Scientific Computing Workflow Specification

## Article

**Scientific Computing for Modeling Workflows**

## Central claim

A modeling workflow is a reproducible mapping from data, parameters, configuration, code, and environment to outputs, diagnostics, metadata, and review artifacts.

## Required workflow records

| Field | Purpose |
|---|---|
| key | Stable identifier |
| workflow_stage | data_intake, parameter_control, model_execution, output_generation, reproducibility, validation, governance |
| computational_object | File, command, script, schema, manifest, model component, or output |
| modeling_role | Plain-language role in the modeling process |
| review_question | Review question |
| status | active, review, revise, or archive |

## High-priority records

High-priority records include input schemas, configuration files, data provenance, model execution scripts, random seeds, software environment metadata, output indexes, validation checks, run manifests, and audit cards.
