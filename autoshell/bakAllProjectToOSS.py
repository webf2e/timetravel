import os, tarfile, datetime
import oss2,sys,shutil

now = datetime.datetime.now()
#项目所在的路径
projectPath = "/root/python_proj/"
#项目名称
projectName = "timetravel"
#备份文件存放路径
tarPath = "/root/"
#oss保存的最大备份数
maxBakCount = 4
#备份数据的shell
bakMysqlFileName = "{}timetravel.dump".format(projectPath)
bakMysqlShell = "/usr/bin/mysqldump -uroot -p1234asdf. timetravel > {}".format(bakMysqlFileName)
#需要备份的文件
bakFileMap={}
bakFileMap["/etc/nginx/nginx.conf"] = "nginx"
bakFileMap["/etc/nginx/conf.d/default.conf"] = "nginx"
#备份python依赖shell命令
pipShell = "pip3 list > {}pip_list.txt".format(projectPath)
staticPath = "/root/python_proj/timetravel/static"


def make_targz(output_filename, source_dir):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))

def percentage(consumed_bytes, total_bytes):
    if total_bytes:
        rate = int(100 * (float(consumed_bytes) / float(total_bytes)))
        print('\r{0}% '.format(rate), end='')
        sys.stdout.flush()

def delDir(path):
    if os.path.exists(path):
        ls = os.listdir(path)
        for i in ls:
            c_path = os.path.join(path, i)
            if os.path.isdir(c_path):
                delDir(c_path)
                if os.path.exists(c_path):
                    os.removedirs(c_path)
            else:
                if os.path.exists(c_path):
                    os.remove(c_path)

def clearStaticDownloadFiles():
    filePath = os.path.join(staticPath, "download")
    if os.path.exists(filePath):
        files = os.listdir(filePath)
        for file in files:
            os.remove(os.path.join(filePath, file))


#清理download文件
print("清理download文件夹")
clearStaticDownloadFiles()
#mysql备份数据库
print("备份mysql数据库")
os.system(bakMysqlShell)
#备份需要备份的文件
print("备份文件")
for p,d in bakFileMap.items():
    pp = os.path.join(projectPath,d)
    if not os.path.exists(pp):
        os.makedirs(pp)
    dst = os.path.join(pp,p[p.rfind("/") + 1:])
    print("文件{}拷贝到{}".format(p, dst))
    shutil.copyfile(p,dst)

#备份pip list
print("备份pip list")
os.system(pipShell)

tarFileName = "{}-{}.tar".format(projectName,now)
print("包名：{}".format(tarFileName))
absTarFileName = os.path.join(tarPath,tarFileName)
print("开始打包")
make_targz(absTarFileName,os.path.join(projectPath))
print("打包结束")

auth = oss2.Auth('LTAIOWHFyQYc3gQN', 'kkN3gdS3x32g4etD7lpYbNnpYZmlmr')
bucket = oss2.Bucket(auth, 'http://oss-cn-hongkong-internal.aliyuncs.com', 'timetravelbak')

#判断文件
fileInOss = []
for obj in oss2.ObjectIterator(bucket, delimiter = '/'):
    fileInOss.append(obj.key)

if len(fileInOss) > maxBakCount:
    print("需要清除oss上的文件")
    fileInOss.sort()
    file2RemoveList = fileInOss[:len(fileInOss) - maxBakCount]
    for removeFile in file2RemoveList:
        print("需要删除的文件：{}".format(removeFile))
        bucket.delete_object(removeFile)
print("清除oss上的文件结束")

oss2.resumable_upload(bucket, tarFileName, absTarFileName,progress_callback=percentage)
print("文件上传完成")

print("删除文件")
os.remove(absTarFileName)
os.remove(bakMysqlFileName)
os.remove("{}pip_list.txt".format(projectPath))
for p in bakFileMap.values():
    pp = os.path.join(projectPath,p)
    if os.path.exists(pp):
        delDir(pp)
        if os.path.exists(pp):
            os.removedirs(pp)
