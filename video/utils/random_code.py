import random


def get_random_code(num):
    code = ''
    for i in range(num):
        random_num = str(random.randint(0, 9))
        code += random_num
    return code


if __name__ == '__main__':
    print(get_random_code(6))
