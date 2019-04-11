from pyspark.sql import HiveContext

# Hive 쿼리를 생성하기 위한 정보를 담고 있을 객체를 생성
hc = HiveContext(sc)

# 지정된 파일로 부터 json 데이터를 읽어와 RDD 객체를 생성한다.
df_json = hc.read.json('file:///root/names.json')
# 테이블로 적재될 데이터 중 상위 5개를 출력한다.
df_json.show(5)
# 만들어질 테이블의 스키마를 확인한다.
df_json.printSchema()

# 테이블을 생성한다.
df_json.write.format('orc').saveAsTable('employees2')