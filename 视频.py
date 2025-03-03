'''
// Function to get all `a` links from `sh-res-h` divs, excluding those where img has title="已完成" and without (必看)
function getFilteredLinks() {
    const divs = document.querySelectorAll('div.sh-res-h');
    const links = [];

    divs.forEach(div => {
        const anchor = div.querySelector('a');
        const img = div.querySelector('img');
        const spans = div.querySelectorAll('span');

        // Check if the anchor exists and if the img is not present with title="已完成"
        // Also check if there is at least one span containing (必看)
        const hasMustWatch = Array.from(spans).some(span => span.textContent.trim() === '(必看)');

        if (anchor && (!img || img.getAttribute('title') !== '已完成') && hasMustWatch) {
            links.push(anchor.href);
        }
    });

    return links;
}

// Usage
const links = getFilteredLinks();
console.log(links);

'''

from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Edge WebDriver路径
edge_driver_path = './edge/msedgedriver.exe'  # 替换为msedgedriver的实际路径
options = Options()

# 去掉用户数据目录的设置（如果需要）
# options.add_argument("--user-data-dir=C:\\Users\\001\\AppData\\Local\\Microsoft\\Edge\\User Data")
# options.add_argument("--profile-directory=Default")

service = Service(edge_driver_path)
driver = webdriver.Edge()

#登录
denglu_link = 'file:///C:/Users/001/Desktop/py/%E6%9D%82%E9%A1%B9/%E8%87%AA%E5%8A%A8%E7%9C%8B%E8%A7%86%E9%A2%91/test.html'

driver.get(denglu_link)
time.sleep(2)  # 等待页面加载

username = "20242310870708"
password = "abc256912"

# 输入账号
username_input = driver.find_element(By.ID, "username")
username_input.send_keys(username)

# 输入密码
password_input = driver.find_element(By.ID, "password")
password_input.send_keys(password)

# 可选：勾选“7天免登录”
# remember_me = driver.find_element(By.ID, "rememberMe")
# if not remember_me.is_selected():
#     remember_me.click()
    
    
# 模拟点击登录按钮
login_button = driver.find_element(By.ID, "login_submit")
login_button.click()

# 等待一段时间，确保登录成功
time.sleep(5)

# time.sleep(999999)

# 链接数组
links = [
 'file:///C:/Users/001/Desktop/py/%E6%9D%82%E9%A1%B9/%E8%87%AA%E5%8A%A8%E7%9C%8B%E8%A7%86%E9%A2%91/test.html',



    # 添加更多链接
]


# 遍历链接数组并每隔10分钟打开一个链接
for link in links:
    try:
        driver.get(link)
        
        # 等待页面加载完成
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body'))
        )
        
        # 等待10秒钟
        time.sleep(10)
        
        # 找到播放按钮并点击
        try:
            play_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.dplayer-icon.dplayer-play-icon'))
            )
            play_button.click()
            try:
                time.sleep(2)
                print(f"开始获取视频时间")
                duration_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '.dplayer-dtime'))
                )
                time_str = duration_element.text
                time_parts = time_str.split(":")
                #print("fffffffffff"+time_parts[0]+time_parts[1])
                num = int(time_parts[0])*60 + int(time_parts[1])
                print(f"获取到视频时间: {time_str}{type(time_str)}转化秒{num}")
            except Exception as e:
                num = 600    
                print(f"视频点击但是没有获取到时间默认,10分钟: {link}")

        except Exception as e:
            num = 5
            print(f"没有获取到视频按钮 {link}: {e}")

    except Exception as e:
        num =1 
        print(f"错误链接 {link}: {e}")
    
    # 等待10分钟（600秒）再打开下一个链接
    print(f"等待{num}后打开下一个视频")
    time.sleep(num)
print(f"结束")
# 完成后关闭浏览器
driver.quit()
