# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

The initial UML includes four classes:

- Task (dataclass): holds a single care action — title, duration, priority, and category. Responsible for knowing whether it fits in a time budget (`is_doable`) and describing itself.
- Pet (dataclass): holds pet identity (name, species, age, special needs) and owns a list of Tasks. Responsible for managing and exposing its task list.
- Owner (dataclass): holds owner identity, total available minutes per day, and preferences. Responsible for managing a list of Pets.
- Scheduler: takes an Owner and a Pet, then builds an ordered daily plan (`build_plan`) and explains it in plain English (`explain_plan`). It is the only class with scheduling logic.

Relationships: Owner → Pet (one-to-many), Pet → Task (one-to-many), Scheduler uses Owner + Pet to produce a plan.

**b. Design changes**

Two changes were made during implementation:

1. **Added `completed` field and `mark_complete()` to `Task`** — the skeleton had no way to track whether a task was done. This was needed for tests and for future UI display (showing checked-off tasks).

2. **Added `get_all_tasks()` to `Owner`** — the skeleton only had `get_pets()`. The Scheduler needed a way to pull every (pet, task) pair from the owner without reaching into each Pet's internals directly. Adding this method keeps the logic clean and avoids tight coupling between Scheduler and Pet.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler considers three constraints: available time (tasks are dropped if they exceed the remaining budget), task priority (high → medium → low), and completion state (completed tasks are excluded from the plan). Priority was ranked first because a missed high-priority task (e.g. medication) has real consequences, whereas a missed enrichment task does not.

**b. Tradeoffs**

Conflict detection only flags exact `start_time` overlaps — it does not account for tasks that have no `start_time` set. This means two untimed tasks could end up scheduled back-to-back without a conflict warning even if a real owner couldn't do both at once. The tradeoff is simplicity: requiring a start_time for every task would make the app harder to use for quick task entry, while the lightweight check still catches the most common scheduling mistake (accidentally double-booking a specific time slot).

---

## 3. AI Collaboration

**a. How you used AI**

AI was used across every phase: brainstorming class responsibilities and UML relationships in Phase 1, generating class skeletons and method stubs in Phase 2, wiring Streamlit session state in Phase 3, drafting algorithmic methods (sorting, conflict detection, recurrence) in Phase 4, and generating test cases in Phase 5.

The most effective prompts were specific and code-grounded — e.g. "Based on my skeletons in pawpal_system.py, how should the Scheduler retrieve all tasks from the Owner's pets?" rather than open-ended questions. Providing context (file references, existing method names) consistently produced more useful output than asking in the abstract.

**b. Judgment and verification**

When AI suggested using a single flat list of tasks on the `Owner` class (rather than delegating to `Pet`), that suggestion was rejected. A flat list on `Owner` would break encapsulation — it would mean `Owner` needs to know about `Task` internals directly, bypassing `Pet` entirely. The decision to keep `Pet` as the task owner and add `get_all_tasks()` as a convenience aggregator on `Owner` was verified by checking that the Scheduler still only needed to call `pet.get_tasks()` and that no circular dependency was introduced.

Every AI-generated method was run through `main.py` and the test suite before being kept — the output had to match expected behavior, not just look plausible.

---

## 4. Testing and Verification

**a. What you tested**

22 automated tests cover: `is_doable` true/false, `mark_complete` status change and recurrence (daily, weekly, one-time), task count after `add_task`, filtering by completion status (pending / done / all), scheduler budget enforcement, priority ordering, same-priority tiebreaker (shorter first), exclusion of completed tasks, empty-plan edge cases (no tasks, zero budget), `sort_by_duration` order, and conflict detection (overlap, exact same start time, no false positives).

These tests matter because the scheduler's value depends entirely on correctness — a plan that silently drops high-priority tasks or misses a conflict is worse than no plan at all.

**b. Confidence**

★★★★☆ — All 22 tests pass and cover the main happy paths and the most common edge cases. The next cases to test would be: tasks that span midnight (e.g. `start_time="23:50"` with a 30-minute duration), a pet with 20+ tasks under a 15-minute budget, and verifying that recurring task chains don't drift over many completions.

---

## 5. Reflection

**a. What went well**

The clean separation between `Task`, `Pet`, `Owner`, and `Scheduler` made every phase easier. Because `Scheduler` was the only class with planning logic, adding features like conflict detection and sorting didn't require touching `Task` or `Pet` at all. That encapsulation paid off more than expected.

**b. What you would improve**

The current scheduler is greedy — it picks tasks in priority order and stops when the budget runs out. A smarter version would use a knapsack-style approach to find the combination of tasks that maximizes total priority value within the time budget, rather than just taking the first tasks that fit. The greedy approach can leave time on the table when a single high-priority long task blocks several shorter medium-priority ones.

**c. Key takeaway**

AI is most useful as a fast first draft, not a final answer. Every suggestion — whether a method implementation, a test case, or a class design — needed to be evaluated against the actual system requirements. The skill that mattered most wasn't prompting; it was knowing enough about the design to recognize when an AI suggestion was technically correct but architecturally wrong.
