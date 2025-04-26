# feeds/leetcode_daily.py
from datetime import datetime, timezone
from typing import Any, Dict, List

import requests
import html

from .base_feed import BaseFeed


class LeetCodeDailyFeed(BaseFeed):
    def __init__(self, session: str):
        self.session = session
        self.url = "https://leetcode.com/graphql"

    def fetch_entries(self) -> List[Dict[str, Any]]:
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
        headers = {
            "Content-Type": "application/json",
            "Cookie": self.session,
        }
        response = requests.post(self.url, json=query, headers=headers)
        response.raise_for_status()

        data = response.json()["data"]["activeDailyCodingChallengeQuestion"]
        slug = data["question"]["titleSlug"]

        content = self.get_question_content(slug)

        entry = {
            "title": data["question"]["title"],
            "link": f"https://leetcode.com{data['link']}",
            "guid": data["question"]["titleSlug"],
            "pubDate": datetime.strptime(data["date"], "%Y-%m-%d").replace(
                tzinfo=timezone.utc
            ),
            "description": content,
            "content": content,
            "slug": slug,
        }

        return [entry]

    def get_question_content(self, slug: str) -> str:
        query = {
            "operationName": "questionContent",
            "query": """
            query questionContent($titleSlug: String!) {
              question(titleSlug: $titleSlug) {
                content
              }
            }
            """,
            "variables": {"titleSlug": slug},
        }

        headers = {
            "Content-Type": "application/json",
            "Cookie": self.session,
            "Referer": f"https://leetcode.com/problems/{slug}/",
            "Origin": "https://leetcode.com",
            "User-Agent": "Mozilla/5.0",
        }

        response = requests.post(self.url, json=query, headers=headers)
        response.raise_for_status()

        return response.json()["data"]["question"]["content"]
