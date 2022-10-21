# coding=utf-8
# @Time : 2022/10/21 13:31 PM
# @Author : 王思哲
# @File : choose_room.py
# @Software: PyCharm

import pandas as pd
import numpy as np

room_time_header  = ["8-9", "9-10", "10-11", "11-12", "12-13", "13-14", "14-15", "15-16", "16-17", "17-18", "18-19", "19-20", "20-21"]

class ChooseRoom:
    def __init__(self):
        self.data = pd.read_csv('./test_data.csv')
        self.dp = self.get_dp()

    def get_dp(self):
        time_data = self.data.values.tolist()
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
            print(dp)
            dp_all.append(dp)

        return dp_all

    def get_result(self):
        '''
        返回：一个数和一个list --- 教室NUMBER, 选择哪几个下标[list]
        :return:
        '''
        for room in self.dp:
            max_idx = np.argmax(room)
            max_num = room[max_idx]
            print(room_time_header[max_idx-max_num+1 : max_idx+1])
            print(max_idx)



if __name__ == "__main__":
    a = ChooseRoom()
    a.get_result()