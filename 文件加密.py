import threading
from os import system as cmd
from pathlib import Path as Ph
from os.path import split as sp
from hashlib import sha256 as sha
from os.path import splitext as st
from json import dumps as ds, loads as ls


def read_file(mode: bool):
    while True:  # 循环直到成功读取了文件内容
        path_ = input("输入文件路径：")
        if exists(path_):  # 如果输入的路径存在并且是一个文件
            try:
                with open(path_, "rb") as file_obj_:
                    if mode:
                        return [file_obj_.read(), st(path_)[-1], path_]
                    else:
                        return [ls(file_obj_.read()), st(path_)[-1], path_]
            except:
                print("读取文件失败 :(")
                print("请检查文件是否损坏")
                print()
                continue  # 重新循环
        else:
            print("请输入一个文件的路径（不带引号）:(")
            print()
            continue


def encryption(bytes_: list, path: str):
    while True:  # 输入密码
        passwd1 = input("\r请输入用于加密文件的密码（请确保无人看见）：")
        passwd2 = input("请再输入一遍：")
        if passwd1 == passwd2:
            cmd("cls")
            break
        else:
            print("输入不一致！")

    passwd = list(bytearray(sha(passwd1.encode("utf-8")).hexdigest().encode()))
    del passwd1, passwd2
    long = len(passwd)
    b_long = len(bytes_)
    text = {"file": []}

    cmd("cls")
    print(f"开始加密 {sp(path)[-1]}...")
    last_ = 0
    for i in range(b_long):
        text["file"].append(passwd[i % long] + bytes_[i])

        n_ = round(i / b_long * 100, 1)
        ts = int((i / b_long) * 50)
        if last_ != n_:
            progress = f"""\r{ts * "#" + (50 - ts) * " "}| 已完成 {n_}%"""
            print(progress, end="")
            last_ = n_

    cmd("cls")
    return text


def decryption(bytes_: list, passwd: list, path: str):
    long = len(passwd)
    b_long = len(bytes_)
    print(f"开始解密 {sp(path)[-1]}...")

    class MyThread(threading.Thread):
        def __init__(self, bytes__):
            super(MyThread, self).__init__()
            self.bytes__ = bytes__
            self.text = b""

        def run(self):
            try:
                for q in range(len(self.bytes__)):
                    self.text += int.to_bytes(self.bytes__[q] - passwd[q % long], byteorder="little", length=1)
            except:
                print("出了点错误 :(")
                print("请检查文件是否损坏")
                print()
                return

        def get_result(self):
            return self.text

    threads = []
    yu = b_long % long
    l_index = 0
    if yu:
        num = b_long // 64000 + 1
    else:
        num = b_long // 64000
    for i in range(num - 1):
        thread = MyThread(bytes_[i * 64000:(i + 1) * 64000])
        thread.start()
        threads.append(thread)
        l_index = (i + 1) * 64000
    thread = MyThread(bytes_[l_index:])
    thread.start()
    threads.append(thread)
    for thread in threads:
        thread.join()

    ttt = b""
    for thread in threads:
        ttt += thread.get_result()
    cmd("cls")
    del threads
    return ttt


def exists(path_):
    file__ = Ph(path_)
    if file__.is_file() and file__.exists():
        return True
    else:
        return False


if __name__ == "__main__":
    while True:  # 开始主循环
        try:
            ed = input("加密（输入“e”）或 解密（输入“d”）？：")
            if ed == "e":
                returns = read_file(True)
                file = bytearray(returns[0])
                suffix = returns[1]
                encrypted_text = encryption(list(file), returns[2])

                print(f"""\r开始保存...{" " * 80}""", end="")

                n = 0
                while exists(f"encrypted_{n}{suffix}") or exists(f"key_{n}.txt"):
                    n += 1  # 循环直到找到不存在的文件名，以免覆盖其他文件

                with open(f"encrypted_{n}{suffix}", "w") as file_obj:
                    file_obj.write(ds(encrypted_text))

                print(f"\r{sp(returns[2])[-1]} 加密完成 :)")
                print(f"| 加密后文件已保存至当前目录下的 encrypted_{n}{suffix}")
                print("| 请妥善保存这个文件！")
                print()
            elif ed == "d":
                returns = read_file(False)
                file = returns[0]["file"]
                suffix = returns[1]

                passwd_ = input("\r请输入加密时输入的密码（请确保无人看见）：")
                passwd_ = list(bytearray(sha(passwd_.encode("utf-8")).hexdigest().encode()))
                cmd("cls")

                decrypted_text = decryption(list(file), passwd_, returns[2])

                print(f"""\r开始保存...{" " * 80}""", end="")
                n = 0
                while exists(f"decrypted_{n}{suffix}"):
                    n += 1  # 循环直到找到不存在的文件名，以免覆盖其他文件

                with open(f"decrypted_{n}{suffix}", "wb") as file_obj:
                    file_obj.write(decrypted_text)

                print(f"\r{sp(returns[2])[-1]} 解密完成 :)")
                print(f"| 解密后的文件已保存至当前目录下的 decrypted_{n}{suffix}")
                print()
            else:
                print("输入错误，请重新选择 :(")
                print()
        except:
            print("出了点错误 :(")
            print("请检查文件是否损坏")
            print()
