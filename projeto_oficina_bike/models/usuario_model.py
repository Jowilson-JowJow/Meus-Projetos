from database.conexao import conectar

class UsuarioModel:

    def validar_login(self, email, senha):
        conn = conectar()
        cursor = conn.cursor()
        sql = "SELECT * FROM usuarios WHERE email=%s AND senha=%s"
        cursor.execute(sql, (email, senha))
        usuario = cursor.fetchone()
        conn.close()
        return usuario

    def listar(self):
        conn = conectar()
        cursor = conn.cursor()
        sql = "SELECT * FROM usuarios"
        cursor.execute(sql)
        dados = cursor.fetchall()
        conn.close()
        return dados

    def inserir(self, nome, email, senha):
        conn = conectar()
        cursor = conn.cursor()
        sql = "INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)"
        cursor.execute(sql, (nome, email, senha))
        conn.commit()
        conn.close()

    def atualizar(self, id, nome, email, senha):
        conn = conectar()
        cursor = conn.cursor()
        sql = "UPDATE usuarios SET nome=%s, email=%s, senha=%s WHERE id=%s"
        cursor.execute(sql, (nome, email, senha, id))
        conn.commit()
        conn.close()

    def deletar(self, id):
        conn = conectar()
        cursor = conn.cursor()
        sql = "DELETE FROM usuarios WHERE id=%s"
        cursor.execute(sql, (id,))
        conn.commit()
        conn.close()
