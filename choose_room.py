# coding=utf-8
# @Time : 2022/10/21 13:31 PM
# @Author : 王思哲
# @File : choose_room.py
# @Software: PyCharm

import numpy as np

##########################################################################################
room_time_header = [f'{x}-{x+1}' for x in range(8,21)]
room_time_header_idx = [x+1 for x in range(13)]

with open('./user_config.txt', encoding='utf-8') as f:
    user_config = eval(f.read())
##########################################################################################

# 使用：实例化类(传入data数据, 二维list) -> 调用get_result()方法, 接收两个返回值
class ChooseRoom:
    def __init__(self, data:list):
        self.data = data
        self.dp = self.get_dp()
        self.chosen_list = self.convert_dp()

    def get_dp(self):
        '''
        获取dp数组
        :return:
        '''
        time_data = self.data
        dp_all = []
        # 遍历每一个房间, 产生dp表, 用于结果选择
        for room in time_data:

            dp = [0 for x in range(len(room))]
            dp[0] = 0 if room[0] == 0 else 1

            for i in range(1, len(room)):

                if room[i] == 0:
                    dp[i] = 0

                else:
                    if room[i - 1] == 0:
                        dp[i] = 1

                    if room[i - 1] == 1:
                        dp[i] = dp[i - 1] + 1
            dp_all.append(dp)

        return dp_all

    def convert_dp(self):
        '''
        返回：一个字典列表，代表所有研讨室的预约指导
        :return:
        '''
        chosen_list = []

        for room in self.dp:
            reverse_room = room[::-1]
            max_idx = len(reverse_room) - np.argmax(reverse_room) - 1
            max_num = room[max_idx]

            if max_num >= 4:
                sub_chosen_list = room_time_header_idx[max_idx-4+1 : max_idx+1]
            elif max_num > 0:
                sub_chosen_list = room_time_header_idx[max_idx-max_num+1 : max_idx+1]
            else:
                sub_chosen_list = []
            chosen_list.append({
                "chosen_num": len(sub_chosen_list),
                "chosen_list": sub_chosen_list
            })

        return  chosen_list

    def get_result(self):
        '''
        返回值第一个代表：选择第几个研讨室。编号按照网页html规则，第一个研讨室为1
        返回值第二个代表：选择哪几个时间段。根据css选择器 nth-child(i)规则，也是从1开始的
        使用的时候直接把这两个值传入find_element()参数即可 [nth-child要根据list返回值做循环]
        :return: int, list
        '''
        final_choose_room = 0
        final_choose_time = []
        nums = [x["chosen_num"] for x in self.chosen_list]
        four_time_room = []
        three_time_room = []
        two_time_room  = []
        one_time_room = []

        for idx, num in enumerate(nums):
            if num == 4:
                four_time_room.append(idx)
            if num == 3:
                three_time_room.append(idx)
            if num == 2:
                two_time_room.append(idx)
            if num == 1:
                one_time_room.append(idx)

        user_prefered = user_config["prefer_room"]

        CHOOSE_FLAG = False
        for up in user_prefered:
            if user_config["room_list"][up]-3 in four_time_room:
                final_choose_room = user_config["room_list"][up]
                final_choose_time = self.chosen_list[final_choose_room-3]["chosen_list"]
                CHOOSE_FLAG = True
                break

        if not CHOOSE_FLAG:
            for up in user_prefered:
                if user_config["room_list"][up] - 3 in three_time_room:
                    final_choose_room = user_config["room_list"][up]
                    final_choose_time = self.chosen_list[final_choose_room - 3]["chosen_list"]
                    CHOOSE_FLAG = True
                    break

        if not CHOOSE_FLAG:
            for up in user_prefered:
                if user_config["room_list"][up] - 3 in two_time_room:
                    final_choose_room = user_config["room_list"][up]
                    final_choose_time = self.chosen_list[final_choose_room - 3]["chosen_list"]
                    CHOOSE_FLAG = True
                    break

        if not CHOOSE_FLAG:
            for up in user_prefered:
                if user_config["room_list"][up] - 3 in one_time_room:
                    final_choose_room = user_config["room_list"][up]
                    final_choose_time = self.chosen_list[final_choose_room - 3]["chosen_list"]
                    CHOOSE_FLAG = True
                    break

        return final_choose_room, final_choose_time