import requests
import os

from urllib.parse import urlencode
from hashlib import md5
from multiprocessing.pool import Pool


def get_page(offset):
    '''
    获取源码
    :param offset:
    :return:
    '''
    params = {
        'offset': offset,
        'format': 'json',
        'keyword': '街拍',
        'autoload': 'true',
        'count': '20',
        'cur_tab': '1',
        'from': 'search_tab',
    }
    base_url = 'https://www.toutiao.com/search_content/?'
    url = base_url + urlencode(params)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError as e:
        print(e.args)
        return None

def get_images(json):
    '''
    解析源码
    :param json:
    :return:
    '''
    if json.get('data'):
        for item in json.get('data'):
            if item.get('cell_type') is not None:
                continue
            title = item.get('title')
            images = item.get('image_list')
            for image in images:
                yield {
                    'image':'https' + image.get('url'),
                    'title':title
                }

def save_image(item):
    '''
    保存图片
    :param item:
    :return:
    '''
    # 创建文件夹
    img_path = 'img' + os.path.sep + item.get('title')
    if not os.path.exists(img_path):
        os.makedirs(img_path)

    try:
        response = requests.get(item.get('image'))
        if response.status_code == 200:
            file_path = img_path + os.path.sep + '{file_name}.{file_suffix}'.format(
                file_name = md5(response.content).hexdigest(),
                file_suffix = 'jpg'
            )
            if not os.path.exists(file_path):
                with open(file_path, "wb") as f:
                    f.write(response.content)
                    print("图片下载成功！")
            else:
                print("图片已经下载了，无需再下载！", file_path)
    except requests.ConnectionError:
        print('图片下载失败')
