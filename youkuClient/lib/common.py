
import os
import hashlib


# 发送消息到服务端


# 获取电影的md5值
def get_movie_md5(movie_path):

    md5 = hashlib.md5()
    # 获取文件大小
    movie_size = os.path.getsize(movie_path)

    # 拼接在文件大小的4个位置做记录，目的是为了在四个位置截取10个bytes的数据，
    # 减少内存的占用，并且可以保证视频文件的唯一性
    md5_list = [0, movie_size//3, (movie_size//3) * 2, movie_size-10]

    with open(movie_path, 'rb') as f:
        for line in md5_list:
            f.seek(line)
            data = f.read(10)
            md5.update(data)
    return md5.hexdigest()


# if __name__ == '__main__':
#     res = get_movie_md5(r'D:\上海Python11期视频\python11期视频\day47\youku_sys\youku_client\upload_movies\01 markdown语法.mp4')
#     print(res)