import matplotlib.pyplot as plt
import os

class Visualizer:

    def __init__(self):
        os.makedirs("assets", exist_ok=True)

    def plot_by_source(self, dataframe):
        plt.rcParams.update({"font.size": 13})
        source_counts = dataframe["source"].value_counts()

        fig, ax = plt.subplots(figsize=(12, 6))
        source_counts.plot(kind="bar", ax=ax, color="#02645e", edgecolor="white")

        ax.set_title("Number of Articles per Source", fontsize=15, pad=12)
        ax.set_xlabel("Source", fontsize=13)
        ax.set_ylabel("Number of Articles", fontsize=13)
        ax.tick_params(axis="x", rotation=45, labelsize=10)
        ax.tick_params(axis="y", labelsize=11)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        plt.tight_layout()

        path = "assets/chart_by_source.png"
        plt.savefig(path, dpi=150)
        plt.close()
        return path

    def plot_by_category(self, dataframe):
        plt.rcParams.update({"font.size": 13})
        category_counts = dataframe["category"].value_counts()

        colors = ["#02645e", "#ffde59", "#04a699", "#7ececa",
                  "#014d49", "#e6c800"]

        fig, ax = plt.subplots(figsize=(7, 7))
        ax.pie(
            category_counts,
            labels=category_counts.index,
            autopct="%1.1f%%",
            startangle=140,
            colors=colors[:len(category_counts)],
            textprops={"fontsize": 12}
        )

        ax.set_title("Articles by Category", fontsize=15, pad=12)
        plt.tight_layout()

        path = "assets/chart_by_category.png"
        plt.savefig(path, dpi=150)
        plt.close()
        return path