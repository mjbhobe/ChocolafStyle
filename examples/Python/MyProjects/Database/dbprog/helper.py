words = """
and,as,assert,break,class,continue,def,del,elif,else,
except,eval,finally,for,from,global,if,import,in,is,lambda,
nonlocal,not,or,pass,raise,repr,return,str,try,while,with,yield,
int,float,complex,list,tuple,dict,bool,set
"""

wordlist = []

for word in words.split(","):
    word = word.strip()
    wordlist.append(word)
print(f"Original count: {len(wordlist)}")

# create a sorted list of unique words
wordlist = sorted(list(set(wordlist)))
print(f"Final count: {len(wordlist)}")
wordlist_str = ",".join(wordlist)
print(wordlist_str)

print("Other info")
list_type = []
tuple_type = ()
dict_type = {}
print(type(list_type), type(tuple_type), type(dict_type))
