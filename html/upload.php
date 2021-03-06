<?php

ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

function safe_filename($input) {
     $whitelist = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_äöüÄÖÜß';
     $result = '';
     
     $i = 0;
     while ($i < strlen($input)) {
          if (strpos($whitelist, $input{$i}, 0) !== false) {
               $result = $result . $input{$i};
          } else 
          {
               $result = $result . '_';
          }
          $i++;
     }

     return $result;
}

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
                         rmdir_recursive($folderName.'/'.$file);
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

file_put_contents( $target_dir . '/email.txt' , $email);
     
// Get original file extension
$path_parts = pathinfo($_FILES['file']['name']);

// Move input file to input.<ext> into the hash-named folder.
$destination = $target_dir . "/input." . $path_parts['extension'];
if (move_uploaded_file($tmp_file, $destination)) {

     $mailsubject = safe_filename($_FILES['file']['name']);
     
     // Build a commandline for Zeitkippen.py:
     $cmd = 'python3 ./Zeitkippen.py -ll DEBUG -mt ' . $email . ' -ms ' . $mailsubject . ' -if ' . $target_dir . '/input.mp4 > ' . $target_dir . '/stdout.txt 2> ' . $target_dir . '/stderr.txt';
     file_put_contents( $target_dir . '/cmd.txt' , $cmd);
     exec($cmd . ' > /dev/null &');

     header('Location: /upload_ok.html');
	exit;
}

header('Location: /upload_error.html');

?>
