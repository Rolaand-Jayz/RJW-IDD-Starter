# Example Evidence Entries

This file provides example evidence entries to illustrate the expected format for `evidence_index.json` and `evidence_index_raw.json`.

## Raw Evidence Example

Raw evidence index contains ALL harvested items before curation:

```json
[
  {
    "id": "RAW-0001",
    "source": "reddit",
    "url": "https://reddit.com/r/devops/comments/xyz123/test_driven_development_at_scale",
    "title": "Test-Driven Development at Scale: Our 6-Month Journey",
    "author": "senior_dev_2024",
    "timestamp": "2025-01-02T14:30:00Z",
    "content_snippet": "After 6 months of enforcing TDD, we saw 40% reduction in production bugs but test maintenance became a challenge. Here's what we learned...",
    "tags": ["testing", "tdd", "lessons-learned"],
    "stance": "pain",
    "relevance_score": 0.92,
    "metadata": {
      "subreddit": "devops",
      "upvotes": 342,
      "comments": 87
    }
  },
  {
    "id": "RAW-0002",
    "source": "github",
    "url": "https://github.com/example/project/issues/456",
    "title": "Proposal: Add governance layer to CI/CD pipeline",
    "author": "contributor_xyz",
    "timestamp": "2025-01-01T09:15:00Z",
    "content_snippet": "We need automated checks to ensure specs and tests are aligned before merging. Proposed guards: ID validation, change log enforcement, test coverage...",
    "tags": ["governance", "ci-cd", "automation"],
    "stance": "fix",
    "relevance_score": 0.88,
    "metadata": {
      "repository": "example/project",
      "issue_type": "enhancement",
      "labels": ["governance", "quality"]
    }
  },
  {
    "id": "RAW-0003",
    "source": "hn",
    "url": "https://news.ycombinator.com/item?id=38765432",
    "title": "The Hidden Costs of AI-Assisted Coding",
    "author": "techcto",
    "timestamp": "2024-12-28T16:45:00Z",
    "content_snippet": "AI coding tools are great but without governance frameworks, we've seen 3x increase in technical debt. Organizations need structured approaches...",
    "tags": ["ai-coding", "technical-debt", "governance"],
    "stance": "risk",
    "relevance_score": 0.85,
    "metadata": {
      "points": 287,
      "comments": 143,
      "item_type": "story"
    }
  }
]
```

## Curated Evidence Example

Curated evidence index contains PROMOTED items after human review:

```json
[
  {
    "id": "EVD-0201",
    "raw_id": "RAW-0001",
    "source": "reddit",
    "url": "https://reddit.com/r/devops/comments/xyz123/test_driven_development_at_scale",
    "title": "Test-Driven Development at Scale: Our 6-Month Journey",
    "author": "senior_dev_2024",
    "timestamp": "2025-01-02T14:30:00Z",
    "curated_date": "2025-01-03T10:00:00Z",
    "curator": "Evidence Lead",
    "summary": "Team implemented strict TDD practices for 6 months. Results: 40% fewer production bugs, improved code confidence, but 20% longer initial development time and challenges maintaining large test suites. Key insight: Test refactoring needs dedicated time.",
    "key_insights": [
      "TDD reduces production bugs significantly (quantified at 40%)",
      "Test maintenance overhead grows with codebase complexity",
      "Team velocity initially drops but recovers after 2-3 months",
      "Test refactoring should be scheduled work, not ad-hoc"
    ],
    "related_requirements": ["REQ-0201", "REQ-0202"],
    "related_specs": ["SPEC-0201"],
    "related_decisions": ["DEC-0004"],
    "stance": "pain",
    "actionable": true,
    "action_taken": "Added test maintenance section to SPEC-0201, scheduled quarterly test refactoring sprints",
    "tags": ["testing", "tdd", "lessons-learned", "technical-debt"],
    "quality_score": 0.92,
    "metadata": {
      "subreddit": "devops",
      "community_engagement": "high",
      "practitioner_level": "senior"
    }
  },
  {
    "id": "EVD-0202",
    "raw_id": "RAW-0002",
    "source": "github",
    "url": "https://github.com/example/project/issues/456",
    "title": "Proposal: Add governance layer to CI/CD pipeline",
    "author": "contributor_xyz",
    "timestamp": "2025-01-01T09:15:00Z",
    "curated_date": "2025-01-03T10:15:00Z",
    "curator": "Spec Curator",
    "summary": "Open-source project successfully implemented governance guards in CI: ID validation, change log enforcement, test coverage checks. Reduced merge conflicts by 60% and improved audit trail. Guards run in <30 seconds, acceptable overhead.",
    "key_insights": [
      "Automated governance guards prevent common errors before merge",
      "Change log enforcement improved traceability significantly",
      "Performance impact minimal (<30s) when properly optimized",
      "Team adoption required clear error messages and documentation"
    ],
    "related_requirements": ["REQ-0201", "REQ-0203"],
    "related_specs": ["SPEC-0201", "SPEC-0003"],
    "related_decisions": ["DEC-0005"],
    "stance": "fix",
    "actionable": true,
    "action_taken": "Informed guard implementation in tools/testing/, validated design approach",
    "tags": ["governance", "ci-cd", "automation", "quality-gates"],
    "quality_score": 0.88,
    "metadata": {
      "repository": "example/project",
      "implementation_status": "production",
      "team_size": "15"
    }
  }
]
```

## Evidence Classification

### Stance Types
- **pain:** Practitioner pain points, challenges, failures
- **fix:** Solutions, mitigation strategies, successful implementations
- **risk:** Emerging risks, warnings, potential pitfalls
- **insight:** General learnings, best practices, observations

### Quality Score Factors
- Relevance to RJW-IDD principles (0.0 - 1.0)
- Recency (fresher = higher score)
- Author credibility (verified practitioners)
- Community engagement (upvotes, comments)
- Actionability (specific, implementable insights)

### Curation Criteria

**Promote to curated index if:**
- ✅ Relevance score > 0.80
- ✅ Contains actionable insights
- ✅ Aligns with RJW-IDD methodology
- ✅ Provides evidence for requirements/decisions
- ✅ Recent (within configured timeframe)

**Reject if:**
- ❌ Irrelevant to governance/methodology
- ❌ Duplicate of existing evidence
- ❌ Low quality or unverifiable
- ❌ Opinion without supporting data

## Using Evidence in Practice

### 1. Link to Requirements
```csv
# In requirement-ledger.csv
req_id,title,evidence_refs,...
REQ-0201,"Enforce test-first development",EVD-0201;EVD-0202,...
```

### 2. Reference in Specs
```markdown
## 3.2 Test-First Enforcement (REQ-0201)

Based on practitioner evidence (EVD-0201), TDD reduces production bugs by 40% 
but requires dedicated test maintenance time. Our guard implementation (EVD-0202) 
automates enforcement with minimal CI overhead.
```

### 3. Support Decisions
```markdown
# DEC-0012 — Implement Test-First Guards

## Evidence
- EVD-0201: Practitioners report TDD effectiveness but consistency challenges
- EVD-0202: Automated guards successfully enforce TDD in production systems
```

## Evidence Freshness

Per `scripts/validate_evidence.py`, evidence must be:
- **Raw index:** No age limit (historical record)
- **Curated index:** Refreshed evidence < 14 days old (configurable)
- **Stale evidence:** Flagged for re-validation or removal

---

**Note:** These are EXAMPLES only. Replace with actual harvested evidence from your domain.
