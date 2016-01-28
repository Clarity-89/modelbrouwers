'use strict';

import $ from 'jquery';

import tpl1 from 'templates/tpl1.hbs!ponyjs/templates/handlebars/loader';
import tpl2 from 'templates/tpl2.hbs!ponyjs/templates/handlebars/loader';


$('#hook-1').html(tpl1());
$('#hook-2').html(tpl2());
$('#hook-3').html(tpl2({'message1': 'First message'}));
