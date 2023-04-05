# Tree - Website thương mại hóa mua bán cây cảnh

## Cài đặt môi trường

### Cài đặt Python
> Cũng có thể tự cài đặt Python 3.10 (và pip) [ở đây](https://www.python.org/downloads/windows/)

Khuyến khích sử dụng công cụ quản lý phiên bản Python [pyenv-win](https://github.com/pyenv-win/pyenv-win) và [pipenv](https://pipenv.pypa.io/en/latest/) (quản lý môi trường phát triển + dependency)


### Cài đặt phiên bản python 3.10.10 với pyenv-win

```bash
$ pyenv install 3.10.10
$ pyenv version
Python 3.10.10 (tức là đang chịu sự quản lý của pyenv-win)
```

### Cài pipenv

```bash
$ pip install --user pipenv
$ pipenv --version
pipenv, version 2023.3.20
```

Clone project về máy và cài đặt các thư viện cần thiết

```bash
$ git clone https://github.com/ppvan/tree.git
$ cd tree
$ pipenv install
$ pipenv shell
(tree)$ python manage.py runserver
```

Truy cập [localhost](http://localhost:8000/), nếu thấy hình tên lửa = thành công.


### Tham khảo tài liệu các công cụ
- [pipenv](https://pipenv.pypa.io/en/latest/)
- [pyenv-win](https://github.com/pyenv-win/pyenv-win)

> Những công cụ này giải quyết vấn đề về môi trường phát triển, ví dụ như dependency, phiên bản python, cô lập môi trường phát triển giữa các dự án.

## Cách dùng git
- Chỉ làm việc trên branch của mình
- Tạo pull request để merge code vào branch `main`

## Tip django
[CONTRIBUTE.md](https://github.com/ppvan/tree/blob/main/CONTRIBUTE.md)

## Tiêu chuẩn code
- Luôn đặt tên biến, hàm dạng `snake_case`
- Hạn chế comment, nếu bạn phải comment để giải thích, nghĩa là code chưa đủ tốt
- Sử dụng VScode + flake8 + autopep8 để format code
- Tham khảo [Zen of Python](https://github.com/zedr/clean-code-python) cái này rất phức tạp, đọc sơ qua thôi