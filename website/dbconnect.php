<?php

$db_host = "localhost";
$db_name = "Boxsand";
$db_user = "boxsanddb";
$db_pass = "lOlsBS7sqnuI7MKM";


$conn = mysqli_connect($db_host, $db_user, $db_pass, $db_name);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}
