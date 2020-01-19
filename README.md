## 安装
### python3.6 安装
[python链接](https://www.python.org/)
##### 在 CentOS 7 中安装 Python 依赖
```bash
$ yum -y groupinstall development
$ yum -y install zlib-devel
$ yum install -y python3-devel openssl-devel libxslt-devel libxml2-devel libcurl-devel
```
##### 在 Debian 中，我们需要安装 gcc、make 和 zlib 压缩/解压缩库
```bash
$ aptitude -y install gcc make zlib1g-dev
```
##### 运行下面的命令来安装 Python 3.6：
```bash
$ wget https://www.python.org/ftp/python/3.6.3/Python-3.6.3.tar.xz
$ xz -d  Python-3.6.3.tar.xz
$ tar xvf Python-3.6.3.tar
$ cd Python-3.6.3/
$ ./configure
$ make && make install

# 查看安装
$ python3 -V
```

##### pip3安装
```bash
$ curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
$ python3 get-pip.py

# 查看安装
$ pip3 -V
```
##### SDK 安装
```bash
$ pip3 install -U git+git+https://github.com/yehecarry/yhops.git
```

## 结构
```shell
├── README.md    项目readme
└── yhopssdk
    ├── backup      备份模块
    ├── cloudsdk    公有云封装的一些方法
    ├── db          数据库连接方法
    └── operate     运维操作