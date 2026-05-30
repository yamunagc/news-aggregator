import queue
import threading
import textwrap
import tkinter as tk
from tkinter import messagebox, ttk
import webbrowser

from PIL import Image, ImageTk

from classes.fetcher import NewsFetcher
from classes.processor import DataProcessor
from classes.scraper import Scraper
from classes.visualizer import Visualizer

MAIN_COLOR = "#0f766e"
DARK_MAIN = "#115e59"
LIGHT_BG = "#f5fbfa"
WHITE = "#ffffff"
BORDER_COLOR = "#cfe9e5"
TEXT_DARK = "#1f2937"
TEXT_MUTED = "#6b7280"
SELECTED_BG = "#e6f7f4"
HOVER_BG = "#f0fdfa"
LINK_BLUE = "#2563eb"


class NewsApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("News Information Aggregator")
        self.root.geometry("1380x880")
        self.root.minsize(1200, 780)
        self.root.configure(bg=LIGHT_BG)

        self.fetcher = NewsFetcher()
        self.scraper = Scraper()
        self.processor = DataProcessor()
        self.visualizer = Visualizer()

        self.articles = []
        self.filtered_articles = []
        self.article_frames = []
        self.current_url = ""
        self.is_fetching = False
        self.is_closing = False
        self.ui_queue = queue.Queue()
        self.chart_images = []
        self.chart_labels = []
        self.queue_job = None

        self._setup_styles()
        self._build_ui()
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        self.queue_job = self.root.after(100, self._process_ui_queue)

    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TCombobox", padding=6)
        style.configure("Primary.TButton", padding=8, font=("Segoe UI", 10, "bold"))
        style.configure("Secondary.TButton", padding=8, font=("Segoe UI", 10))

    def _build_ui(self):
        self._build_header()
        self._build_toolbar()
        self._build_body()
        self._build_footer()

    def _build_header(self):
        header = tk.Frame(self.root, bg=MAIN_COLOR, height=58)
        header.pack(fill="x")
        header.pack_propagate(False)

        left = tk.Frame(header, bg=MAIN_COLOR)
        left.pack(side="left", fill="both", expand=True)

        tk.Label(
            left,
            text="News Information Aggregator",
            bg=MAIN_COLOR,
            fg="white",
            font=("Segoe UI", 20, "bold")
        ).pack(anchor="w", padx=18, pady=12)

    def _build_toolbar(self):
        toolbar = tk.Frame(self.root, bg=LIGHT_BG, padx=16, pady=12)
        toolbar.pack(fill="x")

        filter_card = tk.Frame(toolbar, bg=WHITE, highlightbackground=BORDER_COLOR, highlightthickness=1)
        filter_card.pack(fill="x")

        row = tk.Frame(filter_card, bg=WHITE, padx=14, pady=12)
        row.pack(fill="x")

        tk.Label(row, text="Category", bg=WHITE, fg=TEXT_DARK, font=("Segoe UI", 10, "bold")).pack(side="left")
        self.category_var = tk.StringVar(value="general")
        self.category_menu = ttk.Combobox(
            row,
            textvariable=self.category_var,
            values=["all"] + self.fetcher.VALID_CATEGORIES,
            width=18,
            state="readonly"
        )
        self.category_menu.pack(side="left", padx=(8, 14))

        tk.Label(row, text="Fetch Count", bg=WHITE, fg=TEXT_DARK, font=("Segoe UI", 10, "bold")).pack(side="left")
        self.count_var = tk.StringVar(value="10")
        self.count_menu = ttk.Combobox(
            row,
            textvariable=self.count_var,
            values=["5", "10", "15", "20", "30"],
            width=8,
            state="readonly"
        )
        self.count_menu.pack(side="left", padx=(8, 14))

        ttk.Button(row, text="Fetch News", command=self._on_fetch, style="Primary.TButton").pack(side="left", padx=(0, 8))
        ttk.Button(row, text="Analytics", command=self._show_charts, style="Secondary.TButton").pack(side="left", padx=(0, 12))

        tk.Label(row, text="Search", bg=WHITE, fg=TEXT_DARK, font=("Segoe UI", 10, "bold")).pack(side="left")
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *_: self._filter_articles())
        self.search_entry = tk.Entry(row, textvariable=self.search_var, width=28, relief="solid", bd=1)
        self.search_entry.pack(side="left", padx=(8, 10), ipady=4)

        self.info_label = tk.Label(row, text="Ready", bg=WHITE, fg=TEXT_MUTED, font=("Segoe UI", 9))
        self.info_label.pack(side="right")

    def _build_body(self):
        body = tk.Frame(self.root, bg=LIGHT_BG, padx=16, pady=4)
        body.pack(fill="both", expand=True)
        body.grid_columnconfigure(0, weight=1)
        body.grid_columnconfigure(1, weight=2)
        body.grid_rowconfigure(0, weight=0)
        body.grid_rowconfigure(1, weight=1)

        stats = tk.Frame(body, bg=LIGHT_BG)
        stats.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 10))

        self.stat_total = self._create_stat_card(stats, "Processed", "0")
        self.stat_total.pack(side="left", padx=(0, 10))
        self.stat_sources = self._create_stat_card(stats, "Sources", "0")
        self.stat_sources.pack(side="left", padx=(0, 10))
        self.stat_categories = self._create_stat_card(stats, "Categories", "0")
        self.stat_categories.pack(side="left")

        left_panel = tk.Frame(body, bg=WHITE, highlightbackground=BORDER_COLOR, highlightthickness=1)
        left_panel.grid(row=1, column=0, sticky="nsew", padx=(0, 8))

        left_header = tk.Frame(left_panel, bg=WHITE)
        left_header.pack(fill="x", padx=12, pady=(12, 8))

        tk.Label(left_header, text="Article List", bg=WHITE, fg=TEXT_DARK, font=("Segoe UI", 13, "bold")).pack(anchor="w")
        tk.Label(left_header, text="Click any article card to read the full details", bg=WHITE, fg=TEXT_MUTED, font=("Segoe UI", 9)).pack(anchor="w")
        self.results_label = tk.Label(left_header, text="0 visible results", bg=WHITE, fg=DARK_MAIN, font=("Segoe UI", 9, "bold"))
        self.results_label.pack(anchor="w", pady=(6, 0))

        self.list_canvas = tk.Canvas(left_panel, bg=WHITE, highlightthickness=0)
        scrollbar = ttk.Scrollbar(left_panel, orient="vertical", command=self.list_canvas.yview)
        self.list_frame = tk.Frame(self.list_canvas, bg=WHITE)
        self.list_frame.bind("<Configure>", lambda e: self.list_canvas.configure(scrollregion=self.list_canvas.bbox("all")))
        self.list_canvas.create_window((0, 0), window=self.list_frame, anchor="nw", width=430)
        self.list_canvas.configure(yscrollcommand=scrollbar.set)
        self.list_canvas.pack(side="left", fill="both", expand=True, padx=(8, 0), pady=(0, 8))
        scrollbar.pack(side="right", fill="y", padx=(0, 8), pady=(0, 8))

        right_panel = tk.Frame(body, bg=WHITE, highlightbackground=BORDER_COLOR, highlightthickness=1)
        right_panel.grid(row=1, column=1, sticky="nsew")

        detail_top = tk.Frame(right_panel, bg=WHITE)
        detail_top.pack(fill="x", padx=18, pady=(16, 8))

        self.title_label = tk.Label(
            detail_top,
            text="Select an article",
            bg=WHITE,
            fg=TEXT_DARK,
            font=("Segoe UI", 18, "bold"),
            wraplength=780,
            justify="left",
            anchor="w"
        )
        self.title_label.pack(fill="x")

        self.meta_label = tk.Label(
            detail_top,
            text="",
            bg=WHITE,
            fg=TEXT_MUTED,
            font=("Segoe UI", 10),
            justify="left",
            anchor="w"
        )
        self.meta_label.pack(fill="x", pady=(6, 0))

        self.author_badge = tk.Label(
            detail_top,
            text="Author: -",
            bg="#ecfeff",
            fg=DARK_MAIN,
            font=("Segoe UI", 10, "bold"),
            padx=10,
            pady=6
        )
        self.author_badge.pack(anchor="w", pady=(10, 0))

        link_wrap = tk.Frame(detail_top, bg=WHITE)
        link_wrap.pack(fill="x", pady=(10, 0))
        tk.Label(link_wrap, text="Source:", bg=WHITE, fg=TEXT_DARK, font=("Segoe UI", 10, "bold")).pack(side="left")
        self.link_label = tk.Label(
            link_wrap,
            text="No link available",
            bg=WHITE,
            fg=LINK_BLUE,
            cursor="hand2",
            font=("Segoe UI", 10, "underline"),
            wraplength=620,
            justify="left"
        )
        self.link_label.pack(side="left", padx=(8, 0))
        self.link_label.bind("<Button-1>", self._open_url)

        section = tk.Frame(right_panel, bg=WHITE)
        section.pack(fill="both", expand=True, padx=18, pady=(10, 14))
        tk.Label(section, text="Article Content", bg=WHITE, fg=TEXT_DARK, font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(0, 6))

        text_wrap_frame = tk.Frame(section, bg=WHITE, highlightbackground=BORDER_COLOR, highlightthickness=1)
        text_wrap_frame.pack(fill="both", expand=True)

        text_scroll = ttk.Scrollbar(text_wrap_frame)
        text_scroll.pack(side="right", fill="y")

        self.content_text = tk.Text(
            text_wrap_frame,
            wrap="word",
            font=("Segoe UI", 10),
            bg="#fbfffe",
            fg=TEXT_DARK,
            relief="flat",
            padx=14,
            pady=14,
            yscrollcommand=text_scroll.set,
            spacing1=4,
            spacing2=2,
            spacing3=10
        )
        self.content_text.pack(fill="both", expand=True)
        text_scroll.config(command=self.content_text.yview)
        self.content_text.tag_configure("body", lmargin1=0, lmargin2=0, spacing3=10)
        self.content_text.insert("1.0", "Fetch news and click an article from the left panel to read it here.")
        self.content_text.config(state="disabled")

    def _build_footer(self):
        footer = tk.Frame(self.root, bg=LIGHT_BG, height=30, highlightbackground=BORDER_COLOR, highlightthickness=1)
        footer.pack(fill="x", side="bottom")
        footer.pack_propagate(False)
        self.status_label = tk.Label(footer, text="  Ready", bg=LIGHT_BG, fg=DARK_MAIN, font=("Segoe UI", 9))
        self.status_label.pack(side="left", pady=5)

    def _create_stat_card(self, parent, title, value):
        card = tk.Frame(parent, bg=WHITE, highlightbackground=BORDER_COLOR, highlightthickness=1)
        inner = tk.Frame(card, bg=WHITE, padx=18, pady=12)
        inner.pack()
        tk.Label(inner, text=title, bg=WHITE, fg=TEXT_MUTED, font=("Segoe UI", 9)).pack(anchor="w")
        value_label = tk.Label(inner, text=value, bg=WHITE, fg=MAIN_COLOR, font=("Segoe UI", 18, "bold"))
        value_label.pack(anchor="w")
        card.value_label = value_label
        return card

    def _set_status(self, text):
        if not self.is_closing:
            self.status_label.config(text=f"  {text}")

    def _on_fetch(self):
        if self.is_fetching:
            messagebox.showinfo("Please wait", "A fetch operation is already running.")
            return
        self.is_fetching = True
        self._set_status("Fetching news...")
        self.info_label.config(text="Working...")
        worker = threading.Thread(target=self._fetch_worker, daemon=False)
        worker.start()

    def _fetch_worker(self):
        try:
            category = self.category_var.get()
            count = int(self.count_var.get())

            if category == "all":
                api_articles = self.fetcher.fetch_all_categories(total_limit=count)
            else:
                api_articles = self.fetcher.fetch_headlines(category=category, page_size=count)

            if self.is_closing:
                return

            scraped_articles = self.scraper.scrape_all(api_articles, limit=len(api_articles))
            if self.is_closing:
                return

            self.processor.merge(scraped_articles)
            self.processor.remove_duplicates()
            self.processor.clean()

            self.ui_queue.put(("fetch_done", scraped_articles))
        except Exception as exc:
            self.ui_queue.put(("fetch_error", str(exc)))

    def _process_ui_queue(self):
        if self.is_closing:
            return

        try:
            while True:
                item = self.ui_queue.get_nowait()
                kind = item[0]

                if kind == "fetch_done":
                    scraped_articles = item[1]
                    self.articles = scraped_articles
                    self.filtered_articles = list(scraped_articles)
                    self.is_fetching = False
                    self._populate_list()
                    self._update_stats()

                elif kind == "fetch_error":
                    self.is_fetching = False
                    messagebox.showerror("Error", item[1])
                    self._set_status("Error occurred")
                    self.info_label.config(text="Error")
        except queue.Empty:
            pass

        if not self.is_closing:
            self.queue_job = self.root.after(100, self._process_ui_queue)

    def _update_stats(self):
        df = self.processor.get_data()
        fetched_count = len(self.articles)
        visible_count = len(self.filtered_articles)
        processed_count = len(df)
        sources = df["source"].nunique() if not df.empty and "source" in df.columns else 0
        categories = df["category"].nunique() if not df.empty and "category" in df.columns else 0

        self.stat_total.value_label.config(text=str(processed_count))
        self.stat_sources.value_label.config(text=str(sources))
        self.stat_categories.value_label.config(text=str(categories))
        self.results_label.config(text=f"{visible_count} visible results")
        self.info_label.config(text=f"Fetched {fetched_count} | Processed {processed_count}")
        self._set_status(f"Done — fetched {fetched_count}, processed {processed_count}, visible {visible_count}")

    def _populate_list(self):
        for widget in self.list_frame.winfo_children():
            widget.destroy()
        self.article_frames = []

        if not self.filtered_articles:
            self.results_label.config(text="0 visible results")
            empty = tk.Label(
                self.list_frame,
                text="No articles to display. Try fetching news or changing the search term.",
                bg=WHITE,
                fg=TEXT_MUTED,
                font=("Segoe UI", 10),
                wraplength=340,
                justify="left"
            )
            empty.pack(anchor="w", padx=12, pady=14)
            return

        for i, article in enumerate(self.filtered_articles):
            card = tk.Frame(self.list_frame, bg=WHITE, padx=10, pady=10, cursor="hand2", highlightbackground=BORDER_COLOR, highlightthickness=1)
            card.pack(fill="x", padx=10, pady=(0, 8))

            title_text = article.title if article.title else "Untitled article"
            title = tk.Label(card, text=title_text[:95] + ("..." if len(title_text) > 95 else ""), bg=WHITE, fg=TEXT_DARK, font=("Segoe UI", 10, "bold"), wraplength=360, justify="left", anchor="w")
            title.pack(fill="x", anchor="w")

            meta = tk.Label(card, text=f"{article.source or 'Unknown source'}  •  {article.category or 'general'}", bg=WHITE, fg=TEXT_MUTED, font=("Segoe UI", 8), anchor="w")
            meta.pack(fill="x", pady=(4, 0))

            preview_source = article.description or article.content or "Click to open full article details"
            preview_clean = " ".join(str(preview_source).split())
            preview = tk.Label(card, text=textwrap.shorten(preview_clean, width=110, placeholder="..."), bg=WHITE, fg=TEXT_MUTED, font=("Segoe UI", 8), wraplength=360, justify="left", anchor="w")
            preview.pack(fill="x", pady=(6, 0))

            open_hint = tk.Label(card, text="Click to view full article", bg=WHITE, fg=MAIN_COLOR, font=("Segoe UI", 8, "bold"), anchor="w")
            open_hint.pack(fill="x", pady=(6, 0))

            for widget in (card, title, meta, preview, open_hint):
                widget.bind("<Button-1>", lambda e, idx=i: self._select_article(idx))
                widget.bind("<Enter>", lambda e, w=card: self._set_card_hover(w, True))
                widget.bind("<Leave>", lambda e, w=card: self._set_card_hover(w, False))

            self.article_frames.append((card, title, meta, preview, open_hint))

        self.results_label.config(text=f"{len(self.filtered_articles)} visible results")
        self._select_article(0)

    def _set_card_hover(self, card, hovering):
        if str(card.cget("bg")) != SELECTED_BG:
            new_bg = HOVER_BG if hovering else WHITE
            card.configure(bg=new_bg)
            for child in card.winfo_children():
                child.configure(bg=new_bg)

    def _filter_articles(self):
        term = self.search_var.get().strip().lower()
        if not term:
            self.filtered_articles = list(self.articles)
        else:
            self.filtered_articles = [
                a for a in self.articles
                if term in (a.title or "").lower()
                or term in (a.source or "").lower()
                or term in (a.category or "").lower()
                or term in (a.author or "").lower()
            ]
        self._populate_list()
        self._update_stats()

    def _format_article_content(self, article):
        raw = article.content or article.description or "No content available."
        cleaned = str(raw).replace("\r\n", "\n").replace("\r", "\n")
        cleaned = cleaned.replace("\xa0", " ")
        cleaned = "\n".join(line.strip() for line in cleaned.split("\n"))
        cleaned = "\n".join(line for line in cleaned.split("\n") if line)

        noise_lines = {
            "Share",
            "Save",
            "Add as preferred on Google",
            "Comment",
            "Advertisement",
            "Read more",
            "Most read",
            "Related topics",
        }

        filtered_lines = []
        for line in cleaned.split("\n"):
            stripped = line.strip()
            lowered = stripped.lower()
            if not stripped:
                continue
            if stripped in noise_lines:
                continue
            if any(token in lowered for token in ["share save", "add as preferred on google", "getty images", "photo caption"]):
                continue
            filtered_lines.append(stripped)

        cleaned = "\n\n".join(filtered_lines).strip()

        if not cleaned:
            return "Full article content is unavailable for this source. Open the source link to read more."

        return cleaned

    def _select_article(self, index):
        if not self.filtered_articles:
            return
        article = self.filtered_articles[index]

        for card, title, meta, preview, open_hint in self.article_frames:
            card.configure(bg=WHITE)
            title.configure(bg=WHITE, fg=TEXT_DARK)
            meta.configure(bg=WHITE, fg=TEXT_MUTED)
            preview.configure(bg=WHITE, fg=TEXT_MUTED)
            open_hint.configure(bg=WHITE, fg=MAIN_COLOR)

        card, title, meta, preview, open_hint = self.article_frames[index]
        for widget in (card, title, meta, preview, open_hint):
            widget.configure(bg=SELECTED_BG)
        title.configure(fg=MAIN_COLOR)
        meta.configure(fg=DARK_MAIN)

        self.title_label.config(text=article.title or "Untitled article")
        published = str(article.published_at)[:19] if article.published_at else "Unknown date"
        self.meta_label.config(text=f"{article.source or 'Unknown source'}  •  {article.category or 'general'}  •  {published}")
        self.author_badge.config(text=f"Author: {article.author or 'Unknown'}")

        formatted_content = self._format_article_content(article)
        self.content_text.config(state="normal")
        self.content_text.delete("1.0", tk.END)
        self.content_text.insert("1.0", formatted_content, "body")
        self.content_text.config(state="disabled")

        self.current_url = article.url or ""
        if self.current_url:
            display_link = self.current_url if len(self.current_url) < 90 else self.current_url[:90] + "..."
            self.link_label.config(text=display_link, fg=LINK_BLUE, cursor="hand2")
        else:
            self.link_label.config(text="No link available", fg=TEXT_MUTED, cursor="arrow")

    def _open_url(self, _event=None):
        if self.current_url:
            webbrowser.open(self.current_url)

    def _load_chart_image(self, parent, path, size):
        if not path:
            tk.Label(parent, text="No chart data available", bg=WHITE, fg=TEXT_MUTED).pack(padx=12, pady=30)
            return

        pil_img = Image.open(path)
        pil_img.thumbnail(size, Image.LANCZOS)
        photo = ImageTk.PhotoImage(pil_img)
        self.chart_images.append(photo)

        lbl = tk.Label(parent, image=photo, bg=WHITE)
        lbl.image = photo
        lbl.pack(padx=12, pady=12)
        self.chart_labels.append(lbl)

    def _show_charts(self):
        df = self.processor.get_data()
        if df.empty:
            messagebox.showinfo("No Data", "Fetch some articles first.")
            return

        path1 = self.visualizer.plot_by_source(df)
        path2 = self.visualizer.plot_by_category(df)
        path3 = self.visualizer.plot_top_authors(df)
        path4 = self.visualizer.plot_title_keywords(df)

        chart_win = tk.Toplevel(self.root)
        chart_win.title("Analytics Dashboard")
        chart_win.geometry("1100x760")
        chart_win.configure(bg=LIGHT_BG)

        header = tk.Frame(chart_win, bg=MAIN_COLOR, height=58)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="News Analytics Dashboard", bg=MAIN_COLOR, fg="white", font=("Segoe UI", 17, "bold")).pack(side="left", padx=16, pady=14)

        summary = tk.Frame(chart_win, bg=LIGHT_BG, padx=16, pady=14)
        summary.pack(fill="x")
        cards = [
            ("Processed Articles", str(len(df))),
            ("Unique Sources", str(df["source"].nunique() if "source" in df.columns else 0)),
            ("Unique Categories", str(df["category"].nunique() if "category" in df.columns else 0)),
        ]
        for title, value in cards:
            card = tk.Frame(summary, bg=WHITE, highlightbackground=BORDER_COLOR, highlightthickness=1)
            card.pack(side="left", padx=(0, 10))
            inner = tk.Frame(card, bg=WHITE, padx=18, pady=12)
            inner.pack()
            tk.Label(inner, text=title, bg=WHITE, fg=TEXT_MUTED, font=("Segoe UI", 9)).pack(anchor="w")
            tk.Label(inner, text=value, bg=WHITE, fg=MAIN_COLOR, font=("Segoe UI", 18, "bold")).pack(anchor="w")

        canvas = tk.Canvas(chart_win, bg=LIGHT_BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(chart_win, orient="vertical", command=canvas.yview)
        content = tk.Frame(canvas, bg=LIGHT_BG)
        content.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=content, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        rows = tk.Frame(content, bg=LIGHT_BG, padx=16, pady=8)
        rows.pack(fill="both", expand=True)

        chart_paths = [
            ("Articles by Source", path1, (500, 280)),
            ("Articles by Category", path2, (420, 280)),
            ("Top Authors", path3, (500, 280)),
            ("Title Keywords", path4, (500, 280)),
        ]

        for idx in range(0, len(chart_paths), 2):
            row = tk.Frame(rows, bg=LIGHT_BG)
            row.pack(fill="x", pady=(0, 12))
            for title, path, size in chart_paths[idx:idx + 2]:
                card = tk.Frame(row, bg=WHITE, highlightbackground=BORDER_COLOR, highlightthickness=1)
                card.pack(side="left", fill="both", expand=True, padx=(0, 10))
                tk.Label(card, text=title, bg=WHITE, fg=TEXT_DARK, font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=14, pady=(14, 8))
                self._load_chart_image(card, path, size)

        self._set_status("Charts generated")

    def _on_close(self):
        if self.is_fetching:
            if not messagebox.askyesno("Exit", "Fetching is still in progress. Close anyway?"):
                return

        self.is_closing = True

        if self.queue_job is not None:
            try:
                self.root.after_cancel(self.queue_job)
            except Exception:
                pass
            self.queue_job = None

        self.chart_images.clear()
        self.chart_labels.clear()

        try:
            self.root.quit()
        except Exception:
            pass

        try:
            self.root.destroy()
        except Exception:
            pass

    def run(self):
        self.root.mainloop()
