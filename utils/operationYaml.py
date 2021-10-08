#!/usr/bin/env python
# coding=utf-8

import yaml
from common.public import filePath

class OperationYaml(object):
	def readYaml(self):
		with open(filePath(), 'r', encoding='utf-8') as f:
			# 将yaml文件对象转换成列表后返回
			return list(yaml.safe_load_all(f))

	def dictYaml(self, fileDir='data', fileName='books.yaml'):
		with open(filePath(fileDir=fileDir, fileName=fileName), 'r', encoding='utf-8') as f:
			return yaml.safe_load(f)

if __name__ == '__main__':
	obj = OperationYaml()
	print(obj.dictYaml())