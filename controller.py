# 引入类或依赖包
import uuid

import PySql
import config.config
import flask
import imghdr
import os
from flask import Flask, render_template, request, redirect, url_for, abort, send_from_directory
from werkzeug.utils import secure_filename

import util

PORT = config.config.SERVER_PORT  # 端口

# 定义服务
server = flask.Flask(__name__)


# 首页
@server.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')  # 定义位置


# 添加
@server.route('/Add', methods=['GET', 'POST'])
def Add():
    content = {
        'data': '添加数据'
    }
    return render_template('add.html', content=content, ensure_ascii=False)  # 页面 参数值 UTF-8


# 删除
@server.route('/Delete', methods=['GET', 'POST'])
def Delete():
    content = {
        'data': '删除数据'
    }
    return render_template('delete.html', content=content, ensure_ascii=False)  # 页面 参数值 UTF-8


# 修改
@server.route('/Modify', methods=['GET', 'POST'])
def Modify():
    content = {
        'data': '修改数据'
    }
    return render_template('modify.html', content=content, ensure_ascii=False)  # 页面 参数值 UTF-8


# 查看
@server.route('/Check', methods=['GET', 'POST'])
def Check():
    content = {
        'data': '查看数据'
    }
    return render_template('check.html', content=content, ensure_ascii=False)  # 页面 参数值 UTF-8


# 列表
@server.route('/List', methods=['GET', 'POST'])
def List():
    content = {
        'data': '列表数据'
    }
    return render_template('list.html', content=content, ensure_ascii=False)  # 页面 参数值 UTF-8


# 单文件上传
@server.route('/Upload', methods=['GET', 'POST'])
def Upload():
    content = {
        'data': '单文件上传'
    }
    return render_template('upload.html', content=content, ensure_ascii=False)  # 页面 参数值 UTF-8


# 多文件上传
@server.route('/Uploads', methods=['GET', 'POST'])
def Uploads():
    content = {
        'data': '多文件上传'
    }
    return render_template('uploads.html', content=content, ensure_ascii=False)  # 页面 参数值 UTF-8


@server.route('/add', methods=['GET', 'POST'])
def add():
    user = flask.request.values.get('user')
    passwd = flask.request.values.get('pass')
    name = flask.request.values.get('name')
    head = flask.request.values.get('head')
    if user == "":
        return util.ResultJson(400, 'user不能为空', None)
    if passwd == "":
        return util.ResultJson(400, 'pass不能为空', None)
    if name == "":
        return util.ResultJson(400, 'name不能为空', None)
    if head == "":
        return util.ResultJson(400, 'head不能为空', None)
    else:
        sql = "INSERT INTO user (`user`,`pass`,`name`,`head`,`ip`) VALUES ('%s','%s','%s','%s','%s')" % (
            user, passwd, name, head, '0.0.0.0')
        print("执行的sql语句：", sql)
        ret = PySql.add(sql)
        return util.ResultJson(ret[0], ret[1], ret[2])


@server.route('/delete', methods=['GET', 'POST'])
def delete():
    sid = flask.request.values.get('id')
    if sid == "":
        return util.ResultJson(400, 'id不能为空', None)
    else:
        if PySql.ids("SELECT * FROM user WHERE id = '%s' " % sid):
            sql = "DELETE FROM user WHERE `id` = '%s' " % sid
            print("执行的sql语句：", sql)
            ret = PySql.delete(sql)
            return util.ResultJson(ret[0], ret[1], ret[2])
        else:
            return util.ResultJson(400, 'id不存在哦', None)


@server.route('/modify', methods=['GET', 'POST'])
def modify():
    ids = flask.request.values.get('id')
    user = flask.request.values.get('user')
    passwd = flask.request.values.get('pass')
    name = flask.request.values.get('name')
    head = flask.request.values.get('head')
    if ids == "":
        return util.ResultJson(400, 'id不能为空', None)
    if user == "":
        return util.ResultJson(400, 'user不能为空', None)
    if passwd == "":
        return util.ResultJson(400, 'pass不能为空', None)
    if name == "":
        return util.ResultJson(400, 'name不能为空', None)
    if head == "":
        return util.ResultJson(400, 'head不能为空', None)
    else:
        if PySql.ids("SELECT * FROM user WHERE id = '%s' " % ids):
            sql = "UPDATE user SET user='%s',pass='%s',name='%s',head='%s' WHERE id='%s'" % (
                user, passwd, name, head, ids)
            print("执行的sql语句：", sql)
            ret = PySql.modify(sql)
            return util.ResultJson(ret[0], ret[1], ret[2])
        else:
            return util.ResultJson(400, 'id不存在哦', None)


@server.route('/check', methods=['GET', 'POST'])
def check():
    sid = flask.request.values.get('id')
    if sid == "":
        return util.ResultJson(400, 'id不能为空', None)
    else:
        if PySql.ids("SELECT * FROM user WHERE id = '%s' " % sid):
            sql = "SELECT * FROM user WHERE `id` = '%s' " % sid
            print("执行的sql语句：", sql)
            ret = PySql.check(sql)
            return util.ResultJson(ret[0], ret[1], ret[2])
        else:
            return util.ResultJson(400, 'id不存在哦', None)


@server.route('/list', methods=['GET', 'POST'])
def list():
    sql = "SELECT * FROM user"
    print("执行的sql语句：", sql)
    ret = PySql.list(sql)
    return util.ResultJson(ret[0], ret[1], ret[2])


# 设置文件上传保存路径
server.config['UPLOAD_FOLDER'] = 'static/upload/userHead'
# 设置上传文件的大小，单位字节
server.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024
# 格式验证
server.config['ALLOWED'] = {'jpeg', 'jpg', 'png'}


# 格式验证函数
def allowed(name):
    # 合规 True
    # 不合规 False
    return '.' in name and name.rsplit('.', 1)[1] in server.config['ALLOWED']


# 单文件上传
@server.route('/upload', methods=['POST'])
def upload():
    if not os.path.exists(server.config['UPLOAD_FOLDER']):
        os.mkdir(server.config['UPLOAD_FOLDER'])
    uploaded_file = request.files['file']  # 获取文件
    if uploaded_file != "":
        if allowed(uploaded_file.filename):
            filename = secure_filename(uploaded_file.filename)  # 文件名
            ext = filename.rsplit('.')[-1]  # 后缀
            file_name = str(uuid.uuid4()) + "." + ext  # 生成一个uuid作为文件名
            uploaded_file.save(os.path.join(server.config['UPLOAD_FOLDER'], file_name))  # 保存
            file_path = server.config['UPLOAD_FOLDER'] + '/' + file_name  # 地址
            ret = {
                'file-path': file_path
            }
            return util.ResultJson(200, '上传成功', ret)
        else:
            return util.ResultJson(400, '文件格式不合规', None)
    else:
        return util.ResultJson(400, '文件不能为空', None)


# 多文件上传
@server.route('/uploads', methods=['POST'])
def uploads():
    if not os.path.exists(server.config['UPLOAD_FOLDER']):
        os.mkdir(server.config['UPLOAD_FOLDER'])
    upload_files = request.files.getlist('file')
    file_name = []
    file_path = []
    # 循环上传
    for file in upload_files:
        if allowed(file.filename):
            file_name = secure_filename(file.filename)
            ext = file_name.rsplit('.')[-1]  # 后缀
            file_names = str(uuid.uuid4()) + "." + ext  # 生成一个uuid作为文件名
            file.save(os.path.join(server.config['UPLOAD_FOLDER'], file_names))  # 保存
            file_path.append(server.config['UPLOAD_FOLDER'] + '/' + file_names)  # 地址
        else:
            file_path.append('不合规文件')
    return util.ResultJson(200, '上传成功', file_path)


if __name__ == '__main__':
    server.run(port=PORT, debug=True)
