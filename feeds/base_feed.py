from abc import ABC, abstractmethod
from typing import Any, Dict, List


class BaseFeed(ABC):
    @abstractmethod
    def fetch_entries(self) -> List[Dict[str, Any]]:
        """
        Fetch entries for the RSS feed.
        Returns:
            List of dictionaries with keys: title, link, guid, pubDate, description (optional)
        """
        pass
