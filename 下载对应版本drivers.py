from selenium import webdriver
from selenium.webdriver.edge.service import Service
import time
import re
import winreg  # Windows系统 用于从注册表中获取信息
import requests
import zipfile
import os
import subprocess  # 用于获取驱动器的版本号
 
 
def get_edge_version():
    """ 从注册表中获取Edge浏览器的版本号 """
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Edge\BLBeacon")
        version, _ = winreg.QueryValueEx(key, "version")
        winreg.CloseKey(key)
        return version
    except Exception:
        return None
 
 
def get_edgedriver_version():
    """ 获取Edge驱动器版本号 """
    # 指定msedgedriver的路径
    msedgedriver_path = os.path.abspath("edge/msedgedriver.exe")
    try:
        # 尝试获取版本信息
        ver = subprocess.run([msedgedriver_path, '--version'], capture_output=True, text=True)
        if ver.returncode == 0:
            # 形如：Microsoft Edge WebDriver 120.0.2210.91 (f469d579f138ffc82b54354de66117c1cb1bb923)
            match = re.search(r'(\d+\.\d+\.\d+\.\d+)', ver.stdout.strip())
            if match:
                vrsion = match.group(1)
                return vrsion
            else:
                return None
        else:
            print("获取版本时出错:", ver.stderr.strip())
            return None
    except Exception as e:
        print("出现错误:", str(e))
        return None
 
 
def download_edgedriver(version: str):
    """ 下载对应版本的msedgedriver """
    # 检查操作系统位数
    architecture = check_system_bit()
    if architecture == 64:
        # 下载win64位的压缩包
        url = f'https://msedgedriver.azureedge.net/{version}/edgedriver_win64.zip'
    else:
        # 下载win32位的压缩包
        url = f'https://msedgedriver.azureedge.net/{version}/edgedriver_win32.zip'
    print('驱动器压缩包下载地址：')
    print(url)
    response = requests.get(url)
    print('开始获取驱动器压缩包')
    # 保存并解压驱动
    zip_path = f"edgedriver_win{architecture}.zip"
    with open(zip_path, 'wb') as f:
        f.write(response.content)
    print(f'驱动器压缩包已下载到当前工作目录内，文件名{zip_path}')
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall("edge/")
    os.remove(zip_path)
    print('文件已解压，压缩包已删除')
    return os.path.abspath("edge/msedgedriver.exe")
 
 
def check_system_bit():
    """ 检查操作系统位数 """
    if 'PROGRAMFILES(X86)' in os.environ:
        print("你的电脑为 64-bit 操作系统")
        return 64
    else:
        print("你的电脑为 32-bit 操作系统")
        return 32
 
 
def vrsion_comparison(edge_v: str, driver_v: str):
    """ 比较浏览器和驱动的版本号 """
    if edge_v == driver_v:
        return True
    else:
        return False
 
 
def open_edge(url):
    """ 用于展示执行webdriver.Edge方法时检查和设置msedgedriver """
    # 获取浏览器版本
    edge_version = get_edge_version()
    # 获取驱动器版本，同时也是检查驱动器是否存在
    driver_version = get_edgedriver_version()
    if edge_version and driver_version:
        math = vrsion_comparison(edge_version, driver_version)
        if not math:
            print('浏览器和驱动器版本号不一致，但我们仍尝试打开浏览器')
        try:
            # 指定msedgedriver.exe的完整路径
            path_to_executable = os.path.abspath("edge/msedgedriver.exe")
            service = Service(executable_path=path_to_executable)
            driver = webdriver.Edge(service=service)
            driver.get(url)
            # 等待页面加载完成
            time.sleep(30)
        except Exception as e:
            print(f'打开驱动器出错：{e}')
    else:
        print('浏览器或驱动器版本信息缺失，可能导致异常，故暂不能执行爬虫任务。')
 
 
if __name__ == '__main__':
    # 1.获取edge浏览器版本号
    edge_version = get_edge_version()
    print("Edge浏览器版本号:", edge_version)
 
    # 2.获取驱动器版本
    driver_version = get_edgedriver_version()
    print("msedgedriver版本号:", driver_version)
 
    # 3.进行版本信息检查
    check_ok = False
    if driver_version:
        if edge_version:
            # 比较浏览器和驱动器的版本号
            result = vrsion_comparison(edge_version, driver_version)
            if result:
                print('浏览器和驱动的版本一致')
                check_ok = True
            else:
                print(f'浏览器版本{edge_version} 和 驱动器版本{driver_version} 不一致')
                select = input('是否下载浏览器对应版本的驱动？（Y/N）?').strip()
                select = select.lower()
                if select == 'y':
                    # 4.下载驱动器
                    print('开始下载浏览器驱动，请稍候')
                    driver_path = download_edgedriver(edge_version)
                    print(f'驱动已下载，保存在 {driver_path}')
                    check_ok = True
                else:
                    print('您未下载浏览器对应版本的驱动，可能会导致在软件中打开Edge浏览器出问题')
        else:
            print('未获取到Edge浏览器的版本信息')
    else:
        print('未获取到驱动版本信息')
        select = input('是否下载浏览器对应版本的驱动？（Y/N）?').strip()
        select = select.lower()
        if select == 'y':
            # 4.下载驱动器
            print('开始下载浏览器驱动，请稍候')
            driver_path = download_edgedriver(edge_version)
            print(f'驱动已下载，保存在 {driver_path}')
            check_ok = True
        else:
            print('您未下载浏览器对应版本的驱动，可能会导致在软件中打开Edge浏览器出问题')
 
    # 4. 打开浏览器
    if check_ok:
        m_url = 'https://www.baidu.com/'
        open_edge(m_url)
