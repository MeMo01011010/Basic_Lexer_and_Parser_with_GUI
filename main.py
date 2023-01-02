from tkinter import *
import re
index1 = 1.0  # index used to keep track of the beginning of the line
index2 = 2.0  # index used to keep track of the end of the line
lineIndex = 1  # index used to keep track of which line we are analyzing

inToken = []
inTokenType = []
list = []
tokenList = []
def cutOneLineTokens(line):
    global list
    global inTokenType
    global inToken
    global tokenList
    tokenList = []
    tokens = {r'\b(if|else|int|float)\b': 'key',
              r'[0-9]+': 'int',
              r'\d+\.\d+': 'float',
              r'\b(?!if|else|int|float)\w[a-zA-Z0-9]*': 'id',
              r'(\=|\+|>|\*)': 'op',
              r'[()\:\;\"]': 'sep',
              r'\s': 'blankspace'}

    stringLit = r'[^\"]+'
    global tokenTypeList
    tokenTypeList = []
    while len(line) != 0:
        for x in tokens:
            temp = re.match(x, line)
            if temp != None:
                if tokens[x] == 'blankspace':
                    line = line[0: temp.start()] + line[temp.end()::]  # remove spaces from string
                elif tokens[x] == 'sep' and line[0] == '\"':  # if seperator is quotation mark
                    list.append("<Sep," + temp.group() + ">")
                    tokenList.append(temp.group())
                    tokenTypeList.append(tokens[x])
                    line = line[0: temp.start()] + line[temp.end()::]  # remove token from string
                    str = re.match(stringLit, line)  # after quotation mark has been removed, grab string
                    if str != None:
                        list.append("<Str," + str.group() + ">")
                        tokenList.append(temp.group())
                        tokenTypeList.append("str")
                        line = line[0: str.start()] + line[str.end()::]  # remove string
                    if tokens[x] == 'sep' and line[0] == '\"':  # grab second quotation mark after string
                        list.append("<Sep," + temp.group() + ">")
                        tokenList.append(temp.group())
                        tokenTypeList.append(tokens[x])
                        line = line[0: temp.start()] + line[temp.end()::]
                else:  # cut remaining tokens
                    list.append("<" + tokens[x] + ',' + temp.group() + ">")
                    tokenList.append(temp.group())
                    tokenTypeList.append(tokens[x])
                    line = line[0: temp.start()] + line[temp.end()::]
    #inTokenType = tokenTypeList
    return list


def nextLine():
    # outTxt.insert()
    # outTxt.insert(END, "")
    outTxt.delete('1.0', END)  # clear output textbox before inserting next set of tokens
    global lineIndex
    global index1  # starts as 1.0, used as an index for the beggining of the lines
    global index2  # stars as 2.0, used as an index for the end of the line
    tokens = cutOneLineTokens(inputTxt.get(index1, index2))  # grabbing everything in between index 1 and 2 will take one whole line
    for x in tokens:
        outTxt.insert(END, x)
        outTxt.insert(END, "\n")

    index1 = index1 + 1.0  # increment beginning of line index
    index2 = index2 + 1.0  # increment end of line index
    print(tokens)  # for testing
    print(tokenTypeList)
    inputLabel = Label(window, text="Current Processing Line: " + str(lineIndex))  # line index to increment each time
    inputLabel.grid(row=4, column=0)
    parTxt.insert(INSERT,"\n###Parse tree for line " + str(lineIndex) + "\n")
    #print(tokenList)
    parser(tokenList)
    lineIndex = lineIndex + 1
    #parser(tokenList)

def quit():
    window.destroy()  # close window when quit func is called


def accept_token():
    global inToken
    global inTokenType

    print(tokenList)
    parTxt.insert(INSERT, "     accept token from the list:" + inToken)  #tokenList[1]
    if(len(tokenList) != 0):
        inToken = tokenList.pop(0)
        inTokenType = tokenTypeList.pop(0)


def math():
    parTxt.insert(INSERT, "\n----parent node math, finding children nodes:")
    global inToken
    #global tokenTypeList
    global inTokenType
    if (inTokenType == "float"):
        parTxt.insert(INSERT, "\nchild node (internal): float")
        parTxt.insert(INSERT, "   float has child node (token):" + inToken)
        accept_token()
        exp()
    elif (inTokenType == "int"):
        parTxt.insert(INSERT, "\nchild node (internal): int")
        parTxt.insert(INSERT, "   int has child node (token):" + inToken)
        accept_token()
        exp()
    elif (inToken == "*"):
        parTxt.insert(INSERT, "\nchild node (token):" + inToken)
        accept_token()
        parTxt.insert(INSERT, "\nchild node (internal): math")
        math()

    elif (inToken == "+"):
        parTxt.insert(INSERT, "\nchild node (token):" + inToken)
        accept_token()
        parTxt.insert(INSERT, "\n   child node (internal): math")
        math()
        #else:
           # parTxt.insert(INSERT, "error, you need + or * after the int in the math")
    else:
        parTxt.insert(INSERT, "error, math expects float or int")
        return

def exp():
    parTxt.insert(INSERT, "\n----parent node exp, finding children nodes:")
    print("\n----parent node exp, finding children nodes:")
    #global tokenType
   # global tokenTypeList
   # global tokenList
    global inToken
    global inTokenType

    if(inToken == "float" and inTokenType == "key"):
        parTxt.insert(INSERT, "\nchild node (internal): keyword")
        parTxt.insert(INSERT, "   keyword has child node (token):" + inToken)
        accept_token()
    elif (inTokenType == "key"):
        #print("child node (internal): keyword")
        parTxt.insert(INSERT, "\nchild node (internal): keyword")
        parTxt.insert(INSERT, "   keyword has child node (token):" + inToken)
        #print("   keyword has child node (token):" + inToken)
        #if(inToken == "if"):
          #  if_exp()
        accept_token()
    elif (inTokenType == "id"):
      #  print("child node (internal): identifier")
        parTxt.insert(INSERT, "\nchild node (internal): identifier")
        parTxt.insert(INSERT, "   identifier has child node (token):" + inToken)
       # print("   identifier has child node (token):" + inToken)
        accept_token()
    elif(inTokenType == "int" or inTokenType == "float"):
        parTxt.insert(INSERT, "\nchild node (internal): " + inTokenType)
        parTxt.insert(INSERT, "   identifier has child node (token):" + inToken)
        # print("   identifier has child node (token):" + inToken)
        accept_token()
    else:
        parTxt.insert(INSERT, "expect identifier or keyword as the first element of the expression!")
        return

    if (inTokenType == "id"):
      #  print("child node (internal): identifier")
        parTxt.insert(INSERT, "\nchild node (internal): identifier")
        parTxt.insert(INSERT, "   identifier has child node (token):" + inToken)
       # print("   identifier has child node (token):" + inToken)
        accept_token()
    if (inToken == "*" or inToken == "+"):
        parTxt.insert(INSERT, "\nchild node (token):" + inToken)
        parTxt.insert(INSERT, "\nchild node (internal): math")
        accept_token()
        math()

    if (inToken == "="):
        parTxt.insert(INSERT, "\nchild node (token):" + inToken)
        print("child node (token):" + inToken)
        #print("TESTTESTTEST")
        accept_token()
    else:
        parTxt.insert(INSERT, "expect = as the next element of the expression!")
        print("expect = as the next element of the expression!")
        return
    if (inTokenType == "id"):
        print("child node (internal): identifier")
        parTxt.insert(INSERT, "\nchild node (internal): identifier")
        parTxt.insert(INSERT, "   identifier has child node (token):" + inToken)
        print("   identifier has child node (token):" + inToken)
        accept_token()
    elif (inTokenType == "int" or inTokenType == "float"):
        print("child node (internal): " + inTokenType)
        parTxt.insert(INSERT, "\nchild node (internal): " + inTokenType)
        parTxt.insert(INSERT,   inTokenType +" has child node (token):" + inToken)
        accept_token()
    else:
        parTxt.insert(INSERT, "expect identifier, int, or float as the next element of the expression!")
        return
    if (inToken == "*" or inToken == "+"):
        parTxt.insert(INSERT, "\nchild node (token):" + inToken)
        parTxt.insert(INSERT, "\nchild node (internal): math")
        accept_token()
        math()


def if_exp():
    parTxt.insert(INSERT, "\n----parent node if_exp, finding children nodes:")
    global inToken
    global inTokenType
    token = inToken
    if(inToken == "if"):
        parTxt.insert(INSERT, "\nchild node (internal): keyword")
        parTxt.insert(INSERT, "    keyword has child node (token):" + inToken)
        accept_token()
    else:
        parTxt.insert(INSERT, "error, you need keyword as the first element of the expression")
        return
    if(inToken == "("):
        parTxt.insert(INSERT, "\nchild node (token):" + inToken)
        accept_token()
    else:
        parTxt.insert(INSERT, "error, you need ( as second element of the expression")
        return
    comparison_exp()

    if(inToken == ")"):
        parTxt.insert(INSERT, "\nchild node (token): " + inToken)
        accept_token()
    else:
        parTxt.insert(INSERT, "error, you need ) after comparison")
        return

def printExp():
    parTxt.insert(INSERT, "\n----parent node print, finding children nodes:")
    global inToken
    global inTokenType
    if(inToken == "print"):
        parTxt.insert(INSERT, "\nchild node (internal): print")
        parTxt.insert(INSERT, "   print has child node (token):" + inToken)
        accept_token()
    if(inToken == "("):
        parTxt.insert(INSERT, "\nchild node (token):" + inToken)
        accept_token()
    else:
        parTxt.insert(INSERT, "error, you need ( as second element of the expression")
        return
    if(inTokenType == "sep"):
        parTxt.insert(INSERT, "\nchild node (token):" + inToken)
        accept_token()
    else:
        parTxt.insert(INSERT, "error, you need \" following the parenthesis in the expression")
        return
    if(inTokenType == "str"):
        parTxt.insert(INSERT, "\nchild node (token):" + inToken)
        accept_token()
    else:
        parTxt.insert(INSERT, "error, you need a string following the quotation marks in the expression")
        return
    if(inTokenType == "sep"):
        parTxt.insert(INSERT, "\nchild node (token):" + inToken)
        accept_token()
    else:
        parTxt.insert(INSERT, "error, you need \" following the string in the expression")
        return
    if(inToken == ")"):
        parTxt.insert(INSERT, "\nchild node (token):" + inToken)
        accept_token()
    else:
        parTxt.insert(INSERT, "error, you need ) after the quotation mark in the expression")
        return

def comparison_exp():
    global inToken
    global inTokenType

    global tokenType
    token = inToken
    #tempTokenType = tokenType
    parTxt.insert(INSERT, "---parent node comparison_exp, finding children nodes")
    if(inTokenType == "id"):
        parTxt.insert(INSERT, " \nchild node (internal): identifier")
        parTxt.insert(INSERT, " identifier has child node (token): " + inToken)
        accept_token()
    else:
        parTxt.insert(INSERT, " error, expected identifier or operator following expression")
        return
    if(inToken == ">"):
        parTxt.insert(INSERT, " \nchild node (internal): comparison operator")
        parTxt.insert(INSERT, " identifier has child node (token): " + inToken)
        accept_token()
    else:
        parTxt.insert(INSERT, " error, expected > following expression")
        return

    if(inTokenType == "id"):
        parTxt.insert(INSERT, " \nchild node (internal): identifier")
        parTxt.insert(INSERT, " identifier has child node (token): " + inToken)
        accept_token()
    else:
        parTxt.insert(INSERT, " error, expected identifier or operator following expression")
        return
def parser(token):
    global inToken
    global inTokenType
    inToken = tokenList.pop(0)
    inTokenType = tokenTypeList.pop(0)
    if(inToken == "if"):
        if_exp()
    elif(inToken == "print"):
        printExp()
    else:
        exp()
    if(inToken == ";"):
        parTxt.insert(INSERT, "\nparse tree building success!")
        return

    if(inToken == ':'):
        parTxt.insert(INSERT, " \nparse tree building success!")
        return
    else:
        parTxt.insert(INSERT, " \nparse tree building NOT successful")

window = Tk()
window.title("Lexical Analysis for TinyPie")

sourceLabel = Label(window, text="Source code input:")
sourceLabel.grid(row=0, column=0)

outLabel = Label(window, text="Lexical Analyzed Result:")
outLabel.grid(row=0, column=4)

inputLabel = Label(window, text="Current Processing Line: " + str(lineIndex))
inputLabel.grid(row=4, column=0)

#spacerLabel = Label(window, text="", width=10)  # create a space in between the two text boxes
#spacerLabel.grid(row=4, column=3)

inputTxt = Text(window, width=25, height=10)
inputTxt.grid(row=2, column=0)

outTxt = Text(window, width=25, height=10)
outTxt.grid(row=2, column=4)

nextButton = Button(window, text="Next Line", command=nextLine)
nextButton.grid(row=5, column=0, sticky=W)

quitButton = Button(window, text="Quit", command=quit)
quitButton.grid(row=5, column=6, sticky=E)

parLabel = Label(window, text = "Parse Tree:")
parLabel.grid(row = 0, column=6)

parTxt = Text(window, width=80, height=40)
parTxt.grid(row=2, column=6)
window.mainloop()

# int    A1=5
# float BBB2     =1034.2
# float     cresult     =     A1     +BBB2     *      BBB2
# if     (cresult     >10):
# print(“TinyPie    ”    )