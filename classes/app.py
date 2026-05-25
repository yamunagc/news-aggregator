import tkinter as tk
from tkinter import ttk, messagebox
import threading
import webbrowser
from PIL import Image, ImageTk

from classes.fetcher import NewsFetcher
from classes.scraper import Scraper
from classes.processor import DataProcessor
from classes.visualizer import Visualizer

MAIN_COLOR = "#02645e"
SECONDARY_COLOR = "#ffde59"
LIGHT_BG = "#f7fffe"
BORDER_COLOR = "#cce8e6"
WHITE = "#ffffff"
TEXT_DARK = "#333333"
TEXT_MUTED = "#888888"
SELECTED_BG = "#e6f4f3"

class NewsApp:

    def __init__(self):
        self.root = tk.Tk()
        self.root.tk.call("tk", "scaling", 1.5)
        self.root.title("News Information Aggregator")
        self.root.geometry("1200x850")
        self.root.configure(bg="#eeeeee")
        self.root.resizable(True, True)

        self.fetcher = NewsFetcher()
        self.scraper = Scraper()
        self.processor = DataProcessor()
        self.visualizer = Visualizer()

        self.articles = []
        self.article_frames = []
        self.current_url = ""
        self.selected_index = -1

        self._setup_styles()
        self._setup_ui()

    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "TCombobox",
            fieldbackground=WHITE,
            background=WHITE,
            bordercolor=MAIN_COLOR,
            arrowcolor=MAIN_COLOR,
            padding=4
        )

    def _setup_ui(self):
        self._build_titlebar()
        self._build_searchbar()
        self._build_main()
        self._build_statusbar()

    def _build_titlebar(self):
        bar = tk.Frame(self.root, bg=MAIN_COLOR, height=48)
        bar.pack(fill="x")
        bar.pack_propagate(False)
        tk.Label(
            bar, text="  News Information Aggregator",
            bg=MAIN_COLOR, fg=WHITE,
            font=("Segoe UI", 14, "bold")
        ).pack(side="left", padx=8, pady=12)

    def _build_searchbar(self):
        outer = tk.Frame(self.root, bg=LIGHT_BG,
                         highlightthickness=1,
                         highlightbackground=BORDER_COLOR)
        outer.pack(fill="x")

        bar = tk.Frame(outer, bg=LIGHT_BG, pady=8)
        bar.pack(fill="x", padx=12)

        tk.Label(bar, text="Category", bg=LIGHT_BG,
                 fg=MAIN_COLOR, font=("Segoe UI", 10, "bold")).pack(side="left", padx=(0,6))

        self.category_var = tk.StringVar(value="technology")
        category_menu = ttk.Combobox(
            bar, textvariable=self.category_var,
            width=14, values=["all"] + NewsFetcher.VALID_CATEGORIES,
            state="readonly"
        )
        category_menu.pack(side="left", padx=(0,14))
        self.category_var.trace("w", self._on_category_change)

        tk.Label(bar, text="Articles", bg=LIGHT_BG,
                 fg=MAIN_COLOR, font=("Segoe UI", 10, "bold")).pack(side="left", padx=(0,6))

        self.count_var = tk.StringVar(value="10")
        self.count_menu = ttk.Combobox(
            bar, textvariable=self.count_var,
            width=6, values=["5", "10", "15", "20"],
            state="readonly"
        )
        self.count_menu.pack(side="left", padx=(0,14))

        tk.Button(
            bar, text="Fetch News",
            bg=MAIN_COLOR, fg=WHITE,
            font=("Segoe UI", 10, "bold"),
            relief="flat", padx=16, pady=5,
            cursor="hand2", bd=0,
            activebackground="#014d49",
            activeforeground=WHITE,
            command=self._on_fetch
        ).pack(side="left", padx=(0,8))

        tk.Button(
            bar, text="Show Charts",
            bg=SECONDARY_COLOR, fg=MAIN_COLOR,
            font=("Segoe UI", 10, "bold"),
            relief="flat", padx=16, pady=5,
            cursor="hand2", bd=0,
            activebackground="#e6c800",
            activeforeground=MAIN_COLOR,
            command=self._show_charts
        ).pack(side="left")

        self.info_label = tk.Label(
            bar, text="", bg=LIGHT_BG,
            fg=TEXT_MUTED, font=("Segoe UI", 9)
        )
        self.info_label.pack(side="right", padx=8)

    def _build_main(self):
        main = tk.Frame(self.root, bg="#eeeeee")
        main.pack(fill="both", expand=True, padx=10, pady=8)

        # LEFT PANEL
        left_outer = tk.Frame(main, bg=WHITE,
                              highlightthickness=1,
                              highlightbackground=BORDER_COLOR)
        left_outer.pack(side="left", fill="y", padx=(0,8))
        left_outer.pack_propagate(False)
        left_outer.configure(width=320)

        # header
        tk.Frame(left_outer, bg=LIGHT_BG, height=34).pack(fill="x")
        tk.Label(
            left_outer, text="ARTICLES",
            bg=LIGHT_BG, fg=MAIN_COLOR,
            font=("Segoe UI", 9, "bold"),
        ).place(x=12, y=8)
        tk.Frame(left_outer, bg=BORDER_COLOR, height=1).pack(fill="x")

        # scrollable article list
        self.list_canvas = tk.Canvas(
            left_outer, bg=WHITE,
            highlightthickness=0, bd=0
        )
        scrollbar = tk.Scrollbar(
            left_outer, orient="vertical",
            command=self.list_canvas.yview
        )
        self.list_canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.list_canvas.pack(side="left", fill="both", expand=True)

        self.list_frame = tk.Frame(self.list_canvas, bg=WHITE)
        self.list_canvas_window = self.list_canvas.create_window(
            (0, 0), window=self.list_frame, anchor="nw"
        )
        self.list_frame.bind("<Configure>", self._on_frame_configure)
        self.list_canvas.bind("<Configure>", self._on_canvas_configure)

        # RIGHT PANEL
        right_outer = tk.Frame(main, bg=WHITE,
                               highlightthickness=1,
                               highlightbackground=BORDER_COLOR)
        right_outer.pack(side="left", fill="both", expand=True)

        # article detail header
        detail_header = tk.Frame(right_outer, bg=LIGHT_BG, height=34)
        detail_header.pack(fill="x")
        detail_header.pack_propagate(False)
        tk.Label(
            detail_header, text="ARTICLE DETAIL",
            bg=LIGHT_BG, fg=MAIN_COLOR,
            font=("Segoe UI", 9, "bold"),
            padx=12, pady=8
        ).pack(side="left")
        tk.Frame(right_outer, bg=BORDER_COLOR, height=1).pack(fill="x")

        # detail content
        detail = tk.Frame(right_outer, bg=WHITE)
        detail.pack(fill="x", padx=14, pady=10)

        self.title_label = tk.Label(
            detail, text="Select an article from the left panel",
            bg=WHITE, fg=TEXT_DARK,
            font=("", 12, "bold"),
            wraplength=700, justify="left", anchor="w"
        )
        self.title_label.pack(fill="x", pady=(0,6))

        self.meta_label = tk.Label(
            detail, text="",
            bg=WHITE, fg=TEXT_MUTED,
            font=("Segoe UI", 9), anchor="w"
        )
        self.meta_label.pack(fill="x", pady=(0,4))

        self.author_label = tk.Label(
            detail, text="",
            bg=WHITE, fg=MAIN_COLOR,
            font=("Segoe UI", 9, "bold"), anchor="w"
        )
        self.author_label.pack(fill="x", pady=(0,6))

        tk.Frame(detail, bg=BORDER_COLOR, height=1).pack(fill="x", pady=(0,6))

        self.content_text = tk.Text(
            detail, height=5,
            font=("Segoe UI", 10),
            bg=LIGHT_BG, fg=TEXT_DARK,
            relief="flat", wrap="word",
            padx=8, pady=6,
            state="disabled"
        )
        self.content_text.pack(fill="x", pady=(0,8))

        self.link_label = tk.Label(
            detail, text="",
            bg=WHITE, fg=MAIN_COLOR,
            font=("Segoe UI", 9, "underline"),
            cursor="hand2", anchor="w"
        )
        self.link_label.pack(fill="x")
        self.link_label.bind("<Button-1>", self._open_url)

        # charts section
        tk.Frame(right_outer, bg=BORDER_COLOR, height=1).pack(fill="x", pady=(8,0))

        charts_header = tk.Frame(right_outer, bg=LIGHT_BG, height=34)
        charts_header.pack(fill="x")
        charts_header.pack_propagate(False)
        tk.Label(
            charts_header, text="CHARTS",
            bg=LIGHT_BG, fg=MAIN_COLOR,
            font=("Segoe UI", 9, "bold"),
            padx=12, pady=8
        ).pack(side="left")
        tk.Frame(right_outer, bg=BORDER_COLOR, height=1).pack(fill="x")

        self.chart_frame = tk.Frame(right_outer, bg=WHITE)
        self.chart_frame.pack(fill="both", expand=True, padx=8, pady=8)

        tk.Label(
            self.chart_frame,
            text="Fetch news first, then click Show Charts",
            bg=WHITE, fg=TEXT_MUTED,
            font=("Segoe UI", 10)
        ).pack(pady=30)

    def _build_statusbar(self):
        bar = tk.Frame(self.root, bg=LIGHT_BG, height=28,
                       highlightthickness=1,
                       highlightbackground=BORDER_COLOR)
        bar.pack(fill="x", side="bottom")
        bar.pack_propagate(False)
        self.status_label = tk.Label(
            bar, text="  Ready",
            bg=LIGHT_BG, fg=MAIN_COLOR,
            font=("Segoe UI", 9)
        )
        self.status_label.pack(side="left", pady=4)

    def _on_frame_configure(self, event):
        self.list_canvas.configure(
            scrollregion=self.list_canvas.bbox("all")
        )

    def _on_canvas_configure(self, event):
        self.list_canvas.itemconfig(
            self.list_canvas_window, width=event.width
        )

    def _on_fetch(self):
        self._set_status("Fetching news...")
        for w in self.list_frame.winfo_children():
            w.destroy()
        self.article_frames = []
        self.root.update()
        thread = threading.Thread(target=self._fetch_worker)
        thread.daemon = True
        thread.start()

    def _on_category_change(self, *args):
        if self.category_var.get() == "all":
            self.count_menu.config(state="disabled")
        else:
            self.count_menu.config(state="readonly")

    def _fetch_worker(self):
        try:
            category = self.category_var.get()
            count = int(self.count_var.get())

            self._set_status("Fetching from NewsAPI...")
            if category == "all":
                api_articles = self.fetcher.fetch_all_categories(page_size=5)
            else:
                api_articles = self.fetcher.fetch_headlines(category, count)

            self._set_status("Scraping article details...")
            scraped = self.scraper.scrape_all(api_articles)

            self._set_status("Processing data...")
            self.processor.merge(scraped)
            self.processor.remove_duplicates()
            self.processor.clean()

            self.articles = scraped
            self.root.after(0, self._populate_list)

        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", str(e)))
            self.root.after(0, lambda: self._set_status("Error occurred"))

    def _populate_list(self):
        for w in self.list_frame.winfo_children():
            w.destroy()
        self.article_frames = []

        for i, article in enumerate(self.articles):
            frame = tk.Frame(
                self.list_frame, bg=WHITE,
                cursor="hand2"
            )
            frame.pack(fill="x")

            tk.Frame(frame, bg=BORDER_COLOR, height=1).pack(fill="x")

            inner = tk.Frame(frame, bg=WHITE, pady=6, padx=10)
            inner.pack(fill="x")

            title_lbl = tk.Label(
                inner,
                text=article.title[:60] + ("..." if len(article.title) > 60 else ""),
                bg=WHITE, fg=TEXT_DARK,
                font=("Segoe UI", 10),
                anchor="w", wraplength=260,
                justify="left"
            )
            title_lbl.pack(fill="x")

            source_lbl = tk.Label(
                inner, text=article.source or "",
                bg=WHITE, fg=TEXT_MUTED,
                font=("Segoe UI", 8),
                anchor="w"
            )
            source_lbl.pack(fill="x")

            self.article_frames.append((frame, inner, title_lbl, source_lbl))

            for widget in [frame, inner, title_lbl, source_lbl]:
                widget.bind("<Button-1>", lambda e, idx=i: self._select_article(idx))

        count = len(self.articles)
        category = self.category_var.get()
        self.info_label.config(text=f"Last fetched: {category} — {count} articles")
        self._set_status(f"Done — {count} articles loaded")

    def _select_article(self, index):
        # reset all
        for frame, inner, title_lbl, source_lbl in self.article_frames:
            frame.configure(bg=WHITE)
            inner.configure(bg=WHITE)
            title_lbl.configure(bg=WHITE, fg=TEXT_DARK)
            source_lbl.configure(bg=WHITE, fg=TEXT_MUTED)

            # remove left border effect
            for child in frame.winfo_children():
                if isinstance(child, tk.Frame) and child.cget("bg") == MAIN_COLOR:
                    child.destroy()

        # highlight selected
        frame, inner, title_lbl, source_lbl = self.article_frames[index]
        frame.configure(bg=SELECTED_BG)
        inner.configure(bg=SELECTED_BG)
        title_lbl.configure(bg=SELECTED_BG, fg=MAIN_COLOR)
        source_lbl.configure(bg=SELECTED_BG, fg="#04a699")

        # left border
        border = tk.Frame(frame, bg=MAIN_COLOR, width=3)
        border.place(x=0, y=0, relheight=1)

        # update detail panel
        article = self.articles[index]
        self.title_label.config(text=article.title)
        self.meta_label.config(
            text=f"{article.source or ''}   |   {article.category or ''}   |   {str(article.published_at)[:10]}"
        )
        self.author_label.config(
            text=f"Author: {article.author or 'Unknown'}"
        )

        self.content_text.config(state="normal")
        self.content_text.delete("1.0", tk.END)
        self.content_text.insert(
            tk.END,
            article.content[:500] if article.content else "No content available"
        )
        self.content_text.config(state="disabled")

        self.link_label.config(text=article.url or "")
        self.current_url = article.url or ""

    def _open_url(self, event):
        if self.current_url:
            webbrowser.open(self.current_url)

    def _show_charts(self):
        df = self.processor.get_data()
        if df.empty:
            messagebox.showinfo("No data", "Please fetch news first!")
            return

        path1 = self.visualizer.plot_by_source(df)
        path2 = self.visualizer.plot_by_category(df)

        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        try:
            img1 = ImageTk.PhotoImage(
                Image.open(path1).resize((500, 260))
            )
            img2 = ImageTk.PhotoImage(
                Image.open(path2).resize((260, 260))
            )

            lbl1 = tk.Label(self.chart_frame, image=img1, bg=WHITE)
            lbl1.image = img1
            lbl1.pack(side="left", padx=6, pady=4)

            lbl2 = tk.Label(self.chart_frame, image=img2, bg=WHITE)
            lbl2.image = img2
            lbl2.pack(side="left", padx=6, pady=4)

        except Exception as e:
            tk.Label(
                self.chart_frame,
                text=f"Could not load charts: {e}",
                bg=WHITE, fg=TEXT_MUTED
            ).pack()

    def _set_status(self, msg):
        self.root.after(0, lambda: self.status_label.config(text=f"  {msg}"))

    def run(self):
        self.root.mainloop()