# feeds/leetcode_daily.py
from datetime import datetime, timezone
from typing import Any, Dict, List

import requests

from .base_feed import BaseFeed


class LeetCodeDailyFeed(BaseFeed):
    def fetch_entries(self) -> List[Dict[str, Any]]:
        url = "https://leetcode.com/graphql"
        query = {
            "query": """
            query questionOfToday {
              activeDailyCodingChallengeQuestion {
                date
                link
                question {
                  title
                  titleSlug
                }
              }
            }
            """
        }
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, json=query, headers=headers)
        response.raise_for_status()
        data = response.json()["data"]["activeDailyCodingChallengeQuestion"]
        entry = {
            "title": data["question"]["title"],
            "link": f"https://leetcode.com{data['link']}",
            "guid": data["question"]["titleSlug"],
            "pubDate": datetime.strptime(data["date"], "%Y-%m-%d").replace(
                tzinfo=timezone.utc
            ),
            "description": f"LeetCode Daily Challenge for {data['date']}",
        }

        return [entry]
