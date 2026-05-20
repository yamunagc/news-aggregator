import pandas as pd

class DataProcessor:

    def __init__(self):
        self.dataframe = pd.DataFrame()

    def merge(self, articles):
        rows = [a.to_dict() for a in articles]
        self.dataframe = pd.DataFrame(rows)

    def remove_duplicates(self):
        self.dataframe = self.dataframe.drop_duplicates(subset="url")
        self.dataframe = self.dataframe.reset_index(drop=True)

    def clean(self):
        self.dataframe["title"] = self.dataframe["title"].fillna("No title")
        self.dataframe["source"] = self.dataframe["source"].fillna("Unknown")
        self.dataframe["author"] = self.dataframe["author"].fillna("Unknown") if "author" in self.dataframe.columns else self.dataframe.get("author", "Unknown")
        self.dataframe["published_at"] = pd.to_datetime(
            self.dataframe["published_at"], errors="coerce"
        )

    def get_data(self):
        return self.dataframe