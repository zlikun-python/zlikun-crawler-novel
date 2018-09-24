#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: zlikun
import utils

it = iter([])

print(utils.get_first_from_list([i for i in it]))
print(utils.get_first_from_list([]))
print(utils.get_first_from_list([1, 2, 3]))

# print(next(it))

print("ABC\nDEF".replace("\n", "<br>"))
