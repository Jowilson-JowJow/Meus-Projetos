<?php
    include_once __DIR__ . '/../Includes/header.php';
?>
<main class = "container mt-5">
    <div class = "row justify-content-center">
        <div class = "col-md-6">
            <div class = "card shadow">
                <div class ="card-header bg-primary text-white">
                    <h4 class = "mb-0">Cadastro de Usuário</h4>
                </div>
                <div class="card-body">
                    <form action="/primeiro_mvc/index.php?url=usuario/salvar" method="POST">
                        <div class ="mb-3">
                            <label for = "nome" class="form-label">Nome Completo:</label>
                            <input type = "text" class="form-control" id="nome" name="nome" required>
                        </div>
                        
                        <div class ="mb-3">
                            <label for = "email" class="form-label">E-mail:</label>
                            <input type = "email" class="form-control" id="email" name="email" required>
                        </div>
                        
                        <div class ="mb-3">
                            <label for = "senha" class="form-label">Senha:</label>
                            <input type = "password" class="form-control" id="senha" name="senha" required>
                        </div>

                        <div class="d-grid gap-2">
                            <button type="submit" class="btn btn-success">Salvar Cadastro</button>
                            <a href="/primeiro_mvc/index.php?url=usuario/loginForm" class="btn btn-secondary">Já tenho conta</a>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</main>

<?php
    include_once __DIR__ . '/../Includes/footer.php';
?>