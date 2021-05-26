# potato-bot

### 环境
框架：
[nonebot2](https://github.com/nonebot/nonebot2)

Python： 3.8.5

### 使用说明
- 修改.env配置
  
  `ENVIRONMENT=prod`
  
- 增加数据库配置
  `MONGODB_URI=mongodb://...`
  
- 若使用自己搭建的datacenter服务器，需要修改.env.prod
  
  `DATACENTER=http://xxxxx.com`
  
- 安装环境依赖

  `pip install -r requirements.txt`
- 启动
  
  `python bot.py`

###### 详细配置说明请看框架文档
### 模块说明
laisha2 -- 莱莎2
jx3 -- 剑网三