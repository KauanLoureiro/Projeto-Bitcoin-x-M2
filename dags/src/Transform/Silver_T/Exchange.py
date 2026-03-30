from airflow.providers.postgres.hooks.postgres import PostgresHook

def exchange():
    hook = PostgresHook(postgres_conn_id="postgres_dw")
    conn = hook.get_conn()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS silver.m2_cn_dol(
                YearMonth TEXT,
                m2_cn_m_dol FLOAT
                );
                """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS silver.m2_eu_dol(
                YearMonth TEXT,
                m2_eu_m_dol FLOAT
                );
                """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS silver.m2_jp_dol(
                YearMonth TEXT,
                m2_jp_m_dol FLOAT
                );
                """)

    cur.execute("TRUNCATE TABLE silver.m2_cn_dol;")
    cur.execute("TRUNCATE TABLE silver.m2_eu_dol;")
    cur.execute("TRUNCATE TABLE silver.m2_jp_dol;")

    cur.execute("""
        INSERT INTO silver.m2_cn_dol(
                SELECT
                    t1.yearmonth,
                    t1.m2_cn*t2.cnyusd AS m2_cn_m_dol
                FROM silver.m2_cn_cny AS t1

                LEFT JOIN silver.fx AS t2
                ON t1.yearmonth = t2.yearmonth
                );
                """)

    cur.execute("""
        INSERT INTO silver.m2_eu_dol(
                SELECT
                    t1.yearmonth,
                    t1.m2_eu*t2.eurusd AS m2_eu_m_dol
                FROM silver.m2_eu_eur AS t1

                LEFT JOIN silver.fx AS t2
                ON t1.yearmonth = t2.yearmonth
                );
                """)

    cur.execute("""
        INSERT INTO silver.m2_jp_dol(
                SELECT
                    t1.yearmonth,
                    t1.m2_jp*t2.jpyusd AS m2_jp_m_dol
                FROM silver.m2_jp_jpy AS t1

                LEFT JOIN silver.fx AS t2
                ON t1.yearmonth = t2.yearmonth
                );
                """)

    conn.commit()
    cur.close()
    conn.close()