"""
本程序采用随机 guid 码（guid 码是由 32 位 16 进制数和分隔符“-”组成的）作为密码进行加密，
将文件转换为 base64 编码后轮番加上 guid 码的某一位，
所以如果不知道密码，解密文件就是很难的

注：如果解密失败，请检查密码是否正确
"""
from uuid import uuid1 as guid
from pathlib import Path as Ph
from os.path import splitext as st
from json import dumps as ds, loads as ls


def read_file(mode: bool):
    while True:  # 循环直到成功读取了文件内容
        path_ = input("输入文件路径：")
        if exists(path_):  # 如果输入的路径存在并且是一个文件
            try:
                with open(path_, "rb") as file_obj_:
                    if mode:
                        return [file_obj_.read(), st(path_)[-1]]
                    else:
                        return [ls(file_obj_.read()), st(path_)[-1]]
            except:
                print("读取文件失败 :(")
                print("请检查文件是否损坏")
                continue  # 重新循环
        else:
            print("请输入一个文件的路径（不带引号）:(")
            continue


def encryption(bytes_: list):
    guid_ = guid()
    g_code = list(bytearray(str(guid_).encode("utf-8")))  # 生成一个 guid 码作为密码
    long = len(g_code)
    text = {"file": []}
    for i in range(len(bytes_)):
        text["file"].append(g_code[i % long] + bytes_[i])

    return [text, guid_]


def decryption(bytes_: list, guid_: list):
    text = b""
    long = len(guid_)
    for i in range(len(bytes_)):
        text += int.to_bytes(bytes_[i] - guid_[i % long], byteorder="little", length=1)
    return text


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
                encrypted_text = encryption(list(file))

                n = 0
                while exists(f"encrypted_{n}{suffix}") or exists(f"key_{n}.txt"):
                    n += 1  # 循环直到找到不存在的文件名，以免覆盖其他文件

                with open(f"encrypted_{n}{suffix}", "w") as file_obj:
                    file_obj.write(ds(encrypted_text[0]))
                with open(f"key_{n}.txt", "w") as file_obj:
                    file_obj.write(str(encrypted_text[1]))

                print("文件加密完成 :)")
                print(f"加密后文件已保存至当前目录下的 encrypted_{n}{suffix}")
                print(f"密码已保存至当前目录下的 key_{n}.txt")
                print("请妥善保存这两个文件！")
            elif ed == "d":
                returns = read_file(False)
                file = returns[0]["file"]
                suffix = returns[1]
                guid___ = list(bytearray(input("密码：").encode("utf-8")))

                decrypted_text = decryption(file, guid___)

                n = 0
                while exists(f"decrypted_{n}{suffix}"):
                    n += 1  # 循环直到找到不存在的文件名，以免覆盖其他文件

                with open(f"decrypted_{n}{suffix}", "wb") as file_obj:
                    file_obj.write(decrypted_text)

                print("文件解密完成 :)")
                print(f"解密后的文件已保存至当前目录下的 decrypted_{n}{suffix}")
            else:
                print("输入错误，请重新选择 :(")
                continue
        except:
            print("出了点错误 :(")
            print("请检查文件是否损坏")
            continue
