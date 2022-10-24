# coding=utf-8
# @Time : 2022/10/21 10:11 AM
# @Author : 王思哲
# @File : auto_room.py
# @Software: PyCharm

import time
import datetime
from choose_room import ChooseRoom
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

##########################################################################################
# 设置网页html加载完后就开始执行下一步代码，不等js加载完成再执行
desired_capabilities = DesiredCapabilities.CHROME
desired_capabilities["pageLoadStrategy"] = "none"

# ChromeDriver的位置，自行更改
CHROME_DRIVER_PATH = './chromedriver'

# 研讨室时间表头
room_time_header = [f'{x}-{x+1}' for x in range(8,21)]
room_time_header_idx = [x+1 for x in range(13)]

# 加载配置信息
with open('config/user_config.txt', encoding='utf-8') as f:
    user_config = eval(f.read())
if user_config["username"] == user_config["companion"]:
    print(f'ERROR        {str(datetime.datetime.now())[:-7]}        配置文件加载失败, 预约人与参会人不能相同!')
    raise NameError.name
##########################################################################################

# 开始
time_start = time.perf_counter()

# 创建浏览器对象
web = Chrome(executable_path=CHROME_DRIVER_PATH, desired_capabilities=desired_capabilities)

# 访问座位预约系统，需要内网
web.get('https://libseminarroom.bjut.edu.cn/#/login')
time.sleep(2)

# 修复Iframe未加载，就执行切换的错误
while True:
    try:
        # 切换到Iframe页面，很关键，否则找不到元素 (登陆框)
        print(web.current_url)
        web.switch_to.frame('loginIframe')
        time.sleep(1)
        break
    except Exception as e:
        continue

try:
    # 输入信息登录
    web.find_element(By.ID, "unPassword").send_keys(user_config["username"])
    web.find_element(By.ID, "pwPassword").send_keys(user_config["password"])

    # 点击登陆按钮
    web.find_element(By.XPATH,'/html/body/div[3]/div[2]/div[2]/div/div[2]/div[2]/div/div[7]/input').click() # 进入网站
    time.sleep(3)

    # 进入预约系统
    # 选择四人研讨室
    web.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div[2]/div[1]/div[2]/div[3]/div').click()
    time.sleep(1)

    # 选择第二天的预约
    web.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div[2]/div[1]/div[3]/div[3]').click()
    time.sleep(1)

    # 获得研讨室的可用时间，按时间段，0为不可用，1为可用  二维list
    all_screen_room_time = []

    # 研讨室编号，2-12有屏幕，可以改成list形式, 第一个room对应XPATH的1，注意不是从0开始的
    ROOM_START = 2
    ROOM_END = 12

    # 查信息
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
            sgl_screen_room_time.append(time_free)

        # 删除最后一个21:00，那里没有进度条
        sgl_screen_room_time.pop()
        # 加入总表
        all_screen_room_time.append(sgl_screen_room_time)

    # 实例化: 算法类 -> 获取结果
    chooseRoom = ChooseRoom(all_screen_room_time)
    room_choose, choose_list = chooseRoom.get_result()
    time_list_info = [room_time_header[x-1] for x in choose_list]

    # 点击房间卡片，进入预约界面
    web.find_element(By.XPATH, f'//*[@id="app"]/div/div[2]/div[2]/div[2]/div[{room_choose}]').click()
    time.sleep(1)

    # 选择预约时间段
    for choose_time in choose_list:
        web.find_element(By.CSS_SELECTOR, f'#app > div > div.body-wrap > div.body-right > div.body-content > div.content-left > div.time-content > div > div:nth-child({choose_time})').click()
        time.sleep(0.5)

    # 添加邀请人账号
    input_companion = web.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div[2]/div[2]/div[2]/div[1]/div[2]/div[1]/input').send_keys(user_config['companion'])
    web.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div[2]/div[2]/div[2]/div[1]/div[2]/div[2]/i').click()

    # 选择预约类型
    web.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div[2]/div[2]/div[1]/div[3]/div[2]/div/div[1]/input').click()
    time.sleep(1)

    # 下拉框选择
    web.find_element(By.XPATH, '/html/body/div[2]/div[1]/div[1]/ul/li[1]').click()

    # 点击确认按钮 [待完成]
    web.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div[2]/div[2]/div[2]/div[3]/button').click()
    time.sleep(2)

    # 输出预约信息
    print(
        f'INFO         {str(datetime.datetime.now())[:-7]}        预约房间号:    {list(filter(lambda k: user_config["room_list"][k] == room_choose, user_config["room_list"]))[0]}        时间段:    {time_list_info}')

    # 保存预约成功截图
    web.save_screenshot(f'./voucher/{str(datetime.datetime.now())[:-7]}.png')
    time.sleep(1)

    # 退出浏览器
    web.quit()

    # 结束
    end_time = time.perf_counter()

except Exception as e:
    print(f'ERROR        {str(datetime.datetime.now())[:-7]}        预约失败')
    web.quit()
    raise e
