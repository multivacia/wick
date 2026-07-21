# UX-R2 Remaining Release — Integral Plan Spec

```text
RELEASE = UX-R2
TASK_ID = UX-R2-REMAINING-RELEASE-INTEGRAL-PLAN-001
PHASE = INTEGRAL_RELEASE_PLANNING_AND_AUTHORIZATION_ASSESSMENT
CHANGE_RISK = HIGH
IMPACT_ASSESSMENT_STATUS = APPROVED
ASSESSMENT_ONLY = true
DECISION = AUTHORIZED_FOR_SINGLE_EXECUTION_WITH_CONDITIONS
REVIEW_STATUS = APPROVED
MERGE_STATUS = AWAITING_HUMAN_AUTHORIZATION
IMPACT = docs/ai-impact/UX-R2-REMAINING-RELEASE-INTEGRAL-PLAN_IMPACT_ASSESSMENT.md
FROZEN_SCOPE = docs/releases/UX-R2-REMAINING-RELEASE-FROZEN-SCOPE.md
```

## Release definition

```text
UX_R2_FINAL_PRODUCT_OBJECTIVE =
  Complete a governed fixture-backed Evidence and Audit Explorer so operators can
  inspect curated evidence metadata, provenance, and governance state across
  releases/gates without implying scientific approval, real-data readiness,
  or operational activation.

UX_R2_PRIMARY_USER =
  Wick operator / governance reviewer (read-only research operations)

UX_R2_PRIMARY_USER_JOURNEY =
  Open Evidências → search/filter curated catalog → inspect detail (supports,
  limitations, known/unknown, flags) → optionally arrive from MVP screens via
  safe cross-links → understand R3D≠R3E and pending≠failed → leave without
  executing ops or validation.

UX_R2_RELEASE_BOUNDARY =
  Fixture-backed read-only Evidence Explorer completion (I1 shipped + I2–I5);
  no backend; no real data; no runtime repo/FS; no host/scheduler activation;
  no gate-decision workflow; no R4/R5.

UX_R2_REMAINING_INCREMENTS = I2, I3, I4, I5
UX_R2_INCREMENT_ORDER = I2 → I3 → I4 → I5
```

### Dependency graph

```text
I1 (MERGED) ──► I2 (catalog history)
                   └──► I3 (provenance UX)
                          └──► I4 (cross-nav)
                                 └──► I5 (fixture acceptance + closure)
```

I4 depends on I2 evidenceIds being stable. I3 may proceed after I2. I5 depends on I2–I4 PASS checkpoints.

## Acceptance criteria (release)

```text
1. Curated catalog covers representative release/gate/ops-debt evidence records.
2. Provenance and governance-state presentation is explicit and tested.
3. Safe read-only cross-navigation exists from MVP screens to evidence entries.
4. Semantic inequalities enforced in UI/tests (evidence≠approval; R3D≠R3E; pending≠failed; sourcePath≠file access).
5. Zero new runtime/dev dependencies.
6. No new routes/screens; Evidence Explorer remains /governance/evidence.
7. UX-R1 screens preserved.
8. Scientific/operational truth unchanged.
9. Final independent review APPROVED.
10. Final human validation passed before merge.
```

## Closure criteria

```text
UX_R2 fixture-backed Evidence and Audit Explorer scope is complete and governed.
```

Wording must **not** claim production readiness, trading authorization, real-data integration, scheduler activation, or R4/R5 unlock.

## Explicit out of scope / deferred backlog

```text
UX_R2_EXPLICIT_OUT_OF_SCOPE =
  real-data adapters; runtime repository/FS browse; Markdown/HTML render;
  downloads; external links; Approvals/Backlog Kanban (UX-B8 app);
  scientific gate decision workflow; validate/effect peeking;
  host discovery; scheduler activation; R4 unlock; R5 start;
  experiment registry comparison screens; FU result payloads.

UX_R2_DEFERRED_BACKLOG =
  C experiment registry; F collection monitoring; G readiness progression UI
  beyond existing Readiness screen; H real-data read; I host/scheduler workflow;
  build-time catalog ingest; backend evidence index; hybrid live+fixture.
```

## Continuous execution model

```text
DEVELOPMENT_MODE = CONTINUOUS_SINGLE_BRANCH
PR_MODEL = ONE_DRAFT_PR_FOR_ALL_REMAINING_INCREMENT_WORK
MERGE_MODEL = FINAL_MERGE_ONLY
HUMAN_REVIEW_MODEL = SINGLE_FINAL_VALIDATION
INTERNAL_CHECKPOINTS = MANDATORY
NO_INTERMEDIATE_MERGES = true
```

### Checkpoint plan

| Checkpoint | When | Must PASS before |
|------------|------|------------------|
| CHECKPOINT_ARCHITECTURE | Start of single execution | I2 |
| CHECKPOINT_INCREMENT_I2 | After I2 | I3 |
| CHECKPOINT_INCREMENT_I3 | After I3 | I4 |
| CHECKPOINT_INCREMENT_I4 | After I4 | I5 |
| CHECKPOINT_INCREMENT_I5 | After I5 | INTEGRATION |
| CHECKPOINT_INTEGRATION | After I5 | REGRESSION |
| CHECKPOINT_REGRESSION | After integration | SECURITY |
| CHECKPOINT_SECURITY | After regression | ACCESSIBILITY |
| CHECKPOINT_ACCESSIBILITY | After security | GOVERNANCE |
| CHECKPOINT_GOVERNANCE | After a11y | FINAL_INDEPENDENT_REVIEW |
| CHECKPOINT_FINAL_INDEPENDENT_REVIEW | End | Human validation |

Each checkpoint: versioned handoff doc, commit SHA, independently rerunnable, may set `EXECUTION_BLOCKED` (human-input handoff; not merge; not human approval of product).

### Stop conditions → human-input handoff

```text
scope ambiguity
architecture change beyond approved plan
new runtime or dev dependency
backend introduction not explicitly approved
real-data requirement
runtime repository/filesystem access
future-unseen result access
validation execution
effect peeking
host or scheduler activation
secret or credential requirement
scientific interpretation change
R4 or R5 state change
security boundary failure
checkpoint failure not locally resolvable
PR exceeds approved size/risk threshold
```

### Maximum PR boundary / split trigger

```text
MAX_PLANNED_INCREMENTS = 4
MAX_CHANGED_PRODUCT_FILES = 40
MAX_NET_CHANGED_LINES = 2500
MAX_NEW_ROUTES = 0
MAX_NEW_SCREENS = 0
MAX_NEW_VIEWMODELS = 0
MAX_NEW_FIXTURES = 0
MAX_DEPENDENCIES = 0

SPLIT_TRIGGER =
  exceed any maximum without justified checkpoint waiver;
  EXECUTION_BLOCKED stop condition;
  need for backend/real-data/repo-read;
  human rejects continuous-execution model.
```

## Increment contracts (summary)

See `docs/releases/UX-R2-REMAINING-RELEASE-FROZEN-SCOPE.md` for full per-increment fields.

## Authorization flags (remain false until separate execution prompt)

```text
UX_R2_REMAINING_IMPLEMENTATION_AUTHORIZED = false
UX_R2_SINGLE_BRANCH_EXECUTION_AUTHORIZED = false
UX_R2_SINGLE_PR_EXECUTION_AUTHORIZED = false
UX_R2_SINGLE_FINAL_VALIDATION_AUTHORIZED = false
PRODUCT_CODE_AUTHORIZED = false
```

## Next

```text
NEXT_RECOMMENDED_TASK = UX_R2_REMAINING_RELEASE_SINGLE_EXECUTION
NEXT_ITEM = UX_R2_SEPARATE_HUMAN_APPROVED_SINGLE_EXECUTION_PROMPT
```
