#!/usr/bin/env python
# coding=utf-8
import json

from base.method import Requests
from utils.operationYaml import OperationYaml
from utils.operationExcel import OperationExcel
from common.public import *
import pytest

class TestBook(object):
	excel = OperationExcel()
	obj = Requests()

	def result(self, req, row):
		assert req.status_code==200
		assert self.excel.getExpect(row=row) in json.dumps(req.json(), ensure_ascii=False)

	def test_book_001(self):
		'''获取所有书籍的信息'''
		r = self.obj.get(url=self.excel.getUrl(row=1))
		self.result(req=r, row=1)

	def test_book_002(self):
		'''添加书籍'''
		r = self.obj.post(
			url=self.excel.getUrl(row=2),
			json=self.excel.getJson(row=2)
		)
		self.result(req=r, row=2)
		# 注意这里需要把id记录到文件中给后面的接口调用
		bookid = r.json()[0]['datas']['id']
		writeContent(title="bookid", content=bookid)

	def test_003(self):
		'''查看添加的书籍'''
		r = self.obj.get(url=self.excel.getUrl(row=3))
		self.result(req=r, row=3)

	def test_004(self):
		'''编辑书籍'''
		r = self.obj.put(
			url=self.excel.getUrl(row=4),
			json=self.excel.getJson(row=4)
		)
		self.result(req=r, row=4)

	def test_005(self):
		'''删除书籍'''
		r = self.obj.delete(
			url=self.excel.getUrl(row=5),
		)
		self.result(req=r, row=5)


if __name__ == '__main__':
	pytest.main(["-s", "-v", "test_book.py"])