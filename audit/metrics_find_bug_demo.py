"""
Small console demo to show the bug caused by using str.find in HTTP routing logic:

    if http_msg.method == "get" and http_msg.url.find("/metrics"):
        ...
    elif http_msg.method == "post" and http_msg.url.find("/metrics"):
        ...

Run with: python3 metrics_find_bug_demo.py
"""


def buggy_route(method: str, url: str) -> str:
    """Original routing logic using str.find (buggy)."""

    if method == "get" and url.find("/metrics"):
        return "GET /metrics handler"
    elif method == "post" and url.find("/metrics"):
        return "POST /metrics handler"
    return "invalid"


def correct_route(method: str, url: str) -> str:
    """Fixed routing logic using startswith/in."""

    if method == "get" and url.startswith("/metrics"):
        return "GET /metrics handler"
    elif method == "post" and url.startswith("/metrics"):
        return "POST /metrics handler"
    return "invalid"


def main() -> None:
    test_cases = [
        ("get", "/metrics"),
        ("get", "/metrics?foo=bar"),
        ("get", "xyz/metrics"),   # substring not at the start
        ("get", "/other"),
    ]

    print("=== Buggy routing (using str.find) ===")
    for method, url in test_cases:
        print(f"{method.upper():4} {url:20} -> {buggy_route(method, url)}")

    print("\n=== Correct routing (using startswith) ===")
    for method, url in test_cases:
        print(f"{method.upper():4} {url:20} -> {correct_route(method, url)}")


if __name__ == "__main__":
    main()

