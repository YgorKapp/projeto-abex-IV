<?php
include('../../validalogin.php');
?>
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="../css/style.css">
    <link rel="website icon" type="png" href="../img/logo.png">
    <title>Login</title>
</head>
<body class="body-background">
    <a href="#" class="goback" id="backButton"><img src="{{url_for('static', filename='img/goback.png')}}" alt="seta para voltar a home" title="Seta para voltar a home"></a>
    <div class="div-login">
        <h1 class="login">Login</h1>
    </div>
    <form class="input-login" method="post">
        <input type="text" name="username" placeholder="Usuário" class="input-login-usuario" required>
        <input type="password" name="password" placeholder="Senha" class="input-login-senha" required>
        <input type="submit" name="submit" class="button-login" value="Entrar">
    </form>
</body>
</html>