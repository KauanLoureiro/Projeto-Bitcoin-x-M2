from airflow.providers.postgres.hooks.postgres import PostgresHook

def gold_operation():

    hook = PostgresHook(postgres_conn_id="postgres_dw")
    conn = hook.get_conn()
    cur = conn.cursor()

    cur.execute("CREATE SCHEMA IF NOT EXISTS gold;")

    cur.execute(""" 
                CREATE TABLE IF NOT EXISTS gold.btc_dol(
                yearmonth TEXT,
                btc_price FLOAT
                ); 
                """)

    cur.execute(""" 
                CREATE TABLE IF NOT EXISTS gold.m2_global(
                yearmonth TEXT,
                m2_global FLOAT
                ); 
                """)

    cur.execute("""
                TRUNCATE TABLE gold.btc_dol
    """)

    cur.execute("""
                TRUNCATE TABLE gold.m2_global
    """)

    cur.execute("""
                INSERT INTO gold.btc_dol(
                SELECT * FROM silver.btc_dol
                );
    """)

    cur.execute("""
                INSERT INTO gold.m2_global(
                SELECT 
                    t1.yearmonth, 
                    m2_cn_m_dol+m2_eu_m_dol+m2_jp_m_dol+m2_us AS m2_global
                FROM silver.m2_cn_dol AS t1

                INNER JOIN silver.m2_eu_dol AS t2
                ON t1.yearmonth = t2.yearmonth

                INNER JOIN silver.m2_jp_dol AS t3
                ON t1.yearmonth = t3.yearmonth

                INNER JOIN silver.m2_us_dol AS t4
                ON t1.yearmonth = t4.yearmonth
                );
    """)

    conn.commit()
    cur.close()
    conn.close()