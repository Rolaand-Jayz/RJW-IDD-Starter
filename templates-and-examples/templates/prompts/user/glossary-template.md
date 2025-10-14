# Glossary Prompt Template

Use this to generate or refresh a glossary that keeps novices aligned on RJW-IDD
terminology.

```
You are curating the shared glossary for <project name>.

Inputs:
- Existing glossary entries:<link or paste if available>
- New terms to define:<bullet list>
- Sources:<decisions/specs/change-log references>

Instructions:
1. For each term, produce a beginner-friendly definition (2–3 sentences).
2. Mention the artifact type or workflow stage where the term appears.
3. Flag any terms that still need evidence or spec coverage.

Format as Markdown bullet list (`- Term — definition`) so we can copy it
into `docs/prompts/user/glossary.md`.
```
