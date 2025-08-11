# Wei Dai's Personal Homepage

这是基于jemdoc模板构建的个人主页，部署在GitHub Pages上。

## 文件结构

- `*.jemdoc` - jemdoc源文件
- `*.html` - 生成的HTML文件
- `jemdoc.css` - 样式文件
- `simple_jemdoc.py` - jemdoc转换脚本
- `mysite.conf` - jemdoc配置文件
- `MENU` - 菜单配置文件

## 如何更新网站

1. 编辑相应的 `.jemdoc` 文件
2. 运行转换脚本：`python3 simple_jemdoc.py`
3. 提交更改到GitHub

## 部署到GitHub Pages

1. 创建名为 `WeiDaiATM.github.io` 的GitHub仓库
2. 将所有文件推送到仓库的main分支
3. 在仓库设置中启用GitHub Pages，选择main分支作为源

## 自定义内容

请根据你的实际情况修改以下内容：

- `index.jemdoc` - 个人信息、教育背景、研究兴趣等
- `research.jemdoc` - 研究项目和方向
- `publications.jemdoc` - 发表的论文和著作
- `teaching.jemdoc` - 教学经历
- `contact.jemdoc` - 联系方式
- 添加你的个人照片，命名为 `photo.jpg`

## 注意事项

- 确保所有链接和邮箱地址都是正确的
- 添加真实的个人照片替换占位符
- 根据需要调整CSS样式