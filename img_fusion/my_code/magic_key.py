import os
import random
# import Class
import json


# key = 'SC00-PC00PR45GR04PP03WK00BF00NC00UC00-0000'
# key = 'SC00-BC01BF05NF07NC02US05BP05-0000'

def magic_key_generator(rule):
    pass


def key_code_to_dict(key_code):
    lexiconDict = {}
    lexiconLen = len(key_code)
    for x in range(lexiconLen):
        lexicon = key_code[x]
        startLetter = lexicon[0]
        dictLexicons = lexiconDict.get(startLetter, {})
        # 空字典说明没有Key,则添加Key;否则追加Key对应的Value
        if len(dictLexicons) == 0:
            lexiconDict[startLetter] = {key_code[x][1]: key_code[x][2:]}
        else:
            dictLexicons[key_code[x][1]] = key_code[x][2:]
            pass

    return lexiconDict


def dict2obj(obj, dict):
    obj.__dict__.update(dict)
    return obj


def dict_to_obj(d):
    top = type('new', (object,), d)
    seqs = tuple, list, set, frozenset
    for i, j in d.items():
    	if isinstance(j, dict):
    	    setattr(top, i, dict_to_obj(j))
    	elif isinstance(j, seqs):
    	    setattr(top, i, 
    		    type(j)(dict_to_obj(sj) if isinstance(sj, dict) else sj for sj in j))
    	else:
    	    setattr(top, i, j)
    return top


def magic_key_parsing(magic_key):
    key_code = []
    # img_code = list('PGWF')
    # text_code = list('BNUEIR')
    key_list = magic_key.split('-')
    # print(img_code)

    for i in range(0, len(key_list[1]), 4):
        key_code.append(key_list[1][i:i+4])

    key_code.sort()
    obj_dict = key_code_to_dict(key_code)
    # dict to json
    # json.dumps(obj_dict)
    return obj_dict


if __name__ == "__main__":
    # magic_key_parsing(key)
    pass
