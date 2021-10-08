#!/usr/bin/env python
# coding=utf-8

from base.method import Requests
from utils.operationExcel2 import OperationExcel, ExcelVarles
from common.public import *
import pytest
import allure
import json
import os

excel = OperationExcel()
obj = Requests()

class TestBook2(object):

	def case_assert_result(self, req, data):
		assert req.status_code == int(data[ExcelVarles.status_code])
		assert data[ExcelVarles.expect] in json.dumps(req.json(), ensure_ascii=False)

	def set_url(self, data):
		url = str(data[ExcelVarles.caseUrl]).replace('{bookID}', readContent())

	@pytest.mark.parametrize('datas', excel.runs())
	def test_login_book(self, datas):
		'''
		思路：
		1、先获取到所有前置测试点的测试用例
		2、执行前置测试点
		3、获取它的结果信息
		4、拿它的结果信息替换对应测试点的变量
		'''
		# 执行前置条件关联的测试点
		r = obj.post(
			url=excel.case_prev(datas[ExcelVarles.casePre])[ExcelVarles.caseUrl],
			json=excel.case_prev(datas[ExcelVarles.casePre])[ExcelVarles.params]
		)
		self.case_assert_result(req=r, data=excel.case_prev(datas[ExcelVarles.casePre]))
		prevResult=r.json()['access_token']
		#print(prevResult)
		header=excel.prevHeaders('{token}', prevResult)
		#status_code = int(datas[ExcelVarles.status_code])

		# 执行剩余用例
		r = obj.request(
			url=datas[ExcelVarles.caseUrl],
			method=datas[ExcelVarles.method],
			#headers=datas[ExcelVarles.headers],
			headers=header,
			json=datas[ExcelVarles.params]
		)
		print(r.json())
		#assert datas[ExcelVarles.expect] in json.dumps(r.json(), ensure_ascii=False)
		self.case_assert_result(req=r, data=datas)

if __name__ == '__main__':
	reportDir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "report/result")
	htmlDir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "report/html")
	pytest.main(["-v", "-s", "test_book2.py", "--alluredir", reportDir])
	import subprocess
	subprocess.call('allure generate {0} -o {1} --clean'.format(reportDir, htmlDir), shell=True)
	subprocess.call('allure open -h 127.0.0.1 -p 8088 {0}'.format(htmlDir), shell=True)