# -*- coding: UTF-8 -*-

import re
import math


def calculate(n1, n2, operator):
    """
    :param n1: float
    :param n2: float
    :param operator: + - * \
    :return: float
    """
    result = 0

    if operator == "+":
        result = n1 + n2
    if operator == "-":
        result = n1 - n2
    if operator == "*":
        result = n1 * n2
    if operator == "/":
        result = n1 / n2
    return result


# 判断是否是运算符，如果是返回True
def is_operator(e):
    """
    :param e: str
    :return: bool
    """
    opers = ['+', '-', '*', '/']
    return True if e in opers else False


# 将算式处理成列表，解决横杠是负数还是减号的问题
def formula_format(formula):
    # 以 '横杠数字' 分割， 其中正则表达式：(\-\d+\.?\d*) 括号内：
    # \- 表示匹配横杠开头； \d+ 表示匹配数字1次或多次；\.?表示匹配小数点0次或1次;\d*表示匹配数字1次或多次。
    formula_list = [i for i in re.split('(\-\d+\.?\d*)', formula) if i]

    # 最终的算式列表
    final_formula = []
    for item in formula_list:
        # 第一个是以横杠开头的数字（包括小数）final_formula。即第一个是负数，横杠就不是减号
        if len(final_formula) == 0 and re.search('^\-\d+\.?\d*$', item):
            final_formula.append(item)
            continue

        if len(final_formula) > 0:
            # 如果final_formal最后一个元素是运算符['+', '-'], 则横杠数字不是负数
            if re.search('[\+\-\*\/]$', final_formula[-1]):
                final_formula.append(item)
                continue
        # 按照运算符分割开
        item_split = [i for i in re.split('([\+\-\*\/)])', item) if i]
        final_formula += item_split
    return final_formula


def decision(tail_op, now_op):
    """
    :param tail_op: 运算符栈的最后一个运算符
    :param now_op: 从算式列表取出的当前运算符
    :return: 1 代表弹栈运算， -1 表示入栈
    """

    # 定义2种运算符级别
    rate1 = ['+', '-']
    rate2 = ['*', '/']

    if tail_op in rate1:
        if now_op in rate2:
            # 说明连续两个运算优先级不一样，需要入栈
            return -1
        else:
            return 1

    elif tail_op in rate2:
        return 1

    else:
        return -1


def final_calc(formula_list):
    num_stack = []       # 数字栈
    op_stack = []        # 运算符栈
    for e in formula_list:
        operator = is_operator(e)
        if not operator:
            # 压入数字栈
            # 字符串转换为符点数
            num_stack.append(float(e))
        else:
            # 如果是运算符
            while True:
                # 如果运算符栈等于0无条件入栈
                if len(op_stack) == 0:
                    op_stack.append(e)
                    break

                # decision 函数做决策
                tag = decision(op_stack[-1], e)
                if tag == -1:
                    # 如果是-1压入运算符栈进入下一次循环
                    op_stack.append(e)
                    break
                elif tag == 1:
                    # 如果是1弹出运算符栈内最后一个运算符，弹出数字栈内后两个元素。
                    op = op_stack.pop()
                    num2 = num_stack.pop()
                    num1 = num_stack.pop()
                    # 执行计算
                    # 计算之后压入数字栈
                    num_stack.append(calculate(num1, num2, op))

    # 处理大循环结束后 数字栈和运算符栈中可能还有元素 的情况
    while len(op_stack) != 0:
        op = op_stack.pop()
        num2 = num_stack.pop()
        num1 = num_stack.pop()
        num_stack.append(calculate(num1, num2, op))

    return num_stack, op_stack


if __name__ == '__main__':
    #用户交互界面
    print("Welcome Aho Calculator!")
    print("Enter 'quit' to end the program.")
    formula = ""

    while formula != "quit":
        formula = input("Write down the formula you want to calculate.\n-->")
        if formula != "quit":
            formula_list = formula_format(formula)
            result, _ = final_calc(formula_list)
            print("The result is: ", '%.2f' % result[0])
        else:
            break
