# MARLIN: Multi-Agent Robotic Language-based Indoor Navigation 🤖🧠

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Environment: AI2-THOR](https://img.shields.io/badge/Environment-AI2--THOR-green)](https://ai2thor.allenai.org/)

**MARLIN** is a hybrid Neuro-Symbolic planning architecture designed for complex, long-horizon indoor navigation tasks involving heterogeneous multi-agent robot teams. 

This repository contains the core implementation of a system that bridges the gap between the flexible reasoning of **Large Language Models (LLMs)** and the logical absolute safety of **Symbolic Planning (PDDL)**, all grounded by a **Retrieval-Augmented Generation (RAG)** based long-term memory module.

## 🌟 Key Features

* **Central LLM Planner (πLLM):** Translates high-level natural language instructions (e.g., *"Find the phone using two robots"*) into an executable, Pythonic Domain-Specific Language (DSL).
* **Symbolic Validator (PDDL Engine):** Automatically translates the generated Pythonic DSL into formal PDDL problems and verifies them against domain constraints using the Fast Downward engine.
* **Contextual Long-Term Memory (RAG):** Utilizes `ChromaDB` to store environmental rules, API definitions, and historical state changes ($H = \{s_1, s_2, \dots, s_t\}$), allowing the LLM to avoid hallucinations.
* **Dynamic Feedback Loop:** Captures execution errors or logical failures and feeds them back to the LLM as *Error Predicates* for iterative plan correction.
* **Multi-Agent Execution:** Seamlessly executes validated tasks within the AI2-THOR 3D physical simulation environment.

## 🏗️ Architecture Overview

The pipeline follows a **Proposal-Execution-Feedback-Adjustment (PEFA)** loop:
1. **User Input:** Natural language task instruction.
2. **Memory Retrieval:** RAG pulls relevant environmental rules and state history.
3. **Task Decomposition:** LLM generates a Pythonic DSL plan.
4. **Formal Verification:** DSL is parsed into PDDL and verified.
5. **Execution & Feedback:** Valid plans are sent to AI2-THOR; errors trigger a dynamic feedback loop for replanning.

## 📂 Repository Structure

```text
thesis_project/
├── config/              # YAML configurations for models, prompts, and environment
├── data/
│   ├── pddl/            # Generated PDDL domain and problem files
│   └── wiki/            # AI2-THOR API and PDDL mappings (Markdown)
├── scripts/             # Utility scripts (e.g., metrics evaluation, wiki generation)
├── src/
│   ├── core/            # Error handling and central logging
│   ├── memory/          # RAG module (ChromaDB client, Context Builder)
│   ├── planner/         # LLM Agent (Mistral/LLaMA/GPT) and DSL Generator
│   ├── validator/       # Symbolic Validator (PDDL parser, Fast Downward API)
│   ├── execution/       # AI2-THOR environment wrapper and Task Allocator
│   └── feedback/        # Dynamic Error Handler
└── tests/               # Unit and integration tests
```

## 🚀 Quick Start

### 1. Installation
Clone the repository and install the required dependencies:
```bash
git clone https://github.com/yourusername/marlin-nav.git
cd marlin-nav
pip install -r requirements.txt
```

### 2. Setup Vector Database (RAG)
Initialize the local ChromaDB and embed the environmental rules from the wiki:
```bash
python -m src.memory.context_builder
```

### 3. Run the Planner (Mock/Test Mode)
Test the Pythonic DSL generation with a mock LLM setup:
```bash
python -m src.planner.llm_agent
```

### 4. Validate with PDDL
Run the DSL to PDDL parser to ensure logical validity:
```bash
python -m src.validator.dsl_parser
```

## 📝 License
This project is licensed under the MIT License - see the LICENSE file for details.