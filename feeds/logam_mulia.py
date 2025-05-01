from datetime import datetime, timezone
from typing import Any, Dict, List

from bs4 import BeautifulSoup
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

from .base_feed import BaseFeed

TIMEOUT = 60_000  # in millis (60s)


class LogamMuliaFeed(BaseFeed):
    def __init__(self):
        self.url = "https://www.logammulia.com/id/harga-emas-hari-ini"
        self.current_day = datetime.now().strftime("%A, %d %B %Y")

    def __table_template(self, items):
        html = f"""
        <style>
            table {{
                border-collapse: collapse;
                width: 100%;
                font-family: Arial, sans-serif;
                font-size: 14px;
            }}
            th, td {{
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
            }}
            thead {{
                background-color: #f2f2f2;
                font-weight: bold;
            }}
            tbody tr:nth-child(even) {{
                background-color: #f9f9f9;
            }}
            tbody tr:hover {{
                background-color: #f1f1f1;
            }}
            h2 {{
                font-family: Arial, sans-serif;
                color: #333;
            }}
        </style>
        <table>
            <thead>
                <tr>
                    <th>Category</th>
                    <th>Weight</th>
                    <th>Base Price</th>
                    <th>Price + Tax</th>
                </tr>
            </thead>
            <tbody>
                {"".join(items)}
            </tbody>
        </table>
        """
        return html.strip()

    def fetch_entries(self) -> List[Dict[str, Any]]:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)

            # give context to mask automation to be able to hit the actual website
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
            page = context.new_page()
            page.goto(self.url, timeout=TIMEOUT)

            try:
                page.wait_for_selector("table.table.table-bordered", timeout=10000)
            except PlaywrightTimeoutError:
                raise RuntimeError("Table did not load in time")

            html = page.content()
            browser.close()

        soup = BeautifulSoup(html, "html.parser")
        table = soup.select_one("table.table.table-bordered")
        if table is None:
            raise RuntimeError("Could not find the gold price table")

        rows = table.find_all("tr")
        section = ""
        items = []
        for row in rows:
            cols = row.find_all("td")
            if not cols:
                th = row.find("th")
                if th and "colspan" in th.attrs:
                    section = th.text.strip()
                continue

            weight = cols[0].text.strip()
            base_price = cols[1].text.strip()
            taxed_price = cols[2].text.strip()
            items.append(
                f"<tr><td>{section}</td><td>{weight}</td><td>{base_price}</td><td>{taxed_price}</td></tr>"
            )

        return [
            {
                "title": f"Gold Price in Indonesia - {self.current_day}",
                "link": self.url,
                "guid": f"{self.url}-{datetime.utcnow().isoformat()}",
                "pubDate": datetime.now(tz=timezone.utc),
                "content": self.__table_template(items),
            }
        ]
