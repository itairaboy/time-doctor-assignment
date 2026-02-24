import os
import numpy as np
from faker import Faker

from .config import (
    SEED, DATE_START, DATE_END, OUTPUT_DIR,
    N_ACCOUNTS, USERS_PER_ACCOUNT, PROJECTS_PER_ACCOUNT,
    TASKS_PER_PROJECT, EVENTS_PER_TASK,
    USER_DEACTIVATION_RATE,
)
from .generators import (
    generate_accounts,
    generate_users,
    generate_projects,
    generate_tasks,
    generate_events,
)

def main():
    rng  = np.random.default_rng(SEED)
    fake = Faker()
    Faker.seed(SEED)

    accounts = generate_accounts(
        n=N_ACCOUNTS, date_start=DATE_START, date_end=DATE_END, rng=rng, fake=fake,
    )
    users = generate_users(
        accounts=accounts, users_per_account=USERS_PER_ACCOUNT, date_end=DATE_END,
        deactivation_rate=USER_DEACTIVATION_RATE, rng=rng, fake=fake,
    )
    projects = generate_projects(
        accounts=accounts, users=users, projects_per_account=PROJECTS_PER_ACCOUNT,
        date_end=DATE_END, rng=rng,
    )
    tasks = generate_tasks(
        projects=projects, users=users, tasks_per_project=TASKS_PER_PROJECT,
        date_end=DATE_END, rng=rng,
    )
    events = generate_events(
        users=users, tasks=tasks, events_per_task=EVENTS_PER_TASK,
        date_end=DATE_END, rng=rng,
    )

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    accounts.to_csv(f"{OUTPUT_DIR}/accounts.csv", index=False)
    users.to_csv(f"{OUTPUT_DIR}/users.csv",       index=False)
    projects.to_csv(f"{OUTPUT_DIR}/projects.csv", index=False)
    tasks.to_csv(f"{OUTPUT_DIR}/tasks.csv",       index=False)
    events.to_csv(f"{OUTPUT_DIR}/events.csv",     index=False)

    print(f"accounts : {accounts.shape}")
    print(f"users    : {users.shape}")
    print(f"projects : {projects.shape}")
    print(f"tasks    : {tasks.shape}")
    print(f"events   : {events.shape}")
    print(f"Output dir: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()