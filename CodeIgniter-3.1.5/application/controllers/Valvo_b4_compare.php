<!-- 
Project's website is implemented using Codeigniter PHP framework. For learning and simplicity's sake,
the whole webpage with its subpages are contained in this Valvo.php -file, in their own functions.

-->

<?php
class Valvo extends CI_Controller {

# http://172.20.240.54/index.php/valvo/

        public function index()
        {
?>
<head>
  <title>Valvontadata</title>
  <h1>Valvontadata</h1>
</head>
<br>

<div class="topnav">
  <a href="http://172.20.240.54/">Home</a>
  <a href="http://172.20.240.54/index.php/valvo/tables">Full database</a>
  <a href="http://172.20.240.54/index.php/valvo/pictures">Pictures</a>
</div>

<style>
/* GRID DEFINING WITH CSS FOR WEB LAYOUT */
* {
  box-sizing: border-box;
}

body {
  font-family: Arial, Helvetica, sans-serif;
}

/* Style the header */
.header {
  grid-area: header;
  background-color: #f1f1f1;
  padding: 20px;
  text-align: center;
  font-size: 18px;
}

/* The grid container */
.grid-container {
  display: grid;
  grid-template-areas: 
    'header header header header' 
    'left left right right' 
    'footer footer footer footer';
  /* grid-column-gap: 10px; - if you want gap between the columns */
} 

.left,
.right {
  padding: 10px;
}

/* Style the left column */
.left {
  grid-area: left;
}

/* Style the right column */
.right {
  grid-area: right;
}

/* Style the footer */
.footer {
  grid-area: footer;
  background-color: #f1f1f1;
  padding: 10px;
  text-align: center;
}

/* Responsive layout - makes the three columns stack on top of each other instead of next to each other */
@media (max-width: 900px) {
  .grid-container  {
    grid-template-areas: 
      'header header header header' 
      'left left left left' 
      'right right right right' 
      'footer footer footer footer';
  }
}

/*####### Add a black background color to the top navigation #########*/
.topnav {
  background-color: #333;
  overflow: hidden;
}

/* Style the links inside the navigation bar */
.topnav a {
  float: left;
  color: #f2f2f2;
  text-align: center;
  padding: 14px 16px;
  text-decoration: none;
  font-size: 17px;
}

/* Change the color of links on hover */
.topnav a:hover {
  background-color: #ddd;
  color: black;
}

/* Add a color to the active/current link */
.topnav a.active {
  background-color: #4CAF50;
  color: white;
}
</style>


<div class="grid-container"> <!-- HEADER CONTENT HERE (stops at /div) -->
  <div class="header">
  <div id="box" align="center">

<h2>Latest image: </h2>

<?php 
$dir2 = "images/";
$images2 = glob($dir2 . "*.{gif,png,jpg,jpeg}", GLOB_BRACE); //formats to look for
foreach ($images2 as $f) {
    # store the image name
    $list[] = $f;
}

sort($list);                    # sort is oldest to newest,

$newimg = array_pop($list);   # Newest
echo "<img src='/$newimg' width='960' height='540'><br><br>"; # print image
echo "$newimg"; # print image directory
echo "<br>";
echo "<br>";

$this->load->helper('url');

        # Lataa codeigniterin DB-kirjaston, login asetukset ovat \application\config\database.php
        $this->load->database();
                
        # Lataa codeigniterin automaattisen taulukko-muotoilun kirjastosta

        $this->load->library('table');

        $template = array(
                'table_open' => '<table border="1" cellpadding="2" cellspacing="1" class="mytable">'
        );
        
        $this->table->set_template($template); 

$query = $this->db->query('SELECT idTunnistus as ID, k_aika as Time, ihmiset_kpl as Camera, odotettu_kpl as Sensors FROM Tunnistus ORDER BY k_aika DESC LIMIT 1');
echo $this->table->generate($query);

?>
</div>
</div> <!-- ------------------------------------------------------------------ -->


<div class="left" style="background-color:#aaa;"> <!-- - LEFT COLUMN CONTENT - -->

<html>
<!-- http://172.20.240.54/images/snapshot-2019-12-05-095605-detected.jpg
tai
2019-12-05-095605 <- karikuva -->
<p>Show image by timestamp. Format: yyyy-mm-dd-hhmmss</p>
<p> (eg. 2019-12-05-095605) </p>
<form onsubmit="location.href='http://172.20.240.54/images/' + 'snapshot-' + document.getElementById('myInput').value + '-detected.jpg'; return false;">
  <input type="text" id="myInput" />
  <input type="submit" />
</form>
<br>
<h3>Human Detection Count by Camera & Sensors: </h3>
</html> 
<?php
        # Toteutetaan SQL-kyselyt ja sovitetaan arvot taulukkoon 
         $query = $this->db->query('SELECT idTunnistus as ID, k_aika as Time, ihmiset_kpl as Camera, odotettu_kpl as Sensors FROM Tunnistus ORDER BY k_aika DESC LIMIT 15');
         echo $this->table->generate($query);
         echo '</br>';

         ?>
         </div>

<div class="right" style="background-color:#aaa;"> <!-- - RIGHT COLUMN CONTENT - -->
<html>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<h3>Sensor measures: </h3>
</html>
<?php

          $query = $this->db->query('SELECT idArduino1, a1_aika as Time, a1_leveys as Width, idTunnistus as ID FROM Arduino1 ORDER BY a1_aika DESC LIMIT 15');
          echo $this->table->generate($query);
          echo '</br>';
?>
<h3>Detection count (hourly): </h3>
<?php
          $query2 = $this->db->query('SELECT sum(ihmiset_kpl) as Camera, sum(odotettu_kpl) as Sensors, date_format(k_aika, "%H - %d/%m/%y") as datecreated FROM Tunnistus WHERE k_aika > NOW() - INTERVAL 504 HOUR GROUP BY date_format(k_aika, "%H - %d/%m/%y") ORDER BY min(k_aika) ASC');
          echo $this->table->generate($query2);
          echo '</br>';

          #$query = $this->db->query('SELECT * FROM Arduino2 ORDER BY a2_aika DESC LIMIT 15');
          #        echo $this->table->generate($query);
          #        echo '</br>';
   

          $query = $this->db->query('SELECT sum(ihmiset_kpl) as ihmiset_kpl, date_format(k_aika, "%H - %d/%m/%y") as datecreated FROM Tunnistus WHERE k_aika > NOW() - INTERVAL 504 HOUR GROUP BY date_format(k_aika, "%H - %d/%m/%y") ORDER BY min(k_aika) ASC');
          $data_points = array();
          foreach ($query->result_array() as $row)
          {
            $point = array("label" => $row['datecreated'] , "y" => $row['ihmiset_kpl']);
            array_push($data_points, $point);    
          }

          $query = $this->db->query('SELECT sum(odotettu_kpl) as odotettu_kpl, date_format(k_aika, "%H - %d/%m/%y") as datecreated FROM Tunnistus WHERE k_aika > NOW() - INTERVAL 504 HOUR GROUP BY date_format(k_aika, "%H - %d/%m/%y") ORDER BY min(k_aika) ASC');
          $data_points2 = array();
          foreach ($query->result_array() as $row)
          {
            $point = array("label" => $row['datecreated'] , "y" => $row['odotettu_kpl']);
            array_push($data_points2, $point);    
          }
          echo "<br>";
?>
  <style>
  {
    border-collapse: collapse;
    width: 100%;
  }

  td, th {
    border: 1px solid #ddd;
    padding: 6px;
  }

  tr:nth-child(even){background-color: #f2f2f2;}

  tr:hover {background-color: #ddd;}

  th {
    padding-top: 3px;
    padding-bottom: 3px;
    text-align: left;
    background-color: #333;
    color: white;
  }
  </style>
</div>
</div>

 <!DOCTYPE HTML>
 <html>
 <head>  
 <script>

var dps = <?php echo json_encode($data_points, JSON_NUMERIC_CHECK); ?>;
var dps2 = <?php echo json_encode($data_points2, JSON_NUMERIC_CHECK); ?>;

 window.onload = function () {
 var chart = new CanvasJS.Chart("chartContainer", {
         animationEnabled: true,
         theme: "light2",
         title:{
                 text: "Detections per Hour"
         },
         legend:{
                 cursor: "pointer",
                 verticalAlign: "center",
                 horizontalAlign: "right",
                 itemclick: toggleDataSeries
         },
         data: [{
                 type: "area",
                 fillOpacity: .2,
                 name: "Camera",
                 indexLabel: "{y}",
                 yValueFormatString: "#0.##",
                 showInLegend: true,
                 dataPoints: dps
         },{
                 type: "area",
                 fillOpacity: .2,
                 name: "Sensordata",
                 indexLabel: "{y}",
                 yValueFormatString: "#0.##",
                 showInLegend: true,
                 dataPoints: dps2
         }]
 });
 chart.render();
  
 function toggleDataSeries(e){
         if (typeof(e.dataSeries.visible) === "undefined" || e.dataSeries.visible) {
                 e.dataSeries.visible = false;
         }
         else{
                 e.dataSeries.visible = true;
         }
         chart.render();
 }
 }
 </script>
 </head>
 <body>
 <div class="footer" id="chartContainer" style="height: 370px; width: 100%;"></div>
 <script src="https://canvasjs.com/assets/script/canvasjs.min.js"></script>
 </body>
 </html>                           

<?php
        }

########################################################################################
########################################################################################
########################################################################################

# Subpages
# 

        public function tables()
        {
          ?>

          <head>
            <title>Valvontadata</title>
            <h1>Valvontadata</h1>
          </head>
          <meta http-equiv="refresh" content="30">
          <br>
          
          <div class="topnav">
            <a href="http://172.20.240.54/">Home</a>
            <a href="http://172.20.240.54/index.php/valvo/tables">Full database</a>
            <a href="http://172.20.240.54/index.php/valvo/pictures">Pictures</a>
          </div>
          
          <style>
          /* GRID DEFINING WITH CSS FOR WEB LAYOUT */
          * {
            box-sizing: border-box;
          }
          
          body {
            font-family: Arial, Helvetica, sans-serif;
          }
          
          /* Style the header */
          .header {
            grid-area: header;
            background-color: #f1f1f1;
            padding: 30px;
            text-align: center;
            font-size: 35px;
          }
          
          /* The grid container */
          .grid-container {
            display: grid;
            grid-template-areas: 
              'header header header header' 
              'left left right right' 
              'footer footer footer footer';
            /* grid-column-gap: 10px; - if you want gap between the columns */
          } 
          
          .left,
          .right {
            padding: 10px;
          }
          
          /* Style the left column */
          .left {
            grid-area: left;
          }
          
          /* Style the right column */
          .right {
            grid-area: right;
          }
          
          /* Style the footer */
          .footer {
            grid-area: footer;
            background-color: #f1f1f1;
            padding: 10px;
            text-align: center;
          }
          
          /* Responsive layout - makes the three columns stack on top of each other instead of next to each other */
          @media (max-width: 900px) {
            .grid-container  {
              grid-template-areas: 
                'header header header header' 
                'left left left left' 
                'right right right right' 
                'footer footer footer footer';
            }
          }
        
          /*####### Add a black background color to the top navigation #########*/
          .topnav {
            background-color: #333;
            overflow: hidden;
          }
          
          /* Style the links inside the navigation bar */
          .topnav a {
            float: left;
            color: #f2f2f2;
            text-align: center;
            padding: 14px 16px;
            text-decoration: none;
            font-size: 17px;
          }
          
          /* Change the color of links on hover */
          .topnav a:hover {
            background-color: #ddd;
            color: black;
          }
          
          /* Add a color to the active/current link */
          .topnav a.active {
            background-color: #4CAF50;
            color: white;
          }
          </style>
          
          
          <div class="grid-container"> <!-- HEADER CONTENT HERE (stops at /div) -->
          
          <div class="left" style="background-color:#aaa;"> <!-- - LEFT COLUMN CONTENT - -->
          <?php
          
                      $this->load->helper('url');
          
                      # Lataa codeigniterin DB-kirjaston, login asetukset ovat \application\config\database.php
                      $this->load->database();
                          
                  # Lataa codeigniterin automaattisen taulukko-muotoilun kirjastosta
          
                  $this->load->library('table');
          
                  $template = array(
                          'table_open' => '<table border="1" cellpadding="2" cellspacing="1" class="mytable">'
                  );
                  
                  $this->table->set_template($template);        
          
                  # Toteutetaan SQL-kyselyt ja sovitetaan arvot taulukkoon 
                   $query = $this->db->query('SELECT * FROM Tunnistus ORDER BY k_aika DESC');
                   echo $this->table->generate($query);
                   echo '</br>';
          
                   ?>
                   </div>
          
          <div class="right" style="background-color:#aaa;"> <!-- - RIGHT COLUMN CONTENT - -->
          
                  <?php
          
                    $query2 = $this->db->query('SELECT sum(ihmiset_kpl) as ihmiset_kpl, sum(odotettu_kpl) as odotettu_kpl, date_format(k_aika, "%H - %d/%m/%y") as datecreated FROM Tunnistus WHERE k_aika > NOW() - INTERVAL 504 HOUR GROUP BY date_format(k_aika, "%H - %d/%m/%y") ORDER BY min(k_aika) ASC');
                            echo $this->table->generate($query2);
                            echo '</br>';

                    $query = $this->db->query('SELECT * FROM Arduino1 ORDER BY a1_aika DESC');
                            echo $this->table->generate($query);
                            echo '</br>';
          
                    $query = $this->db->query('SELECT * FROM Arduino2 ORDER BY a2_aika DESC');
                            echo $this->table->generate($query);
                            echo '</br>';
             
          
          $query = $this->db->query('SELECT sum(ihmiset_kpl) as ihmiset_kpl, date_format(k_aika, "%H - %d/%m/%y") as datecreated FROM Tunnistus WHERE k_aika > NOW() - INTERVAL 1504 HOUR GROUP BY date_format(k_aika, "%H - %d/%m/%y") ORDER BY min(k_aika) ASC');
          $data_points = array();
          foreach ($query->result_array() as $row)
          {
            $point = array("label" => $row['datecreated'] , "y" => $row['ihmiset_kpl']);
            array_push($data_points, $point);    
          }
          
          $query = $this->db->query('SELECT sum(odotettu_kpl) as odotettu_kpl, date_format(k_aika, "%H - %d/%m/%y") as datecreated FROM Tunnistus WHERE k_aika > NOW() - INTERVAL 1504 HOUR GROUP BY date_format(k_aika, "%H - %d/%m/%y") ORDER BY min(k_aika) ASC');
          $data_points2 = array();
          foreach ($query->result_array() as $row)
          {
            $point = array("label" => $row['datecreated'] , "y" => $row['odotettu_kpl']);
            array_push($data_points2, $point);    
          }
                 
          ?>
          
          <style>
          {
            border-collapse: collapse;
            width: 100%;
          }
          
          td, th {
            border: 1px solid #ddd;
            padding: 6px;
          }
          
          tr:nth-child(even){background-color: #f2f2f2;}
          
          tr:hover {background-color: #ddd;}
          
          th {
            padding-top: 3px;
            padding-bottom: 3px;
            text-align: left;
            background-color: #333;
            color: white;
          }
          </style>
          </div>
          </div>
          
          <?php
        }

#############################################################################################
###################################### PICTURES ###############################################
#############################################################################################
        public function pictures()
        {
?>       

<head>
  <title>Valvontadata</title>
  <h1>Valvontadata</h1>
</head>
<br>

<div class="topnav">
  <a href="http://172.20.240.54/">Home</a>
  <a href="http://172.20.240.54/index.php/valvo/tables">Full database</a>
  <a href="http://172.20.240.54/index.php/valvo/pictures">Pictures</a>
</div>

<style>

body {
  font-family: Arial, Helvetica, sans-serif;
}

/* Add a black background color to the top navigation */
.topnav {
  background-color: #333;
  overflow: hidden;
}

/* Style the links inside the navigation bar */
.topnav a {
  float: left;
  color: #f2f2f2;
  text-align: center;
  padding: 14px 16px;
  text-decoration: none;
  font-size: 17px;
}

/* Change the color of links on hover */
.topnav a:hover {
  background-color: #ddd;
  color: black;
}

/* Add a color to the active/current link */
.topnav a.active {
  background-color: #4CAF50;
  color: white;
}
</style>

<div id="content" align="center">

<h2>Latest image: </h2>

<?php 
$dir2 = "images/";
$images2 = glob($dir2 . "*.{gif,png,jpg,jpeg}", GLOB_BRACE); //formats to look for
foreach ($images2 as $f) {
    # store the image name
    $list[] = $f;
}

sort($list);                    # sort is oldest to newest,

$newimg = array_pop($list);   # Newest
echo "<img src='/$newimg' width='960' height='540'><br><br>";
echo "$newimg";
echo "<br>";

?>

 <body style="text-align:center;"> 
        
      <h4> 
        
      </h4> 
    
      <?php

$this->load->database();
$this->load->library('table');

$template = array(
           'table_open' => '<table border="1" cellpadding="2" cellspacing="1" class="mytable">'
           );
        
$this->table->set_template($template);      

$query = $this->db->query('SELECT idTunnistus as ID, k_aika as Time, ihmiset_kpl as Camera, odotettu_kpl as Sensors FROM Tunnistus ORDER BY k_aika DESC LIMIT 1');
  echo $this->table->generate($query);
  echo '</br>';


          # Take a photo-button
          if(isset($_POST['snapshot'])) {
           $command = "/usr/bin/env python3 /var/www/CodeIgniter/images/hellopython.py";  
           $message2=exec($command, $out, $status);
            print_r($message2);
            echo ", refreshing after 5 seconds";
            echo "<meta http-equiv='refresh' content='5'>";
          }
          # Compress images-button
          if(isset($_POST['compress'])) { 
            echo "Compression requested: ";
            $message=shell_exec("/var/www/CodeIgniter/images/compressJpeg.sh");
            print_r($message);
          }
      ?> 
      <!-- HTML buttons -->  
      <form method="post"> 
          <input type="submit" name="snapshot"
                  value="Take a photo"/> 
      </form>

      <form method="post"> 
          <input type="submit" name="compress"
                  value="Compress uncompressed images"/> 
      </form>  
  </head> 
  
  <?php

 ##### GALLERY #####

// READ FILES FROM THE GALLERY FOLDER
$dir = "images/";
$images = glob($dir . "*.{jpg,jpeg,gif,png}", GLOB_BRACE);

?>
</div>

<html>
  <head>
    <link href="1-basic.css" rel="stylesheet">
  </head>
    <!-- [THE GALLERY] -->
    <div id="gallery"><?php
    foreach ($images as $i) {
      printf("<img src='/images/%s' title='%s' />", basename($i), basename($i));
    }
    ?></div>
  </body>
</html>



<style>

  {
    border-collapse: collapse;
    width: 100%;
  }

  td, th {
    border: 1px solid #ddd;
    padding: 6px;
  }

  tr:nth-child(even){background-color: #f2f2f2;}

  tr:hover {background-color: #ddd;}

  th {
    padding-top: 3px;
    padding-bottom: 3px;
    text-align: left;
    background-color: #333;
    color: white;
  }

body, html {
  padding: 0;
  margin: 0;
}

/* [GALLERY] */
#gallery {
  max-width: 1200px;
  margin: 0 auto;
}

#gallery img {
  box-sizing: border-box;
  width: 25%;
  max-height: 150px;
  padding: 5px;
  /* fill, contain, cover, scale-down : use whichever you like */
  object-fit: cover;
  cursor: pointer;
}

/* [RESPONSIVE GALLERY] */
@media screen and (max-width: 850px) {
  #gallery img {
    width: 33%;
  }
}

@media screen and (max-width: 640px) {
  #gallery img {
    width: 50%;
  }
}
</style>
<?php                
        }
}
?>