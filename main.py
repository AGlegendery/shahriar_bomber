# loop_search.py
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

TARGET_URL = "https://panel.shahriareiran.com/auth"   # <-- آدرس صفحه‌ای که می‌خواهید سرچ/سابمیت انجام شود
QUERY_TEXT = str(input("Enter the shahriar student number: "))
ITERATIONS = 50            # تعداد تکرارها؛ یا while True برای بی‌نهایت
MIN_SLEEP = 1              # بین هر مرحله کمترین تأخیر
MAX_SLEEP = 2             # بیشترین تأخیر (برای رفتار طبیعی‌تر)

# روش‌های پیدا کردن المنت: می‌توانید هرکدوم رو امتحان کنید
# search_input: مثلاً By.NAME, "q" یا By.ID, "search" یا xpath
SEARCH_SELECTORS = [
    (By.NAME, "phone"),
    (By.ID, "react-aria2913633346-«rq»"),
    (By.CSS_SELECTOR, "input[type='tel']"),
    (By.XPATH, "//input[contains('شماره موبایل خود را وارد کنید')]")
]

# submit button selectors
SUBMIT_SELECTORS = [
    (By.CSS_SELECTOR, "button[type='submit']"),
    (By.XPATH, "//button[contains(.,'دریافت کد تایید')]"),
]

def find_element_try(driver, selectors, timeout=5):
    wait = WebDriverWait(driver, timeout)
    for by, val in selectors:
        try:
            return wait.until(EC.presence_of_element_located((by, val)))
        except Exception:
            continue
    raise NoSuchElementException("CSS_SELECTOR does not find.")

def main():
    options = webdriver.ChromeOptions()
    #options.add_argument("--headless=new")
    #  اگر می‌خواهید بدون UI اجرا شود
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.maximize_window()

    try:
        for i in range(ITERATIONS):
            print(f"[{i+1}/{ITERATIONS}] Opening {TARGET_URL}")
            driver.get(TARGET_URL)

            # پیدا کردن فیلد جستجو
            try:
                search_input = find_element_try(driver, SEARCH_SELECTORS, timeout=4)
            except NoSuchElementException:
                print("Number target does not find retrying...")
                time.sleep(random.uniform(MIN_SLEEP, MAX_SLEEP))
                continue

            # پاک‌کردن و نوشتن کوئری
            try:
                search_input.clear()
            except Exception:
                pass
            search_input.send_keys(QUERY_TEXT)
            time.sleep(random.uniform(0.2, 0.6))

            # تلاش برای پیدا کردن و کلیک روی دکمه سابمیت
            clicked = False
            for sel in SUBMIT_SELECTORS:
                try:
                    btn = driver.find_element(*sel)
                    btn.click()
                    clicked = True
                    break
                except Exception:
                    continue

            # اگر دکمه پیدا نشد، سعی می‌کنیم Enter را ارسال کنیم
            if not clicked:
                print("submit button wasn't find")
                try:
                    search_input.send_keys(Keys.ENTER)
                    clicked = True
                except Exception:
                    print("sending POST payload failed")

            # بعد از ارسال، کمی صبر کن
            time.sleep(random.uniform(1.0, 3.0))

            # اگر خواستید تأیید کنید که URL تغییر کرده یا نتیجه لود شده،
            # می‌توانید اینجا چک بزنید (مثال: انتظار برای المنت نتایج)
            # WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".results")))

            # بازگشت به آدرس اولیه (یا driver.back() اگر می‌خواهید history استفاده شود)
            print("redirecting ...")
            driver.get(TARGET_URL)

            time.sleep(random.uniform(MIN_SLEEP, MAX_SLEEP))

    except KeyboardInterrupt:
        print("prosess canceld by user")
    finally:
        print("closing driver...")
        driver.quit()

if __name__ == "__main__":
    main()

