# DOC-0020 — Deployment Runbook

**Applies to:** All production and staging deployments.  
**Cross-links:** `SPEC-0701`, `SPEC-0801`, `DOC-0018`.

## Purpose

Provide step-by-step procedures for deploying applications to staging and production environments with proper validation, rollback capabilities, and audit trails.

## Prerequisites

Before initiating deployment:

- [ ] All quality gates passed (`scripts/ci/test_gate.sh` clean).
- [ ] Change Log entry prepared with deployment plan.
- [ ] Rollback plan documented and rollback rehearsed in staging.
- [ ] On-call rotation notified with deployment window.
- [ ] Backup taken within last 24 hours and verified.
- [ ] Deployment approval obtained (Governance Sentinel for production).
- [ ] Runbooks updated if deployment introduces new operational procedures.

## Deployment Checklist

### Staging Deployment

**Purpose:** Validate changes in production-equivalent environment before production rollout.

**Steps:**

1. **Pre-Deployment**
   ```bash
   # Verify environment health
   ./scripts/health_check.sh staging
   
   # Confirm git tag/commit
   git log -1 --oneline
   export DEPLOY_VERSION="v1.2.3"
   export DEPLOY_COMMIT="abc123"
   ```

2. **Deploy Application**
   ```bash
   # Option A: Container-based deployment
   kubectl set image deployment/app app=registry/app:${DEPLOY_VERSION} -n staging
   kubectl rollout status deployment/app -n staging --timeout=10m
   
   # Option B: Platform-specific (e.g., AWS Elastic Beanstalk)
   eb deploy staging-env --label ${DEPLOY_VERSION}
   
   # Option C: Custom deployment script
   ./scripts/deploy.sh staging ${DEPLOY_VERSION}
   ```

3. **Smoke Tests**
   ```bash
   # Run automated smoke tests
   pytest tests/smoke/ --env=staging
   
   # Manual validation
   curl https://staging-api.example.com/health
   ```

4. **Validation**
   - Verify error rates within baseline (use dashboards).
   - Check latency within SLO targets.
   - Confirm feature flags active/inactive as expected.

5. **Document**
   ```bash
   # Log deployment
   echo '{
     "timestamp": "'$(date -u +%Y-%m-%dT%H:%M:%SZ)'",
     "environment": "staging",
     "version": "'${DEPLOY_VERSION}'",
     "commit": "'${DEPLOY_COMMIT}'",
     "operator": "'${USER}'",
     "status": "success"
   }' > logs/deployments/deploy_$(date -u +%Y%m%dT%H%M%SZ).json
   ```

### Production Deployment

**Approval Required:** Governance Sentinel + Service Owner

**Steps:**

1. **Pre-Deployment Verification**
   ```bash
   # Verify staging deployment success
   # (Minimum 24 hours soak time in staging recommended)
   
   # Confirm production health
   ./scripts/health_check.sh production
   
   # Verify backup
   ./scripts/verify_backup.sh production --max-age=24h
   ```

2. **Deployment Window Communication**
   ```bash
   # Post status page update (if downtime expected)
   # Send notification to stakeholders
   # Activate enhanced monitoring
   ```

3. **Deploy Application**

   **Blue-Green Strategy:**
   ```bash
   # Deploy to green environment
   kubectl set image deployment/app-green app=registry/app:${DEPLOY_VERSION} -n production
   kubectl rollout status deployment/app-green -n production --timeout=15m
   
   # Run smoke tests on green
   pytest tests/smoke/ --env=production-green
   
   # Switch traffic to green
   kubectl patch service app-service -n production -p '{"spec":{"selector":{"version":"green"}}}'
   
   # Monitor for 15 minutes
   # If issues: kubectl patch service app-service -n production -p '{"spec":{"selector":{"version":"blue"}}}'
   ```

   **Canary Strategy:**
   ```bash
   # Deploy canary (5% traffic)
   kubectl apply -f k8s/canary-5pct.yaml
   
   # Monitor for 15 minutes (error rate, latency)
   # If healthy: scale to 25%
   kubectl apply -f k8s/canary-25pct.yaml
   
   # Monitor for 30 minutes
   # If healthy: scale to 100%
   kubectl apply -f k8s/production-full.yaml
   ```

   **Rolling Update:**
   ```bash
   # Update deployment (Kubernetes handles rolling update)
   kubectl set image deployment/app app=registry/app:${DEPLOY_VERSION} -n production
   kubectl rollout status deployment/app -n production --timeout=20m
   
   # Pause if issues detected
   kubectl rollout pause deployment/app -n production
   ```

4. **Post-Deployment Validation**
   ```bash
   # Smoke tests
   pytest tests/smoke/ --env=production
   
   # Health check
   curl https://api.example.com/health
   
   # Check dashboards
   # - Error rate: within baseline ±5%
   # - P95 latency: within SLO
   # - Business metrics: consistent with forecast
   ```

5. **Monitoring Window**
   - **First 15 minutes:** Active monitoring by deployment engineer.
   - **First hour:** On-call engineer available for immediate rollback.
   - **First 24 hours:** Enhanced monitoring; on-call engineer briefed on deployment.

6. **Document & Communicate**
   ```bash
   # Log deployment
   echo '{
     "timestamp": "'$(date -u +%Y-%m-%dT%H:%M:%SZ)'",
     "environment": "production",
     "version": "'${DEPLOY_VERSION}'",
     "commit": "'${DEPLOY_COMMIT}'",
     "operator": "'${USER}'",
     "strategy": "blue-green",
     "approvals": ["SENTINEL", "SERVICE-OWNER"],
     "status": "success",
     "verification": "logs/ci/smoke_tests_'$(date -u +%Y%m%dT%H%M%SZ)'.log"
   }' > logs/deployments/deploy_$(date -u +%Y%m%dT%H%M%SZ).json
   
   # Update Change Log
   # Post status page update: "Deployment complete"
   # Notify stakeholders via Slack/email
   ```

## Rollback Procedures

### When to Rollback

- Error rate exceeds baseline by >10% for >5 minutes.
- P95 latency exceeds SLO threshold by >20% for >5 minutes.
- Critical functionality broken (confirmed by smoke tests).
- Business metrics anomaly detected (transactions dropped, sign-ups failed).
- Manual decision by Governance Sentinel or on-call engineer.

### Rollback Execution

**Blue-Green Rollback (Immediate):**
```bash
# Switch traffic back to blue (previous version)
kubectl patch service app-service -n production -p '{"spec":{"selector":{"version":"blue"}}}'

# Verify restoration
pytest tests/smoke/ --env=production
curl https://api.example.com/health

# Log rollback
echo "Rollback executed at $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> logs/deployments/rollback_${DEPLOY_VERSION}.log
```

**Canary/Rolling Rollback:**
```bash
# Revert to previous deployment version
kubectl rollout undo deployment/app -n production

# Or specify revision
kubectl rollout undo deployment/app --to-revision=<previous-revision> -n production

# Wait for rollout completion
kubectl rollout status deployment/app -n production

# Verify restoration
pytest tests/smoke/ --env=production
```

**Database Rollback (if schema changes deployed):**
```bash
# Option A: Run rollback migration script
python manage.py migrate app_name 0042_previous_migration

# Option B: Restore from backup (last resort)
# See DOC-0026-backup-restore-runbook.md
```

### Post-Rollback Actions

1. **Verify Service Restoration**
   - Confirm error rate returned to baseline.
   - Validate latency within SLO.
   - Check business metrics recovered.

2. **Create Incident Record**
   ```bash
   mkdir -p artifacts/integration/incident-$(date -u +%Y%m%dT%H%M%SZ)
   cd artifacts/integration/incident-$(date -u +%Y%m%dT%H%M%SZ)
   
   # Create timeline
   cat > timeline.md << EOF
   # Incident Timeline: Deployment Rollback
   
   **Version:** ${DEPLOY_VERSION}
   **Deployed:** [timestamp]
   **Rolled Back:** $(date -u +%Y-%m-%dT%H:%M:%SZ)
   
   ## Timeline
   - [time] - Deployment completed
   - [time] - Error rate spike detected
   - [time] - Rollback initiated
   - [time] - Service restored
   EOF
   ```

3. **Schedule Postmortem**
   - Within 48 hours for production rollbacks.
   - Document in `DEC-INCIDENT-####` per `DOC-0018`.

4. **Update Change Log**
   - Add rollback entry referencing original deployment.
   - Include root cause (once known) and prevention plan.

## Emergency Hotfix Deployment

For critical production issues requiring immediate fix (outside standard windows):

**Approval:** Any two Governance Board members + mandatory postmortem.

**Process:**

1. **Create Hotfix Branch**
   ```bash
   git checkout -b hotfix/critical-issue-fix main
   # Make minimal fix
   git commit -m "Hotfix: Critical issue description"
   git tag hotfix-v1.2.4
   ```

2. **Fast-Track Validation**
   ```bash
   # Run targeted tests (not full suite)
   pytest tests/critical_path/ -v
   
   # Deploy to staging (abbreviated soak time: 15 minutes)
   ./scripts/deploy.sh staging hotfix-v1.2.4
   pytest tests/smoke/ --env=staging
   ```

3. **Production Deployment**
   ```bash
   # Document emergency approval
   echo "Emergency deployment approved by: [NAME1], [NAME2] at $(date)" >> logs/approvals/hotfix-v1.2.4.txt
   
   # Deploy with accelerated timeline
   ./scripts/deploy.sh production hotfix-v1.2.4
   
   # Enhanced monitoring (on-call engineer actively watching)
   ```

4. **Post-Hotfix Actions**
   - Merge hotfix to main branch within 24 hours.
   - Conduct postmortem within 24 hours.
   - Review why issue wasn't caught earlier (improve tests/gates).

## Deployment Troubleshooting

### Issue: Deployment Stuck/Timeout

**Symptoms:** Deployment command times out; pods not ready.

**Diagnosis:**
```bash
# Check pod status
kubectl get pods -n production

# View pod logs
kubectl logs <pod-name> -n production

# Describe pod for events
kubectl describe pod <pod-name> -n production
```

**Common Causes:**
- Image pull failure (registry auth, network).
- Health check failure (misconfigured probe, slow startup).
- Resource limits (insufficient CPU/memory).

**Resolution:**
- Fix underlying issue (update registry secret, adjust probes, scale resources).
- Rollback if issue cannot be resolved quickly.

### Issue: Post-Deployment Error Spike

**Symptoms:** Error rate elevated after deployment.

**Diagnosis:**
```bash
# Check recent logs for new errors
kubectl logs deployment/app -n production --since=10m | grep ERROR

# Compare error types before/after deployment
# Review dashboards for specific endpoint failures
```

**Common Causes:**
- New bug introduced in code.
- Configuration mismatch (environment variable, feature flag).
- Database migration issue (missing index, constraint violation).

**Resolution:**
- If config issue: Apply config fix via fast-track.
- If code bug: Rollback immediately; fix in hotfix branch.

### Issue: Database Connection Failures

**Symptoms:** Application can't connect to database post-deployment.

**Diagnosis:**
```bash
# Test database connectivity
psql -h db-host -U db-user -d db-name -c "SELECT 1;"

# Check connection pool status (app-specific)
curl http://app-pod/admin/db-pool-status
```

**Common Causes:**
- Credentials changed/rotated but not updated in app config.
- Network policy change blocking database access.
- Connection pool exhausted (new code pattern causing more connections).

**Resolution:**
- Verify credentials in secret/vault match database.
- Check network policies (security groups, firewall rules).
- Adjust connection pool size if needed; rollback if issue persists.

## Maintenance Windows

### Scheduled Maintenance

**Frequency:** Monthly (first Tuesday, 02:00-04:00 UTC).

**Notification:** 7 days advance notice to customers.

**Activities:**
- Database maintenance (vacuuming, index rebuilds).
- Security patches (OS, libraries, frameworks).
- Infrastructure scaling/tuning.

### Freeze Periods

**No deployments during:**
- High-traffic events (Black Friday, product launches).
- Holidays (December 24-26, December 31-January 2).
- Executive demos or critical business milestones.

**Exceptions:** SEV-1 hotfixes approved by Governance Board.

## Contacts

- **Deployment Engineer:** Primary deployer (check on-call rotation).
- **On-Call Engineer:** Monitoring and rollback authority.
- **Service Owner:** Business approval and escalation.
- **Governance Sentinel:** Production deployment approval.

Current contacts in `docs/status/oncall-status.md`.

## Continuous Improvement

- Review deployment process quarterly.
- Automate manual steps incrementally.
- Update runbook after every deployment issue.
- Conduct deployment drills (including rollback) quarterly.
- Document learnings in decision records (`DEC-DEPLOY-####`).

By following this runbook, teams ensure safe, repeatable deployments with clear rollback procedures and audit trails that maintain system reliability and customer trust.
