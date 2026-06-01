# RetroLens CLI

A command-line tool for browsing and retrieving **RetroLens** promptlets — focused prompt engineering retrospective analyses you run on top of the RetroLens LLM persona.

No API calls. No dependencies. Copy a promptlet, paste it into any UI or agent.

---

## Directory Layout

```
RETROLENS/
├── retrolens.py                 # CLI
├── retrolens_promptlets.json    # Promptlet library
└── RetroLens_Persona.md         # The base LLM persona (your OS)
```

---

## Usage

```bash
# List all available promptlets
python retrolens.py list

# Filter by category
python retrolens.py list --category diagnostic

# Print a promptlet to the terminal (ready to copy)
python retrolens.py get d1-thinking-loop

# Print and save to <alias>.txt in the same directory
python retrolens.py get d1-thinking-loop --save
```

---

## Promptlet Library

| Category | What it answers |
|---|---|
| **diagnostic** | What went wrong, and where? |
| **extraction** | What came out of this session? |
| **optimization** | How could this have been done better? |
| **comparative** | How did two sessions differ? |
| **archival** | What is worth keeping and reusing? |

Run `python retrolens.py list` to see all 17 promptlets with their aliases and descriptions.

---

## Mental Model

```
RetroLens_Persona.md   →   your OS
promptlets             →   your apps
session logs           →   your input
```

Load the persona into your LLM of choice. Retrieve a promptlet. Attach your session log. The persona handles the rest.

---

## Extending the Library

Add an entry to `retrolens_promptlets.json`:

```json
{
  "alias":       "your-alias",
  "name":        "Human Readable Name",
  "category":    "diagnostic",
  "description": "One-line summary.",
  "promptlet":   "The paragraph(s) you send to RetroLens."
}
```

No code changes required.
