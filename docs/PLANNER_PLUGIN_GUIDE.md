# Agent Zero Planner Plugin Guide

This guide explains how to install the Planner Plugin into an Agent Zero instance. The Planner Plugin enables Agent Zero to create, track, and execute structured plans.

## What is the Planner Plugin?

The Planner Plugin adds a persistent planning capability to Agent Zero. It allows the agent to:
- Break down complex goals into hierarchical tasks.
- Track task status (pending, in progress, done, failed).
- Maintain plan state across restarts.
- Automatically see the plan status in its context.

## Installation

### Method 1: Manual Installation

1. Copy the `install_planner_plugin.py` script to the root directory of your Agent Zero installation.
2. Run the script:
   ```bash
   python install_planner_plugin.py
   ```
3. Restart Agent Zero.

### Method 2: Agent-Assisted Installation

You can instruct Agent Zero to install the plugin itself if it has access to the installer script.

**Prompt for Agent Zero:**

> "I have placed a file named `install_planner_plugin.py` in the root directory. Please execute this script to install the Planner Plugin, and then restart yourself (or tell me to restart you)."

If the agent is running in a container or environment where it can create files, you can even paste the content of `install_planner_plugin.py` to the agent and ask it to save and run it.

## Verification

To verify the installation, start a chat with Agent Zero and ask:
> "Do you have a planner tool available?"

Or give it a complex task:
> "Create a plan to research the history of the internet and write a short summary."

The agent should use the `planner:create_plan` tool.

## Removal

To uninstall the plugin, remove the following files:
- `python/helpers/planner.py`
- `python/tools/planner.py`
- `python/extensions/agent_init/planner.py`
- `python/extensions/system_prompt/planner.py`
- `python/extensions/message_loop_prompts_before/planner.py`
- `tmp/planner/` (directory containing saved plans)
