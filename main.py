from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys 
import time

class InternetSpeedTwitterBot:
    def __init__(self):
        self.USERNAME = 'enter your twitter username'
        self.EMAIL = 'enter your twitter email'
        self.PASSWORD = 'enter your twitter password'
        self.DOWN = 25 #'download speed promised by you ISP'
        self.UP = 10 # upload speed promised by your ISP
        self.ISP = '@reliancejio'  #twitter handle of your ISP

        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_experimental_option('detach', True)

        # Note: uncomment these if you are running online...
        # self.chrome_options.add_argument("--headless")
        # self.chrome_options.add_argument("--no-sandbox")
        # self.chrome_options.add_argument("--disable-dev-shm-usage")

        self.driver = webdriver.Chrome(options=self.chrome_options)
        self.driver.execute_script("window.open('_blank', '_blank');")
        self.all_windows = self.driver.window_handles
        self.driver.switch_to.window(self.all_windows[0])

    # for internet speed
    def get_internet_speed(self):
        self.driver.get('https://www.speedtest.net/')
        time.sleep(7)

        try:
            cookies = self.driver.find_element(By.ID, value='onetrust-accept-btn-handler')
            cookies.click()
            time.sleep(2)
        except:
            pass

        run_test = self.driver.find_element(By.XPATH, value='//*[@id="container"]/div[1]/div[3]/div/div/div/div[2]/div[3]/div[1]/a')
        run_test.click()

        time_count = 30
        while True:
            time.sleep(time_count)
            try:
                result_id = self.driver.find_element(By.XPATH, value='//*[@id="container"]/div[1]/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[1]/div/div/div[2]/div[2]/a').text
                download_speed = self.driver.find_element(By.CLASS_NAME, value='download-speed').text
                upload_speed = self.driver.find_element(By.CLASS_NAME, value='upload-speed').text
                if len(result_id) > 4:
                    break
            except:
                time_count = 5
        result_link = 'https://www.speedtest.net/result/' + result_id.strip()
        print('result_id: ', result_id)
        print('download: ', download_speed, 'upload: ', upload_speed)

        self.driver.close()
        self.driver.switch_to.window(self.all_windows[1])
        return (result_link, download_speed, upload_speed)

    # for twitter
    def tweet_at_provider(self, result_link, download_speed, upload_speed):
        if float(download_speed.strip()) >= self.DOWN:
            print("Internet speed is high!")
            return

        self.driver.get('https://x.com/i/flow/login')

        TWEET = f"Hey {self.ISP}, why is my internet speed {download_speed}down/{upload_speed}up when I pay for {self.DOWN}down/{self.UP}up?\nResult: {result_link}"


        time_count = 5
        while True:
            time.sleep(time_count)
            try:
                email = self.driver.find_element(By.XPATH, value='//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[4]/label/div/div[2]/div/input')
                email.send_keys(self.EMAIL, Keys.ENTER)
                break
            except:
                time_count = 3

        time.sleep(4)
        try:
            username = self.driver.find_element(By.XPATH, value='//*[@id="react-root"]/div/div/div/main/div/div/div/div[2]/div[2]/div[1]/div/div/div[2]/label/div/div[2]')
            username.send_keys(self.USERNAME, Keys.ENTER)
            time.sleep(4)
        except:
            pass
        passowrd = self.driver.find_element(By.NAME, value='password')
        passowrd.send_keys(self.PASSWORD, Keys.ENTER)

        time.sleep(6)
        post = self.driver.find_element(By.XPATH, value='//*[@id="react-root"]/div/div/div[2]/header/div/div/div/div[1]/div[3]/a/div')
        post.click()
        time.sleep(5)

        write = self.driver.find_element(By.XPATH, value='//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[3]/div[2]/div[1]/div/div/div/div[1]/div[2]/div/div/div/div/div/div/div/div/div/div/div/div/div[1]/div/div/div/div/div/div[2]/div')
        write.send_keys(TWEET)

        time.sleep(3)
        tweet = self.driver.find_element(By.XPATH, value='//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[3]/div[2]/div[1]/div/div/div/div[2]/div[2]/div/div/div/button[2]')
        tweet.click()

        print(TWEET, ' posted!')


if __name__ == '__main__':
    bot = InternetSpeedTwitterBot()
    result, down, up = bot.get_internet_speed()
    bot.tweet_at_provider(result, down, up)
