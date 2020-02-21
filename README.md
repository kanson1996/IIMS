# IIMS

库存信息管理系统

## 开发环境说明：

* 系统环境：Windows10（兼容小程序，后端及数据库环境也可使用（玩玩）Win10 linux子系统（WSL）Ubuntu18.04，由于镜像源的问题会有点闹心）

* 数据库：mysql 5.7.28

* 后端开发环境：基于Python 3.6.2，Flask 1.1.1（推荐使用virtualenv指定虚拟环境开发，方便类库和版本管理），虚拟环境创建完后使用以下命令导入类库依赖

  ```linux
  pip install -r requirement.txt
  ```

* 后端IDE：PyCharm

* 小程序开发环境：VS Code（coding）+微信开发者工具（debug）

  vscode安装并启用小程序开发扩展：wxml，wechat-snippet，minapp

  代码格式化扩展：Prettier - Code formatter

  远程窗口扩展：Remote - WSL

## 数据库、服务器使用说明：

* 数据库配置：见app/secure.py文件中SQLALCHEMY_DATABASE_URI配置项

* 静态资源服务：在images上级目录中开启8000端口（参考资料：[静态资源服务器（部署前端项目）](https://blog.csdn.net/weixin_43821273/article/details/90750242)），并获取当前IP，修改小程序app.js中imageCtx所对应的URL地址

* 静态资源上传商品:

  images目录初始内容：包含 轮播图、修改删除按钮、统一商品标识

  用户上传商品图片后保存到指定根目录images下 根目录配置参见IIMS 的app/web/product.py文件editorData方法

