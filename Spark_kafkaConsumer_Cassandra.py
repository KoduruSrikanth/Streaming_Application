from cassandra.cluster import Cluster
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, FloatType, IntegerType, StringType
from pyspark.sql.functions import from_json, col

cluster = Cluster()
session = cluster.connect()

session.execute('''DROP KEYSPACE IF EXISTS random_user''')

session.execute('''CREATE KEYSPACE random_user WITH REPLICATION{
                 'class':'SimpleStrategy',
                 'replication_factor':3
}''')

session.execute('''CREATE TABLE IF NOT EXISTS random_user.random_data (
                full_name TEXT,
                gender TEXT,
                location TEXT,
                city TEXT,
                country TEXT,
                postcode INT,
                latitude FLOAT,
                longitude FLOAT,
                email TEXT,
                PRIMARY KEY (full_name)
)''')

spark = SparkSession.builder().appName("Streaming_Project").config("spark.jars.packages", "com.datastax.spark:spark-cassandra-connector_2.12:3.0.0,org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.0").config(
    "spark.cassandra.connection.host", "cassandra").config("spark.cassandra.connection.port", "9042").config("spark.cassandra.auth.username", "student").config("spark.cassandra.auth.password", "ism6562").getOrCreate()

df = spark.readStream().format("kafka").options("kafka.bootstrap.servers", "kafka_broker_1:19092,kafka_broker_2:19093,kafka_broker_3:19094").options(
    "subscribe", "json_data").option("delimiter", ",").option("startingOffsets", "earliest").load()

schema = StructType([
    StructField("full_name", StringType(), False),
    StructField("gender", StringType(), False),
    StructField("location", StringType(), False),
    StructField("city", StringType(), False),
    StructField("country", StringType(), False),
    StructField("postcode", IntegerType(), False),
    StructField("latitude", FloatType(), False),
    StructField("longitude", FloatType(), False),
    StructField("email", StringType(), False)
])

df = df.selectExpr("CAST(value AS STRING)").select(
    from_json(col("value"), schema).alias("data")).select("data.*")

df.writeStream().format(
    'org.apache.spark.sql.cassandra').outputMode("append").options(table="random_data", keyspace="random_user").start().awaitTermination()
