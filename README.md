<div align="center">

<!-- Dynamic Typing SVG Header -->
<p align="center">
  <a href="https://git.io/typing-svg">
    <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=22&pause=1000&color=61DAFB&center=true&vCenter=true&width=750&lines=Hi+there,+I'm+Afnan+Mojumder+%F0%9F%91%8B;Systems+Software+%C2%B7+Compilers+%C2%B7+Applied+AI;CS+Undergrad+%40+BRAC+University;Upstream+Open+Source+Contributor+(Rust,+C%2B%2B,+Python)" alt="Typing SVG" />
  </a>
</p>

<p align="center">
  <strong>Systems Engineering • Low-Level Runtimes • Applied AI & Mobile Architecture</strong>
</p>

<!-- Social Connect Badges -->
<p align="center">
  <a href="https://www.linkedin.com/in/afnan-mojumder/" target="_blank">
    <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" />
  </a>
  <a href="mailto:afnan.mojumder@gmail.com">
    <img src="https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white" alt="Email" />
  </a>
  <a href="https://github.com/afnan-mojumder">
    <img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub" />
  </a>
  <img src="https://img.shields.io/badge/Location-Dhaka%2C%20Bangladesh-008080?style=for-the-badge&logo=googlemaps&logoColor=white" alt="Location" />
</p>

<!-- Terminal Profile Card -->
<p align="center">
  <img src="./info-card.svg" alt="Terminal Profile Card" width="520" />
</p>

---

</div>

### 🚀 About Me

- 🎓 **Education:** Pursuing B.Sc. in Computer Science & Engineering at **BRAC University** (Dhaka, Bangladesh • Expected May 2027)
- ⚙️ **Systems & Infrastructure:** Deep focus on low-level performance, Linux syscalls & internals, compilers, graphics pipelines (Vulkan, SPIR-V), and asynchronous runtime design (Rust, C/C++)
- 🤖 **Applied AI & Agentic Systems:** Developing multi-agent architectures, on-device SLMs (`Gemma`, `EmbeddingGemma`, `Qwen`), RAG pipelines, explainable AI (SHAP/LIME), and LLM gateway tooling (`LiteLLM`, `TRL`, `llama.cpp`)
- 📱 **Mobile & Modern Web:** Architecting offline-first mobile systems in **Flutter/Dart** (Riverpod, Isar) and high-throughput web platforms (**Next.js 16**, **React 19**, **FastAPI**, **TypeScript**)
- 🌐 **Upstream Open Source:** Prolific contributor to critical systems software, reverse proxies, eBPF libraries, and translation layers

---

### 🌐 Upstream Open Source Contributions

I actively contribute upstream to production infrastructure, systems software, and developer tooling:

| Repository | Tech Stack | Contribution Highlight |
| :--- | :--- | :--- |
| **[uutils/coreutils](https://github.com/uutils/coreutils)** | `Rust` | Implemented GNU Coreutils 9.12 error-parity diagnostics for cross-device directory fallbacks, delivering a **+20.6% performance speedup** on the `mv_force_overwrite` benchmark (CodSpeed). |
| **[cloudflare/pingora](https://github.com/cloudflare/pingora)** | `Rust` | Authored dynamic retry policies, asynchronous exponential backoff hooks (`retry_backoff`), and per-session attempt tracking for Cloudflare's high-scale proxy framework. |
| **[BerriAI/litellm](https://github.com/BerriAI/litellm)** | `Python` | Co-authored upstream PR #49474 implementing bearer auth forwarding and environment secret expansion across Agent-to-Agent (A2A) hops. |
| **[falcosecurity/libs](https://github.com/falcosecurity/libs)** | `C++` | Preserved layer-4 transport protocols across IPv6-to-IPv4-mapped socket transitions in the Linux kernel security event engine. |
| **[aya-rs/aya](https://github.com/aya-rs/aya)** | `Rust` | Extended pure-Rust eBPF introspection by exposing program section names across all 29 concrete program types. |
| **[vkd3d-proton](https://github.com/HansKristian-Work/vkd3d-proton) / [dxil-spirv](https://github.com/HansKristian-Work/dxil-spirv)** | `C` `C++` | Direct3D 12 to Vulkan translation and SPIR-V compiler fixes (Hull Shader varyings, mesh shader workgroup payloads, barrier scoping). |
| **[huggingface/trl](https://github.com/huggingface/trl)** | `Python` | Handled Qwen3.5 tool-calling reasoning boundary handling in reinforcement learning training pipelines. |

---

### 💼 Featured Projects

| Project | Description | Tech Stack | Repository |
| :--- | :--- | :--- | :--- |
| **[DocFlow](https://github.com/afnan-mojumder/DocFlow)** | Universal local-first document processing platform combining deterministic conversions (PDF, Office, Images, OCR) with zero-API-key local table & entity parsing, WebAssembly tools, and Bubblewrap sandboxing. | `Next.js 16` `React 19` `TypeScript` `FastAPI` `Python 3.12` `Bubblewrap` | [afnan-mojumder/DocFlow](https://github.com/afnan-mojumder/DocFlow) |
| **[DistillEd](https://github.com/Nishmam12/DistillEd)** | Offline-first Flutter notebook and AI study platform featuring an Excalidraw-style canvas, shape recognition, palm rejection, vector/stroke erasing, and local Gemma/EmbeddingGemma on-device models. Verified with **1,380+ tests**. | `Flutter` `Dart` `Gemma` `EmbeddingGemma` `ML Kit` `Riverpod` | [Nishmam12/DistillEd](https://github.com/Nishmam12/DistillEd) |
| **[The Committee (QuantAgent)](https://github.com/sharzilnfz/QuantAgent)** | Multi-agent quantitative paper-trading reference architecture with Alpaca ingestion, point-in-time safeguards (`TemporalGuard`), deterministic offline replay under a 3-second SLA, and fractional-Kelly volatility allocation. | `TypeScript` `Python` `Alpaca API` `PostgreSQL` | [sharzilnfz/QuantAgent](https://github.com/sharzilnfz/QuantAgent) |
| **Explainable AI for IIoT Anomaly Detection** | Reproducible Edge-IIoTset benchmark study comparing deep anomaly detection models, evaluating KernelSHAP/LIME fidelity and coupling with SLMs (Qwen2.5) to synthesize grounded incident triage narratives. | `PyTorch` `SHAP` `LIME` `Qwen2.5-1.5B` `Edge-IIoTset` | *Academic Research* |
| **[Wayfarer](https://github.com/Nishmam12/matha-noshto-game)** | Retro exploration game engine strictly constrained to a 1.44 MB floppy disk with automated build size-gate enforcement, custom RLE sprite compression, and resilient world generation. | `C99` `SDL2` `PowerShell` | [Nishmam12/matha-noshto-game](https://github.com/Nishmam12/matha-noshto-game) |

---

### 🛠️ Tech Stack & Tooling

<div align="center">

#### Systems & Languages
<a href="https://skillicons.dev">
  <img src="https://skillicons.dev/icons?i=rust,c,cpp,python,dart,ts,js,go,bash" alt="Systems and Languages" />
</a>

#### Frameworks & Modern Runtimes
<a href="https://skillicons.dev">
  <img src="https://skillicons.dev/icons?i=flutter,react,nextjs,fastapi,nodejs,express,tailwind" alt="Frameworks" />
</a>

#### AI / ML & Scientific Computing
<a href="https://skillicons.dev">
  <img src="https://skillicons.dev/icons?i=pytorch,tensorflow,pandas,numpy,opencv" alt="AI and Machine Learning" />
</a>

#### Databases, Cloud & DevOps
<a href="https://skillicons.dev">
  <img src="https://skillicons.dev/icons?i=linux,docker,postgres,mongodb,mysql,redis,git,github,githubactions,cloudflare,vscode" alt="Tools and Infrastructure" />
</a>

</div>

---

### 📊 GitHub Activity & Metrics

<p align="center">
  <img src="https://img.shields.io/github/followers/afnan-mojumder?label=Followers&style=for-the-badge&color=238636&logo=github" alt="Followers" />
  <img src="https://img.shields.io/badge/Status-Active%20Building%20%26%20Contributing-58a6ff?style=for-the-badge&logo=codefactor" alt="Status" />
  <img src="https://img.shields.io/badge/Focus-Systems%20%26%20AI-orange?style=for-the-badge&logo=rust" alt="Focus" />
</p>

<p align="center">
  <img src="./contrib-heatmap.svg" alt="Afnan's GitHub Contribution Heatmap" width="100%" />
</p>

---

<div align="center">
  <sub>Engineered with precision by Afnan Mojumder • © 2026</sub>
</div>
