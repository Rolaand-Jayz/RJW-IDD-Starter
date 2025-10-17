# Release Process

This project follows lightweight semver for releases with annotated tags for pre-releases.

## Preparing a release

1. Ensure `pyproject.toml` version is updated to the desired value (PEP 440 compliant). Example: `0.1.1a0` for alpha.
2. Run tests and CI locally where possible.
3. Update `CHANGELOG.md` or add `logs/change-YYYYMMDD-topic.md` describing the release.

## Tagging

Use an annotated tag with a human-readable message:

```bash
git tag -a v0.1.1-alpha -m "v0.1.1-alpha"
```

Push tag to origin:

```bash
git push origin v0.1.1-alpha
```

## Publishing

This project is not published to PyPI by default. If you publish, ensure credentials are rotated and the publish process is audited. Document publish artifacts in `RELEASE.md` when you perform them.

## Rollbacks

If a release must be reverted, create a small patch release (e.g., `0.1.1.post1`) or follow your organization's rollback process; do not rewrite published tags.
