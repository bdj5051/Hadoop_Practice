# 필요 패키지 import
# 개발자가 셋팅한 정보를 토대로 hive 명령문을 생성한다.
from pyspark.sql import HiveContext
# hive에서 사용하는 데이터 타입과 관련된 모듈
from pyspark.sql.types import *
# hive에 저장할 Row 데이터 구성을 위한 모듈
from pyspark.sql import Row

# hdfs에 저장되어 있는 데이터를 읽어올 수 있는
# 객체를 생성한다.
#csv_ata = sc.textFile('names/names.csv')
# 로컬 컴퓨터에 있는 파일을 읽어올 수 있는 객체를 생성한다.
# 리눅스에 pwd 명령어를 이용해 현재 경로를 파악한다.
csv_ata = sc.textFile('file:///root/names.csv')
# , 쉼표를 기준으로 데이터를 잘라낸다.
csv_data = csv_ata.map(lambda p : p.split(','))

# csv 파일에 해더가 포함되어 있다면 이를 제거해준다.
header = csv_data.first()
csv_data = csv_data.filter(lambda p: p != header)

# , 를 기준으로 잘라낸 데이터를 어디에 저장할 것인지 컬럼이름을
# 매핑시켜준다.
df_csv = csv_data.map(lambda p: Row(
    employeeid=int(p[0]),
    firstname=p[1],
    title=p[2],
    state=p[3],
    laptop=p[4])).toDF()
# 저장한다.
hc = HiveContext(sc)
df_csv.write.format('orc').saveAsTable('employees1')

# hive 접속해서 다음과 같이 조회해 보세요
# select * from employees1;




















