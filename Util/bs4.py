import base64
import re
from io import BytesIO
from fontTools.ttLib import TTFont


def bs4_str(mystr, html_str):
    '''
    :param mystr: 要转码的字符串
    :param bs64_str:  转码格式
    :return: 转码后的字符串
    '''
    bs64_str = re.findall(r"charset=utf-8;base64,(.*?)'\)", html_str)[0]
    font = TTFont(BytesIO(base64.decodebytes(bs64_str.encode())))
    c = font['cmap'].tables[0].ttFont.tables['cmap'].tables[0].cmap
    ret_list = []
    for char in mystr:
        decode_num = ord(char)
        if decode_num in c:
            num = c[decode_num]
            num = int(num[-2:]) - 1
            ret_list.append(num)
        else:
            ret_list.append(char)
    ret_str_show = ''
    for num in ret_list:
        ret_str_show += str(num)
    return ret_str_show


if __name__ == '__main__':
    pass
