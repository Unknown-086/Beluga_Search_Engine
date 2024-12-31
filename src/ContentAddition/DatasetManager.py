import pandas as pd
import os
from src.CrawlingWebLinks.CrawlUrl import scrape_website

class DatasetManager:
    def __init__(self):
        self.dataset_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                                    'data', 
                                    'UserContent', 
                                    'UserContent.csv')
        self.starting_doc_id = 2455685
        self.columns = ['DocID', 'title', 'description', 'content', 'url', 'source']
    
    def initialize_dataset(self):
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(self.dataset_path), exist_ok=True)
        
        if not os.path.exists(self.dataset_path):
            df = pd.DataFrame(columns=self.columns)
            df.to_csv(self.dataset_path, index=False)
            print(f"Created new dataset at {self.dataset_path}")
            return True
        return False

    def get_next_doc_id(self):
        try:
            df = pd.read_csv(self.dataset_path)
            if df.empty:
                return str(self.starting_doc_id)  # Return as string
            # Convert to string after calculation
            return str(int(df['DocID'].max()) + 1)
        except (pd.errors.EmptyDataError, FileNotFoundError):
            return str(self.starting_doc_id)  # Return as string

    def is_url_duplicate(self, url):
        """Check if URL already exists in dataset"""
        try:
            if not os.path.exists(self.dataset_path):
                return False
                
            df = pd.read_csv(self.dataset_path)
            return url in df['url'].values
        except (pd.errors.EmptyDataError, FileNotFoundError):
            return False

    def add_new_content(self, content_data):
        try:
            # Check for duplicate URL
            if self.is_url_duplicate(content_data['url']):
                return {'error': 'This URL already exists in the dataset'}

            # Create directory and file if doesn't exist
            os.makedirs(os.path.dirname(self.dataset_path), exist_ok=True)
            
            if not os.path.exists(self.dataset_path):
                df = pd.DataFrame(columns=self.columns)
                df.to_csv(self.dataset_path, index=False)

            # Add new content
            new_row = pd.DataFrame([content_data])
            new_row.to_csv(self.dataset_path, 
                          mode='a', 
                          header=not os.path.exists(self.dataset_path),
                          index=False)
            return {'status': 'success'}
        except Exception as e:
            return {'error': str(e)}