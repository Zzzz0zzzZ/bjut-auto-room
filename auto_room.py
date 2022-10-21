# coding=utf-8
# @Time : 2022/10/21 10:11 AM
# @Author : 王思哲
# @File : auto_room.py
# @Software: PyCharm
import time
import pandas as pd
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By

room_time_header  = ["8-9", "9-10", "10-11", "11-12", "12-13", "13-14", "14-15", "15-16", "16-17", "17-18", "18-19", "19-20", "20-21"]

with open('./user_config.txt', encoding='utf-8') as f:
    user_config = eval(f.read())

web = Chrome('./chromedriver')

web.get('https://libseminarroom.bjut.edu.cn/#/login')
time.sleep(2)

redirect_url = web.current_url
web.get(redirect_url)
time.sleep(2)

# Iframe页面，很关键，否则找不到元素
web.switch_to.frame('loginIframe')

try:
    # 输入信息登录
    web.find_element(By.ID, "unPassword").send_keys(user_config["username"])
    web.find_element(By.ID, "pwPassword").send_keys(user_config["password"])

    # 点击登陆按钮
    web.find_element(By.XPATH,'/html/body/div[3]/div[2]/div[2]/div/div[2]/div[2]/div/div[7]/input').click() # 进入网站

    # 进入预约系统
    print(web.current_url)

    # 选择四人研讨室
    web.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div[2]/div[1]/div[2]/div[3]/div').click()
    time.sleep(1)

    # 选择第二天的预约
    web.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div[2]/div[1]/div[3]/div[3]').click()
    time.sleep(1)

    # 获得研讨室的可用时间，按时间段，0为不可用，1为可用
    all_screen_room_time = []
    # 研讨室编号，2-12有屏幕，可以改成list形式
    ROOM_START = 2
    ROOM_END = 12

    for i in range(ROOM_START, ROOM_END):
        # 找到每一个有显示屏的卡片
        room_detail = web.find_element(By.XPATH, f'//*[@id="app"]/div/div[2]/div[2]/div[2]/div[{i+1}]')
        # 找到所有时间段
        time_details = room_detail.find_elements(By.CLASS_NAME, 'time-show')
        # 遍历时间段，看哪个时间段有效
        sgl_screen_room_time = []
        for time_detail in time_details:
            time_aval = time_detail.find_element(By.CLASS_NAME, 'time-text').text
            time_free = 0 if time_detail.find_elements(By.CLASS_NAME, 'tiem-section-free') == [] else 1
            print(time_detail.find_elements(By.CLASS_NAME, 'tiem-section-free'))
            sgl_screen_room_time.append(time_free)

        # 删除最后一个21:00，那里没有进度条
        sgl_screen_room_time.pop()
        all_screen_room_time.append(sgl_screen_room_time)

    write_obj = pd.DataFrame(data=all_screen_room_time)
    write_obj.to_csv('./test_data.csv', index=False,header=room_time_header, encoding='utf-8-sig')
    print(all_screen_room_time)
    print(len(all_screen_room_time))

except Exception as e:
    print(web.current_url)
    raise e
