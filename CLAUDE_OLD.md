This file provides guidance to coding agents when working with code in this repository.

## My Coding Guidelines

- I encourage to-the-point documentation
- Avoid in-line comments explaining the code, unless the code is complex or weird, than clarification is encouraged
- If you see the oppurtunity to make reusable code do so. I prefer reusable more modular pieces. The shared repo is particularly useful for this.
- If there is existing documentation and you change how something works, rewrite that documentation
- Methods that can be static should be labeled as such
- If possible without overcomplication UI should lean on reusable components in `shared-components` and business logic should call into `shared-utils` when it can be shared. However, do not go overkill on this, sometimes it makes sense for something to be owned by the server or a specific client respectively.
- **TypeScript**:
  - Strict typing required, use explicit types for function parameters and returns
- **Imports**:
  - Group imports by source (React, third-party, project modules)
  - All imports from util library shoukld be formatted like import { ... } from "@ai-dm/utils"; (unless you are writing code in the utility library)
- **Naming**:
  - Use PascalCase for components/interfaces, camelCase for variables/functions
  - Files that contain just a class use PascalCase
  - Util/helper files use camelCase
- **Error handling**: Use try/catch for async operations, proper error propagation
- **Components**: Use functional components with React.FC type declaration
- **File structure**: Keep related files in same directory (component with styles and tests)
- **Utility functions**: Extract reusable logic to utility files
- **React patterns**: Use React hooks for state and side effects, not class components

## Useful Reusable Functions

- Always use isPresent from shared-utils for null checks
- When crafting LLM prompts, prefer the shared describe helpers to avoid hand-maintaining structure changes:
  - describePrimeRealms (with optional header level)
  - describeRegion (use for continents too)
  - describeCenterOfPower / describeCenterOfPowersAtTile
  - describeRiverAtTile / describeRiverSize
  - describeRoadAtTile
  - describeBiome
  - describePOI / describeRoom / describeItem / describeCreature / describeEffect
  - describeFaction
  - World helpers: describeTile, describeContinentLoreAt / describeNearbyOcean, getBiomeBreakdownCenterOfPower, getBiomeBreakdownForPolygon

## Monorepo Structure

- **server-zain (server)**: Houses API surface, world generation, dungeon master engines, persistence, auth, llm integrations, and any external integrations. Keep domain logic, data validation, and long-running jobs here; do not pull server-only logic into clients.
- **web-zain (game client)**: Player-facing React app. Owns game UI flows, client-side state, session handling, and network calls to `server-zain`.
- **web-devtools (devtools client)**: Internal tooling for world editing, debugging, and monitoring. Shares UI and helper layers with the game client but should not contain gameplay-only code. Connects to `server-zain` for data and reuse shared libs for consistency.
- **shared-components**: Reusable React component library and styling primitives used by both clients. Keep components presentation-focused; avoid app-specific business logic or server coupling.
- **shared-utils**: Environment-agnostic utilities, shared types, constants, and pure logic. No React dependencies, minimal side effects, and safe to import from server and both clients.

## Overview Files in agents/

There are a few workflow overviews in the directory agents/. This give overviews on how certain systems work. If they seem relevant, they are often a context-efficient way to understand how certain systems work. Not they might be out of date, but are still useful.
The following ones currently exist:

- religion-generation-overview.md
- center-of-power-generation-overview.md

## Commands

### Build Commands

**From Root Directory (Recommended)**:

- `npm run build` - Build all workspaces (shared-utils, shared-components, server-zain, web-zain, web-devtools)
- `npm run clean` - Clean build artifacts

**Using --workspace Flag**:

- `npm run build --workspace web-zain` - Build only web-zain workspace
- `npm run build --workspace web-devtools` - Build only web-devtools workspace
- `npm run build --workspace server-zain` - Build only server-zain workspace

### Development Commands

**IMPORTANT**: When developing with the web clients, always use `dev` scripts instead of `start` to enable auto-rebuild of shared packages on save.

**From Root Directory (Recommended)**:

- `npm run dev:web` - Start web client with auto-rebuild for shared packages (RECOMMENDED)
- `npm run dev:devtools` - Start devtools with auto-rebuild for shared packages (RECOMMENDED)
- `npm run dev:server` - Start server in development mode
- `npm run start:web` - Start web client without auto-rebuild (requires manual rebuild of shared packages)
- `npm run start:devtools` - Start devtools without auto-rebuild (requires manual rebuild of shared packages)
- `npm run start:server` - Start server

**Using --workspace Flag (Alternative)**:

- `npm run dev --workspace web-zain` - Start web client with auto-rebuild
- `npm run dev --workspace web-devtools` - Start devtools with auto-rebuild
- `npm run start --workspace server-zain` - Start server

The `dev` scripts run the web app and watch shared-utils and shared-components for changes, automatically recompiling them when you save files in those workspaces.

### Test Commands

- `cd server-zain && npm test` - Run all server tests
- `cd server-zain && npx jest path/to/test.ts` - Run a specific server test file
- `cd web-zain && npm test` - Run all web client tests
