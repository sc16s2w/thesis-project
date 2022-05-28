import copy
import json
import re
from collections import deque
## the three function are used for the lexical part.

## this function is write to find the different words in the simple sentence compared with the complex one
# def find_different_words(complex_sentence,simple_sentence):
#     retD = list(set(simple_sentence).difference(set(complex_sentence)))
#     print(retD)



# ## this function is going to solve the corrospending efficient word
# def find_according_effcient_word:


## find the same rules exsist in the databse:
from sqlalchemy import and_

from app.models import LexicalRules, SyntacticRules, largelexicalRules, SyntacticRulesLargewithScore, \
    largelexicalruleswithScore

pos_taggers = ['CC','CD','DT','EX','FW','IN','JJ','JJR','JJS','LS',
               'MD','NN','NNS','NNP','NNPS','IN','PDT','POS','PRP',
               'RB','RBR','RBS','RP','SYM','TO','UH','VB','VBD','VBG',
               'VBN','VBP','VBZ','WDT','WP','WRB']

## 多个数据来判断应该用rule
def find_lexical_rules(filename):
    rules = []
    count  = 0
    input_original = []
    output_original = []
    with open('/Users/wangsiwei/Downloads/TS_T5-main_base/experiments/model_5tokens/outputs/test.txt', 'r') as f:
        for line in f:
            output_original.append(line.strip('\n'))
    with open('/Users/wangsiwei/Downloads/TS_T5-main_base/resources/datasets/asset/asset.test.orig', 'r') as f:
        for line in f:
            input_original.append(line.strip('\n'))
    with open(filename, 'r') as f:
        for line in f:
            line = line.replace('\n', '').replace('\r', '')
            if line == '&':
                rules.append(line)
            else:
                print(line)
                line = line.replace('\n', '').replace('\r', '')
                temp = line.split("#")
                rules.append([temp[0],temp[1]])
    print(rules)
    l=set()
    f = open("store_lexical_rules_100examples.txt", "w")
    f.write("&" + '\n')
    for rule in rules:
        if(rule=='&'):
            print(count)
            f.write(str(count)+"\n")
            print("input sentence",input_original[count])
            f.write(input_original[count]+"\n")
            print("output sentence",output_original[count])
            f.write(output_original[count]+"\n")
            count+=1
            print("rules")
            f.write("rules"+"\n")
        else:
            # print(rule)
            filterList = []
            filterList = (largelexicalruleswithScore.ComplexWord==' ' + rule[1]+" ")
            filterList = and_(filterList,largelexicalruleswithScore.SimpleWord==' ' + rule[0]+" ")
            collects =largelexicalruleswithScore.query.filter(filterList).order_by(largelexicalruleswithScore.score.desc()).limit(5)
            for collect in collects:
                f.write(collect.ComplexWord+"->"+collect.SimpleWord+"\n")
                print(collect.ComplexWord+"->"+collect.SimpleWord)
                l.add(collect.ComplexWord+"->"+collect.SimpleWord)
    # print("rules find in the ppdb")
    # print(l)

# ## 找出syntactic的子树
def find_subtrees(tree):
    tree = tree.replace(" ", "")
    print(tree)
    temp = list(tree)
    stack = deque()
    result = []
    i=0
    while(i<len(temp)):
        if temp[i]=='(':
            stack.append(temp[i])
        elif temp[i] == ')':
            j = i
            list_temp = deque()
            while(len(stack)!=0 and stack[len(stack)-1] !='(' ):
                list_temp.append(stack.pop())
                j+=1
            stack.pop()
            i = j-1
            te = list(reversed(list_temp))
            t = te.copy()
            # if(len(t)!=0):
            result.append(t)
            while len(te)!=0:
                stack.append(te.pop())
        else:
            j = i
            str = ""
            while(j<len(temp) and (temp[j].isalpha() or temp[j]==","or temp[j]=='.')):
                # if str in pos_taggers:
                #     stack.append(str)
                #     str = ""
                str+=temp[j]
                j+=1
            stack.append(str)
            i = j-1
        i+=1
    print(result)

def test_lexicalrules(complex_word, simple_word):
    filterList = (largelexicalRules.complexWord == complex_word)
    # filterList = and_(filterList, LexicalRules.SimpleWord.contains(simple_word))
    collects = largelexicalRules.query.filter(filterList)
    # print("rule")
    for collect in collects:
        print(collect.complexWord + "->" + collect.simpleWord)

## search databse to find corresponding syntactic rules
def find_syntactic_rules(filename):
    rules = []
    count = 0
    input_original = []
    output_original = []
    with open('/Users/wangsiwei/Downloads/TS_T5-main_base/experiments/model_5tokens/outputs/test.txt', 'r') as f:
        for line in f:
            output_original.append(line.strip('\n'))
    with open('/Users/wangsiwei/Downloads/TS_T5-main_base/resources/datasets/asset/asset.test.orig', 'r') as f:
        for line in f:
            input_original.append(line.strip('\n'))
    with open(filename, 'r') as f:
        for line in f:
            line = line.replace('\n', '').replace('\r', '')
            if line == '&':
                rules.append(line)
            else:

                line = line.replace('\n', '').replace('\r', '')
                temp = line.split("#")
                rules.append([temp[0], temp[1]])
    # print(rules)
    l = {}
    f = open("syntactic_rules_100examples.txt", "w")
    for rule in rules:
        if (rule == '&'):
            f.write("&" + '\n')
            f.write(input_original[count]+"\n")
            f.write(output_original[count] + "\n")
            f.write("rules" + '\n')
            if(count>0): l[str(count)] = store
            store = {}
            count+=1
        else:
            print(rule)
            filterList = (SyntacticRulesLargewithScore.SimpleStructure.contains(rule[0]))
            filterList = and_(filterList,SyntacticRulesLargewithScore.ComplexStructure.contains(rule[1]))
            collects = SyntacticRulesLargewithScore.query.filter(filterList).order_by(SyntacticRulesLargewithScore.score.desc()).limit(5)
            print("rule")
            temp = []
            length = 0
            for collect in collects:
                collect_list_complex = collect.ComplexStructure.split(" ")
                collect_list_simple = collect.SimpleStructure.split(" ")
                flagComplex = False
                flagSimple = False
                print(rule[0]+" "+rule[1])
                for complex_example in collect_list_complex:
                    print(complex_example)
                    complex_example = complex_example.replace(" ", "")
                    if complex_example==rule[1]:flagComplex = True
                for simple in collect_list_simple:
                    print(simple)
                    simple = simple.replace(" ","")
                    if simple==rule[0]:flagSimple = True
                if flagComplex and flagSimple:
                    f.write(collect.ComplexStructure+"->"+collect.SimpleStructure+"->"+str(collect.score)+"\n")
                    temp.append(collect.ComplexStructure+"->"+collect.SimpleStructure+"->"+str(collect.score))
                    print(collect.ComplexStructure+" "+collect.SimpleStructure+"->"+str(collect.score))
                length += 1

            key = rule[0]+"->"+rule[1]

            # temp.append('[PP/NP,1] [PP/NP,2] made a significant contribution [PP/RP,1] [PP/RB,1] -> [PP/NP,1] [PP/NP,2] made a significant contribution [PP/RP,1] [PP/RB,1]  ')
            store[key] = temp
    return l

def readfile(filename):
    count = 0
    with open(filename, 'r') as f:
        for line in f:
            if count==1:break
            print(line)
            count+=1


class syntactic_tree_store:
    def __init__(self,pre1,pre2, word,post1,post2,complex_syntactic_structure,simple_syntactic_structure,
                 ispre1,ispre2,ispost1,ispost2):
        self.pre1 = pre1
        self.pre2 = pre2
        self.word = word
        self.post1 = post1
        self.post2 = post2
        self.complex_syntactic_structure = complex_syntactic_structure
        self.simple_syntactic_structure = simple_syntactic_structure
        self.ispre1 = ispre1
        self.ispre2 = ispre2
        self.ispost1 = ispost1
        self.ispost2 = ispost2

    def tostring(self):
        return "pre1 "+self.pre1+" pre2 "+self.pre2+\
                " word "+self.word+" post1 "+self.post1+" post2 "+self.post2\
                 +" comple syntactic stucture "+self.complex_syntactic_structure\
                + " simple syntactic structure "+self.simple_syntactic_structure+\
                " ispre1 "+str(self.ispre1)+" ispre2 "+str(self.ispre2)+" ispost1 "+str(self.ispost1)\
               +" ispost2 "+str(self.ispost2)

##match simple syntactic tree
def find_syntactictree(filename,l):
    syntactic_tree = []
    with open(filename, 'r') as f:
        for line in f:
            syntactic_tree.append(line.strip('\n'))
    f.close()
    syntactic_tree_complex = []
    with open("/Users/wangsiwei/Downloads/python-flask-login-register-master/app/store_syntactic_input.txt", 'r') as f:
        for line in f:
            syntactic_tree_complex.append(line.strip('\n'))
    f.close()
    output_original = []
    with open('/Users/wangsiwei/Downloads/TS_T5-main_base/experiments/model_5tokens/outputs/test.txt', 'r') as f:
        for line in f:
            output_original.append(line.strip('\n'))
    f.close()
    input_original = []
    with open('/Users/wangsiwei/Downloads/TS_T5-main_base/resources/datasets/asset/asset.test.orig', 'r') as f:
        for line in f:
            input_original.append(line.strip('\n'))
    f.close()
    f = open("/Users/wangsiwei/Downloads/python-flask-login-register-master/app/test.txt", "w")
    for count in range(0,len(l)):

        # f.write(input_original[count])
        # f.write('\n')
        # # f.write("simple sentence\n")
        # f.write(output_original[count])
        # f.write('\n')
        f.write("&"+"\n")
        syntactic_tree_list = split(syntactic_tree[count],output_original[count])
        lists = l[str(count+1)]
        for key, value in lists.items():
            if len(value) == 0: continue
            tempkey = key.split("->")
            word = tempkey[0]
            index = 0
            for i in range(0,len(syntactic_tree_list)):
                if re.search(word, syntactic_tree_list[i]) is not None:
                    index = i
                    break

            for val in value:
                pre1 = ""
                pre2 = ""
                post1 = ""
                post2 = ""
                ispre1 = True
                ispost1 = True
                ispre2 = True
                ispost2 = True
                temp = val.split("->")
                temps = temp[1].split(" ")
                m = 0
                for j in range(0,len(temps)):
                    if temps[j]==word:
                        m=j
                        break

                if m == 0: continue
                flagpre = 0
                flagpost = 0
                print(temps)
                for j in range(1, len(temps)):
                    n = temps[j]
                    if(flagpre==0 and len(n)>0 and n[0]=='['and j<m):
                        pre1 = temps[j]
                        flagpre+=1
                    elif(flagpre==1 and len(n)>0 and n[0]=='['and j<m):
                        pre2 = temps[j]
                    elif(flagpost ==0 and len(n)>0 and n[0]=='[' and j>m):
                        post1 = temps[j]
                        flagpost+=1
                    elif (flagpost == 1 and len(n) > 0 and n[0] == '[' and j > m):
                        post2 = temps[j]
                if pre1 != "":
                    ispre1 = False
                    pre1 = pre1.replace("[","")
                    pre1 = pre1.replace("]","")
                    t = []
                    first = "#"
                    second = "#"
                    if("/" in pre1):
                        t = pre1.split("/")
                        first = t[0]
                        second = t[1]
                    elif("\\" in pre1):
                        t = pre1.split("\\")
                        first = t[0]
                        second = t[1]
                    else:
                        first = pre1
                    flag_no_num_first = False
                    flag_no_num_second = False
                    if "," not in first:
                        flag_no_num_first = True
                    if "," not in second:
                        flag_no_num_second = True
                    for i in range(0, index):
                        if syntactic_tree_list[i] == first or syntactic_tree_list[i] == second:
                            ispre1 = True
                        if flag_no_num_first and re.search(first, syntactic_tree_list[i]) is not None:
                            ispre1 = True
                        if flag_no_num_second and re.search(second, syntactic_tree_list[i]) is not None:
                            ispre1 = True
                if pre2 != "":
                    ispre2 = False
                    pre2 = pre2.replace("[", "")
                    pre2 = pre2.replace("]", "")
                    t = []
                    first = "#"
                    second = "#"
                    if ("/" in pre2):
                        t = pre2.split("/")
                        first = t[0]
                        second = t[1]
                    elif ("\\" in pre2):
                        t = pre2.split("\\")
                        first = t[0]
                        second = t[1]
                    else:
                        first = pre2
                    flag_no_num_first = False
                    flag_no_num_second = False
                    if "," not in first:
                        flag_no_num_first = True
                    if "," not in second:
                        flag_no_num_second = True
                    for i in range(0, index):
                        if syntactic_tree_list[i] == first or syntactic_tree_list[i] == second:
                            ispre2 = True
                        if flag_no_num_first and re.search(first, syntactic_tree_list[i]) is not None:
                            ispre2 = True
                        if flag_no_num_second and re.search(second, syntactic_tree_list[i]) is not None:
                            ispre2 = True
                if post1 != "":
                    ispost1 = False
                    post1 = post1.replace("[", "")
                    post1 = post1.replace("]", "")
                    t = []
                    first = "#"
                    second = "#"
                    if ("/" in post1):
                        t = post1.split("/")
                        first = t[0]
                        second = t[1]
                    elif ("\\" in post1):
                        t = post1.split("\\")
                        first = t[0]
                        second = t[1]
                    else:
                        first = post1
                    flag_no_num_first = False
                    flag_no_num_second = False
                    if "," not in first:
                        flag_no_num_first = True
                    if "," not in second:
                        flag_no_num_second = True
                    for i in range(0, index):
                        if syntactic_tree_list[i] == first or syntactic_tree_list[i] == second:
                            ispost1 = True
                        if flag_no_num_first and re.search(first, syntactic_tree_list[i]) is not None:
                            ispost1 = True
                        if flag_no_num_second and re.search(second, syntactic_tree_list[i]) is not None:
                            ispost1 = True
                if post2 != "":
                    ispost2 = False
                    post2 = post2.replace("[", "")
                    post2 = post2.replace("]", "")
                    t = []
                    first = "#"
                    second = "#"
                    if ("/" in post2):
                        t = post2.split("/")
                        first = t[0]
                        second = t[1]
                    elif ("\\" in post2):
                        t = post2.split("\\")
                        first = t[0]
                        second = t[1]
                    else:
                        first = post2
                    flag_no_num_first = False
                    flag_no_num_second = False
                    if "," not in first:
                        flag_no_num_first = True
                    if "," not in second:
                        flag_no_num_second = True
                    for i in range(0, index):
                        if syntactic_tree_list[i] == first or syntactic_tree_list[i] == second:
                            ispost2 = True
                        if flag_no_num_first and re.search(first, syntactic_tree_list[i]) is not None:
                            ispost2 = True
                        if flag_no_num_second and re.search(second, syntactic_tree_list[i]) is not None:
                            ispost2 = True
                example = syntactic_tree_store(pre1,pre2,word,post1,post2,temp[0],temp[1],ispre1,ispre2,ispost1,ispost2)
                complex_example = complex_example_create(syntactic_tree_complex,input_original,key,val,count)
                print(example.tostring())
                if(example.ispre1 and example.ispre2 and example.ispost1 and example.ispost2 and complex_example.ispre1
                        and complex_example.ispre2 and complex_example.ispost1 and complex_example.ispost2):
                    # f.write("complex sentence\n")
                    # f.write("syntactic tree\n")
                    # f.write(str(syntactic_tree_list))
                    # f.write('\n')
                    # f.write("simple example\n")
                    print(example.tostring())
                    now = example.complex_syntactic_structure+"->"+example.simple_syntactic_structure
                    res = replace_syntactic_rules_with_understandble_words(now)
                    f.write(res+'\n')
                    # f.write("complex examplre\n")
                    # f.write(complex_example.tostring() + '\n')

    # print(syntactic_tree)

##match complex syntactic tree
def complex_example_create(syntactic_tree, input_original,key,value,count):
    tempkey = key.split("->")
    word = tempkey[1]
    index = 0
    syntactic_tree_list = split(syntactic_tree[count - 1], input_original[count - 1])
    for i in range(0, len(syntactic_tree_list)):
        if re.search(word, syntactic_tree_list[i]) is not None:
            index = i
            break
    print(index)
    pre1 = ""
    pre2 = ""
    post1 = ""
    post2 = ""
    ispre1 = True
    ispost1 = True
    ispre2 = True
    ispost2 = True
    temp = value.split("->")
    temps = temp[0].split(" ")
    m = 0
    for j in range(0, len(temps)):
        if temps[j] == word:
            m = j
            break
    flagpre = 0
    flagpost = 0
    for j in range(1, len(temps)):
        n = temps[j]
        if (flagpre == 0 and len(n) > 0 and n[0] == '[' and j < m):
            pre1 = temps[j]
            flagpre += 1
        elif (flagpre == 1 and len(n) > 0 and n[0] == '[' and j < m):
            pre2 = temps[j]
        elif (flagpost == 0 and len(n) > 0 and n[0] == '[' and j > m):
            post1 = temps[j]
            flagpost += 1
        elif (flagpost == 1 and len(n) > 0 and n[0] == '[' and j > m):
            post2 = temps[j]

    if pre1 != "":
        ispre1 = False
        pre1 = pre1.replace("[", "")
        pre1 = pre1.replace("]", "")
        t = []
        first = "#"
        second = "#"
        if ("/" in pre1):
            t = pre1.split("/")
            first = t[0]
            second = t[1]
        elif ("\\" in pre1):
            t = pre1.split("\\")
            first = t[0]
            second = t[1]
        else:
            first = pre1
        if "," not in first:
            first = first + "," + "1"
        if "," not in second:
            second = second + "," + "1"
        for i in range(0, index):
            if syntactic_tree_list[i] == first or syntactic_tree_list[i] == second:
                ispre1 = True
    if pre2 != "":
        ispre2 = False
        pre2 = pre2.replace("[", "")
        pre2 = pre2.replace("]", "")
        t = []
        first = "#"
        second = "#"
        if ("/" in pre2):
            t = pre2.split("/")
            first = t[0]
            second = t[1]
        elif ("\\" in pre2):
            t = pre2.split("\\")
            first = t[0]
            second = t[1]
        else:
            first = pre2
        if "," not in first:
            first = first + "," + "1"
        if "," not in second:
            second = second + "," + "1"
        for i in range(0, index):
            if syntactic_tree_list[i] == first or syntactic_tree_list[i] == second:
                ispre2 = True
    if post1 != "":
        ispost1 = False
        post1 = post1.replace("[", "")
        post1 = post1.replace("]", "")
        t = []
        first = "#"
        second = "#"
        if ("/" in post1):
            t = post1.split("/")
            first = t[0]
            second = t[1]
        elif ("\\" in post1):
            t = post1.split("\\")
            first = t[0]
            second = t[1]
        else:
            first = post1
        if "," not in first:
            first = first + "," + "1"
        if "," not in second:
            second = second + "," + "1"
        print("first", first)
        print("second", second)
        for i in range(index, len(syntactic_tree_list)):
            if syntactic_tree_list[i] == first or syntactic_tree_list[i] == second:
                ispost1 = True
    if post2 != "":
        ispost2 = False
        post2 = post2.replace("[", "")
        post2 = post2.replace("]", "")
        t = []
        first = "#"
        second = "#"
        if ("/" in post2):
            t = post2.split("/")
            first = t[0]
            second = t[1]
        elif ("\\" in post2):
            t = post2.split("\\")
            first = t[0]
            second = t[1]
        else:
            first = post2
        if "," not in first:
            first = first + "," + "1"
        if "," not in second:
            second = second + "," + "1"
        for i in range(index, len(syntactic_tree_list)):
            if syntactic_tree_list[i] == first or syntactic_tree_list[i] == second:
                ispost2 = True
    example = syntactic_tree_store(pre1, pre2, word, post1, post2, temp[0], temp[1], ispre1, ispre2, ispost1,
                                    ispost2)
    return example

def split(tree,original_sentence):
    tree = list(tree)
    original_sentence = original_sentence.replace(".","")
    original_sentence = original_sentence.replace("-","")
    original_sentence = original_sentence.split(" ")
    result = []
    i = 0
    while (i < len(tree)):
        if(tree[i].isalpha() or tree[i] == "," or tree[i] == '.'):
            j = i
            stre = ""
            while (j < len(tree) and (tree[j].isalpha() or tree[j] == "," or tree[j] == '.')):
                stre+=tree[j]
                j+=1
            result.append(stre)
            i = j-1
        i +=1
    i = 0
    j = 0
    final_result = []
    while(i<len(result) and j<len(original_sentence)):
        if original_sentence[j] not in result[i]:
            final_result.append(result[i])
            i+=1
        else:
            index = result[i].find(original_sentence[j])
            final_result.append(result[i][0:index])
            final_result.append(result[i][index:len(result[i])])
            i+=1
            j+=1
    dict = {}
    copyresult  = copy.copy(final_result)
    for i in range(0,len(copyresult)):
        if final_result[i] in dict.keys():
            j =dict[final_result[i]]+1
            j = str(j)
            copyresult[i] = copyresult[i]+","+j
            dict[final_result[i]] = dict[final_result[i]]+1
        else:
            copyresult[i] = copyresult[i] + "," + "1"
            dict[final_result[i]] = 1
    return copyresult

def test_syntactic_search(complexword,simpleword):
    filterList = (SyntacticRules.SimpleStructure.contains(simpleword))
    filterList = and_(filterList, SyntacticRules.ComplexStructure.contains(complexword))
    collects = SyntacticRules.query.filter(filterList)
    for collect in collects:
        print(collect.ComplexStructure+"->"+collect.SimpleStructure)

def replace_syntactic_rules_with_understandble_words(rule):
    rules = rule.split("->")
    pre = rules[0].split(" ")
    res = ""
    for word in pre:
        print(word)
        if len(word)>0 and word[0]== '[':
            res+=relace_single_syntactic(word)+" "
        else:
            res+=word+" "
    res+="->"
    post = rules[1].split(" ")
    for word in post:
        if len(word)>0 and word[0]== '[':
            res+=relace_single_syntactic(word)+" "
        else:
            res+=word+" "
    return res


def relace_single_syntactic(rule):
    store  =set()
    dict = {"CC": "Coordinating conjunction", "CD": "number", "DT": "Determiner", "EX": "there type words",
            "FW": "Foreign word", "IN": "Preposition or subordinating conjunction", "JJ": "Adjective",
            "JJR": "Adjective", "JJS": "Adjective", "LS": "List item marker", "MD": "Modal", "NN": "Noun",
            "NNS": "Noun", "NNP": "Noun", "NNPS": "Noun", "PDT": "Predeterminer", "POS": "Possessive ending",
            "PRP": "pronoun", "RB": "Adverb", "RBR": "Adverb", "RBS": "Adverb", "RP": "Particle", "SYM": "Symbol",
            "TO": "to", "UH": "Interjection", "VB": "Verb", "VBD": "Verb", "VBG": "Verb", "VBN": "Verb", "VBP": "Verb",
            "VBZ": "Verb", "WDT": "determiner", "WP": "pronoun", "WP": "pronoun", "WRB": "Wh-adverb",
            "SBAR": "Subordinate Clause","S":"simple declarative clause", "SBARQ":"Direct question(eg: when)",
            "SQ": "Inverted yes/no question","ADJP":"Adjective Phrase","ADVP":"Adverb Phrase","CONJP":"Conjunction Phrase",
            "FRAG":"Fragment","INTJ":"Interjection","LST":"List marker", "NAC": "Not a Constituent; used to show the scope of certain prenominal modifiers within an NP",
            "NP":"Noun Phrase","NX":"Used within certain complex NPs to mark the head of the NP",
            "PP":"Prepositional Phrase", "PRN":"Parenthetical","PRT": "Particle","QP":"Quantifier Phrase",
            "RRC":"Reduced Relative Clause","UCP":"Unlike Coordinated Phrase","VP":"Verb Phrase","WHADJP":"Wh-adjective Phrase",
            "WHAVP":"Wh-adverb Phrase","WHNP":"Wh-noun Phrase","WHPP":"Wh-prepositional Phrase","X":"Unknown",
            }
    res= "["
    rule = rule.replace("[","")
    rule = rule.replace("]","")
    first = ""
    second = ""
    if ("/" in rule):
        t = rule.split("/")
        first = t[0]
        second = t[1]
    elif ("\\" in rule):
        t = rule.split("\\")
        first = t[0]
        second = t[1]
    else:
        first = rule
    flag_first = False
    flag_second = False
    store_first = []
    store_second = []
    if "," in first:
        store_first = first.split(",")
        first = store_first[0]
        flag_first = True
    if "," in second:
        store_second = second.split(",")
        second = store_second[0]
        flag_second = True
    if first in dict.keys():
        first = dict[first]
    if second in dict.keys():
        second = dict[second]
    res+=first
    store.add(first)
    if second != "" and second not in store:
        res+=" or "
        res+=second
    res+="]"
    return res

def show_different_words(filename):
    dict = {}
    count = 0
    rules = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.replace('\n', '').replace('\r', '')
            if line == '&':
                if count!=0: dict[count] = rules
                count += 1
                rules = []
            else:
                line = line.replace('\n', '').replace('\r', '')
                temp = line.split("#")
                rules.append([temp[0], temp[1]])
    for key,val in dict.items():
        temp = {}
        for l in val:
            if(l[0] in temp.keys()):
                r = temp[l[0]]
                r.append(l[1])
            else:
                r = []
                r.append(l[1])
                temp[l[0]] = r
        dict[key] = temp
    return dict

def show_different_rules(filename):
    dict = {}
    count = 0
    rules = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.replace('\n', '').replace('\r', '')
            if line == '&':
                if count!=0: dict[count] = rules
                count += 1
                rules = []
            else:
                line = line.replace('\n', '').replace('\r', '')
                # temp = line.split("->")
                rules.append(line)
    return dict

def show_different_rules_syntactic(filename):
    dict = {}
    count = 0
    rules = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.replace('\n', '').replace('\r', '')
            if line == '&':
                if count!=0: dict[count] = rules
                count += 1
                rules = []
            else:
                line = line.replace('\n', '').replace('\r', '')
                rules.append(line)
    return dict

if __name__ =='__main__':
    # print(show_different_rules("/Users/wangsiwei/Downloads/python-flask-login-register-master/app/lexical_rules_input.txt"))
    # readfile("/Users/wangsiwei/Downloads/python-flask-login-register-master/app/store_syntactic_output.txt")
    # tree = "(ROOT   (S     (NP (PRP It))     (VP (VBZ is)       (ADJP (VBN situated)         (PP (IN at)           (NP             (NP (DT the) (NN coast))             (PP (IN of)               (NP                 (NP (DT the) (NNP Baltic) (NNP Sea))                 (, ,)                 (SBAR                   (WHADVP (WRB where))                   (S                     (NP (PRP it))                     (VP (VBZ encloses)                       (NP                         (NP (DT the) (NN city))                         (PP (IN of)                           (NP (NNP Stralsund)))))))))))))     (. .)))"
    # find_subtrees(tree)
    # find_lexical_rules("/Users/wangsiwei/Downloads/TS_T5-main_base/store_simple.txt")
    # test_lexicalrules(" extremely "," like")
    # print(split(['(ROOT(S(NP(NP(CDOne)(NNside))(PP(INof)(NP(DTthe)(JJarmed)(NNSconflicts))))(VP(VBZis)(VP(VBNmade)(PRT(RPup))(ADVP(RBmainly))(PP(INof)(NP(NP(DTthe)(JJSudanese)(JJmilitary))(SBAR(S(NP(DTThe)(NNJanjaweed))(VP(VBZis)(NP(NP(DTa)(JJSudanese)(NNmilitia)(NNgroup))(SBAR(S(NP(PRPThey))(VP(VBPare)(ADVP(RBmostly))(PP(INfrom)(NP(DTthe)(NNPAfroArab)(NNPAbbala)(NNStribes)))(PP(INin)(NP(NP(DTthe)(JJnorthern)(NNPRizeigat)(NNregion))(PP(INof)(NP(NNPSudan))))))))))))))))))'],"One side of the armed conflicts is made up mainly of the Sudanese military. The Janjaweed is a Sudanese militia group. They are mostly from the AfroArab Abbala tribes in the northern Rizeigat region of Sudan."))
    # l = find_syntactic_rules("/Users/wangsiwei/Downloads/TS_T5-main_base/store_simple.txt")
    # js = json.dumps(l)
    # file = open('/Users/wangsiwei/Downloads/python-flask-login-register-master/app/syntactic_rules.txt', 'w')
    # file.write(js)
    # print(l)
    # test_syntactic_search("principal","main")
    # print(show_different_rules_syntactic("/Users/wangsiwei/Downloads/python-flask-login-register-master/app/test.txt"))
    file = open('/Users/wangsiwei/Downloads/python-flask-login-register-master/app/syntactic_rules.txt', 'r')
    js = file.read()
    l = json.loads(js)
    find_syntactictree("/Users/wangsiwei/Downloads/python-flask-login-register-master/app/store_syntactic_output.txt",l)
