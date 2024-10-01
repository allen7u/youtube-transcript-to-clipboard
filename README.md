# youtube-transcript-to-clipboard
YouTube URL > subtitle.txt > Clipboard

建议搭配以下 Quicker 脚本使用

https://getquicker.net/Sharedaction?code=9bf14774-f55d-469f-2e7d-08dce1d6121b

### 配置：

1，下载该 repository 到合适的路径并安装依赖

2，导入 Quicker 动作的分享链接（默认在 Chrome 窗口下生效）

3，修改该动作以指向步骤一中的路径
![image](https://github.com/user-attachments/assets/130760bb-d56c-43d3-9a74-b8763415736c)
![image](https://github.com/user-attachments/assets/7d983036-2960-4e8a-893a-828dfc69ec63)

### 使用：

1，从 YouTube 搜索结果或相关推荐中“复制链接地址”

2，呼出 Quicker 插件（如单击 Ctrl），点击导入的动作

3，在 ChatGPT 等工具的输入框中 Ctrl + V

### 原理：

https://github.com/jdepoix/youtube-transcript-api 会下载剪贴板中 URL 对应 Youtube 视频的字幕，将其保存为一个 txt 文件，然后复制该文件到剪贴板
