# `.nexus` — Personal AI Agent OS

Welcome to **`.nexus`**, your modular Agent Operating System built for **Session 03 · The Agent OS (Vibe Coding Mastery)**.

Think of `.nexus` as the headquarters for your AI agents:
- **`skills/orchestrator.md`** is the **front door**: it reads what you type, identifies which skill you need, confirms the routing out loud, and hands off the request.
- **`config/skills.json`** is the **registry**: it indexes all available skills and their natural trigger phrases.
- **`skills/`** holds each specialized agent as a portable `.md` system prompt.
- **`memory/context.json`** stores persistent brand and session context between conversations.

---

## Folder Structure

```text
.nexus/
├── skills/
│   ├── skill_builder.md     # Activity 02: Creates, tests, and refines new .md skills
│   ├── orchestrator.md      # Activity 03: Routes requests across your Agent OS
│   ├── brand_kit.md         # Activity 04: Builds 9 brand elements + single-page HTML brand book
│   └── carousel.md          # Activity 05: Generates 7-slide Instagram carousels + 3 captions
├── config/
│   └── skills.json          # Registry of all 4 skills and their trigger phrases
├── memory/
│   └── context.json         # Session memory for brand identity and content history
└── README.md                # Guide and audit checklist for this Agent OS
```

---

## How to Use in Antigravity IDE / OpenCode

1. **Test the Orchestrator (`skills/orchestrator.md`)**
   - Open a chat in Antigravity IDE (or the OpenCode tab) and load `skills/orchestrator.md` as your system prompt.
   - Type: `"I want to create a 7-slide post for my coffee business"` -> It will confirm routing to `carousel`.
   - Type: `"Help me pick colors and fonts for my studio"` -> It will confirm routing to `brand_kit`.
   - Type: `"I want to build a new skill that writes newsletters"` -> It will confirm routing to `skill_builder`.

2. **Run the Brand Kit Agent (`skills/brand_kit.md`)**
   - Load `skills/brand_kit.md` and optionally drop a screenshot or URL of a brand aesthetic you love.
   - It will analyze the visual style first, then guide you one element at a time (2–3 questions per step) through all 9 brand elements and output a complete HTML Brand Guide.

3. **Run the Carousel Generator (`skills/carousel.md`)**
   - Load `skills/carousel.md`.
   - It will ask you 3 intake questions (Topic, Target Audience, Goal) and then produce a 7-slide Instagram carousel (Hook <=10 words, 5 Content slides with <=6-word titles and 3 bullets <=12 words each, CTA slide) plus 3 captions with hashtags.

---

## How to Add a New Skill Later

1. Load `skills/skill_builder.md` and describe the new agent you want to build.
2. Save the generated prompt as `.nexus/skills/[new_skill_name].md`.
3. Register its `id`, `file`, `description`, and `trigger_phrases` inside `.nexus/config/skills.json`.
