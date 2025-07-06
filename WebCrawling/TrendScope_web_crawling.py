# TrendScope 프로젝트(웹 크롤링 부분)

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from pytrends.request import TrendReq
import os
import pandas as pd

# 다운로드 경로 설정
def set_download_dir():
    download_dir = os.path.join(os.getcwd(), 'downloads')
    os.makedirs(download_dir, exist_ok = True)

    chrome_options = webdriver.ChromeOptions()
    prefs = {
        'download.default_directory': download_dir,
        'download.prompt_for_download': False,
        'directory_upgrade': True 
    }
    chrome_options.add_experimental_option('prefs', prefs)
    
    return chrome_options, download_dir

    
# 웹 페이지 접속
def access(driver, url):
    driver.get(url)

    # 웹 페이지의 모든 요소 로딩 확인
    all_elem = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'yDmH0d'))
    )
    print('\n[페이지 로딩 성공]\n')
    # 페이지의 모든 요소 반환
    return all_elem


# 실시간 인기 페이지로 이동
def move_to_popularity_page(driver, elem):
    menu_button = elem.find_element(By.CLASS_NAME, 'gb_Lc')    
    menu_button.click()

    # 메뉴 구성요소만 추출
    li_list = elem.find_elements(By.CLASS_NAME, 'VfPpkd-rymPhb-Tkg0ld')
    is_page_found = False
    try:
        for li in li_list:
            a = li.find_element(By.TAG_NAME, 'a')
            label = a.get_attribute('aria-label')
            if label == '실시간 인기 링크':
                a.click()
                print('\n[이동중...]')
                time.sleep(3)
                is_page_found = True
                break
        
        if is_page_found:
            # 페이지 모든 요소 로딩 확인
            all_elem = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, 'yDmH0d'))
                )
            print('\n[실시간 인기 페이지로 이동 성공]')
            # 페이지의 모든 요소 반환
            return all_elem
        
    except Exception as e:
        print('\n[페이지 이동 실패]')
        print(f'[오류]: {type(e).__name__}: {e}')


# csv파일 내보내기
def export_file(driver, elem):
    export_file_button = elem.find_element(By.CLASS_NAME, 'UrKq0e')
    export_file_button.click()

    try:
        # csv파일 다운로드 버튼
        csv_download_button = elem.find_element(By.CSS_SELECTOR, "li[aria-label='CSV 다운로드']")
        # 화면에 보이게 스크롤
        driver.execute_script("arguments[0].scrollIntoView(true);", csv_download_button)
        # JS로 강제 클릭
        driver.execute_script("arguments[0].click();", csv_download_button)

    except Exception as e:
        print(f'[오류]: {type(e).__name__}: {e}')
    

# 다운로드 완료까지 대기
def wait_for_download(download_dir, timeout = 15):
    elapsed = 0
    while elapsed < timeout:
        for file in os.listdir(download_dir):
            if file.endswith('.csv'):
                print(f'\n[다운로드 성공] {file}')
                return os.path.join(download_dir, file)
        time.sleep(1)
        elapsed += 1
    raise TimeoutError('\n[다운로드 실패]')


def main():
    google_trend_url = 'http://trends.google.co.kr/trends/'
    
    # 다운로드 경로 설정
    chrome_options, download_dir = set_download_dir()

    # 드라이버 객체 생성
    driver = webdriver.Chrome(options = chrome_options)

    # 사이트 접속
    home_page_all_elem = access(driver, google_trend_url)

    # 실시간 인기 메뉴로 이동
    popularity_page_all_elem = move_to_popularity_page(driver, home_page_all_elem)

    # 실시간 트렌드 csv파일로 가져오기
    export_file(driver, popularity_page_all_elem)
    
    # 파일 다운로드 완료까지 대기
    wait_for_download(download_dir)


if __name__ == '__main__':
    main()


