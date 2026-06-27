## Available Skills (auto-detect)

**Rule: Check if any skill below applies to the user's request BEFORE responding. If a match is found, read its SKILL.md at the path shown and follow it.**

### Process Skills (check first — determine HOW to approach)
| Skill | Triggers | Path |
|-------|----------|------|
| brainstorming | creative work, new features, components, design, adding functionality | `.claude/skills/superpowers/brainstorming/SKILL.md` |
| systematic-debugging | bugs, test failures, errors, unexpected behavior | `.claude/skills/superpowers/systematic-debugging/SKILL.md` |
| using-superpowers | meta-skill: check if ANY other skill applies | `.claude/skills/superpowers/using-superpowers/SKILL.md` |

### Implementation Skills
| Skill | Triggers | Path |
|-------|----------|------|
| test-driven-development | feature implementation, bugfix (write test FIRST) | `.claude/skills/superpowers/test-driven-development/SKILL.md` |
| writing-plans | multi-step tasks with specs, before touching code | `.claude/skills/superpowers/writing-plans/SKILL.md` |
| executing-plans | have a written implementation plan to execute | `.claude/skills/superpowers/executing-plans/SKILL.md` |
| subagent-driven-development | independent parallel tasks in current session | `.claude/skills/superpowers/subagent-driven-development/SKILL.md` |
| dispatching-parallel-agents | 2+ independent tasks, no shared state | `.claude/skills/superpowers/dispatching-parallel-agents/SKILL.md` |
| frontend-design | web components, pages, dashboards, React, HTML/CSS | `.claude/skills/frontend-design/SKILL.md` |
| ui-ux-pro-max | icons, visual hierarchy, interaction patterns, design polish | `.claude/skills/ui-ux-pro-max/SKILL.md` |
| gh-cli | GitHub repos, issues, PRs, Actions, releases | `.claude/skills/gh-cli/SKILL.md` |
| planning-with-files | complex multi-step tasks (3+ steps), Manus-style file planning | `.claude/skills/planning-with-files/SKILL.md` |

### Quality & Completion Skills
| Skill | Triggers | Path |
|-------|----------|------|
| verification-before-completion | before claiming work is done, requires evidence | `.claude/skills/superpowers/verification-before-completion/SKILL.md` |
| requesting-code-review | before merging, verify work meets requirements | `.claude/skills/superpowers/requesting-code-review/SKILL.md` |
| receiving-code-review | before implementing review feedback | `.claude/skills/superpowers/receiving-code-review/SKILL.md` |
| finishing-a-development-branch | implementation complete, tests pass, integrate work | `.claude/skills/superpowers/finishing-a-development-branch/SKILL.md` |

### Workflow Skills
| Skill | Triggers | Path |
|-------|----------|------|
| using-git-worktrees | feature work needing isolation from workspace | `.claude/skills/superpowers/using-git-worktrees/SKILL.md` |
| writing-skills | creating/editing skills, verifying skills work | `.claude/skills/superpowers/writing-skills/SKILL.md` |

**Red Flags (from using-superpowers):**
- "This is just a simple question" → Questions are tasks. Check skills.
- "I need more context first" → Skill check comes BEFORE clarifying questions.
- "This doesn't need a formal skill" → If a skill exists, use it.
