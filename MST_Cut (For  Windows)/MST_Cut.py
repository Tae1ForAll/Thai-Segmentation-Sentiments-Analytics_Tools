#!/usr/bin/env python
# coding: utf-8

# In[1]:


import random
import pandas as pd
from pythainlp import word_tokenize as wt
from pythainlp import pos_tag as pt


# # Modify_Data
# 
# - เป็นฟังชันก์ที่นำข้อมูลคำเชื่อมต่างๆ มาลองตัดด้วย Engine ใดๆ แล้วนำมาเก็บไว้ในตัวแปร Dicts 
#   โดยที่จะแยกหมวดหมู่ตามจำนวนพยางค์ที่ตัดได้

# In[2]:


def Modify_Data(tokenize_engine):
    y = open(r'StartWord.txt', 'r', encoding="utf8")
    Data = y.read()
    Data_Split = Data.split("|")
    Start_Word_Dicts = {1:[],2:[],3:[],4:[],5:[]}
    for n in Data_Split:
        Start_Word_Dicts[len(wt(n,engine=tokenize_engine))].append(wt(n,engine=tokenize_engine))
    return Start_Word_Dicts


# # Get_Boundary
# 
# - หาขอบเขตการค้นหา

# In[3]:


def Get_Boundary(lenght,boundary):
    Lower_Bound = (lenght-boundary)
    Upper_Bound = (lenght+boundary)
    return Lower_Bound, Upper_Bound


# # Modify_Text
# 
# - วน Loop นำตัดกลุ่มคำออกมาตามระยะและขอบเขตที่กำหนด

# In[4]:


def Modify_Text(text,Lower_Bound,Upper_Bound,tokenize_engine):
    Array_Of_Text = []
    Real_len_Array = []
    Real_len = 0
    Word_len = 0
    for n in wt(text,engine=tokenize_engine):
        if n not in ['/n',' ','(',')','“','”']:
            Word_len += 1
            if Word_len == Lower_Bound:
                Real_len_Array.append(Real_len)
            elif Word_len == Upper_Bound:
                Real_len_Array.append(Real_len)
        Real_len += 1 
    Array_Of_Text = wt(text,engine=tokenize_engine)[Real_len_Array[0]:Real_len_Array[1]+1]
    return Array_Of_Text,Real_len_Array


# ### Check_Size_Of_Sentence

# In[5]:


def Check_Size_Of_Sentence(text, lenght, tokenize_engine):
    if len(wt(text,engine=tokenize_engine)) <= 50:
        return True
    else:
        return False


# ## Search_Line
# - ไล่หาเว้นบรรทัด

# In[6]:


def Search_Line(Array_Of_Text):
    Line_Target = []
    for n in range(0,len(Array_Of_Text)):
        if Array_Of_Text[n] in ["\n"] and (n-4) >= 0 and (n+4) >= 0 :
            Line_Target.append(n)
    return Line_Target


# ## Choose_Best_Line
# - เลือกหาเว้นบรรทัดมา 1 ค่า

# In[7]:


def Choose_Best_Line(Line_Target,boundary):
    print(boundary)
    if len(Line_Target) > 1:
        Fin_Case = [random.choice(Line_Target)]
    elif len(Line_Target) == 1:
        Fin_Case = Line_Target
    elif len(Line_Target) == 0:
        Fin_Case = [boundary]
    return Fin_Case


# # Search_Space
# 
# - ไล่หาเว้นวรรค

# In[8]:


def Search_Space(Array_Of_Text):
    SP_Target = []
    for n in range(0,len(Array_Of_Text)):
        if Array_Of_Text[n] in [" ","\xa0\xa0"] and (n-4) >= 0 and (n+4) >= 0 :
            SP_Target.append(n)
    return SP_Target


# # Tag_Prio_Each_SP
# 
# - หากกรณีที่มี Space หลายตัว จะเริ่มกระบวนการหา Space ที่ดีที่สุด ตามเคสที่กำหนด

# In[9]:


def Tag_Prio_Each_SP(Array_Of_Text,SP_Target,Start_Word_Dicts):
    Case_Target_B = []
    Case_Target_N = []
    Case_Bad = []
    SP_Case = ""
    count = 0
    for n in SP_Target:
        n4_B = Array_Of_Text[(n-4):n]
        n3_B = Array_Of_Text[(n-3):n]
        n2_B = Array_Of_Text[(n-2):n]
        n1_B = Array_Of_Text[(n-1):n]
        n1_N = Array_Of_Text[(n+1):(n+2)]
        n2_N = Array_Of_Text[(n+1):(n+3)]
        n3_N = Array_Of_Text[(n+1):(n+4)]
        n4_N = Array_Of_Text[(n+1):(n+5)]
        if n4_B in Start_Word_Dicts[4]:
            Case_Target_B.append(n-4)
            What_Case = ""
        elif n3_B in Start_Word_Dicts[3]:
            Case_Target_B.append(n-3)
        elif n2_B in Start_Word_Dicts[2]:
            Case_Target_B.append(n-2)
        elif n1_B in Start_Word_Dicts[1]:
            Case_Target_B.append(n-1)
        if Case_Target_B == []:
            if n4_N in Start_Word_Dicts[4]:
                Case_Target_N.append(n+1)
            elif n3_N in Start_Word_Dicts[3]:
                Case_Target_N.append(n+1)
            elif n2_N in Start_Word_Dicts[2]:
                Case_Target_N.append(n+1)
            elif n1_N in Start_Word_Dicts[1]:
                Case_Target_N.append(n+1)
            if Case_Target_N == []:
                Case_Bad.append(n+1)
                SP_Case = "Case_Bad"
            else:
                SP_Case = "Case_Target_N"
                    
        else:
            SP_Case = "Case_Target_B"
    if Case_Target_B != []:
        return Case_Target_B,SP_Case
    elif Case_Target_N != []:
        return Case_Target_N,SP_Case
    elif Case_Bad != []:
        return Case_Bad,SP_Case           


# # Choose_Best_SP
# 
# - เลือกหา space มาหนึ่งค่า

# In[10]:


def Choose_Best_SP(SP_Case_Target,boundary):
    if len(SP_Case_Target) > 1:
        Fin_Case = [random.choice(SP_Case_Target)]
    elif len(SP_Case_Target) == 1:
        Fin_Case = SP_Case_Target
    elif len(SP_Case_Target) == 0:
        Fin_Case = [boundary]
    return Fin_Case


# # Search_CONJ
# 
# - กรณีที่ไม่เจอ SPACE เลย จะทำการหาคำเชื่อมแทน

# In[11]:


def Search_CONJ(Array_Of_Text,Start_Word_Dicts):
    Case_CONJ_1 = []
    Case_CONJ_2 = []
    Case_CONJ_3 = []
    Case_CONJ_4 = []
    for n in range(0,len(Array_Of_Text)):
        n1_N = Array_Of_Text[n:(n+1)]
        n2_N = Array_Of_Text[n:(n+2)]
        n3_N = Array_Of_Text[n:(n+3)]
        n4_N = Array_Of_Text[n:(n+4)]
        if n4_N in Start_Word_Dicts[4]:
            Case_CONJ_4.append(n-1)
        elif n3_N in Start_Word_Dicts[3]:
            Case_CONJ_3.append(n-1)
        elif n2_N in Start_Word_Dicts[2]:
            Case_CONJ_2.append(n-1)
        elif n1_N in Start_Word_Dicts[1]:
            Case_CONJ_1.append(n-1)
    if Case_CONJ_4 != []:
        return Case_CONJ_4
    elif Case_CONJ_3 != []:
        return Case_CONJ_3
    elif Case_CONJ_2 != []:
        return Case_CONJ_2
    elif Case_CONJ_1 != []:
        return Case_CONJ_1
    else:
        return Case_CONJ_1
            
            


# # Choose_Best_CONJ
# 
# - เลือกหา CONJ มาหนึ่งค่า

# In[12]:


def Choose_Best_CONJ(Case_CONJ,boundary):
    if len(Case_CONJ) > 1:
        Fin_Case = [random.choice(Case_CONJ)]
    elif len(Case_CONJ) == 1:
        Fin_Case = Case_CONJ
    elif len(Case_CONJ) == 0:
        Fin_Case = [boundary]
    return Fin_Case


# # Cut_Sentence
# 
# - เป็นฟังก์สำหรับการตัด Sentence

# In[13]:


def Cut_Sentence(text,Fin_Case,Real_len_Array,tokenize_engine):
    List_Text = wt(text,engine=tokenize_engine)
    Size_Cut = Fin_Case[0] + Real_len_Array[0] 
    Output_Sentence = ''.join(List_Text[0:Size_Cut])
    return Output_Sentence,Size_Cut,List_Text


# # New_Sentence
# 
# - มาตัดประโยคแล้ว จะนำระยะที่ใช้ตัดมาสร้างประโยคใหม่

# In[14]:


def New_Sentence(Size_Cut,List_Text,Last_Sentence,lenght):
    Last_Sentence = 0
    New_text = ''.join(List_Text[Size_Cut:])
    if len(List_Text[Size_Cut:]) <= lenght*2:
        Last_Sentence = 1
    return New_text,Last_Sentence


# # Create_List_Of_Keyword
# - เก็บ Keyword ต่างๆแยกไว้ใน List

# In[15]:


def Create_List_Of_Keyword():
    data = pd.read_excel('NLP.xlsx', sheet_name = "Sentiment")
    Positive = (data['Positive'].dropna()).tolist()
    Negative = (data['Negative'].dropna()).tolist()
    Neutral = (data['Neutral'].dropna()).tolist()
    Negation = (data['Negation (-)'].dropna()).tolist()
    return Positive,Negative,Neutral,Negation


# # Check_Sentiment_By_Keyword
# - เช็ค Sentiment ที่อยู่ในประโยค

# In[16]:


def Check_Sentimenet_By_Keyword(Positive,Negative,Neutral,Negation,Output_Sentence):
    Mytext = Output_Sentence
    Mytext = Mytext.replace(' ','')
    for n in Neutral:
        Mytext = Mytext.replace(n,'|Neutral|')
    for n in Negative:
        Mytext = Mytext.replace(n,'|Negative|')
    for n in Positive:
        Mytext = Mytext.replace(n,'|Positive|')
    for n in Negation:
        Mytext = Mytext.replace(n,'|Negation|')
    Mytext = Mytext.replace('|Negative||Negation|','|Positive|')
    Mytext = Mytext.replace('|Negation||Negative|','|Positive|')
    Mytext = Mytext.replace('|Positive||Negation|','|Negative|')
    Mytext = Mytext.replace('|Negation||Positive|','|Negative|')
    Neu_Count = len(Mytext.split('|Neutral|'))-1
    Neg_Count = len(Mytext.split('|Negative|'))-1
    Pos_Count = len(Mytext.split('|Positive|'))-1
    return [Pos_Count,Neu_Count,Neg_Count]


# # Get_Sentiment 
# - Count และ Generate Sentiment ที่มีจำนวนมากที่สุด

# In[17]:


def Get_Sentiment(STM_Count):
    y = 0
    for n in range(0,len(STM_Count)):
        x = STM_Count[n]
        if x > y:
            My_Sentiment = '<'+str(n)+'>'
            y = x
        elif x == y:
            My_Sentiment = '<3>'
    return My_Sentiment


# # sentence 
# 
# - เป็นฟังก์ชั่นหลักเพื่อเรียกใช่งาน

# In[18]:


def sentence(text,lenght,boundary,tokenize_engine,sentiment):
    Last_Sentence = 0
    New_text = text
    Fin_Sentence = ""
    My_Check = Check_Size_Of_Sentence(text, lenght, tokenize_engine)
    if My_Check == True:
        return text
    while Last_Sentence == 0:
        Start_Word_Dicts = Modify_Data(tokenize_engine)
        Lower_Bound, Upper_Bound = Get_Boundary(lenght,boundary)
        Array_Of_Text,Real_len_Array = Modify_Text(New_text,Lower_Bound,Upper_Bound,tokenize_engine)
        SP_Target = Search_Space(Array_Of_Text)
        Line_Target = Search_Line(Array_Of_Text)
        if Line_Target != []: 
            Fin_Case = Choose_Best_Line(Line_Target,boundary)
        elif SP_Target == []:
            Case_CONJ = Search_CONJ(Array_Of_Text,Start_Word_Dicts)
            Fin_Case = Choose_Best_CONJ(Case_CONJ,boundary)
        else:
            SP_Case_Target,SP_Case = Tag_Prio_Each_SP(Array_Of_Text,SP_Target,Start_Word_Dicts)
            Fin_Case = Choose_Best_SP(SP_Case_Target,boundary)
        Output_Sentence,Size_Cut,List_Text = Cut_Sentence(New_text,Fin_Case,Real_len_Array,tokenize_engine)
        New_text,Last_Sentence = New_Sentence(Size_Cut,List_Text,Last_Sentence,lenght)
        if sentiment == True:
            Positive,Negative,Neutral,Negation = Create_List_Of_Keyword()
            STM_Count = Check_Sentimenet_By_Keyword(Positive,Negative,Neutral,Negation,Output_Sentence)
            My_Sentiment = Get_Sentiment(STM_Count)
        else:
            My_Sentiment = ''
        if Line_Target != []:
            Output_Sentence += My_Sentiment+"\n"
        else :
            Output_Sentence += My_Sentiment+"\n\n"
        Fin_Sentence += Output_Sentence
    Fin_Sentence += New_text
    return Fin_Sentence


# In[ ]:




