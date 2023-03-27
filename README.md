# Tree - Website thương mại hóa mua bán cây cảnh

## Cài đặt môi trường

### Cài đặt Python
> Cũng có thể tự cài đặt Python 3.10 [ở đây](https://www.python.org/downloads/windows/)

Khuyến khích sử dụng công cụ quản lý phiên bản Python [pyenv-win](https://github.com/pyenv-win/pyenv-win)

Vì tôi không dùng Windows nên chắc ae tự đọc hướng dẫn cài đặt nhé

### Cài đặt phiên bản python 3.10.10 với pyenv-win

```bash
$ pyenv install 3.10.10
$ cd tree
$ pyenv local 3.10.10
$ python -V
Python 3.10.10
```

### Cài pipenv (vẫn đang ở trong thư mục tree nhé)

```bash
$ pip install --user pipenv
$ pipenv --version
pipenv, version 2023.3.20
```

Đồng thời cài đặt các thư viện cần thiết

```bash
$ pipenv install
```

