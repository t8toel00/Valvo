<?php
defined('BASEPATH') OR exit('No direct script access allowed');
class Home extends CI_Controller
{
    function __construct() {
        parent::__construct();
    }
    public function index(){
        if($this->input->post('submit')){
            //Upload to the local server
            $config['upload_path'] = 'uploads/';
            $config['allowed_types'] = '*';
            $this->load->library('upload', $config);
            if($this->upload->do_upload('file'))
            {
                //Get uploaded file information
                $upload_data = $this->upload->data();
                $fileName = $upload_data['file_name'];
                //File path at local server
                $source = 'uploads/'.$fileName;
                //Load codeigniter FTP class
                $this->load->library('ftp');
                //FTP configuration
                $ftp_config['hostname'] = '172.20.240.54';
                $ftp_config['username'] = 'ubuntu';
                $ftp_config['password'] = 'hongkong123';
                $ftp_config['debug']    = TRUE;
                //Connect to the remote server
                $this->ftp->connect($ftp_config);
                //File upload path of remote server
                $destination = '/assets/'.$fileName;
                //Upload file to the remote server
                $this->ftp->upload($source, ".".$destination);
                //Close FTP connection
                $this->ftp->close();
                //Delete file from local server
                @unlink($source);
            }
        }
        $this->load->view('home/index');
    }
}
