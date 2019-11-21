<?php
class Latest extends CI_Controller {
    
  public function view() {
    if ( ! file_exists(APPPATH.'/views/pages/Latest.php')) {
      //Whoops, we don't have a page for that!
      show_404();
    }       
    $data['title'] = ucfirst('Latest data'); 

    # Lataa codeigniterin DB-kirjaston, login asetukset ovat \application\config\database.php
    $this->load->database();
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
}