# Tree

## Cài đặt môi trường

### Cài đặt WSL 2 hoặc Dual Boot
> Nếu bạn chưa cài đặt WSL 2 hoặc Dual Boot, hãy làm theo hướng dẫn [ở đây](https://docs.microsoft.com/en-us/windows/wsl/install-win10)

### Cài đặt Vscode để kết nối với WSL
> Cài đặt Vscode [ở đây](https://code.visualstudio.com/download)

> Hướng dẫn sử dụng Vscode và WSL [ở đây](https://code.visualstudio.com/docs/remote/wsl)

### Cài đặt Python
Cài đặt Python 3.10 (bắt buộc) và thêm vào PATH. Kiểm tra
```bash
$ python --version
Python 3.10.10
```
Clone project về máy và cài đặt các thư viện cần thiết

```bash
$ git clone https://github.com/ppvan/tree.git
$ cd tree
```

Tạo môi trường ảo Python
```bash
$ python -m venv venv
```

Kích hoạt môi trường ảo
> Windows
```bash
$ venv\Scripts\activate
```
> Linux
```bash
$ source venv/bin/activate
```

Cài đặt các thư viện
```bash
$ pip install -r requirements.txt
```

Chạy server
```bash
$ python manage.py runserver
```

Khi dev frontend, mở thêm 1 terminal để chạy tailwind (cần cài sẵn nodejs)

```bash
$ cd tailwind/
$ npm run dev
```

Để vscode nhận diện thư viện nhằm hỗ trợ auto complete, format code, ...
Tổ hợp phím `Ctrl + Shift + P` và gõ `Python: Select Interpreter` chọn `venv` trong thư mục project

## Cách dùng git
- Chỉ làm việc trên branch của mình
- Tạo pull request để merge code vào branch `main`
- Trước khi code bất kì thứ gì, hãy pull code mới nhất về

## Tip django
[CONTRIBUTE.md](https://github.com/ppvan/tree/blob/main/CONTRIBUTE.md)

## Tiêu chuẩn code
- Luôn đặt tên biến, hàm dạng `snake_case`, tên class dạng `CamelCase`
- Hạn chế comment nhưng cần viết Docsstring cho các hàm, class
- Sử dụng VScode + flake8 + autopep8 để format code