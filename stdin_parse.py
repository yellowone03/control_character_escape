#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Author: huangyi


import re
import time


def parse_stdin(std_str):
    parse_stack = []
    col_index = 0
    i = 0
    len_str = len(std_str)
    begin_time = int(time.time())

    while i < len_str:
        if int(time.time()) > begin_time + 2:
            return
        if i < len_str - 1 and std_str[i:i+1] == '^C':
            return ''
        if std_str[i] == '\r':
            i += 1
            col_index = 0
            continue
        # 如果不是控制字符，直接入栈
        if 32 <= ord(std_str[i]) <= 126:
            if len(parse_stack) == col_index:
                parse_stack.insert(col_index, std_str[i])
            else:
                parse_stack[col_index] = std_str[i]
            col_index += 1
            i += 1
            continue

        # 如果是响铃(BEL)，或者Control-C，直接跳过
        if ord(std_str[i]) == 7 or ord(std_str[i]) == 3:
            i += 1
            continue

        # 如果是退格，将col_index左移一位
        if ord(std_str[i]) == 8:
            col_index -= 1
            col_index = max(0, col_index)
            i += 1
            continue

        # 如果是转义字符(ASCII 0x1B)
        if ord(std_str[i]) == 27:
            # 跳过CSI转义字符'['
            i += 2
            # 检测是否有数字参数
            num_str = ''
            while '0' <= std_str[i] <= '9':
                num_str += std_str[i]
                i += 1

            # 无数字参数转义
            if len(num_str) == 0:
                if std_str[i] == 'K':
                    parse_stack = parse_stack[:col_index+1]
                    i += 1
                elif std_str[i] == 'C':
                    col_index += 1
                    i += 1
                elif std_str[i] == 'D':
                    col_index -= 1
                    i += 1

            # 有数字参数转义
            else:
                offset = int(num_str)
                if std_str[i] == 'P':
                    while offset > 0:
                        if col_index < len(parse_stack):
                            parse_stack.pop(col_index)
                        offset -= 1
                    i += 1
                elif std_str[i] == '@':
                    i += 1
                    while offset > 0:
                        parse_stack.insert(col_index, std_str[i])
                        i += 1
                        col_index += 1
                        offset -= 1


    return ''.join(parse_stack)


def color_escape(std_str):
    chr_escape = chr(27)
    regex_color_escape = chr_escape + '\[([0-9]{1,2}(;[0-9]{1,3}){0,2})?[m|K]'
    regex_other_escape = chr_escape + '\]0;.*' + chr(7)
    escape_str = re.sub(regex_color_escape, '', std_str)
    escape_str = re.sub(regex_other_escape, '', escape_str)
    return escape_str


if __name__ == "__main__":
    pass

