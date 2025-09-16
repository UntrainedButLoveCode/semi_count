#
# import os
# import numpy as np
# import skimage.io
# import json
# import scipy.io
# # len(os.listdir('part_A/test_data/images/'))
#
#
# def crop_gen(img, points):
#     rn = np.random.choice(4, size=1, replace=True, p=None)[0]
#     tar = np.zeros([img.shape[0], img.shape[1]])
#     for co in range(len(points)):
#         if (np.rint(points[co,1]).astype(int) < img.shape[0]) and (np.rint(points[co,0]).astype(int) < img.shape[1]):
#             tar[  np.rint(points[co,1]).astype(int), np.rint(points[co,0]).astype(int)] = 1
#         else:
#             tar[  points[co,1].astype(int), points[co,0].astype(int)] = 1
#
#     if rn == 0:
#         temp_img = img[:img.shape[0]//512 * 512, :img.shape[1]//512 * 512]
#         temp_tar = tar[:img.shape[0]//512 * 512, :img.shape[1]//512 * 512]
#     elif rn == 1:
#         temp_img = img[-(img.shape[0]//512 * 512):, :img.shape[1]//512 * 512]
#         temp_tar = tar[-(img.shape[0]//512 * 512):, :img.shape[1]//512 * 512]
#     elif rn == 2:
#         temp_img = img[:img.shape[0]//512 * 512, -(img.shape[1]//512 * 512):]
#         temp_tar = tar[:img.shape[0]//512 * 512, -(img.shape[1]//512 * 512):]
#     elif rn == 3:
#         temp_img = img[-(img.shape[0]//512 * 512):, -(img.shape[1]//512 * 512):]
#         temp_tar = tar[-(img.shape[0]//512 * 512):, -(img.shape[1]//512 * 512):]
#
#
#     crop_tar = []
#     crop_list = []
#     for x in range(temp_img.shape[0]//512):
#         for y in range(temp_img.shape[1]//512):
#             crop_list.append(temp_img[x*512:(x*512+512), y*512:(y*512+512)])
#             crop_tar.append( temp_tar[x*512:(x*512+512), y*512:(y*512+512)] )
#
#     # for x in range(img.shape[0]//512):
#     #     crop_list.append( img[x*512:(x*512+512), (img.shape[1] - 512):img.shape[1]] )
#     # crop_list.append( img[(img.shape[0] - 512):img.shape[0], (img.shape[1] - 512):img.shape[1]] )
#
#     # for y in range(img.shape[1]//512):
#     #     crop_list.append( img[ (img.shape[0] - 512):img.shape[0], y*512:(y*512+512)] )
#     return crop_list, crop_tar
# # crop_list.append( img[(img.shape[0] - 512):img.shape[0], (img.shape[1] - 512):img.shape[1]] )
#
# imglist = os.listdir('low/train_data/images/')
# shape_list = []
# for i in range(len(imglist)):
#     try:
#         img = skimage.io.imread('low/train_data/images/' + imglist[i])
#         # mat = scipy.io.loadmat('low/train_data/ground-truth/' + 'GT_' + imglist[i].split('.jpg')[0] + '.mat')
#         json_path = ('low/train_data/images/' + imglist[i]).replace('.jpg', '.json').replace('images','ground_truth')
#         # json_path = im_path.replace('.jpg', '.json')
#         with open(json_path, 'r') as f:
#             mat = json.load(f)
#         points = []
#         for item in mat['shapes']:
#             # print(item)
#             points.extend(item['points'])
#         ppp = np.array(points)
#
#         # ppp = mat['image_info'][0][0][0][0][0]
#         c_list = crop_gen(img, ppp)
#
#         for nk in range(len(c_list[0])):
#             skimage.io.imsave( 'low/uncertain_data/'  + imglist[i].split('.jpg')[0] + '_' + str(nk) + '.png',   c_list[0][nk] )
#             # 保存标签patch - 修复这里！
#             label_patch = c_list[1][nk]
#             # 方法1: 转换为uint8 (0-255)
#             if label_patch.dtype == np.float32 or label_patch.dtype == np.float64:
#                 # 如果值是0-1范围的浮点数，转换为0-255
#                 if np.max(label_patch) <= 1.0:
#                     label_patch_uint8 = (label_patch * 255).astype(np.uint8)
#                 else:
#                     label_patch_uint8 = label_patch.astype(np.uint8)
#             else:
#                 label_patch_uint8 = label_patch.astype(np.uint8)
#
#             # 确保是2D数组，如果不是则转换为2D
#             if len(label_patch_uint8.shape) > 2:
#                 label_patch_uint8 = label_patch_uint8[:, :, 0]
#
#             skimage.io.imsave('low/uncertain_label/' + imglist[i].split('.jpg')[0] + '_' + str(nk) + '_label.png',
#                               label_patch_uint8)
#     except Exception as e:
#         print(f"Error processing {imglist[i]}: {str(e)}")
#         continue
#         # skimage.io.imsave( 'low/uncertain_label/'  + imglist[i].split('.jpg')[0] + '_' + str(nk) + '_label.png', c_list[1][nk] )
import os
import numpy as np
import skimage.io
import json
import scipy.io


def crop_gen(img, points):
    rn = np.random.choice(4, size=1, replace=True, p=None)[0]
    tar = np.zeros([img.shape[0], img.shape[1]])

    for co in range(len(points)):
        x = points[co, 0]
        y = points[co, 1]

        # 更安全的坐标处理方式
        x_int = int(np.floor(x))  # 向下取整，避免超出
        y_int = int(np.floor(y))

        # 或者使用钳制函数确保在范围内
        x_int = np.clip(int(np.rint(x)), 0, img.shape[1] - 1)
        y_int = np.clip(int(np.rint(y)), 0, img.shape[0] - 1)

        tar[y_int, x_int] = 1

    # 裁剪逻辑保持不变
    if rn == 0:
        temp_img = img[:img.shape[0] // 128 * 128, :img.shape[1] // 128 * 128]
        temp_tar = tar[:img.shape[0] // 128 * 128, :img.shape[1] // 128 * 128]
    elif rn == 1:
        temp_img = img[-(img.shape[0] // 128 * 128):, :img.shape[1] // 128 * 128]
        temp_tar = tar[-(img.shape[0] // 128 * 128):, :img.shape[1] // 128 * 128]
    elif rn == 2:
        temp_img = img[:img.shape[0] // 128 * 128, -(img.shape[1] // 128 * 128):]
        temp_tar = tar[:img.shape[0] // 128 * 128, -(img.shape[1] // 128 * 128):]
    elif rn == 3:
        temp_img = img[-(img.shape[0] // 128 * 128):, -(img.shape[1] // 128 * 128):]
        temp_tar = tar[-(img.shape[0] // 128 * 128):, -(img.shape[1] // 128 * 128):]

    crop_tar = []
    crop_list = []
    for x in range(temp_img.shape[0] // 128):
        for y in range(temp_img.shape[1] // 128):
            crop_list.append(temp_img[x * 128:(x * 128 + 128), y * 128:(y * 128 + 128)])
            crop_tar.append(temp_tar[x * 128:(x * 128 + 128), y * 128:(y * 128 + 128)])

    return crop_list, crop_tar


# 主循环
imglist = os.listdir('high/train_data/images/')
shape_list = []

# 创建输出目录
os.makedirs('high/uncertain_data', exist_ok=True)
os.makedirs('high/uncertain_label', exist_ok=True)

for i in range(len(imglist)):
    try:
        img_path = 'high/train_data/images/' + imglist[i]
        img = skimage.io.imread(img_path)
        print(f"处理: {imglist[i]}, 尺寸: {img.shape}")

        # 加载JSON标注
        json_path = img_path.replace('.jpg', '.json').replace('images', 'ground_truth')
        with open(json_path, 'r') as f:
            mat = json.load(f)

        points = []
        for item in mat['shapes']:
            points.extend(item['points'])

        ppp = np.array(points)
        print(f"  找到 {len(ppp)} 个标注点")

        c_list = crop_gen(img, ppp)

        for nk in range(len(c_list[0])):
            # 保存图像patch
            skimage.io.imsave('high/uncertain_data/' + imglist[i].split('.jpg')[0] + '_' + str(nk) + '.png',
                              c_list[0][nk])

            # 处理标签patch
            label_patch = c_list[1][nk]
            if label_patch.dtype in [np.float32, np.float64]:
                label_patch_uint8 = (label_patch * 255).astype(np.uint8)
            else:
                label_patch_uint8 = label_patch.astype(np.uint8)

            if len(label_patch_uint8.shape) > 2:
                label_patch_uint8 = label_patch_uint8[:, :, 0]

            skimage.io.imsave('high/uncertain_label/' + imglist[i].split('.jpg')[0] + '_' + str(nk) + '_label.png',
                              label_patch_uint8)

    except Exception as e:
        print(f"错误处理 {imglist[i]}: {str(e)}")
        import traceback

        traceback.print_exc()
        continue