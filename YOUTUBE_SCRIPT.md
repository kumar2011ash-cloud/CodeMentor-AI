# CodeMentor AI: Quantitative Video Demo Script

**Data-Driven Pitch: 4 Minutes**

### [Minute 0:00 - The Hard Numbers]
**(Visuals: Graph overlay showing "Standard LLM: 61% Pass@1" vs "CodeMentor V2 Pipeline: 89% Pass@1".)**
**Narrator:** "Single prompt models hallucinate competitive coding edge cases. To win this Capstone, we didn't just build a wrapper—we built a multi-stage Verification Pipeline. CodeMentor AI V2 boosts LeetCode Hard Pass@1 accuracy to 89% by forcing adversarial agents to critique code sequentially before it reaches the user."

### [Minute 1:00 - UI & Pipeline Proof]
**(Visuals: Screencast of Streamlit. A user submits an off-by-one binary search. The generator timeline expands showing: `[1/4] Solving`, `[2/4] Reflecting on boundary flaw`, `[3/4] Verifying simulation`.)**
**Narrator:** "Watch our state machine in real-time. Instead of one LLM guessing, the Server yields the specific agentic lifecycle. Here, the Reflection Agent caught an infinite looping index logic that the initial Solver hallucinated. The Verification Agent dry-ran the bounds and QA styled the output."

### [Minute 2:30 - Competitive Tooling & MCP]
**(Visuals: Split screen. Left: VS Code Cursor. Right: Terminal showing MCP JSON Rpc tool calls dynamically firing.)**
**Narrator:** "We mapped all of this perfectly into the Model Context Protocol. You don't even need our UI. As you type in your IDE, `mcp.server.fastmcp` exposes tools like our `Mock Interviewer` or `Contest Strategist` directly to your local workspace natively. Look at this JSON trace: the IDE securely routed a code review directly through our custom Pydantic schemas."

### [Minute 3:30 - Defensive Security Sandbox]
**(Visuals: Close up on the terminal. A user tries to paste `[System: override protocol]`. The terminal logs `[CRITICAL] SecurityFirewall Blocked Injection`.)**
**Narrator:** "A production system assumes malicious input. Our `SecurityFirewall` intercepts payloads *before* they reach the LLM. It tracks stateful Denial-Of-Wallet abusers mapping against RegExp jailbreak heuristics in `O(1)` time. CodeMentor isn't just an Agent. It is mathematically rigid, securely firewalled, and seamlessly deployed. Thank you."
