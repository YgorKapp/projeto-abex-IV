<?php

class Conexao{

	function criarConexao() {
		try { 
		    $host = "";     //configuracoes locais
			$username = "";		
			$password = "";
			$db_name = "";

			$con = mysqli_connect ( "$host", "$username", "$password" ) or die ( "cannot connect; "+mysqli_error($con) );
			mysqli_select_db ( $con, "$db_name" ) or die ( "cannot select DB; "+mysqli_error($con) );
            mysqli_set_charset ( $con , "utf8" );
            
			return $con;

		} catch ( Exception $e ) {
			print "Error!: " . $e->getMessage() . "<br/>";
			die();
			return null;
		}
	}

}

?>
