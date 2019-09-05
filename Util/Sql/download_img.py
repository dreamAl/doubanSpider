import requests
import json

with open('a.json', 'rb') as f:
    data_info = json.loads(f.read())

# film_imgs = []
# for img in data_info[100:110]:
#     film_imgs.append({'film_name':img['film_name'],'film_img': img['film_img']})
# print(film_imgs)
# for film_img in film_imgs:
#     response = requests.get(film_img['film_img'])
#     with open("img/" + film_img['film_name'] + '.jpg', 'wb') as f:
#         f.write(response.content)

# import os
# base_dir = os.path.join(os.getcwd(), 'img')
# img_info = []
# for name in os.listdir(base_dir):
#     if 'E.T. 外星人 E.T.' == name:
#         continue
#     img_info.append(name.replace(".jpg", ''))
# # print(img_info)
# # print(len(img_info))
# result = []
# for items in data_info:
#     if items['film_name'] not in img_info:
#         continue
#     for item in img_info:
#         if items['film_name'] == item:
#             items['film_img'] = os.path.join(base_dir, item+'.jpg')
#     result.append(items)
#
# with open('douban.json', 'wb') as f:
#     f.write(json.dumps(result, ensure_ascii=False).encode())

with open('douban.json', 'rb') as f:
    data = json.loads(f.read())
#
print(len(data))
