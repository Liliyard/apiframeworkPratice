#!/usr/bin/env python
# coding=utf-8

import os


def filePath(fileDir='data', fileName='login.yaml'):
	'''
	返回yaml文件的路径
	:param fileDir:目录
	:param fileName:文件名
	:return:
	'''
	return os.path.join(os.path.dirname(os.path.dirname(__file__)), fileDir, fileName)

def writeContent(title, content):
	with open(filePath(fileName=title), 'w') as f:
		f.write(str(content))

def readContent():
	with open(filePath(fileDir='data', fileName='bookID'), 'r') as f:
		return f.read()