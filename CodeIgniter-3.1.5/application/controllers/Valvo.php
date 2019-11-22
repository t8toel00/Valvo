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
 <img src="http://172.20.240.54/images/lastshot.jpg" width="960" height="540" />
 <br>

<?php

            $this->load->helper('url');

            # Lataa codeigniterin DB-kirjaston, login asetukset ovat \application\config\database.php
            $this->load->database();
                echo ' ';
                echo '</br>';
                echo '<a href="http://172.20.240.54/index.php/valvo/latest">Latest data</a>';
                echo '</br>';
                echo '</br>';
                
        # Lataa codeigniterin automaattisen taulukko-muotoilun kirjastosta

        $this->load->library('table');

        $template = array(
                'table_open' => '<table border="1" cellpadding="2" cellspacing="1" class="mytable">'
        );
        
        $this->table->set_template($template);        

        # Toteutetaan SQL-kyselyt ja sovitetaan arvot taulukkoon 

         $query = $this->db->query('SELECT * FROM Alue');
         echo $this->table->generate($query);
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

 $dataPoints1 = array(
         array("label"=> "2012019-11-12 16:05:11.1120", "y"=> 2),
         array("label"=> "2019-11-12 14:39:11.111", "y"=> 1),
         array("label"=> "2019-11-12 14:39:11.111", "y"=> 1),
         array("label"=> "2019-11-12 14:39:11.111", "y"=> 2),
         array("label"=> "2019-11-12 14:39:11.111", "y"=> 2),
         array("label"=> "2019-11-12 14:39:11.111", "y"=> 2),
         array("label"=> "2019-11-12 14:39:11.111", "y"=> 2),
         array("label"=> "2019-11-12 14:39:11.111", "y"=> 2)
         
 );
 $dataPoints2 = array(
        array("label"=> "2012019-11-12 16:05:11.1120", "y"=> 2),
        array("label"=> "2019-11-12 14:39:11.111", "y"=> 1),
        array("label"=> "2019-11-12 14:39:11.111", "y"=> 2),
        array("label"=> "2019-11-12 14:39:11.111", "y"=> 1),
        array("label"=> "2019-11-12 14:39:11.111", "y"=> 2),
        array("label"=> "2019-11-12 14:39:11.111", "y"=> 2),
        array("label"=> "2019-11-12 14:39:11.111", "y"=> 2),
        array("label"=> "2019-11-12 14:39:11.111", "y"=> 2)
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
                 name: "to North",
                 indexLabel: "{y}",
                 yValueFormatString: "#0.##",
                 showInLegend: true,
                 dataPoints: <?php echo json_encode($dataPoints1, JSON_NUMERIC_CHECK); ?>
         },{
                 type: "area",
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

<p>Latest image: </p>
 <img src="http://172.20.240.54/images/lastshot.jpg" width="960" height="540" />
 <br>

<?php                


        }
}
?>