from feedgen.feed import FeedGenerator

from feeds.daily_leetcode import LeetCodeDailyFeed

feeds = [
    {
        "feed": LeetCodeDailyFeed(),
        "feed_info": {
            "title": "LeetCode Daily Challenge",
            "link": "https://leetcode_dailyleetcode.com/problemset/all/?daily=true",
            "self_link": "https://william9923.github.io/daily-rss/leetcode.xml",
            "description": "Daily coding challenge from LeetCode",
        },
        "target_file": "output/leetcode.xml",
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

    fg.rss_file(output_path)


if __name__ == "__main__":
    for feed_item in feeds:
        generate_rss(
            feed_item["feed"], feed_item["target_file"], feed_item["feed_info"]
        )
