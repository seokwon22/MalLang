from pyspark.sql import SparkSession

# SparkSession을 생성합니다.
spark = SparkSession.builder.appName("CSV_to_MySQL").getOrCreate()

# 파일 경로와 대상 데이터베이스 및 테이블을 정의합니다.
file_db_mapping = [
    ("/data/diary.csv", "mallangdb.diary")
]

for file_path, target_table in file_db_mapping:
    # CSV 파일을 읽어옵니다.
    diary = spark.read.format("csv").option("header", "true").option("inferSchema","true").load(file_path)

    # MySQL 연결 정보를 설정합니다.
    jdbc_url = "jdbc:mysql://localhost:3306/" + target_table.split(".")[0]
    properties = {"user": "root", "password": "mallang1234", "driver": "com.mysql.cj.jdbc.Driver"}

    # 데이터를 MySQL에 쓰기 위해 저장합니다.
    diary.write.jdbc(url=jdbc_url, table=target_table, mode="overwrite", properties=properties)

    # MySQL에 데이터를 로드하기 위한 명령을 실행합니다.
    spark.sql(f"""
        LOAD DATA INFILE '{file_path}'
        INTO TABLE {target_table}
        FIELDS TERMINATED BY ','
        ENCLOSED BY '\"'
        LINES TERMINATED BY '\\n'
        IGNORE 1 ROWS;
    """)

# SparkSession을 종료합니다.
spark.stop()