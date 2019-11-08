<?php
class Valvo extends CI_Controller {

# http://172.20.240.54/index.php/valvo/

        public function index()
        {
            $this->load->database();
                echo 'Käyttis tänne. Tämän .php:n sijainti on http://172.20.240.54/index.php/valvo/';
                echo '</br>';

                $sql = $this->db->get_compiled_select('Alue');
                echo $sql;
                echo '</br>';

         $query = $this->db->query('SELECT * FROM Alue');
         foreach ($query->result() as $row)
         {
                 echo $row->idAlue;
                 echo $row->paikalla;
                 echo $row->e_meno;
                 echo $row->e_tulo;
                 echo $row->p_meno;
                 echo $row->p_tulo;
                 
         }
                    
        }
# http://172.20.240.54/index.php/valvo/comments

        public function comments()
        {
                echo 'Look at this!';
                $this->load->view('footer');
        }
}