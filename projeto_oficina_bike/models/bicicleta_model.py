from database.conexao import conectar

class BicicletaModel:

    def listar(self):
        conn = conectar()
        cursor = conn.cursor()
        sql = """
            SELECT b.id, c.nome, b.marca, b.modelo, b.cor, b.numero_serie
            FROM bicicletas b
            JOIN clientes c ON b.cliente_id = c.id
        """
        cursor.execute(sql)
        dados = cursor.fetchall()
        conn.close()
        return dados

    def listar_por_cliente(self, cliente_id):
        conn = conectar()
        cursor = conn.cursor()
        sql = "SELECT * FROM bicicletas WHERE cliente_id=%s"
        cursor.execute(sql, (cliente_id,))
        dados = cursor.fetchall()
        conn.close()
        return dados

    def buscar_por_id(self, id):
        conn = conectar()
        cursor = conn.cursor()
        sql = "SELECT * FROM bicicletas WHERE id=%s"
        cursor.execute(sql, (id,))
        dado = cursor.fetchone()
        conn.close()
        return dado

    def inserir(self, cliente_id, marca, modelo, cor, numero_serie):
        conn = conectar()
        cursor = conn.cursor()
        sql = "INSERT INTO bicicletas (cliente_id, marca, modelo, cor, numero_serie) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (cliente_id, marca, modelo, cor, numero_serie))
        conn.commit()
        conn.close()

    def atualizar(self, id, cliente_id, marca, modelo, cor, numero_serie):
        conn = conectar()
        cursor = conn.cursor()
        sql = "UPDATE bicicletas SET cliente_id=%s, marca=%s, modelo=%s, cor=%s, numero_serie=%s WHERE id=%s"
        cursor.execute(sql, (cliente_id, marca, modelo, cor, numero_serie, id))
        conn.commit()
        conn.close()

    def deletar(self, id):
        conn = conectar()
        cursor = conn.cursor()
        sql = "DELETE FROM bicicletas WHERE id=%s"
        cursor.execute(sql, (id,))
        conn.commit()
        conn.close()
