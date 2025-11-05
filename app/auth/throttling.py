import os
from dotenv import load_dotenv
import time
from fastapi import HTTPException, status
from collections import defaultdict


# --- In-memory storage for user requests ---
user_requests = defaultdict(list)

load_dotenv()
GLOBAL_RATE_LIMIT = int(os.getenv("GLOBAL_RATE_LIMIT", 5))
GLOBAL_TIME_WINDOW_SECONDS = int(os.getenv("GLOBAL_TIME_WINDOW_SECONDS", 60))
AUTH_RATE_LIMIT = int(os.getenv("AUTH_RATE_LIMIT", 3))
AUTH_TIME_WINDOW_SECONDS = int(os.getenv("AUTH_TIME_WINDOW_SECONDS", 60))


def apply_rate_limit(user_id: str):
    current_time = time.time()

    print(
        f"Global rate limit: {GLOBAL_RATE_LIMIT} per {GLOBAL_TIME_WINDOW_SECONDS} seconds"
    )
    print(
        f"Authenticated rate limit: {AUTH_RATE_LIMIT} per {AUTH_TIME_WINDOW_SECONDS} seconds"
    )

    if user_id == "global_unauthenticated_user":
        rate_limit = GLOBAL_RATE_LIMIT
        time_window = GLOBAL_TIME_WINDOW_SECONDS
    else:
        rate_limit = AUTH_RATE_LIMIT
        time_window = AUTH_TIME_WINDOW_SECONDS

    # Filter out requests older than the time window
    user_requests[user_id] = [
        t for t in user_requests.get(user_id, []) if current_time - t < time_window
    ]

    if len(user_requests[user_id]) >= rate_limit:
        raise HTTPException(
            status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many requests. Please try again later.",
        )
    else:
        # For debugging: print current usage
        current_usage = len(user_requests[user_id])
        print(f"User {user_id}: {current_usage + 1}/{rate_limit} requests used.")

    user_requests[user_id].append(current_time)
    return True
