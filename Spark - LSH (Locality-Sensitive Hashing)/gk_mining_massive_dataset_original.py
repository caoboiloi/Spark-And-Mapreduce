# -*- coding: utf-8 -*-
"""GK_MINING_MASSIVE_DATASET_ORIGINAL.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1lKC66LNBbolZkMoqmobMV4btBtmPRuax
"""

import re
from random import randint, seed, choice, random
import time
import binascii
import numpy as np
import itertools
import math
from decimal import *
from google.colab import drive
drive.mount('/content/drive',force_remount=True)

f = open("/content/drive/MyDrive/BIGDATA/BTL/data3.txt", "r", encoding="utf-8")

documents = f.read().split("\n")

"""# CÁC HÀM HỖ TRỢ THUẬT TOÁN"""

def split_k_gram(document, shingleNo):
  shingle = []
  shinglesInDocInts = set() # chỉ định lấy duy nhất

  for index in range(len(document) - k_gram + 1):
    shingle = document[index:index + k_gram]
    shingle = ' '.join(shingle)

    # năm shingle thành số nguyên (32-bit integer)
    hashed = binascii.crc32(shingle.encode())

    # lọc ra duy nhất
    if hashed not in shinglesInDocInts:
      shinglesInDocInts.add(hashed)

      # tính số lượng shingles
      shingleNo = shingleNo + 1
  return shinglesInDocInts,shingleNo

def isPrime(n):
  # Corner cases
  if(n <= 1):
      return False
  if(n <= 3):
      return True
    
  # This is checked so that we can skip
  # middle five numbers in below loop
  if(n % 2 == 0 or n % 3 == 0):
      return False
  for i in range(5,int(math.sqrt(n) + 1), 6):
      if(n % i == 0 or n % (i + 2) == 0):
          return False
  return True

# Hàm trả về giá trị nhỏ nhất số nguyên tố lớn hơn N
def nextPrimefunc(N):
  # Base case
  if (N <= 1):
      return 2
  prime = N
  found = False
  while(not found):
      prime = prime + 1

      if(isPrime(prime) == True):
          found = True
  return prime

def pickRandomCoeffs(k):
  # Create a list of 'k' random values.
  randList = []

  while k > 0:
    randIndex = randint(0, maxShingleID)

    while randIndex in randList:
      randIndex = random.randint(0, maxShingleID)
    randList.append(randIndex)
    k = k - 1
  return randList

def signatureFunction(shingleIDSet):
  signature = []
  # vòng lặp trên số hash func
  for i in range(0, numHashesFunction):

    # vọp lặp shingle trong document
    minHashCode = nextPrime + 1

    # vọp lặp shingle trong document
    for shingleID in shingleIDSet:
      hashCode = (coeffA[i] * shingleID + coeffB[i]) % nextPrime
      # điều kiện hash min => lấy hash nhỏ nhất
      if hashCode < minHashCode:
        minHashCode = hashCode

    signature.append(minHashCode)
  return signature

def FindSimilarity_Singles(doc, n_neighbor):
  doc = re.sub("[^\w]", " ", doc).split()
  singlesInput,n = split_k_gram(doc,0)
  neighbors_of_given_document_Test = {}
  for j in range(len(docsAsShingleSets)):
    singles2 = docsAsShingleSets[j]
    s1 = set(singlesInput)
    s2 = set(singles2)
    J = len(s1.intersection(s2)) / float(len(s1.union(s2)))
    # kiểm tra Jaccard similarity có lớn hơn 0 hay ko
    if (float(J) > 0):
        percJ = J * 100
        neighbors_of_given_document_Test[j] = percJ
  neighbors_of_given_documentSIGNATURES_Test= sorted(neighbors_of_given_document_Test.items(), key=lambda x: x[1], reverse=True)
  return list(neighbors_of_given_documentSIGNATURES_Test)[:n_neighbor]

def FindSimilarity_minhash(doc, n_neighbor):
  doc = re.sub("[^\w]", " ", doc).split()
  doc,n = split_k_gram(doc,0)
  signatureInput = signatureFunction(doc)
  neighbors_of_given_documentSIGNATURES_Test ={}

  for j in range(len(signatures)):
    signature2 = signatures[j]
    s1 = set(signatureInput)
    s2 = set(signature2)
    J = len(s1.intersection(s2)) / float(len(s1.union(s2)))
    if (float(J) > 0):
        percJ = J * 100
        neighbors_of_given_documentSIGNATURES_Test[j] = percJ

  neighbors_of_given_documentSIGNATURES_Test= sorted(neighbors_of_given_documentSIGNATURES_Test.items(), key=lambda x: x[1], reverse=True)
  return list(neighbors_of_given_documentSIGNATURES_Test)[:n_neighbor]

def get_band_hashes(np_signature, numBand):
  np_signature  = np.array_split(np_signature, numBand)
  hash_sig = []
  for i in np_signature:
    j = [hash(x) for x in i]
    hash_sig.append(sum(j))
  return hash_sig

def LSH(Test_input,n_neighbor):

  Test_input = re.sub("[^\w]", " ", Test_input).split()
  Test_input,n = split_k_gram(Test_input, 0)
  signatureInput = signatureFunction(Test_input)
  input_band = get_band_hashes(signatureInput, numBand)
  idDoc_samebucket = []
  result = []
  for i in range(len(input_band)):
    if input_band[i] in bucket_value:
      id = bucket_value.index(input_band[i])
      idDoc_samebucket += [x for x in bucket_index[id] if x not in idDoc_samebucket]
  for i in idDoc_samebucket:
    s1 = set(input_band)
    s2 = set(get_band_hashes(signatures[i], numBand))
    sim = len(s1.intersection(s2)) / float(len(s1.union(s2)))*100
    result.append((sim, i))
  result= sorted(result, key=lambda x: x[0], reverse=True)
  return list(result)[:n_neighbor]

"""# SHINGLING - TÌM MA TRẬN BOOLEANS VỚI K-GRAMS = 10

"""

timeShingling = time.time()
k_gram = 10 # size singles k = 10
numHashesFunction = 50
i = 0
d = {}
for document in documents:
  # Cắt data thành các word
  d[i] =  document
  d[i] = re.sub("[^\w]", " ", d[i]).split() # Thay thế bằng biểu thức chính quy: [^\w] -> khớp với các từ hoặc ký tự bắt đầu nào không phải là chữ cái và chữ số
  i += 1

docsAsShingleSets = {} # tập set shingles
docNames = [] # id của từng docs
shingleNo = 0 # số lượng shingles
print("Số documents: ",len(d))

for i in range(0, len(d)):

  document = d[i]
  docID = i
  docNames.append(docID)
  shinglesInDocInts,shingleNo = split_k_gram(document, shingleNo)
  docsAsShingleSets[docID] = shinglesInDocInts

print("Số documents (shingling):",len(docsAsShingleSets))
print("Tổng tất cả Shingles:", shingleNo)

print("Thời gian chuyển đổi Shingling:" , time.time() - timeShingling)

"""# MIN-HASHING - CREATE SIGNATURE MATRIX VỚI SỐ HASH FUNCTION = 50

"""

maxShingleID = shingleNo
nextPrime = nextPrimefunc(shingleNo)
print ('Next prime = ', nextPrime)

# Hàm băm ngẫu nhiên: h(x) = (a*x + b) % c
# x là giá trị input, a và b là 2 chỉ số random và c sẽ là số nguyên tố lớn hơn
# tổng số shingles (shingleNo)

coeffA = pickRandomCoeffs(numHashesFunction)
coeffB = pickRandomCoeffs(numHashesFunction)

timeSig = time.time()
signatures = []

# print(len(docsAsShingleSets))
for docID in docNames:

  # lấy tập shingle từ documents
  shingleIDSet = docsAsShingleSets[docID]
  # Store the MinHash signature for this document.
  signatures.append(signatureFunction(shingleIDSet))

# numDocs = len(signatures)
print("Thời gian chuyển đổi Signature MinHashing:" , time.time() - timeSig)

"""# MIN-HASHING - CALCULATE JACCARD SIMILARITY

## SO SÁNH TỐC ĐỘ TÍNH JACCARD SIMILARITY GIỮA SHINGLES VÀ SIGNATURES
"""

inputNewDoc= documents[0]
print("nội dung document " + str(docNames[0]) + ":")
# document đầu vào
print(documents[0])
print("----------------------------------------------------")
time_JS = time.time()
resSimilarity = FindSimilarity_Singles(inputNewDoc, 7)
for x,y in resSimilarity:
  print("{}% index-document:{} | document:{}".format(round(y,2),x, documents[x]))
print("Thời gian tìm kiếm và tính toán cho Jaccard Shingles::",time.time() - time_JS)

# tốc độ khi tính jaccard bằng shingles và minhash có sự chênh lệch lẫn nhau
inputNewDoc= documents[0]
print("nội dung document " + str(docNames[0]) + ":")
# document đầu vào
print(documents[0])
print("----------------------------------------------------")
time_JShash = time.time()
resSimilarity = FindSimilarity_minhash(inputNewDoc, 7)
# print(resSimilarity)
for x,y in resSimilarity:
  print("{}% index-document:{} | document:{}".format(round(y,2),x, documents[x]))
print("Thời gian tìm kiếm và tính toán cho Jaccard MinHashing: ", time.time() - time_JShash)

"""# LOCALLITY SENSITIVE HASHING"""

time_LSH = time.time()
numBand = 50

bucket_value = []
bucket_index = []


for k in range(len(signatures)):
  for i in get_band_hashes(signatures[k], numBand):
    if i not in bucket_value:
      bucket_value.append(i)
      bucket_index.append([k])
    else:
      index = bucket_value.index(i)
      bucket_index[index].append(k)

lst_result = LSH(documents[1], 7)
for x,y in lst_result:
  print("{}% index-document:{} | document: {}".format(round(x,2),y, documents[y]))

print("Thời gian tìm kiểm LSH ", time.time() - time_LSH)