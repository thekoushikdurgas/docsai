# Sequences Module

**Service:** `backend(dev)/email campaign` (Go, Gin, Asynq)
**Gateway proxy:** Appointment360 GraphQL (`createSequence`, `getSequence`, `listSequences`, `triggerSequence`, `pauseSequence`)
**Direct REST routes:** `POST /sequences`, `GET /sequences/:id`, `POST /sequences/:id/trigger`, `PATCH /sequences/:id/pause` (planned `10.x`)

---

## GraphQL operations (gateway-proxied)

| Operation | Type | Description | Era |
| --- | --- | --- | --- |
| `createSequence` | Mutation | Create a new multi-step email sequence | `10.x` |
| `getSequence` | Query | Get sequence with all steps | `10.x` |
| `listSequences` | Query | List sequences for org | `10.x` |
| `updateSequence` | Mutation | Modify sequence steps or schedule | `10.x` |
| `deleteSequence` | Mutation | Delete sequence and its steps | `10.x` |
| `triggerSequence` | Mutation | Start sequence for an audience | `10.x` |
| `pauseSequence` | Mutation | Pause in-progress sequence | `10.x` |
| `resumeSequence` | Mutation | Resume paused sequence | `10.x` |

---

## GraphQL input/output types

### `createSequence` input

```graphql
input CreateSequenceInput {
  name: String!
  steps: [SequenceStepInput!]!
}

input SequenceStepInput {
  stepType: SequenceStepType!  # SEND_EMAIL | WAIT | BRANCH_ON_OPEN | BRANCH_ON_CLICK
  templateId: ID              # required for SEND_EMAIL step
  delayDays: Int              # required for WAIT step
  condition: String           # for BRANCH steps
}

enum SequenceStepType {
  SEND_EMAIL
  WAIT_DAYS
  BRANCH_ON_OPEN
  BRANCH_ON_CLICK
  BRANCH_ON_NO_OPEN
}
```

### `Sequence` type

```graphql
type Sequence {
  id: ID!
  name: String!
  status: SequenceStatus!  # draft | active | paused | completed
  steps: [SequenceStep!]!
  activeRecipients: Int
  createdAt: DateTime!
}

type SequenceStep {
  id: ID!
  stepType: SequenceStepType!
  template: CampaignTemplate
  delayDays: Int
  condition: String
  position: Int!
}
```

---

## Database tables

| Table | Read | Write |
| --- | --- | --- |
| `sequences` | `getSequence`, `listSequences` | `createSequence`, `updateSequence`, `deleteSequence` |
| `sequence_steps` | `getSequence` | `createSequence` (step insert), `updateSequence` |
| `templates` | Step template fetch | — |
| `recipients` | Active recipient tracking | Sequence trigger creates recipient entries |
| `suppression_list` | Pre-step send check | — |

---

## Frontend page bindings

| Page | Route | Operations used |
| --- | --- | --- |
| Sequences builder | `/campaigns/sequences` | `listSequences`, `createSequence`, `updateSequence` |
| Sequence detail | `/campaigns/sequences/:id` | `getSequence` |
| Sequence trigger | Wizard/launch flow | `triggerSequence` |

---

## Sequence step UI elements

| Step type | UI card | Inputs |
| --- | --- | --- |
| `SEND_EMAIL` | Email step card | Template picker dropdown, subject preview |
| `WAIT_DAYS` | Wait step card | Days input field (numeric) |
| `BRANCH_ON_OPEN` | Branch card | Condition radio: "if opened / if not opened" |
| `BRANCH_ON_CLICK` | Branch card | Condition radio: "if clicked / if not clicked" |

---

## Era context

The sequences engine is a `10.x` feature. In prior eras, sequence-related API calls return `501 Not Implemented`. Era task-pack: `docs/10. Contact360 email campaign/emailcampaign-email-campaign-task-pack.md` (Track B-10.1 and B-10.2).
