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

## Engineering decisions

* **Local-first, model-agnostic inference.** LocalForge AI communicates with locally hosted models through a common inference interface rather than coupling the agent to a single model or vendor. The initial registry supports **OpenAI gpt-oss-20B / 120B, Microsoft Phi-4, Mistral Devstral, and Codestral**. Models can be replaced or upgraded without redesigning the orchestration layer.

* **Deterministic tools before LLM inference.** Repository search, symbol extraction, Git operations, test execution, static analysis, and security checks are delegated to deterministic developer tools whenever possible. LLM inference is reserved primarily for planning, implementation, debugging, code review, and architectural reasoning. This improves reproducibility while reducing unnecessary inference and context consumption.

* **Role-aware model routing instead of one-model-for-everything.** Coding tasks have different computational requirements. LocalForge AI separates planning, coding, debugging, and final-review responsibilities and routes each workload to an appropriate available model. Failed or complex tasks can escalate to stronger models instead of paying the computational cost of running the largest model for every request.

* **Evidence-based completion instead of model-declared completion.** An autonomous model is not allowed to treat its own confidence as proof that a task is finished. LocalForge AI uses a Definition-of-Done pipeline built around executable evidence: compilation/build status, automated tests, security checks, Git state, and independent review. Failed validation returns the task to the engineering loop for diagnosis and repair.

---

## Model data, licensing, and compliance

* **LocalForge AI source code and model weights are separately licensed artifacts.** The project's software license does not override the license, acceptable-use requirements, attribution requirements, redistribution conditions, or other terms associated with individual model weights. Users are responsible for reviewing the applicable license before downloading, redistributing, modifying, or deploying a model.

* **Local inference is the default architectural boundary.** Prompts, repository source code, retrieved context, test output, and agent reasoning can remain on the machine running LocalForge AI when local inference is used. Core coding-agent operation does not require sending repository content to a commercial cloud LLM API.

* **Network-capable operations are separated from local reasoning.** GitHub push, pull-request creation, remote CI inspection, model downloads, package installation, and similar operations inherently require external connectivity. These operations are treated separately from offline inference and can be protected through explicit network/authorization gates.

* **Autonomous execution is security-sensitive.** Model-generated commands execute only through the platform's controlled tool layer, which provides workspace path restrictions, destructive-command controls, secret scanning, and optional container isolation. Credentials and tokens should never be embedded in prompts, model configuration, source files, or committed repository history. Production deployments should additionally use OS/container-level sandboxing and least-privilege credentials.


---

## Known limitations and roadmap

* **Local model quality and performance are hardware-dependent.** Large models such as gpt-oss-120B require substantially more compute and memory than lightweight models such as Phi-4. Current routing considers model role and endpoint availability; **GPU/VRAM-aware scheduling, latency prediction, model benchmarking, and dynamic resource allocation** are planned improvements.

* **Repository retrieval is currently structural rather than fully semantic.** LocalForge AI indexes files and programming-language symbols to avoid injecting an entire repository into the context window. A future retrieval layer will add local embeddings, semantic code search, dependency-aware context construction, and explicit context-window budgeting for very large repositories.

* **Autonomous validation reduces risk but cannot guarantee bug-free software.** Passing builds, tests, security checks, and reviewer gates provides stronger evidence of completion than model self-assessment, but it does not prove correctness for arbitrary software. Planned improvements include generated regression tests, mutation testing, coverage-aware validation, static-analysis integration, and CI-driven repair loops.

* **The Code-style workbench is still evolving toward a complete IDE experience.** The current implementation provides repository exploration, editing, agent chat, tasks, model status, terminal execution, source-control information, security checks, and diff/output views. Planned work includes Monaco-based editing, persistent terminal sessions, interactive Git staging, patch-based edits, parallel specialist agents, semantic repository memory, and richer execution telemetry.

---

## License

LocalForge AI source code is licensed under the **[Apache License 2.0](LICENSE)**.

The license permits use, modification, distribution, and commercial use subject to the Apache License 2.0 terms and includes an explicit patent-license grant.

**Model weights and third-party components retain their own licenses.** In particular, downloading or running OpenAI, Microsoft, Mistral, or other third-party models through LocalForge AI does not cause those model weights to become licensed under Apache 2.0.

Before distributing a packaged LocalForge AI installation containing model weights, review and comply with the license and redistribution requirements of every included model and dependency.





