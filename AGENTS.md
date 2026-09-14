# AGENTS.md — Repository Router

**Structural class:** F — product / application / code repository. See [TBHRC GitHub Repository Pre-Structure](https://github.com/tbhrc/org/blob/main/700-architecture/organisation-pre-structure.md).

<!-- ROUTER_SHARED_LIFECYCLE_START -->
**KISSS:** Execute authorised work through the shortest capable path. Route from the action required, not words or topics in the request.
**Progressive depth:** Do not preload documentation, Skills, memory, policies or orchestration. If direct execution is insufficient or ownership is materially unclear, open [Conditional Routing](https://github.com/tbhrc/skills/blob/main/templates/AGENTS.routing-depth.md) and follow only the smallest relevant branch.
**Canon:** GitHub `main` is mutable canon. Write durable corrections or mutations to the owning repository; repository boundaries represent ownership, not artificial internal information walls.
**Friction:** Issues and process machinery are optional. Do not stop useful authorised work for ceremony. Do not narrow permissions, runtime reach or tools without a concrete current boundary. Do not add machinery unless it materially reduces time, work or maintenance.
**Boundaries:** Human approval is reserved for root/super-admin authority changes, destructive or irreversible actions, spend, legal/compliance commitments, external private-data disclosure, or material external/client commitments. Never expose secrets or unnecessary private data.
**Concurrency:** Keep one active writer only where concurrent writes could actually collide.
**Stop:** Verify the requested outcome once, reconcile durable state only when applicable, then stop.
<!-- ROUTER_SHARED_LIFECYCLE_END -->

**FolderDesk by iMPLEMENTAi owns the portable, non-secret deployment and recovery architecture for reproducing a working Business AI Operating System; mutable live business/system truth stays with its current owner. The existing ChatGPT FolderDesk connector binding at `https://brain.xva.ae/mcp-http/mcp` is current operational capital and the preferred single ChatGPT ingress to the execution mesh. Preserve that enabled binding while backend/runtime wiring evolves; route authorised node execution behind it rather than creating one ChatGPT connector per machine. Current live node routes are VPS and Mac; the home-server node is reserved in the contract and remains unavailable until its real authorised transport is identified. Replace or recreate the binding only on explicit founder direction after a replacement is live-proven.**

**Repository Fast Links:** [README](README.md) · [Atlas](ATLAS.md) · [Architecture](ARCHITECTURE.md) · [FolderDesk Parity](.github/workflows/reconcile-public-skills.yml) · [Public Skill Allowlist](profiles/tbhrc-reference/public-skill-export.json) · [Issues](https://github.com/tbhrc/folderdesk/issues)

## Route

- **Client-facing onboarding, status or business artifact** → use [Client Experience](starter/skills/client-experience/SKILL.md): treat GitHub as backend infrastructure, learn/adapt tone + output expectations, request brand guidelines or representative documents, discover useful connectors, and default natural business-document outputs to polished DOCX/PDF. Keep technical evidence out of normal client replies.
- **User gives you a file/document** → default to [LOOP3](https://github.com/tbhrc/skills/tree/main/loop-data-source-ingestion) + [LIB1](https://github.com/tbhrc/skills/tree/main/ecosystem-librarian): preserve/file the source in its declared private-file owner, ingest useful material, route durable meaning/tasks to the correct owner with provenance, and verify later retrieval. Inventory alone is not ingestion; do not leave the only useful copy/meaning trapped in chat.
- **Cross-repository work** → use any existing authorised cross-repository route that can perform the task; do not invent another credential.

## Rules

- Do not require a controlling Issue for ordinary bounded work. Create/use one when durable continuity, coordination or recovery actually benefits from it.
- Do not pause authorised execution merely to synchronise Issue metadata. If a controlling Issue exists or was warranted, reconcile it before completion or handoff.
- Production-specific controls apply only to actual production-impacting actions.

**`main` keeps progress. KISSS keeps speed. Security protects real boundaries, not paperwork.**
