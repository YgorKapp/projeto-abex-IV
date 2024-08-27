<?php
include_once("conexao/Conexao.php");

session_start(); // Starting Session
$error=''; // Variable To Store Error Message

//$error = "Acesso temporariamente bloqueado.";
    
 
if (isset($_POST['submit'])) {	
	if (empty($_POST['username']) || empty($_POST['password'])) {
		$error = "Informe seu e-mail e senha!<br>";
	}
	else {
	    $Conexao = new Conexao();
	    $conn = $Conexao->criarConexao();
	    
		// Define $username and $password
		$username=$_POST['username'];
		$password=$_POST['password'];
		//Establishing Connection with Server by passing server_name, user_id and password as a parameter
		
		// previne SQL Injection
		$username = stripslashes($username);
		$password = stripslashes($password);
		$username = mysqli_real_escape_string($conn, $username);
		$password = mysqli_real_escape_string($conn, $password);

		$BUSCAUSUARIO = "";
	    $BUSCADADOSUSUARIO = "SELECT idusuario, nome FROM usuarios WHERE email='$username' AND (senha='".sha1($password)."' AND status=1";
	    $query = mysqli_query ( $conn, $BUSCADADOSUSUARIO );
	    $rows = mysqli_num_rows($query);
	    if($rows == 1) {
            $idUsuario = -1;     $nome = "";		
			while($row = mysqli_fetch_array ( $query )){
				$idUsuario= $row['idusuario'];
				$nome = $row['nome'];
			}
            $_SESSION['idUsuario']=$idUsuario;
            $_SESSION['nome']=$nome;
			mysqli_close($conn); 
			header("location: home.html"); 
		} else {      
		    session_unset();     
		    session_destroy();   
			$error = "Usuário ou Senha Inválidos!<br>";
		}
        mysqli_close($conn); 
	}
}

?>