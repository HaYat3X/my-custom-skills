# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Purpose

This repository stores custom Claude Code skills — reusable prompt-based slash commands that extend Claude Code's capabilities.

## Skill File Format

Skills live in `.md` files. Each skill file uses YAML frontmatter to define metadata, followed by the prompt body:

```markdown
---
name: skill-name
description: One-line description shown in the skill picker
---

The skill prompt content goes here.
```

Skills are invoked via `/skill-name` in the Claude Code prompt.

## Registering Skills

To make skills available in Claude Code, add the skills directory to your Claude Code settings (`~/.claude/settings.json`) under `skillsDirectories`.
