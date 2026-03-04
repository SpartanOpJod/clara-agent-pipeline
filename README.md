# Clara Agent Pipeline

## Project Architecture

This repository stores a simple automation pipeline that converts call transcripts into structured account configuration artifacts for a voice agent.

Core components:
- `scripts/`: pipeline scripts (if/when added).
- `workflows/`: declarative workflow definitions.
- `outputs/accounts/<account_id>/`: versioned account artifacts.
- `README.md`: project documentation.

## Pipeline A: Demo -> v1 Agent

Pipeline A processes a demo call transcript and produces initial account outputs:
1. Load transcript.
2. Extract structured account memo.
3. Generate voice agent specification.
4. Store results under `outputs/accounts/<account_id>/v1/`.

For this account, v1 outputs are in `outputs/accounts/ben_electric/v1/`.

## Pipeline B: Onboarding -> v2 Agent

Pipeline B processes onboarding updates and creates the next version:
1. Load onboarding call notes/transcript.
2. Update memo with confirmed details only.
3. Regenerate agent spec for the new version.
4. Store results under `outputs/accounts/<account_id>/v2/`.

For this account, v2 outputs are in `outputs/accounts/ben_electric/v2/`.

## Folder Structure

```text
clara-agent-pipeline/
  outputs/
    accounts/
      ben_electric/
        v1/
          memo.json
          agent_spec.json
        v2/
          memo.json
          agent_spec.json
        changelog.json
  workflows/
    demo_pipeline.json
  scripts/
  README.md
```

## How Outputs Are Stored

Each account is stored in a dedicated folder: `outputs/accounts/<account_id>/`.

Each version folder (`v1`, `v2`, etc.) contains:
- `memo.json`: extracted business configuration data.
- `agent_spec.json`: generated voice agent configuration.

Account-level `changelog.json` tracks version history and source context.

## Limitations Due to Missing Demo Data

This dataset has incomplete operational details. Missing or blank fields are intentionally preserved.

Known limitations include:
- business hours are unspecified,
- office address is missing,
- services supported are not defined,
- emergency definition is not provided,
- transfer routing rules are not fully configured.

The generated agent specs include safe fallback behavior and avoid inventing unsupported business rules.
