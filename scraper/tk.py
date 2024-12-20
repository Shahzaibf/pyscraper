import threading
import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import ttk, messagebox
import ollama


class WebScraperGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Web Scraper with GUI")
        self.root.geometry("600x1000")

        # URL Input
        self.url_label = ttk.Label(root, text="Enter URL:")
        self.url_label.pack(pady=5)

        self.url_entry = ttk.Entry(root, width=80)
        self.url_entry.pack(pady=5)

        # Scrape Button
        self.scrape_button = ttk.Button(
            root, text="Scrape", command=self.start_scraping)
        self.scrape_button.pack(pady=10)

        # Results Display
        self.results_text = tk.Text(root, wrap=tk.WORD, height=15)
        self.results_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Status Label
        self.status_label = ttk.Label(root, text="Status: Idle")
        self.status_label.pack(pady=5)

        # ask for anything specific
        self.tag_button = ttk.Label(
            root, text="Ask our AI assistant about the parsed information!")
        self.tag_button.pack(pady=5)

        self.url_entry2 = ttk.Entry(root, width=80)
        self.url_entry2.pack(pady=5)

        # Specific tag scrape
        self.specific_button = ttk.Button(
            root, text="Confirm", command=self.specific_scrape
        )
        self.specific_button.pack(pady=10)

        # Results2 Display
        self.results_text2 = tk.Text(root, wrap=tk.WORD, height=15)
        self.results_text2.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Status 2
        self.status_label2 = ttk.Label(root, text="Status: Idle")
        self.status_label2.pack(pady=5)

    def start_scraping(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("Input Error", "Please enter a URL.")
            return
        # Disable the button to prevent multiple clicks
        self.scrape_button.config(state=tk.DISABLED)
        self.results_text.delete(1.0, tk.END)
        self.status_label.config(text="Status: Scraping...")

        # Start scraping in a new thread
        thread = threading.Thread(target=self.scrape, args=(url,))
        thread.start()

    def scrape(self, url):
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (compatible; WebScraper/1.0)"
            }
            response = requests.get(url)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser').prettify()
            self.update_results(soup)
            self.update_status("Scraping completed successfully.")
        except requests.exceptions.RequestException as e:
            self.update_status(f"Error: {e}")
        finally:
            # Re-enable the button
            self.scrape_button.config(state=tk.NORMAL)

    def update_results(self, data):
        # Insert data into the text widget

        self.results_text.insert(tk.END, data)

    def update_status(self, message):
        self.status_label.config(text=f"Status: {message}")

    def specific_scrape(self):
        data = self.url_entry.get().strip()
        question = self.url_entry2.get().strip()
        if not data or not question:
            messagebox.showwarning(
                "Input Error", "Please enter your previous URL and question.")
            return
        self.status_label2.config(text="Status: Sending to AI...")
        self.tag_button.config(state=tk.DISABLED)
        self.results_text2.delete(1.0, tk.END)
        thread = threading.Thread(target=self.ask_ai, args=(data, question))
        thread.start()

    def ask_ai(self, data, question):
        try:
            response = ollama.generate(model="llama3.2",
                                       prompt=f"{data}\n\nQuestion: {question}"
                                       )
            print("Response from Ollama:", response)
            answer = response['response'] if response else "No answer."
            self.results_text2.insert(tk.END, answer)
            self.status_label2.config(text="Status: Answer received.")
        except Exception as e:
            self.status_label2.config(text=f"Error: {e}")
        finally:
            self.tag_button.config(state=tk.NORMAL)


def main():
    root = tk.Tk()
    app = WebScraperGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
