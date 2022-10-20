import io
from sqlalchemy import create_engine


def store_data(username, password, host, port, db_name, df,sql_table_name):

        engine = create_engine(f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{db_name}')

        df.head(0).to_sql(sql_table_name, engine, if_exists='replace',index=False) #drops old table and creates new empty table

        conn = engine.raw_connection()
        cur = conn.cursor()
        output = io.StringIO()
        df.to_csv(output, sep='\t', header=False, index=False)
        output.seek(0)
        contents = output.getvalue()
        cur.copy_from(output, sql_table_name, null="") # null values become ''
        conn.commit()
