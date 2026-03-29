# Prompt Policy

## Purpose

Define quality and governance standards for prompt authoring in Contact360.

## Policy Rules

- Use canonical paths from `docs/architecture.md`.
- Do not embed real credentials or tokens.
- Include explicit service ownership in each prompt.
- Include era mapping (`0.x` to `10.x`) where relevant.
- Include a small-task breakdown for implementation prompts.
- Keep prompts measurable (clear acceptance criteria).

## Required Metadata Block

Each prompt file should include:

- `Scope`
- `Services`
- `Era`
- `Inputs`
- `Expected Outputs`
- `Validation`
- `Risks`
- `Small Tasks`

## Sync Rules

When roadmap/version/architecture semantics change, update prompt packs in the same change set.
