import random


def generate_verification_code():
    """随机生成6位的验证码"""
    code_list = []
    for i in range(10):
        code_list.append(str(i))
    myslice = random.sample(code_list, 6)
    verification_code = ''.join(myslice)  # list to string
    return verification_code


if __name__ == '__main__':
    code = generate_verification_code()
    print(code)
