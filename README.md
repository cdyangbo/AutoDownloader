# AutoDownloader
some python tool for download from bilibili.com or magnet link 

# download Bilibili.com video file:
## 1 get cookies:
(1) login bilibili.com，选择某一video
(2) 在浏览器按f12、ctrl+shift+I或“检查”，再按F5刷新
(3)选择network，找到h5_player_op?文件的Request Headers中的Cookie，复制下来

## 2 get mp4 urls
(1) #python bilibili_download.py -c ”上面找到的cookie“ -a avid 
(2) copy urls of avid_url.txt to thunder(迅雷） or other bittorrent downlad tools. 

