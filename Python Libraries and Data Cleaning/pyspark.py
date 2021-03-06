# -*- coding: utf-8 -*-
"""pyspark.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1uecWCA7bakQiW9Uuxp84Hy0aMwBou4Ul
"""

!apt-get install openjdk-8-jdk-headless -qq > /dev/null
!wget -q https://www-us.apache.org/dist/spark/spark-3.0.1/spark-3.0.1-bin-hadoop2.7.tgz
!tar xf spark-3.0.1-bin-hadoop2.7.tgz
!pip install -q findspark
import os
os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-8-openjdk-amd64"
os.environ["SPARK_HOME"] = "/content/spark-3.0.1-bin-hadoop2.7"
import findspark
findspark.init()
from pyspark.sql import SparkSession
spark = SparkSession.builder\
        .master("local")\
        .appName("Colab")\
        .config('spark.ui.port', '4050')\
        .getOrCreate()
print("Pyspark Setup Complete");

import pyspark.sql.functions as F;
from pyspark.sql.functions import isnan,when,count,col,isnull,coalesce,stddev;
from pyspark.sql.types import IntegerType

import numpy as np;
import pandas as pd;
df=spark.read.csv("/content/drive/MyDrive/Dataset/train_cdr.csv",header=True,inferSchema=True);
df=df.drop(*['LAST_INTN_CALL','LAST_RCHG_MNTH','LAST_LOAN_MONTH','id2','Unnamed: 0']);

df.show(5)

df=df\
.withColumn('RMNG_CALL',df['RMNG_INTN_REVN']+df['RMNG_REVN'])\
.withColumn('INTN_CALL',df['RMNG_INTN_REVN']+df['INTN_CALLS']+df['INTN_REVN'])

rev_col=['TOTAL_VOICE_REVENUE','TOTAL_DATA_REVENUE','TOTAL_SMS_REVENUE','TOTAL_OTHER_REVENUE','TOTAL_MMONEY_REVENUE']
df=df.withColumn('Total_Rev',df['TOTAL_VOICE_REVENUE']+df['TOTAL_DATA_REVENUE']+df['TOTAL_SMS_REVENUE']+df['TOTAL_OTHER_REVENUE']+df['TOTAL_MMONEY_REVENUE'])
df=df.withColumn('STD_Rev',F.stddev((df['TOTAL_VOICE_REVENUE'],df['TOTAL_DATA_REVENUE'],df['TOTAL_SMS_REVENUE'],df['TOTAL_OTHER_REVENUE'],df['TOTAL_MMONEY_REVENUE'])))