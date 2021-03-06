'use strict';

import 'jquery';
import Api from 'scripts/api';


$(function() {
    $('[data-toggle="finished"]').click(function(e) {
        e.preventDefault();
        let endpoint = $(this).attr('href');
        let isFinished = $(this).children('.fa-ellipsis-h').length > 0;
        Api.request(endpoint, {finished: !isFinished}).patch().done(response => {
            $(this).find('.fa').toggleClass('fa-check fa-ellipsis-h');
        });
        return false;
    })
});
