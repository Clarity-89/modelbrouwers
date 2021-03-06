<?php

$settingsFile = dirname(dirname(__DIR__)) . DIRECTORY_SEPARATOR . 'conf' . DIRECTORY_SEPARATOR . 'settings.php';
require_once $settingsFile;

define('PREFIX_KEY', $settings->KEY_PREFIX);


class StaticCache extends Memcached {
	protected $TIMEOUT = 900; // 15 minutes

	public function __construct($persistent_id = '') {
		parent::__construct($persistent_id);
		$this->setOption(Memcached::OPT_PREFIX_KEY, PREFIX_KEY);
	}

	/**
	 * Set up the connection
	 */
	function init() {
		$server_list = $this->getServerList();
		if(count($server_list) === 0) {
			$this->addServer('localhost', 11211);
		}
	}

	function set($key, $value, $expiration=null) {
		if(!$expiration) {
			$expiration = $this->TIMEOUT;
		}
		parent::set($key, $value, $expiration);
	}

}
?>
