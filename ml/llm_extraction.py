





def extract(text):
    '''extract and format useful information from text using llama llm'''
    r = {
        'uid': "",
        'title':"",
        'due_date':'', 
    }




import time

def f1():
    for i in range(10):
        yield i
        time.sleep(0.5)

def f2():
    return f1()



for i in f2():
    print(i)



