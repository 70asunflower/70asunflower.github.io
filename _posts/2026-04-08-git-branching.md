---
title: "Understanding Git Branching Strategies"
author: Fu Qilin
categories: [Tutorial]
tags: [git, version-control, best-practices]
date: 2026-04-08
---

## Common Branching Models

### Git Flow

Classic model with `main`, `develop`, `feature/*`, `release/*`, and `hotfix/*` branches. Good for scheduled releases.

### GitHub Flow

Simpler model: `main` + feature branches with pull requests. Ideal for continuous deployment.

### Trunk-Based Development

Everyone commits to `main` (or short-lived branches). Best for teams with strong CI/CD.

## Which One to Choose?

```
Small team / Personal project  →  GitHub Flow
Scheduled releases              →  Git Flow
Strong CI/CD, experienced team  →  Trunk-Based
```

## Useful Git Commands

```bash
# Interactive rebase (clean up commits before merging)
git rebase -i HEAD~3

# Cherry-pick a specific commit
git cherry-pick abc1234

# See branch tree
git log --graph --oneline --all
```

---

> Branching strategy should serve your workflow, not the other way around.
{: .prompt-warning }
