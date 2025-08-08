from utils.filter.base_filter import BaseFilter
from utils.logger import setup_logger

logger = setup_logger(__name__)


class ResultsPerQualityFilter(BaseFilter):
    def __init__(self, config):
        super().__init__(config)

    def filter(self, data):
        filtered_items = []
        resolution_count = {}
        indexer_count = {}
        for item in data:
            logger.info(f"Filtering by quality: {item.parsed_data.resolution}")
            logger.info(f"Filtering by indexer: {item.indexer}")
            if item.parsed_data.resolution not in resolution_count:
                resolution_count[item.parsed_data.resolution] = 1
                filtered_items.append(item)
            if item.indexer not in indexer_count:
                indexer_count[item.indexer] = 1
                filtered_items.append(item)
            if item.indexer in indexer_count and item.parsed_data.resolution in resolution_count:
                if resolution_count[item.parsed_data.resolution] < int(self.config['resultsPerQuality']) and indexer_count[item.indexer] < int(self.config['resultsPerIndexer']):
                    resolution_count[item.parsed_data.resolution] += 1
                    indexer_count[item.indexer] += 1
                    filtered_items.append(item)
        return filtered_items

    def can_filter(self):
        return self.config['resultsPerQuality'] is not None and int(self.config['resultsPerQuality']) > 0
