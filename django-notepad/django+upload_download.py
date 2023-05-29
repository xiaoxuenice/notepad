def upload_file(request): 
    backup_dirpath="/data/django-opsweb/backup/"
    try:
        if request.method == "POST":    # 请求方法为POST时，进行处理
            stime=time.time()
            backupfile =request.FILES.get("filename", None)    # 获取上传的文件，如果没有文件，则默认为None
            if not backupfile:
                return HttpResponse("没有参数 filename !!")
            if 'opsweb' not in backupfile.name:
                return HttpResponse(f"{backupfile} 不是opsweb的备份文件 !!")
            if not os.path.isdir(backup_dirpath):
                os.mkdir(backup_dirpath)
            destination = open(backup_dirpath+backupfile.name,'wb+')    # 打开特定的文件进行二进制的写操作
            for chunk in backupfile.chunks():      # 分块写入文件
                destination.write(chunk)
            destination.close()

            # 打包成tar格式
            taring = tarfile.open(os.path.join(backup_dirpath,"django-opsweb_"+time.strftime("%F_%Hh_%Mm",time.localtime(time.time()))+".tar.gz"), "w:gz")
            os.chdir(backup_dirpath)
            taring.add(backupfile.name)
            taring.close()
            os.remove(os.path.join(backup_dirpath,backupfile.name))

            # 只保留上传的十个备份文件
            allbackup=sorted(os.listdir(backup_dirpath),key=lambda x: os.path.getmtime(os.path.join(backup_dirpath,x)))
            for i in range(len(os.listdir(backup_dirpath)) - 20):
                os.remove(os.path.join(backup_dirpath,allbackup[i]))

            dtime=time.time()
            alltime=dtime-stime
            return HttpResponse(f"{backupfile.name} 上传完成,耗时 {str(alltime)} ")
    except Exception as err:
        return HttpResponse(str(err),status=200)
def download_file(request):
    backup_dirpath = "/data/django-opsweb/backup/"
    if request.session.get("login", None):
        pass
    elif request.method == "POST":
        mess = json.loads(request.body)
        _user=mess.get('user',None)
        _passwd=mess.get('token',None)
        hashwd = username.objects.get(username=_user).password
        if not hashpd(_passwd, hashwd):
            return HttpResponse("token 错误")
    else:
        return JsonResponse({"msg": "403 非法请求  SESSION过期", "code": 5001})

    #docker备份 opsweb 数据库
    backupfile = time.strftime("%F_%Hh_%Mm",time.localtime(time.time()))+'_opsweb.sql'
    os.system(f'docker exec  mysql8.0  bash -c "mysqldump  -uroot -proot --databases opsweb"  >  {os.path.join(backup_dirpath,backupfile)}')

    # 打包成tar格式
    taring = tarfile.open(os.path.join(backup_dirpath, "django-opsweb_" + time.strftime("%F_%Hh_%Mm", time.localtime(
        time.time())) + ".tar.gz"), "w:gz")
    os.chdir(backup_dirpath)
    taring.add(backupfile)
    taring.close()
    os.remove(os.path.join(backup_dirpath, backupfile))

    # 本地只保留上传的20个备份文件
    allbackup = sorted(os.listdir(backup_dirpath), key=lambda x: os.path.getmtime(os.path.join(backup_dirpath, x)))
    for i in range(len(os.listdir(backup_dirpath)) - 20):
        os.remove(os.path.join(backup_dirpath, allbackup[i]))

    #返回最新opsweb备份文件
    backup_filename=sorted(os.listdir(backup_dirpath),key=lambda x: os.path.getmtime(os.path.join(backup_dirpath,x)))[-1]
    down_file = open(os.path.join(backup_dirpath,backup_filename), 'rb')
    response = FileResponse(down_file, filename=backup_filename, as_attachment=True)
    response['Content-Type'] = 'application/octet-stream'
    return response

