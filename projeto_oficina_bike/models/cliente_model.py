from database.conexao import conectar

class ClienteModel:

    def listar(self):
        conn = conectar()
        cursor = conn.cursor()
        sql = "SELECT * FROM clientes"
        cursor.execute(sql)
        dados = cursor.fetchall()
        conn.close()
        return dados

    def buscar_por_id(self, id):
        conn = conectar()
        cursor = conn.cursor()
        sql = "SELECT * FROM clientes WHERE id=%s"
        cursor.execute(sql, (id,))
        dado = cursor.fetchone()
        conn.close()
        return dado

    def inserir(self, nome, telefone, email, endereco):
        conn = conectar()
        cursor = conn.cursor()
        sql = "INSERT INTO clientes (nome, telefone, email, endereco) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (nome, telefone, email, endereco))
        conn.commit()
        conn.close()

    def atualizar(self, id, nome, telefone, email, endereco):
        conn = conectar()
        cursor = conn.cursor()
        sql = "UPDATE clientes SET nome=%s, telefone=%s, email=%s, endereco=%s WHERE id=%s"
        cursor.execute(sql, (nome, telefone, email, endereco, id))
        conn.commit()
        conn.close()

    def deletar(self, id):
        conn = conectar()
        cursor = conn.cursor()
        sql = "DELETE FROM clientes WHERE id=%s"
        cursor.execute(sql, (id,))
        conn.commit()
        conn.close()
