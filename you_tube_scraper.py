import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from time import sleep

def setup_driver():
    options = Options()
    options.headless = True  # Run browser in headless mode
    driver = webdriver.Edge(options=options)
    driver.set_page_load_timeout(10)
    return driver

def search_video(driver, query):
    print("Navigating to YouTube")
    driver.get('https://www.youtube.com/')
    driver.maximize_window()
    sleep(5)
    print("Searching for video")
    search = driver.find_element(By.NAME, "search_query")
    search.clear()
    search.send_keys(query)
    search.send_keys(Keys.ENTER)
    sleep(5)

def click_first_video(driver):
    print("Clicking on the first video")
    link = driver.find_element(By.XPATH, """//*[@id="video-title"]/yt-formatted-string""")
    link.click()
    sleep(10)  # Adjusted sleep time to ensure video page loads

def scroll_and_collect_comments(driver, max_scrolls, stop_scroll_threshold=3):
    print("Scrolling to load comments")
    collected_comments = []
    previous_comment_count = 0
    no_new_comments_counter = 0

    for i in range(max_scrolls):
        driver.execute_script("window.scrollBy(0, 700)")
        sleep(1)  # Adjusted sleep time to 1 second for faster scrolling
        
        comments = driver.find_elements(By.XPATH, """//*[@id="content-text"]""")
        current_comment_count = len(comments)
        
        if current_comment_count > previous_comment_count:
            no_new_comments_counter = 0
            previous_comment_count = current_comment_count
            collected_comments = [comment.text for comment in comments]
            print(f"Collected {len(collected_comments)} comments after {i+1} scrolls")
        else:
            no_new_comments_counter += 1
            print(f"No new comments detected for {no_new_comments_counter} consecutive scrolls")
        
        if no_new_comments_counter >= stop_scroll_threshold:
            print("No new comments detected for several scrolls, stopping.")
            break

    return collected_comments

def save_comments_to_csv(comments, filename):
    print(f"Saving {len(comments)} comments to {filename}")
    df = pd.DataFrame({"comment": comments})
    df.to_csv(filename, index=False)
    print(f"Comments saved to {filename}")

def main():
    driver = setup_driver()
    try:
        search_video(driver, "Your Mobile Videos can Look Like Movies .. In Real Life")
        click_first_video(driver)
        comments = scroll_and_collect_comments(driver, max_scrolls=1000, stop_scroll_threshold=3)  # Adjusted number of scrolls for testing
        save_comments_to_csv(comments, "youtube_comments.csv")
        print(f"Collected {len(comments)} comments.")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
