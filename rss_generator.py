import os
from dotenv import load_dotenv

from feedgen.feed import FeedGenerator

from feeds.daily_leetcode import LeetCodeDailyFeed


load_dotenv()

leetcode_session = f"LEETCODE_SESSION={os.getenv('LEETCODE_SESSION')}"
feeds = [
    {
        "feed": LeetCodeDailyFeed(session=leetcode_session),
        "feed_info": {
            "title": "LeetCode Daily Challenge",
            "link": "https://william9923.github.io/daily-rss/output/leetcode.rss",
            "self_link": "https://william9923.github.io/daily-rss/output/leetcode.rss",
            "description": "Daily coding challenge from LeetCode",
        },
        "target_file": "output/leetcode.rss",
    },
]


def generate_rss(feed_instance, output_path, feed_info):
    fg = FeedGenerator()
    fg.title(feed_info["title"])
    fg.link(href=feed_info["link"], rel="alternate")
    fg.link(href=feed_info["self_link"], rel="self")
    fg.description(feed_info["description"])
    fg.language("en")

    entries = feed_instance.fetch_entries()
    for entry in entries:
        fe = fg.add_entry()
        fe.title(entry["title"])
        fe.link(href=entry["link"])
        fe.guid(entry["guid"])
        fe.pubDate(entry["pubDate"])
        if "description" in entry:
            fe.description(entry["description"])
        if "content" in entry:
            fe.content(entry["content"], type="CDATA")

    fg.rss_file(output_path)


if __name__ == "__main__":
    for feed_item in feeds:
        generate_rss(
            feed_item["feed"], feed_item["target_file"], feed_item["feed_info"]
        )
