<?php
class Valvo extends CI_Controller {

# http://172.20.240.54/index.php/valvo/

        public function index()
        {
            $this->load->helper('url');

            # Lataa codeigniterin DB-kirjaston, login asetukset ovat \application\config\database.php
            $this->load->database();
                echo 'Valvontadata';
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
        
         
         # Ladataan kirjastosta hakemistoauttaja ja ladataan kuvia sivulle
        $this->load->helper('url');
?>
        <img src="<?php echo base_url('images/tables_01.jpg'); ?>" /> 



        <?php
# ------------------------------------------------------------------------------------------- 
# LUO ERILLINEN TAULUKKO JA TRIGGAA DATA VAIKKA TUNTEIHIN; YNNÄÄ HAVAINNOT NIIHIN

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
                 type: "column",
                 name: "to North",
                 indexLabel: "{y}",
                 yValueFormatString: "#0.##",
                 showInLegend: true,
                 dataPoints: <?php echo json_encode($dataPoints1, JSON_NUMERIC_CHECK); ?>
         },{
                 type: "column",
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
# Alihakemisto
# http://172.20.240.54/index.php/valvo/latest

        public function latest()
        {
                echo 'Look at this!';
                $this->load->view('footer');
        }
}
?>