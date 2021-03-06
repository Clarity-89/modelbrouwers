<?php

global $settings;

function joinPath() {
	$bits = func_get_args();
	return implode(DIRECTORY_SEPARATOR, $bits);
}

$PROJECT_DIR = realpath(dirname(__DIR__) . DIRECTORY_SEPARATOR . 'phpbb');
$ROOT_DIR = dirname(dirname($PROJECT_DIR));

$settings = new stdClass();
$settings->PROJECT_DIR = $PROJECT_DIR;
$settings->ROOT_DIR = $ROOT_DIR;

$settings->STATIC_ROOT = realpath(joinPath($ROOT_DIR, 'static'));
$settings->STATIC_URL = getenv('STATIC_URL') ?: '/static/';
$settings->SYSTEMJS_OUTPUT_DIR = getenv('SYSTEMJS_OUTPUT_DIR') ?: 'SYSTEMJS';

$settings->MEDIA_ROOT = realpath(joinPath($ROOT_DIR, 'media'));

$settings->KEY_PREFIX = getenv('KEY_PREFIX') ?: '';

$settings->COMPOSER_AUTOLOADER = realpath(joinPath($ROOT_DIR, 'vendor', 'autoload.php'));

$settings->RAVEN_DSN = getenv('RAVEN_DSN') ?: 'http://example@foo/0';

?>
