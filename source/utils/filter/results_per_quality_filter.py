from utils.filter.base_filter import BaseFilter
from utils.logger import setup_logger

logger = setup_logger(__name__)


class ResultsPerQualityFilter(BaseFilter):
    def __init__(self, config):
        super().__init__(config)

    def filter(self, data):
        filtered_items = []
        items_count = {}
        for item in data:
            logger.info(f"Filtering by quality: {item.parsed_data.resolution}")
            logger.info(f"Filtering by indexer: {item.indexer}")
            if f"{item.parsed_data.resolution}{item.indexer}" not in items_count:
                items_count[f"{item.parsed_data.resolution}{item.indexer}"] = 1
                filtered_items.append(item)
            else:
                if items_count[f"{item.parsed_data.resolution}{item.indexer}"] < int(self.config['resultsPerQuality']):
                    items_count[f"{item.parsed_data.resolution}{item.indexer}"] += 1
                    filtered_items.append(item)
        return filtered_items

    def can_filter(self):
        return self.config['resultsPerQuality'] is not None and int(self.config['resultsPerQuality']) > 0
