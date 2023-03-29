# Tree - Website thương mại hóa mua bán cây cảnh

## Cài đặt môi trường

### Cài đặt Python
> Cũng có thể tự cài đặt Python 3.10 [ở đây](https://www.python.org/downloads/windows/)

Khuyến khích sử dụng công cụ quản lý phiên bản Python [pyenv-win](https://github.com/pyenv-win/pyenv-win)

Vì tôi không dùng Windows nên chắc ae tự đọc hướng dẫn cài đặt nhé

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

> Những công cụ hơi phức tạp này giải quyết 1 số vấn đề trong lập trình và tăng tính chuyên nghiệp :v

## Cách dùng git
- Gửi mail cho tôi để được thêm vào repo
- Tạo 1 branch mới với tên là tên của bạn (tạo nickname đi, của tôi là ppvan, btw)
- Làm việc trên branch đó, khi có thay đổi tạo pull request (tôi là người phê duyệt), đây là kĩ năng cơ bản nhưng nếu k rõ hôm nào họp t chỉ cho ae

## Tip django
[CONTRIBUTE.md](https://github.com/ppvan/tree/blob/main/CONTRIBUTE.md)

## Tiêu chuẩn code
- Luôn đặt tên biến, hàm dạng `snake_case`
- Hạn chế comment, nếu bạn phải comment để giải thích, nghĩa là code chưa đủ tốt
- Tham khảo [Zen of Python](https://github.com/zedr/clean-code-python) cái này rất phức tạp, đọc sơ qua thôi