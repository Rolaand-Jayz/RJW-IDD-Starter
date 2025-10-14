# SPEC-1001 — Data Governance & Management

**Linked Requirements:** REQ-1001-1050 range  
**Linked Decisions:** DEC-DATA-####  
**Status:** Active

## Purpose

Define data lifecycle management, retention policies, backup/restore procedures, migration strategies, and data quality standards to ensure data integrity, availability, and compliance.

## Scope

- Covers data retention, backup/restore, migration, versioning, and quality.
- Applies to application data, evidence archives, logs, artifacts, and configuration.
- Integrates with security (`SPEC-0501`), observability (`SPEC-0401`), and deployment (`SPEC-0701`).

## Data Classification

### 1. Data Categories

| Category | Description | Examples | Retention | Backup Frequency |
|----------|-------------|----------|-----------|------------------|
| **Critical** | Data loss causes business failure | User accounts, transactions, production databases | 7 years | Continuous (point-in-time) |
| **Important** | Data loss causes significant disruption | Evidence indices, decision records, audit logs | 3 years | Daily |
| **Standard** | Data loss causes moderate inconvenience | Observability metrics, CI logs, cost dashboards | 90 days | Weekly |
| **Transient** | Data loss causes minimal impact | Temporary files, cache, debug logs | 7 days | None |

### 2. Data Sensitivity

- **Public:** Can be shared openly (documentation, open-source code).
- **Internal:** For team use only (specs, evidence, decisions).
- **Confidential:** Restricted access (credentials, personal data, financial records).
- **Regulated:** Subject to compliance requirements (PII, PHI, PCI data).

Document data classification in `docs/implementation/data-catalog.md`.

## Data Retention Policies

### 1. Application Data

- **User data:** Retain for duration of account + 90 days grace period.
- **Audit logs:** Retain for 1 year minimum (3 years for compliance-critical systems).
- **Transactional data:** Retain per legal/business requirements (typically 5-7 years).

### 2. RJW-IDD Artifacts

- **Evidence indices:** Raw: 90 days; Curated: 1 year (or until superseded).
- **Decision records:** Permanent retention; archive to cold storage after 3 years.
- **Change Log:** Permanent retention.
- **Integration transcripts:** Retain for 90 days minimum; extend for regulatory needs.
- **CI/CD logs:** Retain for 90 days; production deployment logs: 1 year.
- **Cost dashboards:** Retain for 2 years for trend analysis.

### 3. Logs & Metrics

- **Production logs:** 90 days hot storage, 1 year cold storage.
- **Development logs:** 30 days.
- **Metrics (time-series):** 90 days full resolution, 2 years aggregated.
- **Traces:** 7 days sampling, 30 days for errors.

### 4. Retention Enforcement

- Automate retention policies via lifecycle rules (S3 Lifecycle, Azure Blob Lifecycle).
- Log retention actions to `logs/data-lifecycle/retention-<timestamp>.json`.
- Governance Sentinel audits retention compliance quarterly.

## Backup & Restore Procedures

### 1. Backup Strategy

#### Production Databases

- **Full Backup:** Daily at off-peak hours.
- **Incremental Backup:** Every 4-6 hours.
- **Point-in-Time Recovery (PITR):** Enable transaction log backups for critical databases.
- **Retention:** 30 days online, 1 year archive.

#### Application Files & Artifacts

- **Configuration files:** Daily backup to version control.
- **User-uploaded content:** Daily incremental, weekly full.
- **Logs & evidence:** Per retention policy; archive to cold storage.

### 2. Backup Verification

- **Automated Tests:** Weekly restore test to staging environment.
- **Manual Tests:** Quarterly full disaster recovery drill.
- **Verification Metrics:**
  - Backup success rate: 100% (alert on failure).
  - Restore success rate: >99% (quarterly drill required).
  - Recovery Time Objective (RTO): < 4 hours for critical systems.
  - Recovery Point Objective (RPO): < 1 hour for critical systems.

### 3. Backup Storage

- **Primary:** Same region as production (fast restore).
- **Secondary:** Cross-region replication for disaster recovery.
- **Tertiary:** Offline/air-gapped backups for ransomware protection (quarterly).

### 4. Restore Procedures

**Routine Restore (e.g., user data recovery):**
1. Identify backup timestamp closest to desired state.
2. Restore to temporary environment for validation.
3. Extract and provide requested data to user.
4. Document restore operation in `logs/data-lifecycle/restore-<timestamp>.json`.

**Disaster Recovery (full system restore):**
1. Activate incident response (`docs/runbooks/general-incident-runbook.md`).
2. Provision new infrastructure via IaC (`SPEC-0701`).
3. Restore databases from most recent backup.
4. Replay transaction logs to minimize data loss.
5. Restore application files and configuration.
6. Execute smoke tests before redirecting traffic.
7. Document DR event in `DEC-INCIDENT-####` postmortem.

Document restore procedures in `docs/runbooks/docs/runbooks/deployment-runbook.md-backup-restore-runbook.md`.

## Data Migration

### 1. Migration Types

#### Schema Migrations

- Version all schema changes with migration scripts.
- Use migration tools (Flyway, Liquibase, Alembic, ActiveRecord).
- Test migrations on copy of production data before deploying.

#### Data Transformations

- Extract → Transform → Load (ETL) pattern for large-scale changes.
- Validate data integrity before and after transformation.
- Maintain rollback scripts for every migration.

#### Platform Migrations

- Moving to new database engine, cloud provider, or storage system.
- Plan in phases: read-only replica → dual-write → cutover → decommission.
- Extended parallel operation period to validate equivalence.

### 2. Migration Planning

Create migration plan in `docs/decisions/DEC-DATA-MIGRATION-####.md`:

- **Scope:** What data, why migrating, success criteria.
- **Approach:** Migration strategy, tooling, rollback plan.
- **Risk Assessment:** Data loss risk, downtime window, validation approach.
- **Schedule:** Milestones, dependencies, go/no-go criteria.
- **Stakeholders:** Owners, approvers, communication plan.

### 3. Migration Execution

1. **Backup:** Full backup immediately before migration.
2. **Dry Run:** Execute migration in staging environment.
3. **Validation:** Compare source vs. target data (checksums, row counts, sample queries).
4. **Cutover:** Execute production migration during maintenance window.
5. **Monitoring:** Enhanced observability for 24-48 hours post-migration.
6. **Rollback:** Maintain rollback capability for 7 days post-migration.

### 4. Migration Verification

- **Data Integrity:** Row counts match; checksums/hashes consistent.
- **Application Functionality:** Smoke tests pass; no error rate spike.
- **Performance:** Queries within SLO targets (`SPEC-0801`).
- **Rollback Tested:** Rollback executed in staging; confirmed viable.

Document migration execution in `artifacts/integration/migration-<timestamp>/`.

## Data Versioning

### 1. Schema Versioning

- Every schema change gets version identifier (e.g., v1.2.3).
- Version stored in database metadata or migration history table.
- Application code checks schema version on startup; fails if mismatch.

### 2. API Versioning

- Version APIs to support backward compatibility during migrations.
- Deprecation policy: Support version N-1 for 6 months after N release.
- Document breaking changes in Change Log and API changelog.

### 3. Configuration Versioning

- All configuration in version control (Git).
- Tag deployments with configuration version.
- Store environment-specific overrides in secure vault, not version control.

## Data Quality

### 1. Quality Dimensions

- **Completeness:** No missing required fields; null handling strategy defined.
- **Accuracy:** Data reflects reality; validation rules enforced.
- **Consistency:** Same data represented identically across systems.
- **Timeliness:** Data updated within acceptable latency (e.g., real-time, hourly batch).
- **Uniqueness:** No unintended duplicates; primary keys enforced.

### 2. Quality Monitoring

- **Data Validation:** Input validation on writes; constraints in database.
- **Quality Metrics:** Track % of records passing quality checks.
- **Anomaly Detection:** Alert on sudden changes in data volume, null rates, outliers.

Store quality reports in `logs/data-quality/quality-report-<timestamp>.json`.

### 3. Quality Remediation

- **Immediate:** Block writes failing validation; return error to user.
- **Batch:** Scheduled jobs to clean/deduplicate historical data.
- **Manual:** Data steward reviews and corrects edge cases.

## Data Access & Security

### 1. Access Control

- **Principle of Least Privilege:** Grant minimum necessary access.
- **Role-Based Access Control (RBAC):** Define roles; assign permissions to roles.
- **Audit Logging:** Log all data access (who, what, when) to immutable log.

### 2. Encryption

- **At Rest:** Encrypt databases, backups, logs (AES-256 or equivalent).
- **In Transit:** TLS 1.2+ for all data transmission.
- **Key Management:** Use managed key services (AWS KMS, Azure Key Vault); rotate annually.

### 3. Data Masking

- Mask sensitive data in non-production environments.
- Anonymize logs before sharing with third parties.
- Redact PII from incident transcripts and postmortems.

## Compliance & Regulatory

### 1. Regulatory Requirements

Document applicable regulations in `docs/implementation/compliance-requirements.md`:

- **GDPR:** Right to access, rectification, erasure, portability.
- **CCPA:** Right to know, delete, opt-out of sale.
- **HIPAA:** PHI protection, access controls, breach notification.
- **SOX:** Financial data retention, audit trails, controls.

### 2. Data Subject Rights

- **Access Request:** Provide data export within 30 days.
- **Deletion Request:** Purge data within 30 days (with exceptions for legal retention).
- **Portability:** Export in machine-readable format (JSON, CSV).

Document rights procedures in `docs/runbooks/DOC-0027-data-subject-rights.md`.

### 3. Breach Response

- Follow incident response procedures (`docs/runbooks/security-incident-runbook.md`, `docs/runbooks/general-incident-runbook.md`).
- Notify affected parties within 72 hours (GDPR requirement).
- Report to regulatory authorities as required.
- Document breach in `DEC-INCIDENT-####` with remediation plan.

## Integration with RJW-IDD

### 1. Evidence Data

- Treat evidence indices as Important data (3-year retention).
- Back up curated evidence before promotion (`scripts/promote_evidence.py`).
- Version evidence schemas; migrate when changing structure.

### 2. Decision & Change Log Data

- Permanent retention; back up daily.
- Version control for all decision records and Change Log.
- Include in disaster recovery verification (ensure accessibility post-restore).

### 3. Observability Data

- Follow retention policies for logs/metrics (90 days hot, 1 year cold).
- Validate backup of critical SLO/incident data.
- Include observability data in migration planning if changing platforms.

## Traceability

- Link data policies to requirements (`REQ-DATA-####`) and tests (`TEST-DATA-####`).
- Document migration decisions in `DEC-DATA-####` with evidence and rationale.
- Cross-reference backup/restore procedures with incident runbooks.
- Tag data quality issues with severity and remediation timeline.

## Implementation Guidance

- Start with backup/restore procedures for critical databases.
- Automate retention policies incrementally; begin with transient data.
- Test disaster recovery drills quarterly; document findings.
- Version all schemas from day one; retrofitting is error-prone.
- Document data classification before first production deployment.

## Verification

- Backup success rate tracked in `logs/data-lifecycle/backup-status.json`.
- Restore drill results attached to Change Log quarterly.
- Migration verification included in deployment Change Log entries.
- Data quality metrics reviewed monthly; anomalies trigger investigation.
- Governance Sentinel audits data policies and compliance annually.

## Follow-Up Guidance

- Coordinate with `SPEC-0501` for encryption and access control requirements.
- Reference `docs/runbooks/deployment-runbook.md-backup-restore-runbook.md` for operational procedures.
- Integrate with `SPEC-0701` to include data validation in deployment gates.
- Capture data-specific decisions in `docs/decisions/` when policies evolve.
