<?php
class Pages extends CI_Controller {

        public function view($page = 'home')
        {
                if(!file_exists('application/views/pages/'.$page.'.php'))
			{
				echo "Sorry, file does not exist";
			}
			else
			{
				$data['title']=ucfirst($page);
			$this->load->view('templates/header',$data);
				$this->load->view('pages/'.$page,$data);
				$this->load->view('templates/footer',$data);
			}
        }
}