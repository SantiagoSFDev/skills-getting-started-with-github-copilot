# Salesforce Base Code

Salesforce DX project with Apex triggers for `Account` and `Contact` following the
**Trigger → Handler → Helper** pattern.

## Flow

| Trigger | Event | Handler | Helper | Result |
|---|---|---|---|---|
| `AccountTrigger` | `after insert` | `AccountTriggerHandler.handleAfterInsert` | `AccountTriggerHelper.createOpportunities` | One `Opportunity` per inserted Account (linked via `AccountId`) |
| `ContactTrigger` | `after insert` | `ContactTriggerHandler.handleAfterInsert` | `ContactTriggerHelper.createOpportunities` | One `Opportunity` per inserted Contact (linked to the Contact's Account, if any) |

Created Opportunities use `StageName = 'Prospecting'` and `CloseDate = today + 30 days`.
The helpers are bulkified (a single DML for the whole batch).

## Structure

```
salesforce/
├── sfdx-project.json
├── config/project-scratch-def.json
└── force-app/main/default/
    ├── triggers/  AccountTrigger, ContactTrigger
    └── classes/   *TriggerHandler, *TriggerHelper, *TriggerTest
```

## Deploy & test

```bash
cd salesforce
sf org login web --alias my-org
sf project deploy start --source-dir force-app --target-org my-org
sf apex run test --class-names AccountTriggerTest ContactTriggerTest --result-format human --target-org my-org
```
