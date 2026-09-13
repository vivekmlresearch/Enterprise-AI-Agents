# SovereignCodeAgent v0.3

A local-first autonomous coding agent with a VS Code-style workbench. It uses locally served open-weight models, repository retrieval, deterministic engineering tools, iterative debugging, quality gates, Git/GitHub workflows, and live task events.

## Default local model registry

- OpenAI gpt-oss-20B
- OpenAI gpt-oss-120B
- Microsoft Phi-4
- Mistral Devstral Small 2
- Mistral Codestral

Each model is configured behind an OpenAI-compatible local `/v1` endpoint in `config/models.yaml`. The agent itself does not require a paid cloud LLM API.

## v0.3 engineering layer

- Native VS Code extension commands and status bar
- VS Code-style browser workbench: activity bar, Explorer, Tasks, Models, Security, Source Control, editor tabs, line-number editor, Agent chat, Terminal, Output, Git Diff, Problems and status bar
- Automatic local model fallback/routing
- Planner → coder/debugger → independent reviewer orchestration
- Autonomous edit → execute → debug → retest loop
- Persistent SQLite task history and checkpoints
- Background tasks plus Server-Sent Events for live agent activity
- Git branch/status/diff/commit/push tools
- GitHub CLI repository creation, PR, CI status and failed-log tools
- Explicit network approval gate
- Repository retrieval and Python/JS/TS symbol indexing
- Secret scanning and command blocking
- Definition-of-Done quality gate
- Local token telemetry / estimated cloud-token avoidance
- Optional Docker-isolated command runner with network disabled

## Quick start

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
python -m app.main
```

Open `http://127.0.0.1:8000`.

## Local model endpoints

By default:

- `8001` → gpt-oss-20b
- `8002` → gpt-oss-120b
- `8003` → Phi-4
- `8004` → Devstral Small 2
- `8005` → Codestral

Serve whichever models your hardware can support using an OpenAI-compatible local runtime. Offline fallback means unavailable endpoints are skipped automatically.

## Optional isolated execution

Build the sandbox image:

```bash
docker build -f Dockerfile.sandbox -t sovereign-code-agent-sandbox:latest .
```

Then set `SCA_USE_DOCKER=true`. Agent shell commands are run inside an ephemeral container with `--network none`, CPU and memory limits, and only the workspace mounted.

## VS Code extension

Open `vscode-extension/` and install/package it as a local extension. Commands include:

- `SovereignCodeAgent: Open Local Workbench`
- `SovereignCodeAgent: Run Autonomous Task`
- `SovereignCodeAgent: Run Quality Gate`
- `SovereignCodeAgent: Check Local Models`
- `SovereignCodeAgent: Show Git Diff`

## Completion semantics

The agent is not allowed to mark a task complete merely because a model says so. It must first pass the detected quality gates and then undergo an independent reviewer step. This is a practical Definition of Done, not a mathematical guarantee that arbitrary software contains zero defects.
