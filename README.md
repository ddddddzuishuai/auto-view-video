# auto-view-video
自动刷课


edge下载对应driver

1.手动
edge://version/

https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver

2自动

运行 下载对应版本drivers.py


使用视频.py

1.打开py,配置账号密码

denglu_link ="登录链接"

username = "账号"
password = "密码"

2.获取视频链接

1.使用里面的javascription复制到浏览器F12运行获取需要看视频的链接组（需要自己写）,获取到的链接填入py中的links = []中

2.链接填入all_class_link中，将自动获取

3.配置播放按钮
EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.dplayer-icon.dplayer-play-icon'))

EC.element_to_be_clickable((By.CSS_SELECTOR, '修改成你的视频按钮class'))

EC.presence_of_element_located((By.CSS_SELECTOR, '.dplayer-dtime'))

EC.presence_of_element_located((By.CSS_SELECTOR, '.修改成显示视频文本的class'))


运行





