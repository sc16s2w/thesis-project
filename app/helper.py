import pymysql.cursors
import sys

from app.models import SyntacticRules
from queue import PriorityQueue



def readrules_from_file(filename):
    result = []
    with open(filename, 'r') as f:
        i = 0
        for line in f:
            print(line)
            line.strip()
            # if(line == "[S/PP] ||| [NP/NP,1] such activities [VP/PP,2] ||| [NP/NP,1] those activities [VP/PP,2] ||| PPDB2.0Score=5.36156 PPDB1.0Score=3.840280 -logp(LHS|e1)=0 -logp(LHS|e2)=0 -logp(e1|LHS)=16.57635 -logp(e1|e2)=2.39790 -logp(e1|e2,LHS)=2.39790 -logp(e2|LHS)=15.62083 -logp(e2|e1)=1.44238 -logp(e2|e1,LHS)=1.44238 AGigaSim=0.71152 Abstract=0 Adjacent=0 CharCountDiff=1 CharLogCR=0.05716 ContainsX=0 Equivalence=0.601220 Exclusion=0.000016 GlueRule=0 GoogleNgramSim=0.30473 Identity=0 Independent=0.000134 Lex(e1|e2)=63.30685 Lex(e2|e1)=63.30685 Lexical=0 LogCount=0 MVLSASim=NA Monotonic=1 OtherRelated=0.000039 PhrasePenalty=1 RarityPenalty=0.01832 ForwardEntailment=0.398592 SourceTerminalsButNoTarget=0 SourceWords=2 TargetTerminalsButNoSource=0 TargetWords=2 UnalignedSource=0 UnalignedTarget=0 WordCountDiff=0 WordLenDiff=0.50000 WordLogCR=0 ||| 0-0 1-1 2-2 3-3 ||| Equivalence"):
            #     print(i)
            #     break
            if(i>1280880):
                temp = line.split("|||")
                insert_syntactic(i,temp[1],temp[2])
            i+=1
            result.append(list(line.strip('\n').split(',')))
    # print(result)
    return result


def read_lexical_rules_from_file(filename):
    result = []
    i = 0
    with open(filename, 'r') as f:
        for line in f:
            print(line)
            line.strip()
            temp = line.split("|||")
            score = temp[3].split(" ")
            ppdbscore = score[1].replace("PPDB2.0Score=","")
            ppdbscore = float(ppdbscore)

            insert_large_lexical(i,temp[1],temp[2],ppdbscore)
            i+=1
            # result.append(list(line.strip('\n').split(',')))
    # print(result)
    return result
def read_syntactic_rules_from_file(filename):
    result = []
    i = 0
    with open(filename, 'r') as f:
        for line in f:
            if(i>1970458):
                print(line)
                line.strip()
                temp = line.split("|||")
                score = temp[3].split(" ")
                ppdbscore = score[1].replace("PPDB2.0Score=","")
                ppdbscore = float(ppdbscore)
                insert_large_syntactic(i,temp[1],temp[2],ppdbscore)
            i+=1
            # result.append(list(line.strip('\n').split(',')))
    # print(result)
    return result

def insert(id, comlexWord, simpleWord):
    try:
        # 连接数据库
        connection = pymysql.connect(host='localhost', port=3306, user='root', password='Wsw981017@', db='movic',
                                    charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
        # 创建游标
        cursor = connection.cursor()
        # sql命令
        sql = "insert into lexicalRules(id,complexWord,simpleWord)" \
                " values(%s,%s,%s)"
        # 执行sql语句
        cursor.execute(sql, (
            id, comlexWord, simpleWord))
    except Exception as e:
        print(e)
    finally:
            cursor.close()
            connection.commit()
            connection.close()

def insert_large_lexical(id, comlexWord, simpleWord,score):
    try:
        # 连接数据库
        connection = pymysql.connect(host='localhost', port=3306, user='root', password='Wsw981017@', db='movic',
                                    charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
        # 创建游标
        cursor = connection.cursor()
        # sql命令
        sql = "insert into largelexicalruleswithScore(id,complexWord,simpleWord,score)" \
                " values(%s,%s,%s,%s)"
        # 执行sql语句
        cursor.execute(sql, (
            id, comlexWord, simpleWord,score))
    except Exception as e:
        print(e)
    finally:
            cursor.close()
            connection.commit()
            connection.close()

def insert_large_syntactic(id, ComlexStructure, SimpleStructure,score):
    try:
        # 连接数据库
        connection = pymysql.connect(host='localhost', port=3306, user='root', password='Wsw981017@', db='movic',
                                     charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
        # 创建游标
        cursor = connection.cursor()
        # sql命令
        sql = "insert into SyntacticRulesLargewithScore(id,ComplexStructure,SimpleStructure,score)" \
              " values(%s,%s,%s,%s)"
        # 执行sql语句
        cursor.execute(sql, (
            id, ComlexStructure, SimpleStructure,score))
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        connection.commit()
        connection.close()

def insert_syntactic(id, ComlexStructure, SimpleStructure):
    try:
        # 连接数据库
        connection = pymysql.connect(host='localhost', port=3306, user='root', password='Wsw981017@', db='movic',
                                    charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
        # 创建游标
        cursor = connection.cursor()
        # sql命令
        sql = "insert into SyntacticRules(id,ComplexStructure,SimpleStructure)" \
                " values(%s,%s,%s)"
        # 执行sql语句
        cursor.execute(sql, (
            id, ComlexStructure, SimpleStructure))
    except Exception as e:
        print(e)
    finally:
            cursor.close()
            connection.commit()
            connection.close()


def create_sample():
    list=[]
    for i in range(0,100):
        list.append(i)
    return list

def read_file():
    dict={}
    complex_sentence = []
    simple_sentence=[]
    with open("/Users/wangsiwei/Downloads/TS_T5-main_base/resources/datasets/asset/asset.test.orig", 'r') as f:
        for line in f:
            complex_sentence.append(line)
    with open("/Users/wangsiwei/Downloads/TS_T5-main_base/experiments/model_5tokens/outputs/test.txt", 'r') as f:
        for line in f:
            simple_sentence.append(line)
    for i in range(0,100):
        dict[i] = complex_sentence[i]+"#"+simple_sentence[i]
    print(dict)
    return dict

def read_syntactic_rules():
    dict_syntactic ={}
    count = 1;
    with open("/Users/wangsiwei/Downloads/python-flask-login-register-master/app/output.txt", 'r') as f:
        list = []
        for line in f:
            line = line.replace('\n', '').replace('\r', '')
            line = line.replace('<SEP>', '')
            # line = line.split('|||DisSim')

            list.append(line)
    temp = []
    for line in list:
        # print(temp)
        if line == '#':
            store = []
            for te in temp:
                t = te.split('|||DisSim')
                store.append(t)
            dict_syntactic[count]=store
            temp = []
            count+=1
        else:
            temp.append(line)
    return dict_syntactic

def delete_repeat():
    dict = read_syntactic_rules()
    dict_original = read_file()
    dict_new = {}
    for i in range(0,99):
        temp = dict[i+2]
        for list in temp:
            t1 = list[0]
            t2 = dict_original[i].split("#")[0]
            print(t1)
            print(t2)
            if(list[0]==dict_original[i][0]):
                dict[i+2].remove(list)
        print(dict[i+2])

def search_syntactic_rules(complexword):
    rules = SyntacticRules.query.filter(SyntacticRules.ComplexStructure.like(complexword))
    for rule in rules:
        print(rule.ComplexStructure,rule.SimpleStructure)
    # print(rule)

def initializaData():
    q = PriorityQueue()
    for i in range(0,100):
        q.put((0,i))
    userMap = {}
    # next_item = q.get()
    # q.put((next_item[0],next_item[1]+1))
    # # print(q.get())
    # # print(next_item[1])
    # while not q.empty():
    #     next_item = q.get()
    #     print(next_item)
    return q,userMap

def insert_sentence(id, frequency):
    try:
        # 连接数据库
        connection = pymysql.connect(host='localhost', port=3306, user='root', password='Wsw981017@', db='movic',
                                    charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
        # 创建游标
        cursor = connection.cursor()
        # sql命令
        sql = "insert into Sentence(id,frequency)" \
                " values(%s,%s)"
        # 执行sql语句
        cursor.execute(sql, (
            id, frequency))
    except Exception as e:
        print(e)
    finally:
            cursor.close()
            connection.commit()
            connection.close()

def all_insert_sentence():
    for i in range(0,101):
        insert_sentence(i,0)
# if __name__=="__main__":
#     # readrules_from_file("/Users/wangsiwei/Downloads/ppdb-2.0-s-lexical")
#     # insert(4,"dd",6)
#     # dict = read_syntactic_rules()
#     # print(dict)
#     # initializaData()
#     # search_syntactic_rules('%'+'combination'+'%')
#     # search_syntactic_rules('%'+'NP'+"%"+'DT'+"%" +"the"+'%'+"NN"+"%"+ "city"+"%")
#     # read_lexical_rules_from_file("/Users/wangsiwei/Downloads/ppdb-2.0-xl-lexical")
#     # read_syntactic_rules_from_file("/Users/wangsiwei/Downloads/ppdb-2.0-l-syntax")
#     all_insert_sentence()
