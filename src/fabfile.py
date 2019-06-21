from fabric import Connection
from invoke import Responder
from fabric import util

print(util.get_local_user())
c = Connection('spark@master', connect_kwargs={"password": "123456"})
result = c.run('uname -s')
# 类似expect
sudopass = Responder(pattern=r'\[sudo\] password for spark', response='123456\n', )
result = c.run('sudo ls', pty=True, watchers=[sudopass])
print(result.ok)
# 执行本地命令
c.local("dir /w")
c.close()

import getpass
from fabric import Config

# sudo_pass = getpass.getpass("What's your sudo password?")
config = Config(overrides={'sudo': {'password': "123456"}})
c = Connection('spark@master', connect_kwargs={"password": "123456"}, config=config)
c.sudo('whoami', hide='stderr')

# 传送文件
result = c.put('fabfile.py', remote='/home/spark')
print("Uploaded {0.local} to {0.remote}".format(result))

# 多服务器执行
from fabric import SerialGroup as Group

group = Group('spark@master', connect_kwargs={"password": "123456"})
for c in group:
    result = c.run('uname -s', warn=True)
    print(result)

# 远程服务器，使用私钥登录
c = Connection('yyi@yyifamily.tk', connect_kwargs={"key_filename": "F:\download\my-ssh-key"})
result = c.run('uname -s')

# 执行本地命令,hide隐藏标准输出
from invoke import run
#import  invoke

result = run('dir /w', hide=True, warn=True)
if (result.ok):
    print("result:{0},out:{1}".format(result.ok, result.stdout))
else:
    print("result:{0},out:{1}".format(result.ok, result.stderr))

from fabric import task


@task
def upload_and_unpack(c):
    if c.run('test -f /opt/mydata/myfile', warn=True).failed:
        c.put('myfiles.tgz', '/opt/mydata')
        c.run('tar -C /opt/mydata -xzvf /opt/mydata/myfiles.tgz')
