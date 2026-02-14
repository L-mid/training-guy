## Installation

### 1) Clone the repo
```bash
git clone <YOUR_REPO_URL>   # maybe add this lol
cd kid-quests

# windows powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1

python -m pip install -U pip
python -m pip install -r requirements-dev.txt

# node 
npm install
```

### Testing:

```bash
# run pytest
python -m pytest -q
 
# build the site
npm run build:ci

# (optional) test site locally
npm run start 

# run all tests 
npm test
```

## Curriculum generation + config

Curriculum pages live in `docs/curriculum/` and are generated/updated by:

```bash
python -m scripts.curriculum_gen
```

### Config files

All curriculum content overrides under `curriculum_config/`:

- `curriculum_config/global.json`
  - `defaults`: applied to every curriculum page
- `curriculum_config/tier-XX.json` (e.g. `tier-01.json`)
  - `tier_defaults`: applied to every page in that tier
  - `files`: per-file overrides, keyed by the page slug (the markdown filename without `.md`)

Merge order:
`global defaults → tier defaults → file override`

### Managed sections

Generator only rewrites these sections (if present) (other content is not touched):

- `## Task`
- `## Checklist`
- `## Hints` (only if `hints_block.enabled: true`)
- `## Docs / Tutorials`
- `## Spoiler Code solutions`


