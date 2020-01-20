#!/usr/bin/env python
# coding: utf-8

# In[1]:


import random
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


# # Search_Space
# 
# - ไล่หาเว้นวรรค

# In[5]:


def Search_Space(Array_Of_Text):
    SP_Target = []
    for n in range(0,len(Array_Of_Text)):
        if Array_Of_Text[n] in [" ","\xa0\xa0"] and (n-4) >= 0 and (n+4) >= 0 :
            SP_Target.append(n)
    return SP_Target


# # Tag_Prio_Each_SP
# 
# - หากกรณีที่มี Space หลายตัว จะเริ่มกระบวนการหา Space ที่ดีที่สุด ตามเคสที่กำหนด

# In[6]:


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

# In[7]:


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

# In[8]:


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
            print(Case_CONJ_1)
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

# In[9]:


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

# In[10]:


def Cut_Sentence(text,Fin_Case,Real_len_Array,tokenize_engine):
    List_Text = wt(text,engine=tokenize_engine)
    Size_Cut = Fin_Case[0] + Real_len_Array[0] 
    Output_Sentence = ''.join(List_Text[0:Size_Cut])
    return Output_Sentence,Size_Cut,List_Text


# # New_Sentence
# 
# - มาตัดประโยคแล้ว จะนำระยะที่ใช้ตัดมาสร้างประโยคใหม่

# In[11]:


def New_Sentence(Size_Cut,List_Text,Last_Sentence,lenght):
    Last_Sentence = 0
    New_text = ''.join(List_Text[Size_Cut:])
    if len(List_Text[Size_Cut:]) <= lenght*2:
        Last_Sentence = 1
    return New_text,Last_Sentence


# # sentence 
# 
# - เป็นฟังก์ชั่นหลักเพื่อเรียกใช่งาน

# In[12]:


def sentence(text,lenght,boundary,tokenize_engine):
    Last_Sentence = 0
    New_text = text
    Fin_Sentence = ""
    while Last_Sentence == 0:
        Start_Word_Dicts = Modify_Data(tokenize_engine)
        Lower_Bound, Upper_Bound = Get_Boundary(lenght,boundary)
        Array_Of_Text,Real_len_Array = Modify_Text(New_text,Lower_Bound,Upper_Bound,tokenize_engine)
        SP_Target = Search_Space(Array_Of_Text)
        if SP_Target == []:
            Case_CONJ = Search_CONJ(Array_Of_Text,Start_Word_Dicts)
            Fin_Case = Choose_Best_CONJ(Case_CONJ,lenght)
        else:
            SP_Case_Target,SP_Case = Tag_Prio_Each_SP(Array_Of_Text,SP_Target,Start_Word_Dicts)
            Fin_Case = Choose_Best_SP(SP_Case_Target,boundary)
        Output_Sentence,Size_Cut,List_Text = Cut_Sentence(New_text,Fin_Case,Real_len_Array,tokenize_engine)
        New_text,Last_Sentence = New_Sentence(Size_Cut,List_Text,Last_Sentence,lenght)
        Output_Sentence += "\n"
        Fin_Sentence += Output_Sentence
    Fin_Sentence += New_text
    return Fin_Sentence

