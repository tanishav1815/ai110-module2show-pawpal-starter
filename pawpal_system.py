"""
PawPal+ — backend class skeletons (UML → Python).
Logic is not yet implemented; methods contain `pass` stubs.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Task:
    """Represents a single pet care task."""

    title: str
    duration_minutes: int
    priority: str          # "low" | "medium" | "high"
    category: str = ""     # e.g. "feeding", "exercise", "grooming", "medication"

    def is_doable(self, budget: int) -> bool:
        """Return True if this task fits within the remaining time budget (minutes)."""
        pass

    def describe(self) -> str:
        """Return a human-readable description of the task."""
        pass


@dataclass
class Pet:
    """Represents a pet owned by an Owner."""

    name: str
    species: str           # e.g. "dog", "cat", "other"
    age: int               # in years
    special_needs: list[str] = field(default_factory=list)
    _tasks: list[Task] = field(default_factory=list, repr=False)

    def add_task(self, task: Task) -> None:
        """Add a care task to this pet's task list."""
        pass

    def get_tasks(self) -> list[Task]:
        """Return the full list of tasks for this pet."""
        pass


@dataclass
class Owner:
    """Represents the pet owner."""

    name: str
    available_minutes: int          # total free time in a day
    preferences: list[str] = field(default_factory=list)   # e.g. ["morning", "short tasks first"]
    _pets: list[Pet] = field(default_factory=list, repr=False)

    def add_pet(self, pet: Pet) -> None:
        """Register a pet under this owner."""
        pass

    def get_pets(self) -> list[Pet]:
        """Return all pets belonging to this owner."""
        pass


@dataclass
class Scheduler:
    """Builds and explains a daily care plan for a pet."""

    owner: Owner
    pet: Pet
    time_budget: Optional[int] = None   # defaults to owner.available_minutes if None

    def build_plan(self) -> list[Task]:
        """
        Select and order tasks that fit within the time budget.
        Priority ordering: high > medium > low.
        Returns the scheduled list of Task objects.
        """
        pass

    def explain_plan(self) -> str:
        """
        Return a plain-English explanation of the generated plan,
        including why each task was chosen and its time slot.
        """
        pass
