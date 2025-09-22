from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import os
import json
from time import sleep
import sys

load_dotenv()


class Scrapper:
    def __init__(self, headless=True) -> None:
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=headless)

        self.context = self.browser.new_context()

    def login(self):
        print("[+] Trying to login.....")
        self.page = self.context.new_page()
        self.page.goto("https://www.linkedin.com/login")
        self.page.wait_for_selector('//*[@id="organic-div"]/form/div[4]/button')

        self.page.fill("#username", str(os.environ.get("LINKEDIN_USERNAME")))
        self.page.fill("#password", str(os.environ.get("LINKEDIN_PASSWORD")))
        self.page.locator('//*[@id="organic-div"]/form/div[4]/button').click()
        self.page.close()

    def search(self, LINK=os.environ.get("LINK")):
        print("[+] Applying Search Filters.....")
        self.page = self.context.new_page()
        self.page.goto(str(LINK))

    def scrap_username(self):
        print("[+] Scraping aria-hidden spans...")

        # Grab all <span aria-hidden="true">
        self.page.wait_for_selector(".update-components-actor__title")
        username_span = self.page.query_selector(".update-components-actor__title")
        username = str()
        if username_span:
            username = self.page.evaluate(
                """
            (el) => {
                // Flatten all child text nodes
                const walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
                for (let node = walker.nextNode(); node; node = walker.nextNode()) {
                    const text = node.textContent.trim();
                    if (text) return text;
                }
                return '';
            }
        """,
                username_span,
            )
            print(f"[+] Scrapping Post of User: {username}")
            # Remove the username element from DOM
            self.page.evaluate("(el) => el.remove()", username_span)
        return username

    def scrap(self, max_scroll_attempts: int = 20, wait_timeout: int = 10000):
        print("[+] Scraping infinitely...")

        captions = []
        scroll_attempts = 0  # counter for consecutive failed scrolls

        while True:
            try:
                # Wait for first post element
                self.page.wait_for_selector(
                    ".update-components-text", timeout=wait_timeout
                )
            except:
                # No element found, scroll down
                self.page.evaluate("window.scrollBy(0, window.innerHeight)")
                self.page.wait_for_timeout(2000)
                scroll_attempts += 1
                if scroll_attempts >= max_scroll_attempts:
                    print("[!] No more new posts. Ending scrape.")
                    break
                continue

            username = self.scrap_username()
            # Grab first post
            div = self.page.query_selector(".update-components-text")
            if div:
                caption = div.inner_text().strip()
                captions.append({"username": username, "caption": caption})
                print(f"[+] Scraped captions: {len(captions)}")

                # Append to file
                # with open("captions.txt", "a", encoding="utf-8") as f:
                #     f.write("\n\n" + caption)

                # Remove element from DOM
                self.page.evaluate("(el) => el.remove()", div)

                # Reset scroll_attempts after successful scrape
                scroll_attempts = 0
            else:
                # Scroll if no post found
                self.page.evaluate("window.scrollBy(0, window.innerHeight)")
                self.page.wait_for_timeout(2000)
                scroll_attempts += 1
                if scroll_attempts >= max_scroll_attempts:
                    print("[!] No more new posts. Ending scrape.")
                    break

    def close(self):
        self.browser.close()
        self.playwright.stop()

    def __del__(self):
        self.close()


def main():
    scraper = Scrapper(headless=False)
    scraper.login()
    scraper.search()
    scraper.scrap()
    print("[+] Process Completed.... Enter any key to exit")
    input()
    del scraper


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("[-] Ctrl+C detected. Exitting.......")
        sys.exit(1)
