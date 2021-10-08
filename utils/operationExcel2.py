#!/usr/bin/env python
# coding=utf-8
import json

import xlrd
from common.public import filePath
from utils.operationYaml import OperationYaml
from common.public import *


class ExcelVarles(object):
	'''因为列的内容总是固定的，所以可以把列的内容分离成变量'''
	caseID = "测试用例ID"
	caseModel = "模块"
	caseName = "接口名称"
	caseUrl = "请求地址"
	casePre = "前置条件"
	method = "请求方法"
	paramsType = "请求参数类型"
	params = "请求参数"
	expect = "期望结果"
	isRun = "是否运行"
	headers = "请求头"
	status_code = "状态码"


class OperationExcel(object):

	def getSheet(self, fileDir='data', fileName='books.xls'):
		book = xlrd.open_workbook(filePath(fileDir, fileName))
		return book.sheet_by_index(0)

	@property
	def getRows(self):
		'''获取总行数'''
		return self.getSheet().nrows

	@property
	def getCols(self):
		'''获取总列数'''
		return self.getSheet().ncols

	def getValue(self, row, col):
		'''获取单元格内容'''
		return self.getSheet().cell_value(row, col)

	@property
	def getExcelDatas(self):
		'''获取excel中所有的数据构造成一个列表，其中每个列表元素是一个字典'''
		datas = list()
		sheet = self.getSheet('data', 'login_books.xls')
		title = sheet.row_values(0)
		# 忽略首行进行循环
		for row in range(1, sheet.nrows):
			row_values = sheet.row_values(row)
			datas.append(dict(zip(title, row_values)))
		return datas

	def list_runs(self):
		'''第一步：获取到可执行的测试用例'''
		run_list = []
		for item in self.getExcelDatas:
			isRun = item[ExcelVarles.isRun]
			if isRun == "y":
				run_list.append(item)
			else:
				pass
		return run_list

	def all_case_lists(self):
		'''获取excel中所有的用例'''
		cases = list()
		for item in self.getExcelDatas:
			cases.append(item)
		return cases

	def list_load(self, prarms_list, key):
		'''
		第二步：对需要处理的列做反序列化处理（将字符串转化成字典）
		:param prarms_list: 待处理的列，比如请求参数、请求头
		:param key: 列名
		:return:反序列处理后的列表
		'''
		# tmp_list = self.runs()
		for item in prarms_list:
			params = item[key]
			if len(str(params).strip()) > 0:
				# strip(): 用于移除字符串头尾指定的字符（默认为空格）或字符序列
				item[key] = json.loads(params)  # 将字符串反序列化为字典
		return prarms_list

	def runs(self):
		'''第三步：将最终处理好的列表返回'''
		list1 = self.list_load(self.list_runs(), ExcelVarles.params)
		list2 = self.list_load(list1, ExcelVarles.headers)
		return list2

	def runs_all(self):
		'''第三步：将最终处理好的列表返回'''
		list1 = self.list_load(self.all_case_lists(), ExcelVarles.params)
		list2 = self.list_load(list1, ExcelVarles.headers)
		return list2

	def case_prev(self, casePrev):
		'''
		依据前置测试条件找到关联的前置测试用例
		:param casePrev: 前置测试条件
		:return:
		'''
		if casePrev.strip() != '':
			for item in self.runs_all():
				if casePrev in item[ExcelVarles.caseID]:
					return item
		return None

	def prevHeaders(self, key, prevResult):
		'''
		替换被关联测试点的请求头变量的值
		:param prevResult:
		:return:
		'''
		tmp_list = self.runs()
		for item in tmp_list:
			headers = item[ExcelVarles.headers]
			if headers != '':
				if key in headers['Authorization']:
					item[ExcelVarles.headers]['Authorization'] = headers['Authorization'].replace(key, prevResult)
					return item[ExcelVarles.headers]


	# return tmp_list


if __name__ == '__main__':
	obj = OperationExcel()
	#print(obj.prevHeaders('{token}', 'asdf'))
	obj.prevHeaders('{token}', 'asdf')
