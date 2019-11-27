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
<meta http-equiv="refresh" content="30">
<br>

<div class="topnav">
  <a href="http://172.20.240.54/">All</a>
  <a href="http://172.20.240.54/index.php/valvo/tables">Full database</a>
  <a href="http://172.20.240.54/index.php/valvo/charts">Charts</a>
  <a href="http://172.20.240.54/index.php/valvo/pictures">Pictures</a>
</div>

<style>
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

<p>Latest image: </p>

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
echo array_pop($list);   # 2nd newest
?>

<?php

            $this->load->helper('url');

            # Lataa codeigniterin DB-kirjaston, login asetukset ovat \application\config\database.php
            $this->load->database();
                echo ' ';
                echo '</br>';
                echo '</br>';
                
        # Lataa codeigniterin automaattisen taulukko-muotoilun kirjastosta

        $this->load->library('table');

        $template = array(
                'table_open' => '<table border="1" cellpadding="2" cellspacing="1" class="mytable">'
        );
        
        $this->table->set_template($template);        

        # Toteutetaan SQL-kyselyt ja sovitetaan arvot taulukkoon 
         echo '<p>Total detections per hour: </p>';
         $query = $this->db->query('SELECT sum(ihmiset_kpl), sum(odotettu_kpl), date_format(k_aika, "%H - %d/%m/%y") as datecreated FROM Tunnistus WHERE k_aika > NOW() - INTERVAL 48 HOUR GROUP BY date_format(k_aika, "%H - %d/%m/%y") ORDER BY min(k_aika) ASC');
         echo $this->table->generate($query);
         echo '</br>';

         foreach ($query->result_array() as $tunniste_ihmiset)
         {
          echo '</br>';
          echo $tunniste_ihmiset['sum(ihmiset_kpl)'];
          echo '</br>';
         }

         foreach ($query->result_array() as $tunniste_odotettu)
         {
          echo '</br>';
          echo $tunniste_odotettu['sum(odotettu_kpl)'];
          echo '</br>';
         }

         foreach ($query->result_array() as $tunniste_date)
         {
          echo '</br>';
          echo $tunniste_date['datecreated'];
          echo '</br>';
         }


         echo '</br>';
         $query = $this->db->query('SELECT * FROM Tunnistus ORDER BY k_aika DESC');
         echo $this->table->generate($query);
         echo '</br>';

         $query = $this->db->query('SELECT * FROM Arduino1 ORDER BY a1_aika DESC');
         echo $this->table->generate($query);
         echo '</br>';
        
         $query = $this->db->query('SELECT * FROM Arduino2 ORDER BY a2_aika DESC');
         echo $this->table->generate($query);
         echo '</br>';

# Table CSS styling       
?>
<style>
{
  font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;
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

        <?php
# ------------------------------------------------------------------------------------------- 
# LUO ERILLINEN DB TAULUKKO JA TRIGGAA DATA VAIKKA TUNTEIHIN; YNNÄÄ HAVAINNOT NIIHIN

#fiksaa alla olevat arvot toimiviksi graafille

 $dataPoints1 = array(
         "label"=> $tunniste_date['datecreated'], "y"=> $tunniste_ihmiset['sum(ihmiset_kpl)']
 );
 $dataPoints2 = array(
  "label"=> $tunniste_date, "y"=> $tunniste_odotettu
);
         
 ?>
 
 <!DOCTYPE HTML>
 <html>
 <head>  
 <script>
 window.onload = function () {
  
 var chart = new CanvasJS.Chart("chartContainer", {
         animationEnabled: true,
         theme: "light2",
         title:{
                 text: "BIG VALVO DATA"
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
                 name: "to North",
                 indexLabel: "{y}",
                 yValueFormatString: "#0.##",
                 showInLegend: true,
                 dataPoints: <?php echo json_encode($dataPoints1, JSON_NUMERIC_CHECK); ?>
         },{
                 type: "area",
                 fillOpacity: .2,
                 name: "to South",
                 indexLabel: "{y}",
                 yValueFormatString: "#0.##",
                 showInLegend: true,
                 dataPoints: <?php echo json_encode($dataPoints2, JSON_NUMERIC_CHECK); ?>
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
 <div id="chartContainer" style="height: 370px; width: 100%;"></div>
 <script src="https://canvasjs.com/assets/script/canvasjs.min.js"></script>
 </body>
 </html>                           



<?php
        }

########################################################################################
########################################################################################
########################################################################################

# Alihakemistot
# http://172.20.240.54/index.php/valvo/latest


        public function tables()
        {
?>       
<head>
  <title>Valvontadata</title>
  <h1>Valvontadata</h1>
</head>
<br>

<div class="topnav">
  <a href="http://172.20.240.54/">All</a>
  <a href="http://172.20.240.54/index.php/valvo/tables">Full database</a>
  <a href="http://172.20.240.54/index.php/valvo/charts">Charts</a>
  <a href="http://172.20.240.54/index.php/valvo/pictures">Pictures</a>
</div>

<style>
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



<?php
        }
#############################################################################################
        public function charts()
        {
?>       
<head>
  <title>Valvontadata</title>
  <h1>Valvontadata</h1>
</head>
<br>

<div class="topnav">
  <a href="http://172.20.240.54/">All</a>
  <a href="http://172.20.240.54/index.php/valvo/tables">Full database</a>
  <a href="http://172.20.240.54/index.php/valvo/charts">Charts</a>
  <a href="http://172.20.240.54/index.php/valvo/pictures">Pictures</a>
</div>

<style>
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



<?php                


        }
###########################################################################################
        public function pictures()
        {
?>       

<head>
  <title>Valvontadata</title>
  <h1>Valvontadata</h1>
</head>
<br>

<div class="topnav">
  <a href="http://172.20.240.54/">All</a>
  <a href="http://172.20.240.54/index.php/valvo/tables">Full database</a>
  <a href="http://172.20.240.54/index.php/valvo/charts">Charts</a>
  <a href="http://172.20.240.54/index.php/valvo/pictures">Pictures</a>
</div>

<style>
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

<p>Latest images: </p>
<?php
#$dir = "images/";
#$images = glob($dir . "*.{gif,png,jpg,jpeg}", GLOB_BRACE); //formats to look for

#$num_of_files = 1; //number of images to display

#foreach($images as $image)
#{
#     $num_of_files--;

#     if($num_of_files > -1)
#       echo "<b>".$image."</b><br>Created on ".date('D, d M y H:i:s', filemtime($image))
#        ."<br><img src='/$image' width='960' height='540'><br><br>" ; //display images
#     else
#       break;
#}
?>

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
echo array_pop($list);   # 2nd newest
?>




 <body style="text-align:center;"> 
        
      <h4> 
          Ota kuva
      </h4> 
    
      <?php
        
          if(isset($_POST['snapshot'])) { 
              echo "Photo requested, wait for 5 seconds";
              $command = escapeshellcmd('scripts/request_photo.py');
              $output = shell_exec($command);
              echo $output;
              echo "<br>";
              echo "<meta http-equiv='refresh' content='5'>";
          } 
      ?> 
        
      <form method="post"> 
          <input type="submit" name="snapshot"
                  value="Take a photo"/> 
      </form> 
  </head> 



  <?php

 ##### GALLERY #####

// READ FILES FROM THE GALLERY FOLDER
$dir = "images/";
$images = glob($dir . "*.{jpg,jpeg,gif,png}", GLOB_BRACE);

?>

<html>
  <head>
    <link href="1-basic.css" rel="stylesheet">
  </head>
  <body>
    <!-- [THE GALLERY] -->
    <div id="gallery"><?php
    foreach ($images as $i) {
      printf("<img src='/images/%s'/>", basename($i));
    }
    ?></div>
  </body>
</html>

<style>

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