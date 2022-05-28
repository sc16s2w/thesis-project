import json

from flask_paginate import get_page_parameter, Pagination

from . import home
from flask import render_template, redirect, url_for, flash, session, request
from app.home.forms import RegistForm, LoginForm, PostForm
from app.models import User, db, UserLog, LexicalRules, CollectData, Sentence, Userlabeled
from datetime import datetime
from werkzeug.security import generate_password_hash
from functools import wraps

# 登录装饰器
from ..helper import create_sample, read_file, read_syntactic_rules, initializaData
from ..templates.Simplify import show_different_words, show_different_rules, show_different_rules_syntactic

changed_words = show_different_words("/Users/wangsiwei/Downloads/TS_T5-main_base/store_simple.txt")
lexical_inputs = show_different_rules("/Users/wangsiwei/Downloads/python-flask-login-register-master/app/lexical_rules_input.txt")

dict = read_file()
dict_syntactic = read_syntactic_rules()
item = 0
itemFrequency=[0,0]
collect_syntactic =[]
collect_lexical=[]
input_syntactic=[]
input_lexical=[]
training_sample = 0
q,userMap = initializaData()
syntactic_inputs = show_different_rules_syntactic("/Users/wangsiwei/Downloads/python-flask-login-register-master/app/test.txt")
def user_login_req(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'name' not in session:
            return redirect(url_for("home.login"))
        return func(*args, **kwargs)
    return decorated_function

# 前端首页
@home.route("/")
def index():
    return render_template("home/index.html")


# 用户中心
@home.route("/user")
@user_login_req
def user():
    return render_template("home/user.html")


# 用户登录
@home.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():

        data = form.data
        user = User.query.filter_by(name=data["name"]).first()
        if user:
            if user.check_pwd(data["pwd"]):
                userlog = UserLog(
                    user_id=user.id,
                    ip=request.remote_addr
                )
                db.session.add(userlog)
                db.session.commit()
                session["user_id"] = user.id
                session["name"] = user.name
                print(user.name)
                return redirect(url_for('home.search'))
        else:
            return redirect(url_for('home.register'))
    return render_template("home/login.html", form=form)


# 退出登录
@home.route("/logout",methods=["GET", "POST"])
def logout():
    form = LoginForm()
    if 'name' in session:
        session.clear()
        return render_template("home/index.html")
    return render_template("home/index.html")


# 会员注册
@home.route("/register", methods=["GET", "POST"])
def register():
    form = RegistForm()
    # global userMap
    if form.validate_on_submit():
        data = form.data
        user = User(
            name=data["name"],
            pwd=generate_password_hash(data["pwd"]),
            addtime=datetime.now()
        )
        db.session.add(user)
        db.session.commit()
        visited = set()
        print(user.id)
        # userMap[user.id] = visited
        flash("register successful", "ok")
        return redirect(url_for("home.login"))
    return render_template("home/register.html", form=form)



@home.route('/label_lexical', methods=['GET', 'POST'])
@user_login_req
def search():
    user_id = session["user_id"]
    form = PostForm(request.form)
    global item
    if request.method == 'POST':
        lexical = request.form.getlist('lexicalrule')
        syntactic = request.form.getlist('syntacticrule')
        print(lexical)
        lexical_str = ','.join([str(x) for x in lexical])
        syntactic_str = ','.join([str(x) for x in syntactic])
        # print(form.data)
        collectData = CollectData(
            user_id=user_id,
            item_id=int(item),
            collect_lexical=lexical_str,
            collect_syntactic=syntactic_str,
            input_lexical=form.data['input_lexical'],
            input_syntactic=form.data['input_syntactic']
        )
        sentence = Sentence.query.filter_by(id = int(item)).first()
        print(sentence)
        frequency_update = sentence.frequency+1
        sentence_update = Sentence(
            id = int(item),
            frequency = frequency_update
        )
        userlabeled = Userlabeled.query.filter_by(userid = user_id).first()
        print(sentence_update)
        print(userlabeled)
        if userlabeled:
            c = [int(i) for i in (userlabeled.labeled.split(','))]
            c.append(int(item))
            b = ','.join([str(x) for x in c])
            userlabeled = Userlabeled(userid=user_id,
                                      labeled = b)
        else:
            c=[]
            c.append(int(item))
            b = ','.join([str(x) for x in c])
            userlabeled = Userlabeled(userid=user_id,
                                      labeled=b)
        db.session.add(collectData)
        db.session.merge(sentence_update)
        db.session.merge(userlabeled)
        db.session.commit()
        sentence = Sentence.query.filter(Sentence.frequency < 3).order_by(Sentence.frequency.asc())
        userlabeled = Userlabeled.query.filter_by(userid=user_id).first()
        sentence_list = []
        for sent in sentence:
            sentence_list.append(int(sent.id))
        if userlabeled:
            c = [int(i) for i in (userlabeled.labeled.split(','))]
            l = list(set(sentence_list).difference(set(c)))
            l.sort(key=sentence_list.index)
        else:
            l = sentence_list
        if l == None: return render_template("home/success.html")
        print(l)
        item = l[0]
        data = dict.get(item).split("#")
        change = changed_words[item + 1]
        lexical_input = lexical_inputs[item + 1]
        syntactic_input_now = syntactic_inputs[item + 1]
        total = len(syntactic_input_now)
        # 或许前端请求的页码，通过get请求，查询字符串默认值为page，也可以改成其他的，所有用get_page_parameter()获取就不用担心他到底是什么了。type规定了页码数据类型为整型，默认值为1（就是首页）
        page = request.args.get(get_page_parameter(), type=int, default=1)
        # config.PER_PAGE这个参数写在了配置文件中，代表每页有多少条数据，start和end主要用于数据库里取数据的范围
        start = (page - 1) * 5
        end = start + 5
        # 这个是从数据库中查询的数据
        syntactic_input = syntactic_input_now[start:end]
        # channels = Channel.query.order_by(Channel.priority.asc()).slice(start, end).all()
        # 创建了一个pagination的对象，这个对象是返回给前端页面的，这个对象封装了很多属性，比如前面说的请求字符串的名字，前端拿到这些属性后配合CSS可以组织分页的样式，bs_version代表使用的bootstrap版本为3，默认为2，也可以不写，但是需要自己写分页html模版。page参数是页码，total是总数据数，per_page为每页条数。
        pagination = Pagination(bs_version=3, page=page, total=total, per_page=5, inner_window=2,
                                outer_window=2, prev_label='Previous', next_label='Next')
        # if (q.empty() | len(userMap[user_id]) == 100): return render_template("home/success.html")
        return render_template('home/label.html', data_dict=data,
                               syntacticrules=syntactic_input,  pagination =pagination, data=data,  change = change,lexical_input = lexical_input,form = form)
    else:
        sentence = Sentence.query.filter(Sentence.frequency < 3).order_by(Sentence.frequency.asc())
        userlabeled = Userlabeled.query.filter_by(userid=user_id).first()
        sentence_list = []
        for sent in sentence:
            sentence_list.append(int(sent.id))
        if userlabeled:
            c = [int(i) for i in (userlabeled.labeled.split(','))]
            l = list(set(sentence_list).difference(set(c)))
            l.sort(key=sentence_list.index)
        else:
            l = sentence_list
        if l == None: return render_template("home/success.html")
        item = l[0]
        data = dict.get(item).split("#")
        change = changed_words[item + 1]
        lexical_input = lexical_inputs[item + 1]
        syntactic_input_now = syntactic_inputs[item + 1]
        total = len(syntactic_input_now)
        # 或许前端请求的页码，通过get请求，查询字符串默认值为page，也可以改成其他的，所有用get_page_parameter()获取就不用担心他到底是什么了。type规定了页码数据类型为整型，默认值为1（就是首页）
        page = request.args.get(get_page_parameter(), type=int, default=1)
        # config.PER_PAGE这个参数写在了配置文件中，代表每页有多少条数据，start和end主要用于数据库里取数据的范围
        start = (page - 1) * 5
        end = start + 5
        # 这个是从数据库中查询的数据
        syntactic_input = syntactic_input_now[start:end]
        # channels = Channel.query.order_by(Channel.priority.asc()).slice(start, end).all()
        # 创建了一个pagination的对象，这个对象是返回给前端页面的，这个对象封装了很多属性，比如前面说的请求字符串的名字，前端拿到这些属性后配合CSS可以组织分页的样式，bs_version代表使用的bootstrap版本为3，默认为2，也可以不写，但是需要自己写分页html模版。page参数是页码，total是总数据数，per_page为每页条数。
        pagination = Pagination(bs_version=3, page=page, total=total, per_page=5, inner_window=2,
                                outer_window=2, prev_label='Previous', next_label='Next')
        return render_template('home/label.html', data_dict=data,
                               syntacticrules=syntactic_input, pagination =pagination,data=data, change = change,lexical_input=lexical_input,form=form)

@home.route('/training', methods=['GET', 'POST'])
@user_login_req
def training():
    global item
    global q
    global itemFrequency
    # global userMap
    form = PostForm(request.form)
    if request.method == 'POST':
        lexical = request.form.getlist('lexicalrule')
        syntactic = request.form.getlist('syntacticrule')
        user_id = session["user_id"]
        print(lexical)
        lexical_str = ','.join([str(x) for x in lexical])
        syntactic_str = ','.join([str(x) for x in syntactic])
        # print(form.data)
        collectData = CollectData(
            user_id=user_id,
            item_id=int(item),
            collect_lexical=lexical_str,
            collect_syntactic=syntactic_str,
            input_lexical=form.data['input_lexical'],
            input_syntactic=form.data['input_syntactic']
        )
        db.session.add(collectData)
        db.session.commit()
        item = int(item)
        data = dict.get(item).split("#")
        change = changed_words[item + 1]
        lexical_input = lexical_inputs[item + 1]
        syntactic_input_now = syntactic_inputs[item + 1]
        total = len(syntactic_input_now)
        # 或许前端请求的页码，通过get请求，查询字符串默认值为page，也可以改成其他的，所有用get_page_parameter()获取就不用担心他到底是什么了。type规定了页码数据类型为整型，默认值为1（就是首页）
        page = request.args.get(get_page_parameter(), type=int, default=1)
        # config.PER_PAGE这个参数写在了配置文件中，代表每页有多少条数据，start和end主要用于数据库里取数据的范围
        start = (page - 1) * 5
        end = start + 5
        # 这个是从数据库中查询的数据
        syntactic_input = syntactic_input_now[start:end]
        # channels = Channel.query.order_by(Channel.priority.asc()).slice(start, end).all()
        # 创建了一个pagination的对象，这个对象是返回给前端页面的，这个对象封装了很多属性，比如前面说的请求字符串的名字，前端拿到这些属性后配合CSS可以组织分页的样式，bs_version代表使用的bootstrap版本为3，默认为2，也可以不写，但是需要自己写分页html模版。page参数是页码，total是总数据数，per_page为每页条数。
        pagination = Pagination(bs_version=3, page=page, total=total, per_page=5, inner_window=2,
                                outer_window=2, prev_label='Previous', next_label='Next')
        return render_template('home/label.html', data_dict=data,
                               syntacticrules=syntactic_input, pagination=pagination, data=data,
                               change=change, lexical_input=lexical_input, form=form)
    else:
        data = dict.get(item).split("#")
        change = changed_words[item + 1]
        lexical_input = lexical_inputs[item + 1]
        syntactic_input_now = syntactic_inputs[item + 1]
        total = len(syntactic_input_now)
        # 或许前端请求的页码，通过get请求，查询字符串默认值为page，也可以改成其他的，所有用get_page_parameter()获取就不用担心他到底是什么了。type规定了页码数据类型为整型，默认值为1（就是首页）
        page = request.args.get(get_page_parameter(), type=int, default=1)
        # config.PER_PAGE这个参数写在了配置文件中，代表每页有多少条数据，start和end主要用于数据库里取数据的范围
        start = (page - 1) * 5
        end = start + 5
        # 这个是从数据库中查询的数据
        syntactic_input = syntactic_input_now[start:end]
        # channels = Channel.query.order_by(Channel.priority.asc()).slice(start, end).all()
        # 创建了一个pagination的对象，这个对象是返回给前端页面的，这个对象封装了很多属性，比如前面说的请求字符串的名字，前端拿到这些属性后配合CSS可以组织分页的样式，bs_version代表使用的bootstrap版本为3，默认为2，也可以不写，但是需要自己写分页html模版。page参数是页码，total是总数据数，per_page为每页条数。
        pagination = Pagination(bs_version=3, page=page, total=total, per_page=5, inner_window=2,
                                outer_window=2, prev_label='Previous', next_label='Next')
        return render_template('home/label.html', data_dict=data,
                               syntacticrules=syntactic_input, pagination=pagination, data=data, url_build=url,
                               change=change, lexical_input=lexical_input, form=form)



@home.route('/dropdown_menu', methods=['GET', 'POST'])
@user_login_req
def dropdown_menu():
    list = create_sample()
    rules = LexicalRules.query.limit(10)
    global item
    global collect_lexical
    global collect_syntactic
    global input_syntactic
    global input_lexical
    global q
    global itemFrequency
    global userMap
    if request.method == 'GET':
        syntactic_rule = dict_syntactic[item + 1]
        data = dict.get(item).split("#")
        url = "../../static/saliency" + str(item+1) + ".html"
        return render_template('home/label.html', data_dict=data,
                               syntacticrules=syntactic_rule,rules=rules,menus=list,url_build= url)
    else:
        if(item !="training example two answer")|(item !="training example two")|(item !="training example one")|(item !="training example one answer")|(item=="Choose the next sentence you would like to annotate"):
            rule_list = request.form.getlist("syntacticrule")
            if isinstance(collect_lexical, bytes):
                collect_lexical = collect_lexical.decode()
            if isinstance(collect_syntactic, bytes):
                collect_syntactic = collect_syntactic.decode()
            if isinstance(input_lexical, bytes):
                input_lexical = input_lexical.decode()
            if isinstance(input_syntactic, bytes):
                input_syntactic = input_syntactic.decode()
            collect_lexical = bytes(json.dumps(collect_lexical, ensure_ascii=False),'utf8')
            collect_syntactic = bytes(json.dumps(collect_syntactic, ensure_ascii=False),'utf8')
            input_lexical = bytes(json.dumps(input_lexical, ensure_ascii=False),'utf8')
            input_syntactic = bytes(json.dumps(input_syntactic, ensure_ascii=False),'utf8')
            print(collect_lexical)
            print(collect_syntactic)
            print(input_syntactic)
            print(input_lexical)
            user_id = session["user_id"]
            collectData = CollectData(
                user_id = user_id,
                item_id = int(item),
                collect_lexical = collect_lexical,
                collect_syntactic = collect_syntactic,
                input_lexical = input_lexical,
                input_syntactic = input_syntactic
            )
            itemFrequency[0]=itemFrequency[0]+1;
            temp = userMap[user_id]
            temp.add(itemFrequency[1])
            userMap[user_id] = temp
            if(itemFrequency[0]!=3):
                q.put((itemFrequency[0],itemFrequency[1]))
            db.session.add(collectData)
            db.session.commit()
        if(q.empty()|len(userMap[user_id])==5): return render_template("home/success.html")
        t = q.get()
        user_id = session["user_id"]
        temp = userMap[user_id]
        while t[1] in temp:
            r = q.get()
            q.put(t)
            t = r

        itemFrequency[0] = t[0]
        itemFrequency[1] = t[1]
        item = itemFrequency[1]
        item = int(item)
        collect_lexical = []
        collect_syntactic = []
        input_syntactic = []
        input_lexical = []
        data = dict.get(item).split("#")
        url = "../../static/saliency"+str(item+1)+".html"
        syntactic_rule = dict_syntactic[item+1]
        return render_template('home/label.html', data_dict=data,
                               syntacticrules=syntactic_rule,rules=rules,menus = list,url_build = url)


@home.route('/training_search', methods=['GET', 'POST'])
@user_login_req
def training_select():
    list = create_sample()
    rules = LexicalRules.query.limit(10)
    global item
    global training_sample
    if training_sample == 0:
        url = "../../static/training1.html"
        data = ['This is extremely hard to comprehend', 'This is very hard to understand']
        syntactic_rule = ["null"]
        url_first = 'home/training1.html'
    else:
        url = "../../static/training2.html"
        data = ['Graham attended Wheaton College from 1939 to 1943,when he graduated with a BA in anthropology.',
                'Graham went to Wheaton College from 1939 to 1943.He got a BA inanthropology in 1943']
        syntactic_rule = [["Graham attended Wheaton College from 1939 to 1943. He graduated with a BA in anthropology.",
                           "NonRestrictiveRelativeClauseWhereExtractor"],
                          ["Graham attended Wheaton College from 1939 to 1943.",
                           "NonRestrictiveRelativeClauseWhereExtractor"],
                          ["He graduated with a BA in anthropology.", "NonRestrictiveRelativeClauseWhereExtractor"],
                          ["Graham attended Wheaton College to 1943. He graduated with a BA .",
                           "PrepositionalAttachedtoVPExtractor NonRestrictiveRelativeClauseWhereExtractor"],
                          ["Graham attended Wheaton College from 1939 to 1943 . He graduated with a BA.",
                           "PrepositionalAttachedtoVPExtractor NonRestrictiveRelativeClauseWhereExtractor"],
                          ["Graham attended Wheaton College to 1943. He graduated with a BA in anthropology .",
                           " PrepositionalAttachedtoVPExtractor NonRestrictiveRelativeClauseWhereExtractor"]]
        url_first = 'home/training2.html'
    if request.method == 'GET':
        return render_template(url_first, data_dict=data,
                               syntacticrules=syntactic_rule, rules=rules, data=data, url_build=url, menus=list)
    else:
        rule_list = request.form.getlist( "rule")
        print(rule_list)
        collect_lexical.append(rule_list)
        return render_template(url_first, data_dict=data,
                               syntacticrules=syntactic_rule, rules=rules, data=data, url_build=url, menus=list)



@home.route('/training_syntactic', methods=['GET', 'POST'])
@user_login_req
def training_syntactic():
    list = create_sample()
    rules = LexicalRules.query.limit(10)
    global item
    global training_sample
    if training_sample == 0:
        url = "../../static/training1.html"
        data = ['This is extremely hard to comprehend', 'This is very hard to understand']
        syntactic_rule = ["null"]
        url_first = 'home/training1.html'
    else:
        url = "../../static/training2.html"
        data = ['Graham attended Wheaton College from 1939 to 1943,when he graduated with a BA in anthropology.',
                'Graham went to Wheaton College from 1939 to 1943.He got a BA inanthropology in 1943']
        syntactic_rule = [["Graham attended Wheaton College from 1939 to 1943. He graduated with a BA in anthropology.",
                           "NonRestrictiveRelativeClauseWhereExtractor"],
                          ["Graham attended Wheaton College from 1939 to 1943.",
                           "NonRestrictiveRelativeClauseWhereExtractor"],
                          ["He graduated with a BA in anthropology.", "NonRestrictiveRelativeClauseWhereExtractor"],
                          ["Graham attended Wheaton College to 1943. He graduated with a BA .",
                           "PrepositionalAttachedtoVPExtractor NonRestrictiveRelativeClauseWhereExtractor"],
                          ["Graham attended Wheaton College from 1939 to 1943 . He graduated with a BA.",
                           "PrepositionalAttachedtoVPExtractor NonRestrictiveRelativeClauseWhereExtractor"],
                          ["Graham attended Wheaton College to 1943. He graduated with a BA in anthropology .",
                           " PrepositionalAttachedtoVPExtractor NonRestrictiveRelativeClauseWhereExtractor"]]
        url_first = 'home/training2.html'
    if request.method == 'GET':
        return render_template(url_first, data_dict=data,
                               syntacticrules=syntactic_rule, rules=rules, data=data, url_build=url, menus=list)
    else:
        rule_list = request.form.getlist( "rule")
        print(rule_list)
        for temp in rule_list:
            collect_syntactic.append(temp)
        return render_template(url_first, data_dict=data,
                               syntacticrules=syntactic_rule, rules=rules, data=data, url_build=url, menus=list)

@home.route('/training_submit_lexical', methods=['GET', 'POST'])
@user_login_req
def training_submit_lexical():
    list = create_sample()
    rules = LexicalRules.query.limit(10)
    global item
    global training_sample
    if training_sample == 0:
        url = "../../static/training1.html"
        data = ['This is extremely hard to comprehend', 'This is very hard to understand']
        syntactic_rule = ["null"]
        url_first = 'home/training1.html'
    else:
        url = "../../static/training2.html"
        data = ['Graham attended Wheaton College from 1939 to 1943,when he graduated with a BA in anthropology.',
                'Graham went to Wheaton College from 1939 to 1943.He got a BA inanthropology in 1943']
        syntactic_rule = [["Graham attended Wheaton College from 1939 to 1943. He graduated with a BA in anthropology.",
                           "NonRestrictiveRelativeClauseWhereExtractor"],
                          ["Graham attended Wheaton College from 1939 to 1943.",
                           "NonRestrictiveRelativeClauseWhereExtractor"],
                          ["He graduated with a BA in anthropology.", "NonRestrictiveRelativeClauseWhereExtractor"],
                          ["Graham attended Wheaton College to 1943. He graduated with a BA .",
                           "PrepositionalAttachedtoVPExtractor NonRestrictiveRelativeClauseWhereExtractor"],
                          ["Graham attended Wheaton College from 1939 to 1943 . He graduated with a BA.",
                           "PrepositionalAttachedtoVPExtractor NonRestrictiveRelativeClauseWhereExtractor"],
                          ["Graham attended Wheaton College to 1943. He graduated with a BA in anthropology .",
                           " PrepositionalAttachedtoVPExtractor NonRestrictiveRelativeClauseWhereExtractor"]]
        url_first = 'home/training2.html'
    if request.method == 'GET':
        return render_template(url_first, data_dict=data,
                               syntacticrules=syntactic_rule, rules=rules, data=data, url_build=url, menus=list)
    else:
        input = request.form.get("input_lexical")
        input_lexical.append(input)
        return render_template(url_first, data_dict=data,
                               syntacticrules=syntactic_rule, rules=rules, data=data, url_build=url, menus=list)


@home.route('/training_submit_syntactic', methods=['GET', 'POST'])
@user_login_req
def training_submit_syntactic():
    list = create_sample()
    rules = LexicalRules.query.limit(10)
    global item
    global training_sample
    if training_sample == 0:
        url = "../../static/training1.html"
        data = ['This is extremely hard to comprehend', 'This is very hard to understand']
        syntactic_rule = ["null"]
        url_first = 'home/training1.html'
    else:
        url = "../../static/training2.html"
        data = ['Graham attended Wheaton College from 1939 to 1943,when he graduated with a BA in anthropology.',
                'Graham went to Wheaton College from 1939 to 1943.He got a BA inanthropology in 1943']
        syntactic_rule = [["Graham attended Wheaton College from 1939 to 1943. He graduated with a BA in anthropology.",
                           "NonRestrictiveRelativeClauseWhereExtractor"],
                          ["Graham attended Wheaton College from 1939 to 1943.",
                           "NonRestrictiveRelativeClauseWhereExtractor"],
                          ["He graduated with a BA in anthropology.", "NonRestrictiveRelativeClauseWhereExtractor"],
                          ["Graham attended Wheaton College to 1943. He graduated with a BA .",
                           "PrepositionalAttachedtoVPExtractor NonRestrictiveRelativeClauseWhereExtractor"],
                          ["Graham attended Wheaton College from 1939 to 1943 . He graduated with a BA.",
                           "PrepositionalAttachedtoVPExtractor NonRestrictiveRelativeClauseWhereExtractor"],
                          ["Graham attended Wheaton College to 1943. He graduated with a BA in anthropology .",
                           " PrepositionalAttachedtoVPExtractor NonRestrictiveRelativeClauseWhereExtractor"]]
        url_first = 'home/training2.html'

    if request.method == 'GET':
        return render_template(url_first, data_dict=data,
                               syntacticrules=syntactic_rule, rules=rules, data=data, url_build=url, menus=list)
    else:
        input = request.form.get('ckeditor')
        input_syntactic.append(input)
        return render_template(url_first, data_dict=data,
                               syntacticrules=syntactic_rule, rules=rules, data=data, url_build=url, menus=list)


@home.route('/training_dropdown_menu', methods=['GET', 'POST'])
@user_login_req
def trainging_dropdown_menu():
    list = create_sample()
    rules = LexicalRules.query.limit(10)
    global item
    syntactic_rule = ["null"]
    url = "../../static/training1.html"
    global collect_lexical
    global collect_syntactic
    global input_syntactic
    global input_lexical
    global training_sample
    if request.method == 'GET':
        data = ['This is extremely hard to comprehend', 'This is very hard to understand']
        return render_template('home/training1.html', data_dict=data,
                               syntacticrules=syntactic_rule, rules=rules, menus=list, url_build= url)
    else:
        data = ['This is extremely hard to comprehend', 'This is very hard to understand']
        item = request.form.get('manufacturer')
        item = item.strip()
        print(item == 'training example one answer')
        if item == 'training example one answer':
            url_first = 'home/answer.html'
        elif item == "training example two":
            training_sample = 1
            url = "../../static/training2.html"
            data = ['Graham attended Wheaton College from 1939 to 1943,when he graduated with a BA in anthropology.',
                    'Graham went to Wheaton College from 1939 to 1943.He got a BA inanthropology in 1943']
            syntactic_rule = [
                ["Graham attended Wheaton College from 1939 to 1943. He graduated with a BA in anthropology.",
                 "NonRestrictiveRelativeClauseWhereExtractor"],
                ["Graham attended Wheaton College from 1939 to 1943.",
                 "NonRestrictiveRelativeClauseWhereExtractor"],
                ["He graduated with a BA in anthropology.", "NonRestrictiveRelativeClauseWhereExtractor"],
                ["Graham attended Wheaton College to 1943. He graduated with a BA .",
                 "PrepositionalAttachedtoVPExtractor NonRestrictiveRelativeClauseWhereExtractor"],
                ["Graham attended Wheaton College from 1939 to 1943 . He graduated with a BA.",
                 "PrepositionalAttachedtoVPExtractor NonRestrictiveRelativeClauseWhereExtractor"],
                ["Graham attended Wheaton College to 1943. He graduated with a BA in anthropology .",
                 " PrepositionalAttachedtoVPExtractor NonRestrictiveRelativeClauseWhereExtractor"]]
            url_first = 'home/training2.html'
        elif item == "training example two answer": url_first = 'home/answer1.html'
        else:
            training_sample = 0
            url_first = 'home/training1.html'
        print(url_first)
        return render_template(url_first, data_dict=data,
                               syntacticrules=syntactic_rule,rules=rules,menus = list,url_build = url)