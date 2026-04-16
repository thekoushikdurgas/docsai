
import os
import json
from pathlib import Path

# Create the complete Contact360 documentation structure

base_path = "/tmp/contact360_docs"
os.makedirs(base_path, exist_ok=True)

# Define the complete 11.x.x roadmap structure
roadmap = {
    "0-foundations": {
        "01-authentication": [
            "01-auth-strategy.md",
            "02-jwt-token-implementation.md",
            "03-refresh-token-rotation.md",
            "04-multi-factor-authentication.md",
            "05-passwordless-auth.md",
            "06-oauth2-flow.md",
            "07-single-sign-on-saml.md",
            "08-session-management.md"
        ],
        "02-authorization": [
            "01-rbac-design.md",
            "02-role-hierarchy.md",
            "03-permission-mapping.md",
            "04-policy-enforcement.md",
            "05-api-authorization.md",
            "06-resource-based-access-control.md"
        ],
        "03-database": [
            "01-postgres-schema-design.md",
            "02-connection-pooling.md",
            "03-migration-strategy.md",
            "04-backup-recovery.md",
            "05-data-archival.md"
        ],
        "04-caching": [
            "01-redis-strategy.md",
            "02-cache-invalidation.md",
            "03-distributed-caching.md"
        ],
        "05-message-queue": [
            "01-kafka-topic-design.md",
            "02-event-streaming-architecture.md",
            "03-dlq-handling.md"
        ]
    },
    "1-billing": {
        "01-subscription-management": [
            "01-subscription-plans.md",
            "02-billing-cycle-management.md",
            "03-usage-metering.md",
            "04-overage-handling.md"
        ],
        "02-payment-processing": [
            "01-payment-processor-integration.md",
            "02-payment-retries.md",
            "03-payment-webhooks.md"
        ],
        "03-credit-system": [
            "01-credit-allocation.md",
            "02-credit-expiration.md",
            "03-credit-redemption.md",
            "04-credit-analytics.md"
        ]
    },
    "2-email-phone": {
        "01-email-enrichment": [
            "01-email-discovery-strategy.md",
            "02-provider-integration.md",
            "03-email-validation-service.md",
            "04-pattern-matching-algorithm.md",
            "05-bulk-email-lookup.md",
            "06-email-verification-webhooks.md"
        ],
        "02-phone-system": [
            "01-phone-validation-service.md",
            "02-phone-provider-integration.md",
            "03-phone-lookup-caching.md",
            "04-international-phone-handling.md",
            "05-phone-verification-flow.md"
        ],
        "03-verification": [
            "01-smtp-verification.md",
            "02-dns-mx-record-checking.md",
            "03-bounce-handling.md",
            "04-complaint-tracking.md"
        ]
    },
    "3-contacts-companies": {
        "01-contact-management": [
            "01-contact-entity-design.md",
            "02-contact-deduplication.md",
            "03-contact-merge-strategy.md",
            "04-contact-activity-tracking.md",
            "05-contact-lifecycle.md",
            "06-contact-segmentation.md"
        ],
        "02-company-management": [
            "01-company-entity-design.md",
            "02-company-hierarchy.md",
            "03-company-enrichment.md",
            "04-company-technology-detection.md",
            "05-company-financials.md"
        ],
        "03-relationship-management": [
            "01-contact-company-relationships.md",
            "02-contact-deal-relationships.md",
            "03-contact-activity-relationships.md"
        ]
    },
    "4-extension": {
        "01-browser-extension": [
            "01-chrome-mv3-architecture.md",
            "02-background-script-design.md",
            "03-content-script-communication.md",
            "04-popup-ui-design.md",
            "05-extension-permissions.md"
        ],
        "02-linkedin-integration": [
            "01-linkedin-data-scraping.md",
            "02-linkedin-profile-parsing.md",
            "03-linkedin-sales-navigator-integration.md",
            "04-real-time-linkedin-enrichment.md"
        ],
        "03-gmail-integration": [
            "01-gmail-api-access.md",
            "02-email-context-enrichment.md",
            "03-quick-actions-in-gmail.md"
        ],
        "04-data-ingestion": [
            "01-event-capture-from-extension.md",
            "02-data-normalization.md",
            "03-deduplication-strategy.md",
            "04-real-time-sync.md"
        ]
    },
    "5-ai-workflows": {
        "01-langgraph-orchestration": [
            "01-langgraph-agent-design.md",
            "02-state-machine-workflow.md",
            "03-conditional-execution.md",
            "04-error-handling-in-workflows.md",
            "05-workflow-persistence.md"
        ],
        "02-llm-integration": [
            "01-multi-llm-provider-strategy.md",
            "02-prompt-engineering-framework.md",
            "03-prompt-versioning.md",
            "04-token-optimization.md",
            "05-cost-tracking.md"
        ],
        "03-rag-system": [
            "01-vector-embedding-strategy.md",
            "02-pgvector-indexing.md",
            "03-hybrid-search.md",
            "04-context-retrieval.md",
            "05-semantic-caching.md"
        ],
        "04-agent-actions": [
            "01-tool-calling-framework.md",
            "02-action-execution-engine.md",
            "03-approval-workflows.md",
            "04-rollback-mechanisms.md"
        ]
    },
    "6-reliability-scaling": {
        "01-high-availability": [
            "01-redundancy-strategy.md",
            "02-failover-mechanisms.md",
            "03-circuit-breaker-pattern.md",
            "04-health-checks.md",
            "05-graceful-degradation.md"
        ],
        "02-performance": [
            "01-caching-strategy.md",
            "02-database-optimization.md",
            "03-query-optimization.md",
            "04-index-strategy.md",
            "05-denormalization-decisions.md"
        ],
        "03-scaling": [
            "01-horizontal-scaling.md",
            "02-vertical-scaling.md",
            "03-database-sharding.md",
            "04-load-balancing-strategy.md",
            "05-auto-scaling-rules.md"
        ],
        "04-disaster-recovery": [
            "01-backup-strategy.md",
            "02-rpo-rto-targets.md",
            "03-recovery-procedures.md",
            "04-data-replication.md",
            "05-geo-redundancy.md"
        ]
    },
    "7-deployment": {
        "01-containerization": [
            "01-docker-strategy.md",
            "02-dockerfile-best-practices.md",
            "03-multi-stage-builds.md",
            "04-registry-management.md"
        ],
        "02-orchestration": [
            "01-kubernetes-architecture.md",
            "02-helm-charts.md",
            "03-deployment-strategy.md",
            "04-service-mesh.md",
            "05-ingress-management.md"
        ],
        "03-ci-cd": [
            "01-github-actions-workflow.md",
            "02-automated-testing.md",
            "03-code-quality-gates.md",
            "04-semantic-versioning.md",
            "05-release-management.md"
        ],
        "04-monitoring": [
            "01-prometheus-metrics.md",
            "02-grafana-dashboards.md",
            "03-distributed-tracing.md",
            "04-log-aggregation.md",
            "05-alerting-rules.md"
        ]
    },
    "8-apis": {
        "01-api-design": [
            "01-api-style-decision.md",
            "02-api-versioning-strategy.md",
            "03-api-style-guide.md"
        ],
        "02-http-standards": [
            "01-http-methods-and-status-codes.md",
            "02-request-body-standards.md",
            "03-response-body-standards.md"
        ],
        "03-error-handling": [
            "01-error-response-format.md",
            "02-input-validation-standards.md",
            "03-rate-limit-error-responses.md"
        ],
        "04-authentication": [
            "01-api-key-management.md",
            "02-oauth2-for-apis.md",
            "03-jwt-validation.md"
        ],
        "05-documentation": [
            "01-openapi-specification.md",
            "02-api-documentation-site.md",
            "03-sdk-generation.md",
            "04-changelog-management.md"
        ]
    },
    "9-integrations": {
        "01-crm-integrations": [
            "01-crm-integration-abstraction-layer.md",
            "02-crm-integration-connector-framework.md",
            "03-integration-data-mapping-strategy.md",
            "04-salesforce-oauth2-flow.md",
            "05-salesforce-contact-lead-sync.md",
            "06-salesforce-campaign-integration.md",
            "07-salesforce-activity-logging.md",
            "08-hubspot-oauth2-and-api.md",
            "09-hubspot-contact-company-sync.md",
            "10-hubspot-engagement-tracking.md",
            "11-hubspot-workflow-triggers.md",
            "12-pipedrive-oauth-and-api.md",
            "13-pipedrive-deal-contact-sync.md",
            "14-pipedrive-activity-sync.md",
            "15-copper-crm-integration.md",
            "16-zoho-crm-integration.md",
            "17-microsoft-dynamics-integration.md"
        ],
        "02-email-comms": [
            "01-gmail-api-integration.md",
            "02-outlook-microsoft-graph-integration.md",
            "03-email-sync-strategy.md",
            "04-sendgrid-integration.md",
            "05-mailgun-integration.md",
            "06-aws-ses-integration.md",
            "07-postmark-integration.md",
            "08-twilio-sms-integration.md",
            "09-aws-sns-integration.md",
            "10-whatsapp-business-api-integration.md",
            "11-slack-integration.md",
            "12-microsoft-teams-integration.md",
            "13-discord-integration.md"
        ],
        "03-calendar-meetings": [
            "01-google-calendar-sync.md",
            "02-outlook-calendar-sync.md",
            "03-ical-caldav-support.md",
            "04-gong-integration.md",
            "05-chorus-integration.md",
            "06-otter-ai-integration.md",
            "07-calendly-integration.md",
            "08-acuity-scheduling-integration.md",
            "09-native-scheduling-feature.md"
        ],
        "04-data-partners": [
            "01-hunter-io-integration.md",
            "02-apollo-io-integration.md",
            "03-rocketreach-integration.md",
            "04-clearbit-integration.md",
            "05-crunchbase-integration.md",
            "06-zoominfo-integration.md",
            "07-pitchbook-integration.md",
            "08-zerobounce-integration.md",
            "09-neverbounce-integration.md",
            "10-truecaller-integration.md"
        ],
        "05-automation": [
            "01-zapier-integration.md",
            "02-make-com-integration.md",
            "03-ifttt-integration.md",
            "04-n8n-integration.md",
            "05-automation-anywhere-integration.md",
            "06-uipath-integration.md",
            "07-contact360-workflow-builder.md",
            "08-workflow-templates.md",
            "09-workflow-execution-monitoring.md"
        ],
        "06-analytics": [
            "01-looker-integration.md",
            "02-tableau-integration.md",
            "03-power-bi-integration.md",
            "04-snowflake-integration.md",
            "05-bigquery-integration.md",
            "06-redshift-integration.md",
            "07-mixpanel-integration.md",
            "08-amplitude-integration.md",
            "09-segment-integration.md"
        ],
        "07-billing": [
            "01-stripe-integration.md",
            "02-paddle-integration.md",
            "03-chargebee-integration.md",
            "04-subscription-management.md",
            "05-usage-based-billing.md",
            "06-invoice-receipt-management.md",
            "07-tax-calculation-integration.md",
            "08-revenue-recognition.md",
            "09-accounting-software-integration.md"
        ],
        "08-support": [
            "01-zendesk-integration.md",
            "02-freshdesk-integration.md",
            "03-intercom-integration.md",
            "04-gainsight-integration.md",
            "05-catalyst-integration.md",
            "06-vitally-integration.md",
            "07-notion-integration.md",
            "08-confluence-integration.md",
            "09-help-scout-integration.md"
        ],
        "09-marketing": [
            "01-marketo-integration.md",
            "02-eloqua-integration.md",
            "03-activecampaign-integration.md",
            "04-6sense-integration.md",
            "05-demandbase-integration.md",
            "06-terminus-integration.md",
            "07-linkedin-integration.md",
            "08-g2-integration.md",
            "09-bombora-integration.md"
        ],
        "10-content": [
            "01-wordpress-integration.md",
            "02-contentful-integration.md",
            "03-webflow-integration.md",
            "04-dropbox-integration.md",
            "05-google-drive-integration.md",
            "06-box-integration.md",
            "07-canto-dam-integration.md",
            "08-widen-dam-integration.md"
        ]
    },
    "10-campaigns": {
        "01-campaign-core": [
            "01-campaign-entity-schema.md",
            "02-campaign-lifecycle-states.md",
            "03-campaign-ownership-permissions.md",
            "04-email-campaign-types.md",
            "05-sms-campaign-types.md",
            "06-multi-channel-campaign-types.md",
            "07-abm-campaign-types.md",
            "08-audience-selection-targeting.md",
            "09-segmentation-engine.md",
            "10-dynamic-audience-building.md",
            "11-one-time-send-scheduling.md",
            "12-recurring-send-scheduling.md",
            "13-timezone-aware-scheduling.md",
            "14-optimal-send-time-ai.md"
        ],
        "02-email-builder": [
            "01-email-builder-ui-design.md",
            "02-rich-text-editor-features.md",
            "03-email-block-library.md",
            "04-dynamic-field-insertion.md",
            "05-conditional-email-blocks.md",
            "06-ai-powered-personalization.md",
            "07-email-preview-and-test-send.md",
            "08-spam-score-checking.md",
            "09-ab-testing-variants.md",
            "10-can-spam-compliance.md",
            "11-gdpr-compliance-emails.md",
            "12-email-best-practices.md"
        ],
        "03-sms-builder": [
            "01-sms-editor-and-interface.md",
            "02-sms-personalization-features.md",
            "03-sms-ab-testing.md",
            "04-whatsapp-message-builder.md",
            "05-whatsapp-template-management.md",
            "06-whatsapp-compliance.md",
            "07-push-notification-builder.md",
            "08-mobile-push-app-integration.md",
            "09-push-notification-deep-links.md"
        ],
        "04-templates": [
            "01-template-entity-design.md",
            "02-template-types-categories.md",
            "03-template-versioning-system.md",
            "04-prebuilt-template-library.md",
            "05-custom-template-creation.md",
            "06-template-categories-and-search.md",
            "07-shared-template-management.md",
            "08-template-sharing-permissions.md",
            "09-template-approval-workflow.md",
            "10-template-variable-system.md",
            "11-template-inheritance-and-override.md",
            "12-template-branding-customization.md"
        ],
        "05-execution": [
            "01-campaign-send-queue-design.md",
            "02-batch-delivery-strategy.md",
            "03-delivery-throttling-strategy.md",
            "04-delivery-status-states.md",
            "05-realtime-delivery-updates.md",
            "06-delivery-retry-logic.md",
            "07-campaign-pause-functionality.md",
            "08-campaign-resume-functionality.md",
            "09-campaign-cancellation-handling.md"
        ],
        "06-sequences": [
            "01-sequence-entity-design.md",
            "02-sequence-builder-ui.md",
            "03-sequence-step-types.md",
            "04-sequence-trigger-types.md",
            "05-sequence-condition-logic.md",
            "06-sequence-decision-trees.md",
            "07-sequence-enrollment.md",
            "08-sequence-execution-state.md",
            "09-sequence-step-tracking.md",
            "10-adaptive-sequences.md",
            "11-sequence-reenrollment.md",
            "12-sequence-branching.md"
        ],
        "07-analytics": [
            "01-email-campaign-metrics.md",
            "02-email-engagement-metrics.md",
            "03-email-conversion-metrics.md",
            "04-sms-campaign-metrics.md",
            "05-whatsapp-campaign-metrics.md",
            "06-multi-channel-aggregate-metrics.md",
            "07-campaign-summary-dashboard.md",
            "08-detailed-performance-dashboard.md",
            "09-comparative-campaign-analytics.md",
            "10-campaign-performance-report.md",
            "11-scheduled-report-delivery.md",
            "12-campaign-data-export.md"
        ],
        "08-testing": [
            "01-ab-test-types.md",
            "02-test-variant-creation.md",
            "03-ab-split-configuration.md",
            "04-test-hypothesis-metrics.md",
            "05-statistical-significance-testing.md",
            "06-test-result-analysis.md",
            "07-winner-selection.md",
            "08-winning-variant-rollout.md",
            "09-multivariate-testing.md"
        ],
        "09-workflows": [
            "01-workflow-entity-design.md",
            "02-workflow-trigger-types.md",
            "03-workflow-step-types.md",
            "04-multi-campaign-orchestration.md",
            "05-campaign-handoff-logic.md",
            "06-frequency-capping-rules.md",
            "07-customer-journey-mapping.md",
            "08-cross-campaign-attribution.md",
            "09-campaign-suppression-rules.md"
        ],
        "10-personalization": [
            "01-dynamic-content-blocks.md",
            "02-personalization-tokens.md",
            "03-conditional-content-logic.md",
            "04-ai-subject-line-generation.md",
            "05-ai-content-recommendations.md",
            "06-ai-send-time-optimization.md",
            "07-account-based-personalization.md",
            "08-behavioral-personalization.md",
            "09-predictive-personalization.md"
        ],
        "11-content-library": [
            "01-content-repository-design.md",
            "02-content-tagging-organization.md",
            "03-content-versioning.md",
            "04-image-asset-management.md",
            "05-video-asset-management.md",
            "06-document-asset-management.md",
            "07-asset-sharing-permissions.md",
            "08-brand-asset-management.md",
            "09-asset-license-tracking.md"
        ],
        "12-compliance": [
            "01-can-spam-compliance-enforcement.md",
            "02-gdpr-compliance-enforcement.md",
            "03-casl-compliance.md",
            "04-campaign-approval-workflow.md",
            "05-campaign-content-review.md",
            "06-campaign-audit-logging.md",
            "07-unsubscribe-handling.md",
            "08-email-preference-center.md",
            "09-dnd-list-compliance.md"
        ],
        "13-crm-ai": [
            "01-crm-campaign-creation.md",
            "02-contact-sync-with-crm.md",
            "03-campaign-activity-logging-crm.md",
            "04-ai-campaign-creation.md",
            "05-ai-campaign-optimization.md",
            "06-ai-content-generation.md",
            "07-predictive-campaign-analytics.md",
            "08-anomaly-detection.md",
            "09-ai-recommendations.md"
        ],
        "14-localization": [
            "01-multi-language-templates.md",
            "02-automatic-translation-service.md",
            "03-language-detection.md",
            "04-regional-template-variants.md",
            "05-currency-timezone-localization.md",
            "06-regional-compliance-rules.md"
        ],
        "15-qa": [
            "01-campaign-validation-checklist.md",
            "02-link-validation-and-checking.md",
            "03-content-quality-review.md",
            "04-email-client-preview-testing.md",
            "05-mobile-device-testing.md",
            "06-deliverability-testing.md",
            "07-campaign-load-testing.md",
            "08-failure-scenario-testing.md",
            "09-data-consistency-testing.md"
        ],
        "16-monitoring": [
            "01-campaign-progress-dashboard.md",
            "02-delivery-monitoring.md",
            "03-engagement-monitoring.md",
            "04-campaign-alert-conditions.md",
            "05-campaign-alert-routing.md",
            "06-alert-remediation-actions.md",
            "07-campaign-health-scoring.md",
            "08-campaign-kpi-dashboards.md",
            "09-campaign-trend-analysis.md"
        ],
        "17-automation": [
            "01-event-based-campaign-triggers.md",
            "02-time-based-campaign-triggers.md",
            "03-behavioral-campaign-triggers.md",
            "04-smart-channel-routing.md",
            "05-frequency-intelligence.md",
            "06-audience-intelligence.md",
            "07-adaptive-campaign-sending.md",
            "08-adaptive-content.md",
            "09-predictive-campaign-logic.md"
        ],
        "18-templates": [
            "01-campaign-template-types.md",
            "02-prebuilt-campaign-templates.md",
            "03-custom-campaign-templates.md",
            "04-campaign-cloning.md",
            "05-campaign-variants.md",
            "06-campaign-sequencing.md",
            "07-campaign-benchmarks.md",
            "08-campaign-best-practices.md",
            "09-performance-comparison.md"
        ],
        "19-versioning": [
            "01-campaign-version-control.md",
            "02-campaign-version-comparison.md",
            "03-campaign-version-rollback.md",
            "04-campaign-edit-history.md",
            "05-campaign-send-history.md",
            "06-campaign-audit-trail.md"
        ],
        "20-insights": [
            "01-ai-campaign-insights.md",
            "02-campaign-performance-analysis.md",
            "03-campaign-trend-identification.md",
            "04-next-campaign-recommendations.md",
            "05-content-recommendations.md",
            "06-audience-recommendations.md",
            "07-competitor-campaign-tracking.md",
            "08-industry-benchmark-comparison.md",
            "09-best-practice-alerts.md"
        ]
    },
    "11-lead-generation": {
        "01-lead-generation": [
            "01-lead-generation-platform-design.md",
            "02-lead-source-diversification.md",
            "03-lead-qualification-framework.md",
            "04-inbound-lead-sources.md",
            "05-outbound-lead-sourcing.md",
            "06-partner-lead-sourcing.md",
            "07-event-lead-capture.md",
            "08-bulk-lead-import.md",
            "09-automatic-lead-enrichment.md",
            "10-lead-data-quality-validation.md"
        ],
        "02-lead-scoring": [
            "01-demographic-lead-scoring.md",
            "02-behavioral-lead-scoring.md",
            "03-firmographic-lead-scoring.md",
            "04-ml-based-lead-scoring.md",
            "05-predictive-lead-scoring.md",
            "06-custom-lead-scoring-models.md",
            "07-lead-grade-assignment.md",
            "08-mql-sql-classification.md",
            "09-lead-fit-scoring.md",
            "10-realtime-lead-score-updates.md",
            "11-batch-lead-scoring.md",
            "12-lead-score-decay.md"
        ],
        "03-intent": [
            "01-first-party-intent-tracking.md",
            "02-second-party-intent-data.md",
            "03-third-party-intent-providers.md",
            "04-job-change-signal-detection.md",
            "05-company-activity-signal-detection.md",
            "06-technology-signal-detection.md",
            "07-intent-signal-scoring.md",
            "08-urgency-scoring.md",
            "09-intent-signal-aggregation.md"
        ],
        "04-icp": [
            "01-icp-definition-builder.md",
            "02-icp-attribute-definitions.md",
            "03-icp-attribute-weighting.md",
            "04-icp-matching-scoring.md",
            "05-partial-icp-matching.md",
            "06-lookalike-audience-modeling.md",
            "07-icp-continuous-learning.md",
            "08-win-loss-analysis-for-icp.md",
            "09-icp-versioning-and-updates.md"
        ],
        "05-recommendations": [
            "01-recommendation-engine-design.md",
            "02-recommendation-models.md",
            "03-realtime-vs-batch-recommendations.md",
            "04-per-user-lead-recommendations.md",
            "05-per-account-lead-recommendations.md",
            "06-per-org-lead-recommendations.md",
            "07-lead-fit-for-user-scoring.md",
            "08-lead-relevance-scoring.md",
            "09-lead-priority-ranking.md"
        ],
        "06-content-recommendations": [
            "01-content-recommendation-engine.md",
            "02-personalized-content-recommendations.md",
            "03-content-sequencing.md",
            "04-feature-recommendations.md",
            "05-upsell-recommendations.md",
            "06-expansion-recommendations.md",
            "07-cross-sell-recommendations.md",
            "08-partner-product-recommendations.md",
            "09-bundled-offer-recommendations.md"
        ],
        "07-nba": [
            "01-next-best-action-engine.md",
            "02-action-type-recommendations.md",
            "03-action-timing-recommendations.md",
            "04-channel-recommendation.md",
            "05-outreach-message-recommendations.md",
            "06-optimal-sender-recommendations.md",
            "07-engagement-level-recommendations.md",
            "08-contact-frequency-recommendations.md",
            "09-disengagement-recommendations.md"
        ],
        "08-abm": [
            "01-account-recommendation-engine.md",
            "02-high-value-account-identification.md",
            "03-account-prioritization-ranking.md",
            "04-account-expansion-recommendations.md",
            "05-new-department-opportunities.md",
            "06-use-case-expansion-recommendations.md",
            "07-stakeholder-recommendations.md",
            "08-decision-maker-mapping.md",
            "09-buying-committee-recommendations.md"
        ],
        "09-lead-routing": [
            "01-lead-routing-engine.md",
            "02-territory-based-routing.md",
            "03-skill-based-routing.md",
            "04-round-robin-routing.md",
            "05-capacity-aware-routing.md",
            "06-performance-based-routing.md",
            "07-lead-acceptance-workflow.md",
            "08-automatic-rerouting.md",
            "09-lead-ownership-tracking.md"
        ],
        "10-nurture": [
            "01-nurture-path-recommendations.md",
            "02-nurture-content-recommendations.md",
            "03-nurture-timing-recommendations.md",
            "04-engagement-progression-tracking.md",
            "05-engagement-drop-detection.md",
            "06-reenengagement-recommendations.md",
            "07-dynamic-nurture-sequences.md",
            "08-preference-based-nurture.md",
            "09-role-specific-nurture.md"
        ],
        "11-competitive": [
            "01-competitor-customer-identification.md",
            "02-competitor-win-loss-analysis.md",
            "03-competitive-positioning-recommendations.md",
            "04-market-trend-analysis.md",
            "05-industry-vertical-insights.md",
            "06-emerging-opportunity-detection.md",
            "07-lead-generation-benchmarks.md",
            "08-sales-performance-benchmarks.md",
            "09-pricing-intelligence.md"
        ],
        "12-explainability": [
            "01-recommendation-explainability.md",
            "02-factor-attribution-analysis.md",
            "03-recommendation-confidence-scoring.md",
            "04-recommendation-feedback-loop.md",
            "05-relevance-validation.md",
            "06-recommendation-quality-scoring.md",
            "07-bias-detection.md",
            "08-fairness-monitoring.md",
            "09-bias-mitigation-strategies.md"
        ],
        "13-testing": [
            "01-ab-test-recommendations.md",
            "02-statistical-significance-testing.md",
            "03-multivariate-recommendation-testing.md",
            "04-recommendation-accuracy-metrics.md",
            "05-business-impact-metrics.md",
            "06-conversion-lift-measurement.md",
            "07-model-hyperparameter-tuning.md",
            "08-recommendation-feature-engineering.md",
            "09-model-retraining-schedule.md"
        ],
        "14-dashboard": [
            "01-sales-rep-dashboard.md",
            "02-manager-dashboard.md",
            "03-executive-dashboard.md",
            "04-recommendation-performance-insights.md",
            "05-top-recommendation-insights.md",
            "06-recommendation-adoption-metrics.md",
            "07-recommendation-trend-analysis.md",
            "08-cohort-analysis.md",
            "09-sales-forecasting.md"
        ],
        "15-mobile": [
            "01-mobile-recommendation-ux.md",
            "02-push-notification-recommendations.md",
            "03-realtime-mobile-alerts.md",
            "04-notification-delivery-optimization.md",
            "05-notification-frequency-capping.md",
            "06-notification-preference-learning.md"
        ],
        "16-voice": [
            "01-voice-assistant-integration.md",
            "02-nlp-recommendation-queries.md",
            "03-voice-command-actions.md",
            "04-chatbot-recommendations.md",
            "05-conversational-lead-discovery.md",
            "06-conversational-lead-qualification.md"
        ],
        "17-privacy": [
            "01-privacy-preserving-recommendations.md",
            "02-data-minimization-in-recommendations.md",
            "03-user-consent-for-recommendations.md",
            "04-fairness-in-recommendations.md",
            "05-recommendation-transparency.md",
            "06-user-control-over-recommendations.md",
            "07-gdpr-recommendation-compliance.md",
            "08-responsible-ai-governance.md",
            "09-recommendation-audit-oversight.md"
        ],
        "18-sales-integration": [
            "01-salesforce-recommendation-integration.md",
            "02-hubspot-recommendation-integration.md",
            "03-native-recommendation-experience.md",
            "04-automated-lead-assignment.md",
            "05-automated-outreach-based-on-recommendations.md",
            "06-workflow-triggers-from-recommendations.md",
            "07-recommendation-sharing.md",
            "08-collaborative-recommendation-review.md",
            "09-recommendation-leaderboard.md"
        ],
        "19-advanced-ml": [
            "01-collaborative-filtering-algorithms.md",
            "02-content-based-filtering.md",
            "03-hybrid-recommendation-systems.md",
            "04-neural-network-recommendations.md",
            "05-transformer-recommendation-models.md",
            "06-graph-neural-network-recommendations.md",
            "07-bandit-algorithm-recommendations.md",
            "08-contextual-bandit-recommendations.md",
            "09-reinforcement-learning-recommendations.md"
        ],
        "20-ecosystem": [
            "01-recommendation-api.md",
            "02-third-party-recommendation-plugins.md",
            "03-recommendation-marketplace.md",
            "04-recommendation-as-a-service.md",
            "05-recommendation-scoring-api.md",
            "06-custom-recommendation-models.md",
            "07-premium-recommendation-tiers.md",
            "08-recommendation-data-licensing.md",
            "09-recommendation-affiliate-model.md"
        ]
    }
}

# Create all directories and files
total_files = 0
for phase, categories in roadmap.items():
    phase_path = os.path.join(base_path, phase)
    os.makedirs(phase_path, exist_ok=True)
    
    for category, files in categories.items():
        category_path = os.path.join(phase_path, category)
        os.makedirs(category_path, exist_ok=True)
        
        for file in files:
            file_path = os.path.join(category_path, file)
            # Create empty markdown file with header
            with open(file_path, 'w') as f:
                title = file.replace('.md', '').replace('-', ' ').title()
                f.write(f"# {title}\n\n")
                f.write(f"**File:** `{phase}/{category}/{file}`\n\n")
                f.write("## Overview\n\n")
                f.write("*Content to be added*\n\n")
                f.write("## Details\n\n")
                f.write("- Point 1\n")
                f.write("- Point 2\n")
                f.write("- Point 3\n\n")
                f.write("## Related Files\n\n")
                f.write("- See related documentation\n")
            total_files += 1

# Create a comprehensive index
index_path = os.path.join(base_path, "INDEX.md")
with open(index_path, 'w') as f:
    f.write("# Contact360 Complete Documentation Index\n\n")
    f.write(f"**Total Documentation Files: {total_files}**\n\n")
    f.write("## Directory Structure\n\n")
    
    for phase, categories in roadmap.items():
        phase_name = phase.split('-', 1)[1].replace('-', ' ').title()
        f.write(f"\n### {phase}\n")
        f.write(f"**{phase_name}**\n\n")
        
        for category in categories.keys():
            f.write(f"- `{category}/`\n")

# Generate directory tree
tree_path = os.path.join(base_path, "DIRECTORY_TREE.txt")
with open(tree_path, 'w') as f:
    f.write("Contact360 Documentation Structure\n")
    f.write("=" * 80 + "\n\n")
    
    for phase, categories in sorted(roadmap.items()):
        phase_name = phase.split('-', 1)[1].replace('-', ' ').upper()
        f.write(f"\n{phase}/  ({phase_name})\n")
        f.write("-" * 80 + "\n")
        
        for category, files in sorted(categories.items()):
            f.write(f"\n  {category}/  ({len(files)} files)\n")
            for file in files[:5]:  # Show first 5 files
                f.write(f"    - {file}\n")
            if len(files) > 5:
                f.write(f"    ... and {len(files) - 5} more files\n")

# Create a summary statistics file
stats_path = os.path.join(base_path, "STATISTICS.json")
stats = {
    "total_files": total_files,
    "total_phases": len(roadmap),
    "phases": {}
}

for phase, categories in roadmap.items():
    phase_name = phase.split('-', 1)[1]
    phase_stats = {
        "categories": len(categories),
        "files": sum(len(files) for files in categories.values()),
        "categories_detail": {}
    }
    for category, files in categories.items():
        phase_stats["categories_detail"][category] = len(files)
    stats["phases"][phase_name] = phase_stats

with open(stats_path, 'w') as f:
    json.dump(stats, f, indent=2)

print(f"✅ Contact360 Documentation Structure Created!")
print(f"📁 Location: {base_path}")
print(f"📊 Statistics:")
print(f"   - Total Files: {total_files}")
print(f"   - Total Phases: {len(roadmap)}")
print(f"   - Total Categories: {sum(len(cats) for cats in roadmap.values())}")
print(f"\n📋 Files created:")
print(f"   - INDEX.md")
print(f"   - DIRECTORY_TREE.txt")
print(f"   - STATISTICS.json")
print(f"   - {total_files} content markdown files")

# Print phase breakdown
print(f"\n🎯 Phase Breakdown:")
for phase, categories in sorted(roadmap.items()):
    phase_name = phase.split('-', 1)[1].replace('-', ' ').title()
    file_count = sum(len(files) for files in categories.values())
    print(f"   {phase} - {phase_name}: {file_count} files ({len(categories)} categories)")
