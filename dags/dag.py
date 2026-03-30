
from airflow.decorators import dag, task
from airflow.utils.task_group import TaskGroup

from src.Extract.extract_btc import extract_btc
from src.Extract.extract_fx import extract_fx
from src.Extract.extract_m2_cn import extract_m2_cn
from src.Extract.extract_m2_eu import extract_m2_eu
from src.Extract.extract_m2_jp import extract_m2_jp
from src.Extract.extract_m2_us import extract_m2_us

from src.Load.Bronze.load_btc_bronze import load_btc_bronze
from src.Load.Bronze.load_fx_bronze import load_fx_bronze
from src.Load.Bronze.load_m2_cn_bronze import load_m2_cn_bronze
from src.Load.Bronze.load_m2_eu_bronze import load_m2_eu_bronze
from src.Load.Bronze.load_m2_jp_bronze import load_m2_jp_bronze
from src.Load.Bronze.load_m2_us_bronze import load_m2_us_bronze

from src.Transform.Silver_T.btc_t import extract_btc_silver, transform_btc_silver, load_btc_silver
from src.Transform.Silver_T.fx_t import extract_fx_silver, transform_fx_silver, load_fx_silver
from src.Transform.Silver_T.us_t import extract_us_silver, transform_us_silver, load_us_silver
from src.Transform.Silver_T.jp_t import extract_jp_silver, transform_jp_silver, load_jp_silver
from src.Transform.Silver_T.eu_t import extract_eu_silver, transform_eu_silver, load_eu_silver
from src.Transform.Silver_T.cn_t import extract_cn_silver, transform_cn_silver, load_cn_silver
from src.Transform.Silver_T.Exchange import exchange

from src.Transform.Gold_T.Gold_t import gold_operation


@dag(dag_id="Pipeline_financeira")
def PF_dag():

    @task.bash
    def initialization():
        return "echo 'Initializing pipeline!'"

    # ─────────────────────────────────────────
    # BRONZE
    # ─────────────────────────────────────────
    with TaskGroup("bronze") as bronze_group:

        with TaskGroup("btc_etl"):
            @task
            def extract_bitcoin_bronze():
                return extract_btc()

            @task
            def load_bitcoin_bronze(data):
                return load_btc_bronze(data)

            load_bitcoin_bronze(extract_bitcoin_bronze())

        with TaskGroup("fx_etl"):
            @task
            def extract_tax_bronze():
                return extract_fx()

            @task
            def load_tax_bronze(data):
                return load_fx_bronze(data)

            load_tax_bronze(extract_tax_bronze())

        with TaskGroup("us_etl"):
            @task
            def extract_usa_bronze():
                return extract_m2_us()

            @task
            def load_usa_bronze(data):
                return load_m2_us_bronze(data)

            load_usa_bronze(extract_usa_bronze())

        with TaskGroup("jp_etl"):
            @task
            def extract_japan_bronze():
                return extract_m2_jp()

            @task
            def load_japan_bronze(data):
                return load_m2_jp_bronze(data)

            load_japan_bronze(extract_japan_bronze())

        with TaskGroup("eu_etl"):
            @task
            def extract_europe_bronze():
                return extract_m2_eu()

            @task
            def load_europe_bronze(data):
                return load_m2_eu_bronze(data)

            load_europe_bronze(extract_europe_bronze())

        with TaskGroup("cn_etl"):
            @task
            def extract_china_bronze():
                return extract_m2_cn()

            @task
            def load_china_bronze(data):
                return load_m2_cn_bronze(data)

            load_china_bronze(extract_china_bronze())

    @task.bash
    def bronze_validation():
        return "echo 'Bronze concluded!'"

    # ─────────────────────────────────────────
    # SILVER
    # ─────────────────────────────────────────
    with TaskGroup("silver") as silver_group:

        with TaskGroup("btc_etl") as btc_silver:
            @task
            def extract_bitcoin_silver():
                return extract_btc_silver()

            @task
            def transform_bitcoin_silver(data):
                return transform_btc_silver(data)

            @task
            def load_bitcoin_silver(data):
                return load_btc_silver(data)

            btc_silver_end = load_bitcoin_silver(
                transform_bitcoin_silver(extract_bitcoin_silver())
            )

        with TaskGroup("fx_etl") as fx_silver:
            @task
            def extract_tax_silver():
                return extract_fx_silver()

            @task
            def transform_tax_silver(data):
                return transform_fx_silver(data)

            @task
            def load_tax_silver(data):
                return load_fx_silver(data)

            fx_silver_end = load_tax_silver(
                transform_tax_silver(extract_tax_silver())
            )

        with TaskGroup("us_etl") as us_silver:
            @task
            def extract_usa_silver():
                return extract_us_silver()

            @task
            def transform_usa_silver(data):
                return transform_us_silver(data)

            @task
            def load_usa_silver(data):
                return load_us_silver(data)

            us_silver_end = load_usa_silver(
                transform_usa_silver(extract_usa_silver())
            )

        with TaskGroup("jp_etl") as jp_silver:
            @task
            def extract_japan_silver():
                return extract_jp_silver()

            @task
            def transform_japan_silver(data):
                return transform_jp_silver(data)

            @task
            def load_japan_silver(data):
                return load_jp_silver(data)

            jp_silver_end = load_japan_silver(
                transform_japan_silver(extract_japan_silver())
            )

        with TaskGroup("eu_etl") as eu_silver:
            @task
            def extract_europe_silver():
                return extract_eu_silver()

            @task
            def transform_europe_silver(data):
                return transform_eu_silver(data)

            @task
            def load_europe_silver(data):
                return load_eu_silver(data)

            eu_silver_end = load_europe_silver(
                transform_europe_silver(extract_europe_silver())
            )

        with TaskGroup("cn_etl") as cn_silver:
            @task
            def extract_china_silver():
                return extract_cn_silver()

            @task
            def transform_china_silver(data):
                return transform_cn_silver(data)

            @task
            def load_china_silver(data):
                return load_cn_silver(data)

            cn_silver_end = load_china_silver(
                transform_china_silver(extract_china_silver())
            )

        # ── exchange dentro do silver ──────────
        with TaskGroup("exchange_etl"):
            @task
            def exchange_task():
                return exchange()

            exchange_end = exchange_task()

        # todos os loads disparam o exchange
        [
            btc_silver_end,
            fx_silver_end,
            us_silver_end,
            jp_silver_end,
            eu_silver_end,
            cn_silver_end,
        ] >> exchange_end

    @task.bash
    def silver_validation():
        return "echo 'Silver concluded!'"

    # ─────────────────────────────────────────
    # GOLD
    # ─────────────────────────────────────────
    with TaskGroup("gold") as gold_group:

        with TaskGroup("gold_etl"):
            @task
            def gold_ETL():
                return gold_operation()

            gold_ETL()

    @task.bash
    def gold_validation():
        return "echo 'Gold concluded!'"

    # ─────────────────────────────────────────
    # Dependências
    # ─────────────────────────────────────────
    init = initialization()
    bronze_end = bronze_validation()
    silver_end = silver_validation()
    gold_end = gold_validation()

    init >> bronze_group >> bronze_end
    bronze_end >> silver_group >> silver_end
    silver_end >> gold_group >> gold_end


PF_dag()

# -------------------------------------------------------------------------------------------------------------------------------
# from airflow.decorators import dag, task
# from airflow.utils.task_group import TaskGroup

# from src.Extract.extract_btc import extract_btc
# from src.Extract.extract_fx import extract_fx
# from src.Extract.extract_m2_cn import extract_m2_cn
# from src.Extract.extract_m2_eu import extract_m2_eu
# from src.Extract.extract_m2_jp import extract_m2_jp
# from src.Extract.extract_m2_us import extract_m2_us

# from src.Load.Bronze.load_btc_bronze import load_btc_bronze
# from src.Load.Bronze.load_fx_bronze import load_fx_bronze
# from src.Load.Bronze.load_m2_cn_bronze import load_m2_cn_bronze
# from src.Load.Bronze.load_m2_eu_bronze import load_m2_eu_bronze
# from src.Load.Bronze.load_m2_jp_bronze import load_m2_jp_bronze
# from src.Load.Bronze.load_m2_us_bronze import load_m2_us_bronze

# from src.Transform.Silver_T.btc_t import extract_btc_silver, transform_btc_silver, load_btc_silver
# from src.Transform.Silver_T.fx_t import extract_fx_silver, transform_fx_silver, load_fx_silver
# from src.Transform.Silver_T.us_t import extract_us_silver, transform_us_silver, load_us_silver
# from src.Transform.Silver_T.jp_t import extract_jp_silver, transform_jp_silver, load_jp_silver
# from src.Transform.Silver_T.eu_t import extract_eu_silver, transform_eu_silver, load_eu_silver
# from src.Transform.Silver_T.cn_t import extract_cn_silver, transform_cn_silver, load_cn_silver
# from src.Transform.Silver_T.Exchange import exchange

# from src.Transform.Gold_T.Gold_t import gold_operation

# @dag(

#     dag_id="Pipeline_financeira"

# )

# def PF_dag():

#     # Extraction and loading to the Bronze tier

#     @task.bash
#     def initialization():
#         return "echo 'Initializating pipeline!'"
    
#     @task
#     def extract_bitcoin_bronze():
#         return extract_btc()
    
#     @task
#     def load_bitcoin_bronze(data):
#         return load_btc_bronze(data)
    
#     @task
#     def extract_tax_bronze():
#         return extract_fx()
    
#     @task
#     def load_tax_bronze(data):
#         return load_fx_bronze(data)
    
#     @task
#     def extract_china_bronze():
#         return extract_m2_cn()
    
#     @task
#     def load_china_bronze(data):
#         return load_m2_cn_bronze(data)
    
#     @task
#     def extract_europe_bronze():
#         return extract_m2_eu()
    
#     @task
#     def load_europe_bronze(data):
#         return load_m2_eu_bronze(data)

#     @task
#     def extract_japan_bronze():
#         return extract_m2_jp()
    
#     @task
#     def load_japan_bronze(data):
#         return load_m2_jp_bronze(data)
    
#     @task
#     def extract_usa_bronze():
#         return extract_m2_us()
    
#     @task
#     def load_usa_bronze(data):
#         return load_m2_us_bronze(data)
    
#     @task.bash
#     def bronze_validation():
#         return "echo 'Bronze concluded!'"
    
#     # Extracting ,transforming and loading to the Silver tier
    
#     @task
#     def extract_bitcoin_silver():
#         return extract_btc_silver()
    
#     @task
#     def transform_bitcoin_silver(data):
#         return transform_btc_silver(data)
    
#     @task
#     def load_bitcoin_silver(data):
#         return load_btc_silver(data)
    
#     @task
#     def extract_tax_silver():
#         return extract_fx_silver()
    
#     @task
#     def transform_tax_silver(data):
#         return transform_fx_silver(data)
    
#     @task
#     def load_tax_silver(data):
#         return load_fx_silver(data)
    
#     @task
#     def extract_usa_silver():
#         return extract_us_silver()
    
#     @task
#     def transform_usa_silver(data):
#         return transform_us_silver(data)
    
#     @task
#     def load_usa_silver(data):
#         return load_us_silver(data)
    
#     @task
#     def extract_japan_silver():
#         return extract_jp_silver()
    
#     @task
#     def transform_japan_silver(data):
#         return transform_jp_silver(data)
    
#     @task
#     def load_japan_silver(data):
#         return load_jp_silver(data)
    
#     @task
#     def extract_europe_silver():
#         return extract_eu_silver()
    
#     @task
#     def transform_europe_silver(data):
#         return transform_eu_silver(data)
    
#     @task
#     def load_europe_silver(data):
#         return load_eu_silver(data)
    
#     @task
#     def extract_china_silver():
#         return extract_cn_silver()
    
#     @task
#     def transform_china_silver(data):
#         return transform_cn_silver(data)
    
#     @task
#     def load_china_silver(data):
#         return load_cn_silver(data)
    
#     @task
#     def exchange_silver():
#         return exchange()
    
#     @task.bash
#     def silver_validation():
#         return "echo 'Silver concluded!'"
    
#     # Extracting ,transforming and loading to the Gold tier

#     @task
#     def gold_ETL():
#         return gold_operation()

#     @task.bash
#     def gold_validation():
#         return "echo 'Gold concluded!'"

#     #  Defining variables !
#     init = initialization()

#     btc_bronze_extraction = extract_bitcoin_bronze()
#     btc_bronze_load = load_bitcoin_bronze(btc_bronze_extraction)

#     fx_bronze_extraction = extract_tax_bronze()
#     fx_bronze_load = load_tax_bronze(fx_bronze_extraction)

#     cn_bronze_extraction = extract_china_bronze()
#     cn_bronze_load = load_china_bronze(cn_bronze_extraction)

#     eu_bronze_extraction = extract_europe_bronze()
#     eu_bronze_load = load_europe_bronze(eu_bronze_extraction)

#     jp_bronze_extraction = extract_japan_bronze()
#     jp_bronze_load = load_japan_bronze(jp_bronze_extraction)

#     us_bronze_extraction = extract_usa_bronze()
#     us_bronze_load = load_usa_bronze(us_bronze_extraction)

#     bronze_end = bronze_validation()

#     # Dependências
#     init >> [
#         btc_bronze_extraction, 
#         fx_bronze_extraction, 
#         cn_bronze_extraction, 
#         eu_bronze_extraction, 
#         jp_bronze_extraction, 
#         us_bronze_extraction
#         ]

#     btc_bronze_extraction >> btc_bronze_load
#     fx_bronze_extraction >> fx_bronze_load
#     cn_bronze_extraction >> cn_bronze_load
#     eu_bronze_extraction >> eu_bronze_load
#     jp_bronze_extraction >> jp_bronze_load
#     us_bronze_extraction >> us_bronze_load

#     [
#         btc_bronze_load, 
#         fx_bronze_load, 
#         cn_bronze_load, 
#         eu_bronze_load, 
#         jp_bronze_load, 
#         us_bronze_load
#     ] >> bronze_end


#     btc_silver_extraction = extract_bitcoin_silver()
#     btc_silver_transformation = transform_bitcoin_silver(btc_silver_extraction)
#     btc_silver_load = load_bitcoin_silver(btc_silver_transformation)

#     fx_silver_extraction = extract_tax_silver()
#     fx_silver_transformation = transform_tax_silver(fx_silver_extraction)
#     fx_silver_load = load_tax_silver(fx_silver_transformation)

#     usa_silver_extraction = extract_usa_silver()
#     usa_silver_transformation = transform_usa_silver(usa_silver_extraction)
#     usa_silver_load = load_usa_silver(usa_silver_transformation)

#     jp_silver_extraction = extract_japan_silver()
#     jp_silver_transformation = transform_japan_silver(jp_silver_extraction)
#     jp_silver_load = load_japan_silver(jp_silver_transformation)

#     eu_silver_extraction = extract_europe_silver()
#     eu_silver_transformation = transform_europe_silver(eu_silver_extraction)
#     eu_silver_load = load_europe_silver(eu_silver_transformation)

#     cn_silver_extraction = extract_china_silver()
#     cn_silver_transformation = transform_china_silver(cn_silver_extraction)
#     cn_silver_load = load_china_silver(cn_silver_transformation)

#     exchange_task = exchange_silver()

#     silver_end = silver_validation()

#     gold_op = gold_ETL()

#     gold_end = gold_validation()


#     bronze_end >> [
#         btc_silver_extraction,
#         fx_silver_extraction,
#         usa_silver_extraction,
#         jp_silver_extraction,
#         eu_silver_extraction,
#         cn_silver_extraction
#         ]


#     btc_silver_extraction >> btc_silver_transformation
#     fx_silver_extraction >> fx_silver_transformation
#     usa_silver_extraction >> usa_silver_transformation
#     jp_silver_extraction >> jp_silver_transformation
#     eu_silver_extraction >> eu_silver_transformation
#     cn_silver_extraction >> cn_silver_transformation

#     btc_silver_transformation >> btc_silver_load
#     fx_silver_transformation >> fx_silver_load
#     usa_silver_transformation >> usa_silver_load
#     jp_silver_transformation >> jp_silver_load
#     eu_silver_transformation >> eu_silver_load
#     cn_silver_transformation >> cn_silver_load

#     [
#         btc_silver_load,
#         fx_silver_load,
#         usa_silver_load,
#         jp_silver_load,
#         eu_silver_load,
#         cn_silver_load
#     ] >> exchange_task

#     exchange_task >> silver_end 

#     silver_end >> gold_op

#     gold_op >> gold_end


# PF_dag()