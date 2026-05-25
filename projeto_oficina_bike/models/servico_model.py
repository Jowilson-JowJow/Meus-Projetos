from database.conexao import conectar

class ServicoModel:

    def listar(self):
        conn = conectar()
        cursor = conn.cursor()
        sql = """
            SELECT s.id, c.nome, b.marca, b.modelo, s.descricao, s.valor, s.status, s.data_entrada, s.data_saida
            FROM servicos s
            JOIN bicicletas b ON s.bicicleta_id = b.id
            JOIN clientes c ON b.cliente_id = c.id
        """
        cursor.execute(sql)
        dados = cursor.fetchall()
        conn.close()
        return dados

    def buscar_por_id(self, id):
        conn = conectar()
        cursor = conn.cursor()
        sql = "SELECT * FROM servicos WHERE id=%s"
        cursor.execute(sql, (id,))
        dado = cursor.fetchone()
        conn.close()
        return dado

    def inserir(self, bicicleta_id, descricao, valor, status, data_entrada, data_saida):
        conn = conectar()
        cursor = conn.cursor()
        sql = """
            INSERT INTO servicos (bicicleta_id, descricao, valor, status, data_entrada, data_saida)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (bicicleta_id, descricao, valor, status, data_entrada, data_saida))
        conn.commit()
        conn.close()

    def atualizar(self, id, bicicleta_id, descricao, valor, status, data_entrada, data_saida):
        conn = conectar()
        cursor = conn.cursor()
        sql = """
            UPDATE servicos SET bicicleta_id=%s, descricao=%s, valor=%s, status=%s,
            data_entrada=%s, data_saida=%s WHERE id=%s
        """
        cursor.execute(sql, (bicicleta_id, descricao, valor, status, data_entrada, data_saida, id))
        conn.commit()
        conn.close()

    def deletar(self, id):
        conn = conectar()
        cursor = conn.cursor()
        sql = "DELETE FROM servicos WHERE id=%s"
        cursor.execute(sql, (id,))
        conn.commit()
        conn.close()
