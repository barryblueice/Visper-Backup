# 只是一个垃圾的备份脚本

**现有功能：**

- 以天为单位进行备份
- WebUI Logger
- 基于7-Zip进行分卷压缩备份
- 对备份文件进行SHA256计算并定时检查，以保证备份文件不被修改

首次运行会生成.env文件：

```bash
SOURCE_PATH=/test
TARGET_PATH=/test_backup
TIME=5
WEBPORT=5555
```

内容解释：

项|备注|默认值|范例
:-:|:-:|:-:|:-:
SOURCE_PATH|需要被备份的源目录|/|Windows: `D:\test`</br>Linux: `/test`
TARGET_PATH|备份文件存放目录|/|Windows: `D:\backup`</br>Linux: `/backup`
TIME|备份保存份数（暂时以天为单位计算）|5|5
WEBPORT|WebUI Logger访问端口|5555|5555

WebUI Logger默认使用`Flask Jsonify`的形式返回。接口地址为`{ip}:{port}`.

对应接口如下：

接口|备注|范例
:-:|:-:|:-:
/|展示目前最新的Log文件|{ip}:5555
/log?param={date}|展示某一天的Log文件，日期格式为`YYYY-MM-DD`|{ip}:5555/log?param=2024-07-21
/hash?param={date}|展示某一天备份文件的相关Hash值，日期格式为`YYYY-MM-DD`|{ip}:5555/hash?param=2024-07-21
