<?php

    session_start();

    require_once 'config.php';
    require_once 'Model/UsuarioModel.php';
    require_once 'DAO/UsuarioDAO.php';
    require_once 'Controller/UsuarioController.php';

    $url = $_GET['url'] ?? 'usuario/form';
    $partes = explode('/' , trim($url, '/'));

    $controllerNome = ucfirst($partes[0]) . 'Controller';
    $metodo = $partes[1] ?? 'form';

    if (class_exists($controllerNome) && method_exists($controllerNome, $metodo)){
        $controller = new $controllerNome();
        $controller->$metodo();
    }
    else{
        http_response_code(404);
        echo 'Pagina não encontrada';
    }

?>