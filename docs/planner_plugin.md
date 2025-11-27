# Agent Zero Planner Plugin

This plugin enables Agent Zero to create and follow structured plans.

## Features
- Create a plan with a main goal, tasks, subtasks, success criteria, and things to avoid.
- Track task status (pending, in progress, done, failed).
- Persist plan state across restarts (stored in `tmp/planner/{context_id}.json`).
- Automatically inject plan status into the agent's context.

## Installation
The plugin files are located in:
- `python/helpers/planner.py`
- `python/tools/planner.py`
- `python/extensions/agent_init/planner.py`
- `python/extensions/system_prompt/planner.py`
- `python/extensions/message_loop_prompts_before/planner.py`

## Usage
The agent will automatically receive instructions to use the planner in its system prompt.
When given a complex task, the agent should create a plan.

To disable the plugin, remove the files in `python/extensions/`.
