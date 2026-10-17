<?php

    class UsuarioController{
        public function salvar(){
            //cria o modelo e reenche com os dados enviados via POST pelo formulario
            $model = new UsuarioModel();
            $model->nome = $_POST['nome'];
            $model->email = $_POST['email'];
            $model->senha = $_POST['senha'];

            //envia o modelo para a DAO realizar a gravaçãono banco
            $dao = new UsuarioDAO();
            $dao->inserir($model);

            //redireciona para a agina de login após o cadastro
            header('Location: /primeiro_mvc/index.php?url=usuario/loginForm');
            exit;
        }
        
        public function form(){
            include __DIR__ . '/../View/form_usuario.php';
        }
    }


?>
