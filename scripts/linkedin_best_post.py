import os
# from browseruse import Browser

class LinkedinBestPost():

    def __init__(self, browser, username, password, topic_keywords):

        self.browser = browser
        self.topic_keywords = topic_keywords
        print("Got the topic...!")

        self.login_linkedin(username, password)
        print("linkedin login completed...!")
        self.best_post = self.search_linkedin_for_topic()


    def login_linkedin(self, username, password):

        """Log in to LinkedIn using provided credentials."""

        self.browser.visit("https://www.linkedin.com/login")
        self.browser.find_element("id", "username").send_keys(username)
        self.browser.find_element("id", "password").send_keys(password)
        self.browser.find_element("css selector", "button[type='submit']").click()

    def search_linkedin_for_topic(self):
        """
        Search LinkedIn for posts matching the topic_keywords and return
        the text content of the best post (e.g., the one with the highest engagement).
        """
        print("keyword search started...!")
        # Build a search URL (adjust parameters as needed)
        search_url = f"https://www.linkedin.com/search/results/content/?keywords={self.topic_keywords}"
        self.browser.get(search_url)

        # Allow time for results to load (you might need to add explicit waits)
        self.browser.sleep(3)

        # Assume posts are selectable with a given CSS selector (you'll need to adjust this)
        posts = self.browser.find_elements("css selector", ".search-result__post")

        best_post = None
        best_score = -1
        for post in posts:
            try:
                # Extract like and comment counts (adjust selectors as needed)
                likes_text = post.find_element("css selector", ".social-details-social-counts__reactions-count").text
                comments_text = post.find_element("css selector", ".social-details-social-counts__comments").text

                likes = int(likes_text.replace(',', '') or 0)
                comments = int(comments_text.replace(',', '') or 0)
            except Exception:
                likes, comments = 0, 0

            score = likes + comments
            if score > best_score:
                best_score = score
                best_post = post.text  # or customize what part of the post you need

        return best_post
