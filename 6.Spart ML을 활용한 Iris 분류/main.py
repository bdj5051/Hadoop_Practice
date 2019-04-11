# main.py

# 사용할 패키지
import numpy as np
import pandas as pd
import pyspark

# spark 에서 hive 쿼리를 만들기 위한 패키지
from pyspark.sql.functions import *
# 분류 모델 패키지
from pyspark.ml.classification import*
# 정확도 평가를 위한 패키지
from pyspark.ml.evaluation import *
# 학습을 위한 특성을 관리하는 패키지
from pyspark.ml.feature import *


# spark 세션 시작
# 하나의 spark 세션은 하나의 코드만 처리할 수 있다.
# 만약 동시에 여러 프로그램을 가동하고자 한다면
# 독립적인 spark 세션을 만들어 가동시켜준다.
spark = pyspark.sql.SparkSession.builder.appName('Iris').getOrCreate()

# 독립적인 spark 세션을 활용하여 데이터를 읽어온다.
# 각 데이터의 헤더리스트
names = ['sepal-length','sepal-width','petal-length','petal-width','class']

# 데이터를 읽어온다.
df = pd.read_csv('iris/iris.csv', header = None, names = names)
data = spark.createDataFrame(df)
data.show(10)

# 4가지 입력데이터(sepal-Length, sepal-Width, petal-Length, petal-Width)데이터를 모아 벡터화 시킨다.
feature_cols = data.columns[:-1]
assembler = pyspark.ml.feature.VectorAssembler(inputCols=feature_cols, outputCol='features')
data = assembler.transform(data)
data.show(10)

# 데이터 프레임에서 벡터화된 특성값과 꽃이름 데이터만 추출한다.
data = data.select(['features','class'])
data.show(10)

# 결과데이터(문자열)을 숫자로 만들어준다.
# 인덱서 생성
label_indexer = pyspark.ml.feature.StringIndexer(inputCol='class', outputCol='label').fit(data)
# 변경
data = label_indexer.transform(data)
data.show(10)

# 준비된 데이터를 학습 데이터와 테스트 데이터로 나눈다.
train, test = data.randomSplit([0.70, 0.30])
# 학습 모델을 만든다.
lr = LogisticRegression(regParam=0.01)
# 학습한다.
model = lr.fit(train)

# 교차 검증을 통해 검증한다.
# test 데이터를 입력하여 예측 결과를 생성한다.
prediction = model.transform(test)
prediction.show(10)

# test 데이터에 있는 결과 데이터와 생성한 예측 결과 데이터를
# 교차 검증하여 정확도를 측정한다.
evaluator = MulticlassClassificationEvaluator(metricName='accuracy')
accuracy = evaluator.evaluate(prediction)
print('Accuracy:', accuracy)

