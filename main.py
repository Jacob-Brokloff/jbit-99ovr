from dotenv import load_dotenv
load_dotenv()

from agents import crawler_agent, search_agent
from functions import run


if __name__ == "__main__":
    market = "Architects in Cleveland Ohio"
    target = 20
    collected = []
    attempts = 0

    while len(collected) < target and attempts < 5:
        result = run(market)
        collected += result
        attempts += 1

    print(f"Found {len(collected)} contacts:")
    print(collected)
