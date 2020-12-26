# A_Calculator
Create a simple version of the calculator without UI.

# Lesson 1 - A Calculator
**~本節課的目標是實現一個簡易版本的計算器~**


## A - 簡化要求，先進行 “+” 和 “-” 的運算實現
### 1. 對要求進行粗劣的整體構思

因为不考慮運算優先級的話，運算的本質是一步一步來的，例如 “a+b-c”，實質上是先進行了 ”a+b“ 的運算，得到了 ”a+b=d” 的結果後，再進行 “d-c” 的運算的。

如果能讓程序像人一樣，識別出來哪個是運算子，哪個是運算元的話，那整個步驟就會變得簡單。根據這個思路，我們先將算式中的元素獨立出來，把它們看作一個處理好的列表，按照一定順序把它們分類出來，進行計算時再根據需求把它們一個個地取出來就可以得到結果了。

這時我們瞭解到，有一種計算方式十分符合我們的要求，而且因為它不同於日常的表達方式，甚至不需要括號就能優秀地表達出運算的優先級，它就是「逆波蘭表示法」。

我們引入棧的概念，首先設置兩個棧，然後可以通過壓棧的方式得到計算結果：
`遍歷需要進行計算的算式, 得到列表 [‘a’, ‘+’, ‘b’, ‘-‘, ‘c’]`
由此可見，我們把數字進行類型轉換，變為float型放入數字棧，把運算子放入運算子棧。這樣循環進行下去，到第三步時，我們發現要把 “-” 入棧，這時候我們的兩個棧是這個樣子的：
`運算元棧: ['a', 'b']`
`運算子棧: ['+']`
由於 “-” 和 “+” 是相同優先級的運算子，那這種時候我們按照一般的四則運算法則，從左往右計算，所以此處不再無腦把 “-” 也入棧，而是：

1. 彈出運算元棧中的最後兩個數字，即 “b” 和 “a” 
2. 彈出運算子棧中的最後一個運算子 ”+“
3. 將拿出來的三個元素進行計算，即  b + a = d
4. 把得到的結果重新放回運算元棧，代替之前的 “a” 和 ”b“

那麼目前的兩個棧是這個樣子的：
`運算元棧: [‘d’]`
`運算子棧: [ ]`

此時的運算子棧為空，我們應當把剛才進行判斷的 ”-“ 入棧。當然如果一輪判斷過後運算子棧還有其他的運算符，那麼等待入棧的運算子還要繼續進行比較，直到可以入棧。

### 2. 總結大致流程並進行偽代碼實現

```
將算式整理成列表 formula_list									   
進行循環, 依次取出列表中的元素e									   
	if e 是數字:													   
		放入運算元棧 num_stack, 獲取下一個元素 e   					   
	else e 不是數字(即為運算子):									   
		放入運算子棧 op_stack, 獲取下一個元素 e				  		   
```

分析過後我們可以簡單總結成為幾個函數：
1. 把算式轉換為列表的函數
2. 判斷元素 e 是運算元還是運算子的函數
3. 彈棧時計算 ”兩個數字和運算符計算結果“ 的函數
4. 遍歷算式列表，得到最終結果的主函數
5. 含有用户交互的 main 函數

### 3. 分塊代碼實現

1. 把算式轉換為列表的函數
這個步驟需要處理的是區分橫槓 ”-“ 代表的是負數還是減號。

```
#将算式处理成列表，解决横杠是负数还是减号的问题					   
def formula_format(formula):									   
    # 去掉算式中的空格											   
    formula = re.sub(‘ ‘, ‘’, formula)						   

    # 以 ‘横杠数字’ 分割， 其中正则表达式：(\-\d+\.?\d*) 括号内：	   
    # \- 表示匹配横杠开头； \d+ 表示匹配数字1次或多次；\.?表示匹配小数点0次或1次;\d*表示匹配数字1次或多次。
    formula_list = [I for I in re.split(‘(\-\d+\.?\d*)’, formula) if I]	                  										   
 
    # 最终的算式列表											
    final_formula = []											   
    for item in formula_list:									   
        # 第一个是以横杠开头的数字（包括小数）final_formula。即第一个是负数，横杠就不是减号													   
        if len(final_formula) == 0 and re.search(‘^\-\d+\.?\d*$’, item):														   
            final_formula.append(item)						   
            continue											   

        if len(final_formula) > 0:							   
            # 如果final_formal最后一个元素是运算符[‘+’, ‘-‘], 则横杠数字不是负数										   
            if re.search(‘[\+\-]$’, final_formula[-1]):	  
                final_formula.append(item)					   
                continue										   
        # 按照运算符分割开										   
        item_split = [I for I in re.split(‘([\+\-)’, item) if I]
        final_formula += item_split							   
    return final_formula										   
```

2. 判斷元素 e 是運算元還是運算子的函數
有一個選項是使用 isdigit() 函數來判斷，但是這個函數不能判斷小數和負數

```
#判断是否是运算符，如果是返回True					
def is_operator(e):							
    ‘’’										
    :param e: str								
    :return: bool								
    ‘’’										
    opers = [‘+’, ‘-‘]	
    return True if e in opers else False  	
```

3. 彈棧時計算 ”兩個數字和運算子計算結果“ 的函數
傳入兩個數字，一個運算子，根據運算子不同返回相應的結果

```
def calculate(n1, n2, operator):   
      ‘’’							 
    :param n1: float				 
    :param n2: float				 
    :param operator: + - 	    	 
    :return: float					 
    ‘’’							 
    result = 0						 
    if operator == “+”:			 
        result = n1 + n2			 
    if operator == “-“:			 
        result = n1 - n2			 
    return result					 
```

4. 遍歷算式列表，得到最終結果的主函數
主函數負責遍歷算式列表中的字符，決定入運算元棧或者運算子棧或彈棧運算

```
def final_calc(formula_list):
    num_stack = []       # 数字栈
    op_stack = []        # 运算符栈
    for e in formula_list:
        operator = is_operator(e)
        if not operator:
            # 压入数字栈
            # 字符串转换为符点数
            num_stack.append(float(e))
        else:
            # 如果是运算符
            while True:
                # 如果运算符栈等于0无条件入栈
                if len(op_stack) == 0:
                    op_stack.append(e)
                    break
                else:
                    op = op_stack.pop()
                    num2 = num_stack.pop()
                    num1 = num_stack.pop()
                    # 执行计算
                    # 计算之后压入数字栈
                    num_stack.append(calculate(num1, num2, op))
    # 处理大循环结束后 数字栈和运算符栈中可能还有元素 的情况
    while len(op_stack) != 0:
        op = op_stack.pop()
        num2 = num_stack.pop()
        num1 = num_stack.pop()
        num_stack.append(calculate(num1, num2, op))
 
    return num_stack, op_stack
```

5. 含有用户交互的 main 函數
沒什麼太多要注意的部分，就是用户交互的地方儘量簡潔和人性化

```
if __name__ == ‘__main__’:
  	 #用户交互界面
    print("Welcome Aho Calculator!")
    print("Enter 'quit' to end the program.")
	 formula = input("Write down the formula you want to calculate. \n-->")
    print(“Your formula is: ”, formula)
    formula_list = formula_format(formula)
    result, _ = final_calc(formula_list)
    print(“The result is: ”, result[0])
```

> 參考代碼：
[file:48D4762F-B91E-42D1-BE65-B714E14FEEC7-50877-00039C8221692180/A-version.py]


## B - 疊加需求，添加 ”*“ 和 ”/“ 運算
### 1. 對要求進行粗劣的整體構思

這時我們需要考慮運算得優先級，“*” 和 “/” 的優先級必然高於 ”+“ 和 ”-“ ，我們需要解決這個問題。只需要添加一個優先級的判斷，並在入棧操作的時候使用這個判斷就可以了。

### 2. 總結需要增加的模塊並進行偽代碼實現

```
#創建判斷運算子優先級的函數 decision:								
    首先定義運算符的級別
    rate1 = ['+', '-']
    rate2 = ['*', '/']									   
	
    if 運算子棧的最後一個元素屬於rate1級別:						
        當當前待入棧運算子優先級比它高時，需要入棧
        否則彈出運算元棧最後兩個元素，和運算子棧最後一個元素進行運算，得到的結果重新壓入運算元棧				   
    elif 運算子棧的最後一個元素屬於rate2級別:	
        彈出運算元棧最後兩個元素，和運算子棧最後一個元素進行運算，得到的結果重新壓入運算元棧								   
```

分析過後我們可以簡單總結成為幾個函數：
1. 彈棧時計算 ”兩個數字和運算子計算結果“ 的函數中添加運算子的計算規則
2. 判斷運算子優先級的函數
3. 在遍歷算式列表，得到最終結果的主函數中增加根據判斷函數做出決策的部分

### 3. 分塊代碼實現

1. 彈棧時計算 ”兩個數字和運算子計算結果“ 的函數中添加運算子的計算規則
添加 “*“ 和 ”/“ 的運算規則。

```
def calculate(n1, n2, operator):
    '''
    :param n1: float
    :param n2: float
    :param operator: + - * \
    :return: float
    '''
    result = 0

    if operator == "+":
        result = n1 + n2
    if operator == "-":
        result = n1 - n2
    if operator == "*":
        result = n1 * n2
    if operator == "/":
        result = n1 / n2
    return result
```

2. 判斷運算子優先級的函數
這個步驟需要連續比較兩個運算符來判斷優先級。

```
def decision(tail_op, now_op):
    '''
    :param tail_op: 运算符栈的最后一个运算符
    :param now_op: 从算式列表取出的当前运算符
    :return: 1 代表弹栈运算，0 代表弹运算符栈最后一个元素， -1 表示入栈
    '''
    # 定义2种运算符级别
    rate1 = ['+', '-']
    rate2 = ['*', '/']
 
    if tail_op in rate1:
        if now_op in rate2:
            # 说明连续两个运算优先级不一样，需要入栈
            return -1
        else:
            return 1

    elif tail_op in rate2:
        return 1

    else:
        return -1										   
```

3. 在遍歷算式列表，得到最終結果的主函數中增加根據判斷函數做出決策的部分
决策弹栈还是入栈

```
def final_calc(formula_list):
    num_stack = []       # 数字栈
    op_stack = []        # 运算符栈
    for e in formula_list:
        operator = is_operator(e)
        if not operator:
            # 压入数字栈
            # 字符串转换为符点数
            num_stack.append(float(e))
        else:
            # 如果是运算符
            while True:
                # 如果运算符栈等于0无条件入栈
                if len(op_stack) == 0:
                    op_stack.append(e)
                    break
 
                # decision 函数做决策
                tag = decision(op_stack[-1], e)
                if tag == -1:
                    # 如果是-1压入运算符栈进入下一次循环
                    op_stack.append(e)
                    break
                elif tag == 1:
                    # 如果是1弹出运算符栈内最后一个运算符，弹出数字栈内后两个元素。
                    op = op_stack.pop()
                    num2 = num_stack.pop()
                    num1 = num_stack.pop()
                    # 执行计算
                    # 计算之后压入数字栈
                    num_stack.append(calculate(num1, num2, op))
    # 处理大循环结束后 数字栈和运算符栈中可能还有元素 的情况
    while len(op_stack) != 0:
        op = op_stack.pop()
        num2 = num_stack.pop()
        num1 = num_stack.pop()
        num_stack.append(calculate(num1, num2, op))
 
    return num_stack, op_stack	
```

> 參考代碼：
[file:F2B269DA-49C5-4FBD-8267-9EA8C5858057-50877-00039C9D16EF9172/B-version.py]


## C - 疊加需求，添加括號運算
### 1. 對要求進行粗劣的整體構思

這時我們需要考慮運算得優先級，”(“ 和 “)” 的優先級必然高於 “*” 和 “/” 還有 ”+“ 和 ”-“ ，且 ”(“ 與 “)” 之間有一個先後順序和進行抵消的步驟。

### 2. 總結需要增加的模塊並進行偽代碼實現

```
def decision(tail_op, now_op):
    # return: 1 代表弹栈运算，0 代表弹运算符栈最后一个元素， -1 表示入栈
    # 定义4种运算符级别
    rate1 = ['+', '-']
    rate2 = ['*', '/']
    rate3 = ['(']
    rate4 = [')']

    if tail_op in rate1:
        if now_op in rate2 or now_op in rate3:
            # 说明连续两个运算优先级不一样，需要入栈
            return -1
        else:
            return 1

    elif tail_op in rate2:
        if now_op in rate3:
            return -1
        else:
            return 1
 
    elif 運算子棧最後一個元素是 '(':
        如果當前運算子是 ')":
            需要弹出 '('，並且丢掉 ')'
        否則入棧
        #只要栈顶元素为(，当前元素不是)都应入栈。
    else:
        return -1  
```


### 3.代碼實現

```
def decision(tail_op, now_op):
    """
    :param tail_op: 运算符栈的最后一个运算符
    :param now_op: 从算式列表取出的当前运算符
    :return: 1 代表弹栈运算，0 代表弹运算符栈最后一个元素， -1 表示入栈
    """

    # 定义4种运算符级别
    rate1 = ['+', '-']
    rate2 = ['*', '/']
    rate3 = ['(']
    rate4 = [')']

    if tail_op in rate1:
        if now_op in rate2 or now_op in rate3:
            # 说明连续两个运算优先级不一样，需要入栈
            return -1
        else:
            return 1

    elif tail_op in rate2:
        if now_op in rate3 or now_op in rate5:
            return -1
        else:
            return 1
        
    elif tail_op in rate3:
        if now_op in rate4:
            return 0  # ( 遇上 ) 需要弹出 (，丢掉 )
        else:
            return -1  # 只要栈顶元素为(，当前元素不是)都应入栈。
    
    else:
        return -1
```

> 參考代碼：
[file:2EB78851-6A88-4811-BF73-88CB08EE6C83-50877-0003A50C7E570138/C-version.py]


## D - 疊加需求，添加乘方和開根運算
### 1.分析需求
乘方和開根需要引入專門的math函數，我們只需要在程序的一開始聲明就可以了。關鍵在於兩個運算的優先級，由於我們定義了開跟運算用 “~” 表示，所以為了保證參與開根號運算的兩個數字的整體性，定義開跟運算的優先級大於 “*” 和 “/” 運算。

### 2.代碼實現

```
def decision(tail_op, now_op):
    '''
    :param tail_op: 运算符栈的最后一个运算符
    :param now_op: 从算式列表取出的当前运算符
    :return: 1 代表弹栈运算，0 代表弹运算符栈最后一个元素， -1 表示入栈
    '''
    # 定义5种运算符级别
    rate1 = ['+', '-']
    rate2 = ['*', '/']
    rate5 = ['^', '~']
    rate3 = ['(']
    rate4 = [')']

    if tail_op in rate1:
        if now_op in rate2 or now_op in rate3 or now_op in rate5:
            # 说明连续两个运算优先级不一样，需要入栈
            return -1
        else:
            return 1

    elif tail_op in rate2:
        if now_op in rate3 or now_op in rate5:
            return -1
        else:
            return 1

    elif tail_op in rate5:
        if now_op in rate3:
            return -1
        else:
            return 1

    elif tail_op in rate3:
        if now_op in rate4:
            return 0   # ( 遇上 ) 需要弹出 (，丢掉 )
        else:
            return -1  # 只要栈顶元素为(，当前元素不是)都应入栈。
    else:
        return -1
```


## E - 優化細節，最終代碼展示

```
# -*- coding: UTF-8 -*-

import re
import math


def calculate(n1, n2, operator):

    '''
    :param n1: float
    :param n2: float
    :param operator: + - * / ^ ~
    :return: float
    '''
    result = 0

    if operator == "+":
        result = n1 + n2
    if operator == "-":
        result = n1 - n2
    if operator == "*":
        result = n1 * n2
    if operator == "/":
        result = n1 / n2
    if operator == "^":
        result = math.pow(n1, n2)
    if operator == "~":
        result = math.pow(n1, 1/(n2))
    return result


# 判断是否是运算符，如果是返回True
def is_operator(e):
    '''
    :param e: str
    :return: bool
    '''
    opers = ['+', '-', '*', '/', '^', '~', '(', ')']
    return True if e in opers else False


# 将算式处理成列表，解决横杠是负数还是减号的问题
def formula_format(formula):
    # 以 '横杠数字' 分割， 其中正则表达式：(\-\d+\.?\d*) 括号内：
    # \- 表示匹配横杠开头； \d+ 表示匹配数字1次或多次；\.?表示匹配小数点0次或1次;\d*表示匹配数字1次或多次。
    formula_list = [i for i in re.split('(\-\d+\.?\d*)', formula) if i]

    # 最终的算式列表
    final_formula = []
    for item in formula_list:
        # 第一个是以横杠开头的数字（包括小数）final_formula。即第一个是负数，横杠就不是减号
        if len(final_formula) == 0 and re.search('^\-\d+\.?\d*$', item):
            final_formula.append(item)
            continue

        if len(final_formula) > 0:
            # 如果final_formal最后一个元素是运算符['+', '-', '*', '/', '('], 则横杠数字不是负数
            if re.search('[\+\-\*\/\^\~\(]$', final_formula[-1]):
                final_formula.append(item)
                continue
        # 按照运算符分割开
        item_split = [i for i in re.split('([\+\-\*\/\^\~\(\)])', item) if i]
        final_formula += item_split
    return final_formula


def decision(tail_op, now_op):
    '''
    :param tail_op: 运算符栈的最后一个运算符
    :param now_op: 从算式列表取出的当前运算符
    :return: 1 代表弹栈运算，0 代表弹运算符栈最后一个元素， -1 表示入栈
    '''
    # 定义5种运算符级别
    rate1 = ['+', '-']
    rate2 = ['*', '/']
    rate5 = ['^', '~']
    rate3 = ['(']
    rate4 = [')']

    if tail_op in rate1:
        if now_op in rate2 or now_op in rate3 or now_op in rate5:
            # 说明连续两个运算优先级不一样，需要入栈
            return -1
        else:
            return 1

    elif tail_op in rate2:
        if now_op in rate3 or now_op in rate5:
            return -1
        else:
            return 1

    elif tail_op in rate5:
        if now_op in rate3:
            return -1
        else:
            return 1

    elif tail_op in rate3:
        if now_op in rate4:
            return 0   # ( 遇上 ) 需要弹出 (，丢掉 )
        else:
            return -1  # 只要栈顶元素为(，当前元素不是)都应入栈。
    else:
        return -1


def final_calc(formula_list):
    """
    :rtype: object
    """
    num_stack = []       # 数字栈
    op_stack = []        # 运算符栈
    for e in formula_list:
        operator = is_operator(e)
        if not operator:
            # 压入数字栈
            # 字符串转换为符点数
            num_stack.append(float(e))
        else:
            # 如果是运算符
            while True:
                # 如果运算符栈等于0无条件入栈
                if len(op_stack) == 0:
                    op_stack.append(e)
                    break

                # decision 函数做决策
                tag = decision(op_stack[-1], e)
                if tag == -1:
                    # 如果是-1压入运算符栈进入下一次循环
                    op_stack.append(e)
                    break
                elif tag == 0:
                    # 如果是0弹出运算符栈内最后一个(, 丢掉当前)，进入下一次循环
                    op_stack.pop()
                    break
                elif tag == 1:
                    # 如果是1弹出运算符栈内最后一个元素，弹出数字栈最后两位元素。
                    op = op_stack.pop()
                    num2 = num_stack.pop()
                    num1 = num_stack.pop()
                    # 执行计算
                    # 计算之后压入数字栈
                    num_stack.append(calculate(num1, num2, op))
    # 处理大循环结束后 数字栈和运算符栈中可能还有元素 的情况
    while len(op_stack) != 0:
        op = op_stack.pop()
        num2 = num_stack.pop()
        num1 = num_stack.pop()
        num_stack.append(calculate(num1, num2, op))

    return num_stack, op_stack


if __name__ == '__main__':
    #用户交互界面
    print("Welcome Aho Calculator!")
    print("For the power operation, use '^', eg.3^2=9")
    print("Please use '~' for the root symbol, eg.9~2=3")
    print("Enter 'quit' to end the program.")
    #预设为空，为后面报错做准备
    formula = ""
    while formula != "quit":
        #写入用户输入
        prompt = "Write down the formula you want to calculate. \n-->"
        formula = input(prompt)
        #对用户输入数据进行预处理，删除不必要的空格
        #但还未对字符输入做处理
        formula = re.sub(' ', '', formula)
        if formula == "":
            #如果用户输入了空格或者直接回车提示重新输入
            print("Maybe you can input some formulas.")
        elif formula != "quit":
            #此时用户进行了正常的输入操作
            formula_list = formula_format(formula)
            try:
                result, _ = final_calc(formula_list)
                #为结果取小数点后两位
                print("The result is: ", '%.2f' % result[0])
            except ValueError:
                #当用户错误输入字符时
                print("Please try to input some formulas, not strings.")
            except ZeroDivisionError:
                #当用户把0作为分母或者用来开根方时
                print("0 cannot be used as a divisor or square-root, please try again.")
        else:
            break
```

> 參考代碼：
[file:4E46326C-C597-43B3-AE40-1783F387F8ED-526-0000025DFA389668/calculator.py]


> 
> 參考資料：
1. [Reverse Polish notation](https://en.wikipedia.org/wiki/Reverse_Polish_notation)
2. [Python實現計算器](https://www.cnblogs.com/zingp/p/8666214.html)
3. [用Python寫個計算器](https://blog.csdn.net/sinat_41909065/article/details/104072698)
4. [Python用户輸入和while循環](https://blog.csdn.net/Cengineering/article/details/78491552)
5. [Handling Exceptions](https://wiki.python.org/moin/HandlingExceptions)
6. [Errors and Exceptions](https://docs.python.org/3/tutorial/errors.html)

#Coding_Basic/Zhao’s_Lesson #Zhao’s_Lesson #Python #Calculator
