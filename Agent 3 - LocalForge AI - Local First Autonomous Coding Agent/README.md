# LocalForge AI

### Local-First Autonomous Software Engineering Platform

**Plan → Code → Execute → Test → Debug → Review → Ship**

LocalForge AI is an **offline-first autonomous coding platform** designed to build, debug, validate, and ship software using locally hosted open-weight language models.

Instead of sending every engineering request to a paid cloud LLM, LocalForge AI intelligently combines **multi-model routing, repository intelligence, deterministic developer tools, autonomous debugging, and quality gates** to complete software-engineering tasks while minimizing cloud-token dependency.

> **Engineering Goal:** How much of an end-to-end software development workflow can be autonomously completed using local AI models and deterministic tools—with zero cloud LLM API cost?

---

## Why LocalForge AI?

Modern coding agents are powerful, but continuous cloud inference introduces cost, privacy, connectivity, and data-governance considerations.

LocalForge AI explores a different architecture:

**Local inference first. Deterministic tools whenever possible. Larger models only when necessary.**

```text
Developer Request
       │
       ▼
┌──────────────────────┐
│ Task Understanding   │
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│ Planning Agent       │
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│ Repository Retrieval │
│ Files • Symbols • Git│
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│ Intelligent Router   │
└──────────┬───────────┘
           │
     ┌─────┼─────────────┐
     ▼     ▼             ▼
   Phi   gpt-oss      Coding LLM
     │     │             │
     └─────┼─────────────┘
           ▼
┌──────────────────────┐
│ Engineering Agent    │
│                      │
│ Read → Code → Execute│
│   ↑            ↓     │
│ Fix ← Debug ← Test   │
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│ Definition of Done   │
└──────────┬───────────┘
           ▼
     Review → Git → CI
```

---

# Core Capabilities

### Multi-Model Local AI

LocalForge AI uses a model-agnostic routing layer capable of orchestrating multiple locally hosted models.

Initial model registry:

| Model                   | Primary Role                         |
| ----------------------- | ------------------------------------ |
| OpenAI **gpt-oss-20B**  | Planning, coding and debugging       |
| OpenAI **gpt-oss-120B** | Complex reasoning and final review   |
| Microsoft **Phi-4**     | Fast planning and lightweight coding |
| Mistral **Devstral**    | Agentic software engineering         |
| Mistral **Codestral**   | Code generation and completion       |

Models are accessed through local **OpenAI-compatible inference endpoints**, allowing the underlying inference runtime to be replaced without redesigning the agent.

---

## Intelligent Model Routing

Not every engineering problem requires the largest model.

LocalForge AI dynamically routes workloads based on:

* task type
* model role
* endpoint availability
* task complexity
* previous failures
* escalation stage
* latency
* context requirements

If one model becomes unavailable, the router can automatically fall back to another compatible local model.

---

## Autonomous Engineering Loop

LocalForge AI doesn't stop after generating code.

```text
Understand
    ↓
Plan
    ↓
Implement
    ↓
Execute
    ↓
Test
    ↓
Failure?
 ┌──┴──┐
YES    NO
 │      │
Debug   Review
 │      │
Fix     │
 └──────┤
        ↓
 Quality Gate
        ↓
      Ship
```

The agent can iteratively:

* inspect repositories
* create and modify files
* execute development commands
* run tests
* inspect tracebacks
* diagnose failures
* modify implementations
* rerun validation
* review changes
* interact with Git
* prepare GitHub workflows

---

UI Screenshot:

<img width="1917" height="965" alt="image" src="https://github.com/user-attachments/assets/3cbcbcd0-beca-4157-917b-15682bdae30b" />

---


# Code-Style Developer Experience

LocalForge AI includes a local development workbench inspired by modern IDE workflows.

The interface provides:

* 📁 Repository Explorer
* 📝 Multi-file editor
* 💬 Offline AI Agent Chat
* 🤖 Model selector
* 📋 Autonomous Tasks
* 🖥 Integrated Terminal
* 🔀 Source Control
* 📊 Git Diff
* ⚠ Problems panel
* 🔐 Security scanning
* 📈 Model/token telemetry
* 🟢 Agent status

A native VS Code extension layer is also included for interacting with the local agent directly from the development environment.

---

# Repository Intelligence

Large repositories should not be blindly inserted into an LLM context window.

LocalForge AI therefore includes repository-aware retrieval.

```text
Repository
    │
    ├── File Index
    ├── Symbol Index
    ├── Git State
    └── Relevant Source Retrieval
             │
             ▼
       Context Builder
             │
             ▼
          Local LLM
```

Current indexing supports Python and JavaScript/TypeScript codebases, with an architecture designed for additional languages.

This reduces unnecessary context consumption and improves task relevance.

---

# Token-Avoidance Architecture

A core design principle is:

> **Do not use an LLM when deterministic software can solve the problem more reliably.**

Examples:

| Engineering Task       | Preferred Tool        |
| ---------------------- | --------------------- |
| Repository search      | Ripgrep / indexing    |
| Syntax inspection      | AST                   |
| Symbol extraction      | Parser                |
| Unit testing           | Pytest / test runner  |
| Git operations         | Git                   |
| Dependency inspection  | Package tooling       |
| Static validation      | Linters               |
| Security checks        | Secret scanner        |
| Code reasoning         | Local LLM             |
| Architecture reasoning | Local reasoning model |

The platform tracks local model activity and estimates the amount of cloud inference avoided.

---

# Definition-of-Done Engine

An LLM saying *"the task is complete"* does not make software complete.

LocalForge AI uses explicit engineering quality gates.

```text
                 QUALITY GATE

        ┌────────────┼─────────────┐
        ▼            ▼             ▼
      Build        Tests        Security
        │            │             │
        ▼            ▼             ▼
    Compilation    Results       Secrets
        │            │             │
        └────────────┼─────────────┘
                     ▼
                  Review
                     │
               ┌─────┴─────┐
              FAIL         PASS
               │             │
               ▼             ▼
          Agent Iterates   Complete
```

The goal is **evidence-based completion rather than model-declared completion**.

---

# Security by Design

Executing AI-generated code requires strong boundaries.

LocalForge AI includes:

* workspace path isolation
* command allow/block controls
* secret scanning
* destructive-command protection
* network approval gates
* optional Docker execution
* container network isolation
* CPU/memory constraints
* restricted workspace mounting

Remote operations such as GitHub pushes can require explicit authorization.

---

# Git & GitHub Automation

LocalForge AI supports engineering workflows including:

```text
Create Branch
      ↓
Implement
      ↓
Test
      ↓
Review Diff
      ↓
Commit
      ↓
Push
      ↓
Create Pull Request
      ↓
GitHub CI
      ↓
Inspect Failure
      ↓
Fix → Push → CI
```

The objective is to move beyond **code generation** toward **software delivery automation**.

---

# Persistent Autonomous Tasks

Long-running engineering work is represented as persistent tasks.

LocalForge AI stores:

* task history
* execution state
* checkpoints
* agent actions
* validation results
* model usage
* completion state

This allows engineering tasks to be inspected rather than existing only inside an ephemeral chat conversation.

---

# Local Model Architecture

```text
                    Model Router
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
       Planner          Coder        Reviewer
          │              │              │
       Phi-4         Devstral       gpt-oss
          │              │              │
          └──────────────┼──────────────┘
                         ▼
                    Tool Layer
                         │
           ┌─────────────┼─────────────┐
           ▼             ▼             ▼
        Filesystem     Terminal       Git
           │             │             │
           └─────────────┼─────────────┘
                         ▼
                    Validation
```

Model definitions are externalized from the orchestration logic so newer models can be introduced without redesigning the platform.

---

# Project Structure

```text
LocalForge-AI/
│
├── app/
│   ├── agent/
│   ├── routing/
│   ├── retrieval/
│   ├── tools/
│   ├── security/
│   ├── quality/
│   └── api/
│
├── config/
│   └── models.yaml
│
├── ui/
│   ├── explorer/
│   ├── editor/
│   ├── terminal/
│   └── agent-chat/
│
├── vscode-extension/
│
├── tests/
│
├── workspace/
│
├── docs/
│
├── requirements.txt
├── README.md
└── LICENSE
```

---

# Getting Started

### 1. Navigate

```bash
git clone <your-repository>
cd LocalForge-AI
```

### 2. Create an isolated Python environment

```bash
python -m venv .venv
```

Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure Local Models

Configure local inference endpoints in:

```text
config/models.yaml
```

Example architecture:

```text
localhost:8001 → gpt-oss-20B
localhost:8002 → gpt-oss-120B
localhost:8003 → Phi-4
localhost:8004 → Devstral
localhost:8005 → Codestral
```

No cloud LLM API is required for the core local workflow.

### 5. Start LocalForge AI

```bash
python -m app.main
```

Then open the local workbench in your browser.

---

# Example Engineering Request

```text
Build a quantum-computing portfolio optimization application.

Requirements:
- Python backend
- Qiskit implementation
- QAOA algorithm
- interactive UI
- unit tests
- documentation
- Docker support
- Git repository

Run the application and tests.
Diagnose and fix failures.
Review the final implementation.
Do not mark the task complete until the configured quality gates pass.
```

LocalForge AI converts the high-level request into an iterative software-engineering workflow rather than simply returning generated code.

---

# Engineering Principles

**1. Local First**
Core AI inference should be capable of running without a cloud LLM dependency.

**2. Model Agnostic**
Models are replaceable infrastructure components.

**3. Tool First**
Use deterministic engineering tools whenever they can solve the task reliably.

**4. Evidence-Based Completion**
Tests and quality gates determine completion—not model confidence.

**5. Repository Awareness**
Retrieve relevant code rather than blindly filling context windows.

**6. Controlled Autonomy**
Autonomous execution should operate inside explicit security boundaries.

**7. Observable AI**
Model selection, execution, failures, token usage and quality decisions should be measurable.

---

# Roadmap

### Current

* Multi-model local inference
* Intelligent model routing
* Autonomous coding loop
* Repository indexing
* VS Code-style workbench
* VS Code integration
* Git/GitHub tooling
* Persistent tasks
* Security controls
* Quality gates
* Token telemetry

### Next

* Monaco editor integration
* semantic repository embeddings
* context-window budgeting
* patch-based code editing
* parallel specialist agents
* persistent terminal sessions
* GPU-aware model routing
* model performance benchmarking
* automated model launcher
* CI-driven self-repair workflows
* CUDA-accelerated inference and repository analytics

---

# Research & Engineering Direction

LocalForge AI is also an exploration of several broader AI engineering questions:

**Can autonomous software engineering become local-first?**

**Can model routing reduce inference requirements without materially reducing task quality?**

**Can deterministic tooling eliminate unnecessary LLM inference?**

**Can autonomous agents prove completion through engineering evidence rather than self-assessment?**

**How should heterogeneous CPU/GPU resources be scheduled across multiple local AI models?**

These questions drive the architecture and future benchmarking work.

---

# Notes

LocalForge AI is an experimental autonomous software-engineering platform. Review generated changes before deploying them to production environments.

---

# License

Licensed under the **Apache License, Version 2.0**.

Apache 2.0 permits commercial and private use, modification, and distribution subject to its terms, while also providing an explicit patent license.

See the repository's `LICENSE` file for the complete license text.




