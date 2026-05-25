from __future__ import annotations

import os
import re
from collections import Counter

import matplotlib.pyplot as plt
import pandas as pd


class Visualizer:
    def __init__(self, output_dir: str = "charts"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        plt.style.use("seaborn-v0_8-whitegrid")

    def plot_by_source(self, df: pd.DataFrame) -> str | None:
        if df.empty or "source" not in df.columns:
            return None

        counts = df["source"].fillna("Unknown").value_counts().head(8)
        if counts.empty:
            return None

        fig, ax = plt.subplots(figsize=(8, 4.8))
        counts.sort_values().plot(kind="barh", ax=ax, color="#0f766e")
        ax.set_title("Articles by Source", fontsize=13, fontweight="bold")
        ax.set_xlabel("Number of Articles")
        ax.set_ylabel("Source")
        plt.tight_layout()

        path = os.path.join(self.output_dir, "articles_by_source.png")
        fig.savefig(path, dpi=160, bbox_inches="tight")
        plt.close(fig)
        return path

    def plot_by_category(self, df: pd.DataFrame) -> str | None:
        if df.empty or "category" not in df.columns:
            return None

        counts = df["category"].fillna("general").value_counts()
        if counts.empty:
            return None

        fig, ax = plt.subplots(figsize=(6.2, 4.6))
        colors = ["#0f766e", "#14b8a6", "#2dd4bf", "#5eead4", "#99f6e4", "#115e59", "#134e4a"]
        ax.pie(
            counts.values,
            labels=counts.index,
            autopct="%1.0f%%",
            startangle=140,
            colors=colors[: len(counts)],
            textprops={"fontsize": 9},
        )
        ax.set_title("Articles by Category", fontsize=13, fontweight="bold")
        plt.tight_layout()

        path = os.path.join(self.output_dir, "articles_by_category.png")
        fig.savefig(path, dpi=160, bbox_inches="tight")
        plt.close(fig)
        return path

    def plot_top_authors(self, df: pd.DataFrame) -> str | None:
        if df.empty or "author" not in df.columns:
            return None

        filtered = df.copy()
        filtered["author"] = filtered["author"].fillna("Unknown").astype(str).str.strip()

        bad_patterns = [
            r"\bunknown\b",
            r"\bshare\b",
            r"\bsave\b",
            r"\bgoogle\b",
            r"\bgetty\b",
            r"\bbbc africa\b",
            r"\b\d+\s+day[s]?\s+ago\b",
            r"\b\d+\s+hour[s]?\s+ago\b",
        ]

        for pattern in bad_patterns:
            filtered = filtered[~filtered["author"].str.contains(pattern, case=False, regex=True)]

        filtered = filtered[filtered["author"].str.len() <= 80]
        filtered = filtered[filtered["author"].str.split().str.len() <= 10]

        counts = filtered["author"].value_counts().head(8)
        if counts.empty:
            return None

        fig, ax = plt.subplots(figsize=(8, 4.8))
        counts.sort_values().plot(kind="barh", ax=ax, color="#2563eb")
        ax.set_title("Top Authors", fontsize=13, fontweight="bold")
        ax.set_xlabel("Number of Articles")
        ax.set_ylabel("Author")
        plt.tight_layout()

        path = os.path.join(self.output_dir, "top_authors.png")
        fig.savefig(path, dpi=160, bbox_inches="tight")
        plt.close(fig)
        return path

    def plot_title_keywords(self, df: pd.DataFrame) -> str | None:
        if df.empty or "title" not in df.columns:
            return None

        stopwords = {
            "the", "a", "an", "and", "or", "of", "to", "in", "on", "for", "with",
            "at", "from", "by", "after", "near", "amid", "over", "into", "is",
            "are", "was", "were", "be", "has", "have", "had", "as", "that", "this",
        }

        words = []
        for title in df["title"].dropna():
            for word in str(title).lower().split():
                clean = "".join(ch for ch in word if ch.isalnum())
                if len(clean) > 2 and clean not in stopwords:
                    words.append(clean)

        counts = Counter(words).most_common(10)
        if not counts:
            return None

        labels = [item[0] for item in counts]
        values = [item[1] for item in counts]

        fig, ax = plt.subplots(figsize=(8, 4.8))
        ax.bar(labels, values, color="#7c3aed")
        ax.set_title("Frequent Title Keywords", fontsize=13, fontweight="bold")
        ax.set_xlabel("Keyword")
        ax.set_ylabel("Frequency")
        ax.tick_params(axis="x", rotation=30)
        plt.tight_layout()

        path = os.path.join(self.output_dir, "title_keywords.png")
        fig.savefig(path, dpi=160, bbox_inches="tight")
        plt.close(fig)
        return path
