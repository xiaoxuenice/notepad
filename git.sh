版本库----->工作区----->暂存区---->提交版本库 github xiaoxuenice@qq.com xiaoxoeya.520
   add        添加文件内容至索引
   bisect     通过二分查找定位引入 bug 的变更
   branch     列出、创建或删除分支
   checkout   检出一个分支或路径到工作区
   clone      克隆一个版本库到一个新目录
   commit     记录变更到版本库
   diff       显示提交之间、提交和工作区之间等的差异
   fetch      从另外一个版本库下载对象和引用
   grep       输出和模式匹配的行
   init       创建一个空的 Git 版本库或重新初始化一个已存在的版本库
   log        显示提交日志
   merge      合并两个或更多开发历史
   mv         移动或重命名一个文件、目录或符号链接
   pull       获取并合并另外的版本库或一个本地分支
   push       更新远程引用和相关的对象
   rebase     本地提交转移至更新后的上游分支中
   reset      重置当前HEAD到指定状态
   rm         从工作区和索引中删除文件
   show       显示各种类型的对象
   status     显示工作区状态
   tag        创建、列出、删除或校验一个GPG签名的 tag 对象


git init				创建版本库，文件有个隐藏文件就是./git
git add	a.txt				添加文件到版本库
git commit -m 'this is first file'      !----文件提交到仓库-------!
git status				查看仓库现在状态
git diff a.txt				查看上次修改的文件a.txt
git log --pretty=oneline		版本历史
git rev-parse  HEAD			查看当前版本
git reset --hard HEAD^			回退上一个版本
git reflog				reset命令历史记录
git checkout -- a.txt			丢弃工作取得修改
git reset HEAD a.txt			暂存区的修改撤销，放回工作区
rm test.txt,git rm test.txt		删除文件
git checkout -- test.txt		删除文件恢复到最新版本
#############################################################################################
docker run -dit -p 2222:22 -p 8080:8080 -p80:80 -p 8443:443 --volume /home/gitlab/config:/etc/gitlab --volume /home/gitlab/logs:/var/log/gitlab --volume /home/gitlab/data:/var/opt/gitlab --restart always --name gitlab gitlab/gitlab-ce
vim /etc/gitlab/gitlab.rb --> external_url 'http://192.168.1.12'
docker exec  -it gitlab gitlab-ctl reconfigure
##############################################################################################
git clone  git@192.168.1.15:xiaoxue/python-project.git 				克隆到本地（一种方法）
git clone ssh://git@192.168.1.15:2222/python/python-project.git		        加ssh表示容器映射的端口是2222，非22要加ssh
git remote add origin git@192.168.1.15:xiaoxue/python-project.git               添加远程仓库到本地（二种方法）
git push -u origin master							推送到远程仓库
git pull -u origin master							下拉到本地仓库
git config --global credential.helper store 						保存用户名密码

git checkout -b dev			创建，切换到一个分支
git branch				查看当前分支
echo "add-file" >> a.txt
git add a.txt
git commot -m " branch test" 
git checkout master			分支上添加文本，提交之后，切换到master,此时master文件上不显示提交的内容
git merge dev 				把dev分支上的工作成果合并到master分支上
git branch -d dev 			合并完成之后就删除dev分支
master and dev ---》一起提交，冲突解决，cat a.txt，删除<<<<<======>>>>>，git add a.txt & git commit -m  'ok' & git merge dev
git log --graph				命令可以看到分支合并图。
git merge --no-ff -m "merge with no-ff" dev		准备合并dev分支，请注意--no-ff参数，表示禁用Fast forward：	
git log							合并分支时，加上--no-ff参数就可以用普通模式合并，合并后的历史有分支\
							能看出来曾经做过合并，而fast forward合并就看不出来曾经做过合并。

BUG分支>>>>>工作只进行到一半，还没法提交，预计完成还需1天时间。但是，必须在两个小时内修复该bug，怎么办？
git stash				把当前工作现场“储藏”起来，等以后恢复现场后继续工作：
git checkout master			首先确定要在哪个分支上修复bug，假定需要在master分支上修复，就从master创建临时分支：
git checkout -b issue-101
git checkout master			修复完成后，切换到master分支，并完成合并，最后删除issue-101分支：

git merge --no-ff -m "merged bug fix 101" issue-101
git checkout dev 			接着回到dev分支干活了！
git status  list			工作区是干净的，刚才的工作现场存到哪去了？用git stash list命令看看
git stash apply				1 恢复，但是恢复后，stash内容并不删除，你需要用git stash drop来删除；
git stash pop				2 恢复的同时把stash内容也删了
git stash list				查看，就看不到任何stash内容了
git stash apply stash@{0}		你可以多次stash，恢复的时候，先用git stash list查看，然后恢复指定的stash，用命令：


https://www.liaoxuefeng.com/wiki/896043488029600/900394246995648
https://www.cnblogs.com/chenfool/p/7689438.html
yum localinstall https://mirrors.tuna.tsinghua.edu.cn/gitlab-ce/yum/el7/gitlab-ce-10.0.3-ce.0.el7.x86_64.rpm





