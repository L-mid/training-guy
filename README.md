# Website

This website is built using [Docusaurus](https://docusaurus.io/), a modern static website generator.

## Curriculum generation + config

Curriculum pages live in `docs/curriculum/` and are generated/updated by:

```bash
python scripts/gen_curriculum.py
```

### Config files

All curriculum content overrides are data-driven under `curriculum_config/`:

- `curriculum_config/global.json`
  - `defaults`: applied to every curriculum page
- `curriculum_config/tier-XX.json` (e.g. `tier-01.json`)
  - `tier_defaults`: applied to every page in that tier
  - `files`: per-file overrides, keyed by the page slug (the markdown filename without `.md`)

Merge order:
`global defaults → tier defaults → file override`

### Managed sections

The generator only rewrites these sections (if present), preserving any other manual content:

- `## Task`
- `## Checklist`
- `## Hints` (only if `hints_block.enabled: true`)
- `## Docs / Tutorials`

This lets you safely add custom explanation, examples, or extra sections without them being overwritten.

## Installation

```bash
yarn
```

## Local Development

```bash
yarn start
```

This command starts a local development server and opens up a browser window. Most changes are reflected live without having to restart the server.

## Build

```bash
yarn build
```

This command generates static content into the `build` directory and can be served using any static contents hosting service.

## Deployment

Using SSH:

```bash
USE_SSH=true yarn deploy
```

Not using SSH:

```bash
GIT_USER=<Your GitHub username> yarn deploy
```

If you are using GitHub pages for hosting, this command is a convenient way to build the website and push to the `gh-pages` branch.
