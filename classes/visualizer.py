import matplotlib.pyplot as plt
import os

class Visualizer:

    def __init__(self):
        os.makedirs("assets", exist_ok=True)

    def plot_by_source(self, dataframe):
        source_counts = dataframe["source"].value_counts()

        fig, ax = plt.subplots(figsize=(10, 5))
        source_counts.plot(kind="bar", ax=ax, color="steelblue", edgecolor="black")

        ax.set_title("Number of Articles per Source")
        ax.set_xlabel("Source")
        ax.set_ylabel("Number of Articles")
        ax.tick_params(axis="x", rotation=45)
        plt.tight_layout()

        path = "assets/chart_by_source.png"
        plt.savefig(path)
        plt.close()
        return path

    def plot_by_category(self, dataframe):
        category_counts = dataframe["category"].value_counts()

        fig, ax = plt.subplots(figsize=(7, 7))
        ax.pie(
            category_counts,
            labels=category_counts.index,
            autopct="%1.1f%%",
            startangle=140
        )

        ax.set_title("Articles by Category")
        plt.tight_layout()

        path = "assets/chart_by_category.png"
        plt.savefig(path)
        plt.close()
        return path