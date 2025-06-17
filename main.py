import time
import pyperclip
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def load_config():
    try:
        with open("task.txt", "r", encoding="utf-8") as f:
            lines = f.read().splitlines()
        if len(lines) < 3:
            print("❌ task.txt cần ít nhất 3 dòng: cookie, box_id, delay")
            return None
        cookie = lines[0].strip().replace("cookie=", "")
        box_id = lines[1].strip().replace("box_id=", "")
        delay = int(lines[2].strip().replace("delay=", ""))
    except Exception as e:
        print(f"❌ Lỗi đọc task.txt: {e}")
        return None

    try:
        with open("noidung.txt", "r", encoding="utf-8") as f:
            message = f.read().strip()
    except Exception as e:
        print(f"❌ Lỗi đọc noidung.txt: {e}")
        return None

    return cookie, box_id, delay, message

def create_driver(cookie):
    options = uc.ChromeOptions()
    
    # Bắt buộc dùng headless cho môi trường không có GUI
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-notifications")

    driver = uc.Chrome(options=options)
    driver.get("https://facebook.com")
    time.sleep(3)

    try:
        driver.delete_all_cookies()
        for part in cookie.split(";"):
            if "=" in part:
                name, value = part.strip().split("=", 1)
                driver.add_cookie({
                    "name": name.strip(),
                    "value": value.strip(),
                    "domain": ".facebook.com"
                })
        driver.get("https://facebook.com/me")
        time.sleep(3)
        if "login" in driver.current_url.lower():
            raise Exception("⚠️ Cookie sai hoặc hết hạn!")
    except Exception as e:
        driver.quit()
        raise Exception(f"❌ Lỗi thêm cookie: {e}")

    return driver

def send_message(driver, message):
    wait = WebDriverWait(driver, 20)
    box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[aria-label='Tin nhắn'][contenteditable='true']")))

    actions = ActionChains(driver)
    pyperclip.copy(message)
    box.click()
    actions.key_down(Keys.CONTROL).send_keys("v").key_up(Keys.CONTROL).send_keys(Keys.ENTER).perform()

def run_spam():
    config = load_config()
    if not config:
        return
    cookie, box_id, delay, message = config

    while True:
        driver = None
        try:
            print("🚀 Mở trình duyệt...")
            driver = create_driver(cookie)
            wait = WebDriverWait(driver, 15)

            print(f"📨 Truy cập box chat {box_id}...")
            driver.get(f"https://www.facebook.com/messages/t/{box_id}")
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[aria-label='Tin nhắn'][contenteditable='true']")))
            time.sleep(2)

            while True:
                try:
                    send_message(driver, message)
                    print(f"✅ Đã gửi lúc {time.strftime('%H:%M:%S')}")
                except Exception as e:
                    print(f"⚠️ Lỗi gửi tin: {e}")
                time.sleep(delay)

        except Exception as e:
            print(f"🔁 Lỗi chính: {e} → Đợi 10 giây rồi chạy lại...")
            time.sleep(10)

        finally:
            if driver:
                try:
                    driver.quit()
                except:
                    pass

if __name__ == "__main__":
    run_spam()
