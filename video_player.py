import os
import time


# 定义播放器类
class VideoPlayer:
    # 初始化
    def __init__(self):
        self.video_list = []
        self.video_index = 0
        self.video_name = ''
        self.video_path = ''
        self.video_time = 0
        self.video_status = False
        self.video_total_time = 0
        self.video_play_time = 0
        self.video_play_speed = 1

    # 打开视频
    def open_video(self, video_path):
        if os.path.exists(video_path):
            self.video_path = video_path
            self.video_name = os.path.basename(video_path)
            self.video_status = True
            self.video_total_time = self.get_video_time()
            print('视频已打开：', self.video_name)
        else:
            print('视频不存在！')

    # 获取视频时长
    def get_video_time(self):
        # 这里可以使用ffmpeg等工具获取视频时长
        return 10

    # 播放视频
    def play_video(self):
        if self.video_status:
            print('开始播放：', self.video_name)
            while self.video_play_time < self.video_total_time:
                time.sleep(1)
                self.video_play_time += 1
                print('播放进度：', self.video_play_time, '/', self.video_total_time)
            print('播放完成：', self.video_name)
        else:
            print('请先打开视频！')

    # 暂停播放
    def pause_video(self):
        if self.video_status:
            print('暂停播放：', self.video_name)
            self.video_status = False
        else:
            print('视频未播放！')

    # 继续播放
    def continue_video(self):
        if self.video_status:
            print('视频正在播放！')
        else:
            print('继续播放：', self.video_name)
            self.video_status = True
            self.play_video()

    # 停止播放
    def stop_video(self):
        if self.video_status:
            print('停止播放：', self.video_name)
            self.video_status = False
            self.video_play_time = 0
        else:
            print('视频未播放！')

    # 调整播放速度
    def set_play_speed(self, speed):
        self.video_play_speed = speed
        print('调整播放速度：', speed)


# 使用
if __name__ == '__main__':
    # 创建播放器
    player = VideoPlayer()
    # 打开视频
    player.open_video('test.mp4')
    # 播放视频
    player.play_video()
    # 暂停播放
    player.pause_video()
    # 继续播放
    player.continue_video()
    # 停止播放
    player.stop_video()
    # 调整播放速度
    player.set_play_speed(2)