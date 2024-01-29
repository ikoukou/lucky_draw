from utils.num_trans import arabic_to_chinese


envir_config = {
    # 按钮和中奖名单的字体大小
    "font_size_button": 20,
    "font_size_target": 20,

    # 中奖名单的大小
    "target_persons_width": 150,
    # "target_persons_height": 200,

    # 抽奖按钮的大小
    "award_button_width": 300,
    "award_button_height": 70,

    # 奖品弹窗中奖品图片的大小
    "award_image_width": 200,
    "award_image_height": 200,

    # 背景图片路径
    "image_background": "static/33.png",

    # 抽奖名单路径
    "list_people": "年会参与抽奖人员清单.xlsx",

    # """
    # 奖项配置，字典数组：
    #     id: 奖品等级，严格递增
    #     count: 该等级奖项总个数
    #     awards_list: 子奖项，字典数组
    #         award_name: 该子奖项奖品名称，最好15个字符之内
    #         count: 该子奖项个数
    #         image: 该子奖项图片
    # """
    "awards_tuple": [
        {
            "id": 1,
            "count": 1,
            "awards_list": [
                {
                    "name": "苹果 iPhone15 128G 黑色",
                    "image": "static/phone.png",
                    "count": 1
                }
            ]
        },
        {
            "id": 2,
            "count": 2,
            "awards_list": [
                {
                    "name": "华为 WATCH GT4 曜石黑",
                    "image": "static/phone.png",
                    "count": 2
                }
            ]
        },
        {
            "id": 3,
            "count": 5*2,
            "awards_list": [
                {
                    "name": "小天才儿童电话手表Q1R 蓝色",
                    "image": "static/phone.png",
                    "count": 5
                },
                {
                    "name": "Rigal B1 投影仪",
                    "image": "static/phone.png",
                    "count": 5
                }
            ]
        },
        {
            "id": 4,
            "count": 5*2,
            "awards_list": [
                {
                    "name": "飞科剃须刀 FS903 礼盒装",
                    "image": "static/phone.png",
                    "count": 5
                },
                {
                    "name": "航世 HB318 蓝牙键盘",
                    "image": "static/phone.png",
                    "count": 5
                }
            ]
        },
        {
            "id": 5,
            "count": 5*3,
            "awards_list": [
                {
                    "name": "祥业 米黄汝窑功夫茶具套装",
                    "image": "static/phone.png",
                    "count": 5
                },
                {
                    "name": "米家保温壶 1.8L",
                    "image": "static/phone.png",
                    "count": 5
                },
                {
                    "name": "索爱 SL6真无线蓝牙耳机 油彩白",
                    "image": "static/phone.png",
                    "count": 5
                },
            ]
        },
    ]

}
