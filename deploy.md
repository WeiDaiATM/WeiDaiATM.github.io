# 部署到GitHub Pages的步骤

## 1. 创建GitHub仓库
1. 登录GitHub
2. 创建新仓库，命名为：`WeiDaiATM.github.io`
3. 设置为公开仓库
4. 不要初始化README、.gitignore或license

## 2. 连接本地仓库到GitHub
```bash
git remote add origin https://github.com/WeiDaiATM/WeiDaiATM.github.io.git
git branch -M main
git push -u origin main
```

## 3. 启用GitHub Pages
1. 进入仓库设置页面
2. 滚动到"Pages"部分
3. 在"Source"下选择"Deploy from a branch"
4. 选择"main"分支
5. 选择"/ (root)"文件夹
6. 点击"Save"

## 4. 访问你的网站
几分钟后，你的网站将在以下地址可用：
https://WeiDaiATM.github.io

## 5. 自定义内容
请记得：
- 替换个人信息（姓名、邮箱、大学等）
- 添加真实的个人照片（photo.jpg）
- 更新研究兴趣和项目
- 添加真实的发表论文
- 更新联系方式

## 6. 更新网站
每次修改内容后：
1. 编辑相应的.jemdoc文件
2. 运行：`python3 simple_jemdoc.py`
3. 提交更改：
   ```bash
   git add .
   git commit -m "Update content"
   git push