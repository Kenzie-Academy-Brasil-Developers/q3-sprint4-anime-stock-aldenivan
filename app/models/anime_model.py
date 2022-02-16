from app.models import DataBaseSettings
from psycopg2 import sql


class Anime(DataBaseSettings):

    anime_keys = ["id", "anime", "released_date", "seasons"]
    valid_keys = ["anime", "released_date", "seasons"]

    def __init__(self, **kwargs):
        self.anime = kwargs["anime"].capitalize()
        self.released_date = kwargs["released_date"]
        self.seasons = kwargs["seasons"]
    
    def create_anime(self):
        self.create_table()

        self.get_conn_cur()

        query = """
            INSERT INTO
                animes (anime, released_date, seasons)
            VALUES
                (%s, %s, %s)
            RETURNING*       
        """

        query_values = list(self.__dict__.values())

        self.cur.execute(query, query_values)

        inserted_anime = self.cur.fetchone()

        self.commit_and_close()

        return inserted_anime


    @classmethod
    def create_table(cls):
        cls.get_conn_cur()

        query = """
            CREATE TABLE IF NOT EXISTS animes(
                id 				BIGSERIAL 		PRIMARY KEY,
                anime 			VARCHAR(100) 	NOT NULL UNIQUE,
                released_date 	DATE 			NOT NULL,
                seasons 		INTEGER 		NOT NULL
            );
        """

        cls.cur.execute(query)

        cls.commit_and_close()
        

    @classmethod
    def read_all_animes(cls):
        cls.create_table()

        cls.get_conn_cur()

        query = "SELECT * FROM animes"

        cls.cur.execute(query)

        list_animes = cls.cur.fetchall()

        cls.commit_and_close

        return list_animes


    @classmethod
    def read_by_id(cls, id):
        
        cls.create_table()

        cls.get_conn_cur()

        query = sql.SQL("""
            SELECT 
                * 
            FROM 
                animes 
            WHERE 
                id={id}
        """).format(
            id = sql.Literal(id)
        )

        cls.cur.execute(query)

        anime = cls.cur.fetchone()

        cls.commit_and_close()

        return anime



    @classmethod
    def update_by_id(cls, id, payload):
        cls.create_table()

        cls.get_conn_cur()

        columns = [sql.Identifier(key) for key in payload.keys()]
        values = [sql.Literal(value) for value in payload.values()]

        query = sql.SQL("""
            UPDATE
                animes
            SET
                ({columns}) = ROW({values})
            WHERE
                id = {id}        
            RETURNING *    
        """).format(
            id = sql.Literal(id),
            columns = sql.SQL(",").join(columns),
            values = sql.SQL(",").join(values),
        )

        cls.cur.execute(query)

        anime = cls.cur.fetchone()

        cls.commit_and_close()  

        return anime


    @classmethod
    def delete_by_id(cls, id):

        cls.get_conn_cur()

        query = sql.SQL("""
            DELETE 
            FROM 
                animes 
            WHERE 
                id = {id} 
            RETURNING *
        """).format(
            id = sql.Literal(id)
        )

        cls.cur.execute(query)

        anime = cls.cur.fetchone()

        cls.commit_and_close()

        return anime


    @staticmethod
    def serealiaze_anime(data, keys=anime_keys):
        if type(data) is tuple:
            return dict(zip(keys, data))

        if type(data) is list:
            return [dict(zip(keys, serie)) for serie in data]        

  
    @classmethod
    def available_keys(cls, keys_sended):
        
        wrong_keys = []

        for key in keys_sended:
            if not key in cls.valid_keys:
                wrong_keys.append(key)

        return wrong_keys    