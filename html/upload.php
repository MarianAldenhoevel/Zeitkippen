<?php

ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

function rmdir_recursive($folderName) {
     if (is_dir($folderName)) {
          $folderHandle = opendir($folderName);
          if (!$folderHandle) {
               return false;
          }

          while ($file = readdir($folderHandle)) {
               if ($file != "." && $file != "..") {
                    if (!is_dir($folderName."/".$file)) {
                         unlink($folderName."/".$file);
                    }
                    else {
                         removeFolder($folderName.'/'.$file);
                    }
               }
          }

          closedir($folderHandle);
          rmdir($folderName);
     }
}

// Check for presence and validity of email address:
$email = $_POST["email"];
$email = filter_var($email, FILTER_SANITIZE_EMAIL);
if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
     header('Location: /upload_error.html');
}

// Find the temporary upload file and hash its contents.
$tmp_file = $_FILES['file']['tmp_name'];
$upload_id = md5_file($tmp_file);

// Create a fresh folder with that hash as a name.
$target_dir = "data/" . $upload_id;
rmdir_recursive($target_dir);
if (!is_dir($target_dir)) {
	mkdir($target_dir);
}

// Get original file extension
$path_parts = pathinfo($_FILES['file']['name']);

// Move input file to input.<ext> into the hash-named folder.
$destination = $target_dir . "/input." . $path_parts['extension'];
if (move_uploaded_file($tmp_file, $destination)) {

     // Build a commandline for Zeitkippen.py:

     header('Location: /upload_ok.html');
	exit;
}

header('Location: /upload_error.html');

?>
