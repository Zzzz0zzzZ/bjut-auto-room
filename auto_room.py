# coding=utf-8
# @Time : 2022/10/21 10:11 AM
# @Author : 王思哲
# @File : auto_room.py
# @Software: PyCharm
import time
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By

# 研讨室时间表头
room_time_header = [f'{x}-{x+1}' for x in range(8,21)]
room_time_header_idx = [x+1 for x in range(13)]

# 加载配置信息
with open('./user_config.txt', encoding='utf-8') as f:
    user_config = eval(f.read())

# 创建浏览器对象
web = Chrome('./chromedriver')

# 访问座位预约系统，需要内网
web.get('https://libseminarroom.bjut.edu.cn/#/login')
time.sleep(2)

redirect_url = web.current_url
web.get(redirect_url)
time.sleep(2)

# Iframe页面，很关键，否则找不到元素 (登陆框)
web.switch_to.frame('loginIframe')

try:
    # 输入信息登录
    web.find_element(By.ID, "unPassword").send_keys(user_config["username"])
    web.find_element(By.ID, "pwPassword").send_keys(user_config["password"])

    # 点击登陆按钮
    web.find_element(By.XPATH,'/html/body/div[3]/div[2]/div[2]/div/div[2]/div[2]/div/div[7]/input').click() # 进入网站
    time.sleep(2)

    # 进入预约系统
    print(web.current_url)

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

    # 保存文件仅用于算法可行性测试
    # write_obj = pd.DataFrame(data=all_screen_room_time)
    # write_obj.to_csv('./test.csv', index=False, header=room_time_header, encoding='utf-8-sig')
    # print(all_screen_room_time)
    # print(len(all_screen_room_time))

    # 实例化: 算法类 -> 获取结果  [待完成]
    # codes

    # 从算法获取 room_choose_number 和 room_choose_time
    example_choose = 2  # 407   [测试用]

    # 点击房间卡片，进入预约界面
    web.find_element(By.XPATH, f'//*[@id="app"]/div/div[2]/div[2]/div[2]/div[{example_choose}]').click()
    time.sleep(1)


    # 选择预约时间段, 最后改成 in [list] 形式 , 循环是 [测试用]
    for i in range(3):
        web.find_element(By.CSS_SELECTOR, f'#app > div > div.body-wrap > div.body-right > div.body-content > div.content-left > div.time-content > div > div:nth-child({i+5})').click()
        time.sleep(0.5)

    # 添加邀请人账号
    input_companion = web.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div[2]/div[2]/div[2]/div[1]/div[2]/div[1]/input').send_keys(user_config['companion'])
    web.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div[2]/div[2]/div[2]/div[1]/div[2]/div[2]/i').click()

    # 选择预约类型 [待测试]
    web.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div[2]/div[2]/div[1]/div[3]/div[2]/div/div[1]/input').click()
    web.find_element(By.XPATH, '/html/body/div[2]/div[1]/div[1]/ul/li[1]/span').click()

    # 点击确认按钮 [待完成]
    # codes

    # 保存预约成功截图
    web.save_screenshot('./test_pic.png')

except Exception as e:
    print(web.current_url)
    raise e
