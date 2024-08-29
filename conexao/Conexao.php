<?php

class Conexao{

	function criarConexao() {
		try { 
		    $host = "http://onebus.cx8kmic8cryz.us-east-2.rds.amazonaws.com/";   //18.216.171.234
			$username = "admin";		
			$password = "onebus123";
			$db_name = "onebus";

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
