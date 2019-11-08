<?php
class Valvo extends CI_Controller {

# http://172.20.240.54/index.php/valvo/

        public function index()
        {
            # Lataa codeigniterin DB-kirjaston, login asetukset ovat \application\config\database.php
            $this->load->database();
                echo 'Käyttis tänne. Tämän .php:n verkkosijainti on http://172.20.240.54/index.php/valvo/';
                echo '</br>';

                $sql = $this->db->get_compiled_select('Alue');
                echo $sql;
                echo '</br>';
                echo '</br>';

        # Lataa codeigniterin automaattisen taulukko-muotoilun kirjastosta
        $this->load->library('table');

        # Toteutetaan SQL-kyselyt ja sovitetaan arvot taulukkoon 
         $query = $this->db->query('SELECT * FROM Alue');
         echo $this->table->generate($query);
         echo '</br>';

         $query = $this->db->query('SELECT * FROM Tunnistus');
         echo $this->table->generate($query);
         echo '</br>';

         $query = $this->db->query('SELECT * FROM Arduino1');
         echo $this->table->generate($query);
         echo '</br>';
        
         $query = $this->db->query('SELECT * FROM Arduino2');
         echo $this->table->generate($query);
         echo '</br>';

         echo '</br>';
        



         
         # Ladataan kirjastosta hakemistoauttaja ja ladataan kuvia sivulle
        $this->load->helper('url');
?>
        <img src="<?php echo base_url('images/tables_01.jpg'); ?>" />  
<?php
        }
# Alihakemisto
# http://172.20.240.54/index.php/valvo/comments

        public function comments()
        {
                echo 'Look at this!';
                $this->load->view('footer');
        }
}
?>