'use strict';

import $ from 'bootstrap'; // bootstrap returns a jquery version
import Handlebars from 'general/js/hbs-pony';
import { Photo, MyPhoto } from 'albums/js/models/photo';


$(function() {

    // http://www.bootply.com/79859

    var $lightbox = $('#modal-lightbox'),
        $lightboxBody = $lightbox.find('.modal-content');


    $('#photo-thumbs').on('click', '.album-photo', function(event) {
        event.preventDefault();

        var id = $(this).data('id');

        // remove all 'old' bits
        $lightboxBody.find('.modal-body').remove();
        $('#image-loader').show();

        var renderLightbox = function(currentID, photos) {
            var current = photos.filter(function(e) {
                return e.id == currentID;
            })[0];
            current.state = {selected: true};
            var context = {
                photos: photos,
                current: current,
            };
            Handlebars
                .render('albums::photo-lightbox', context)
                .done(function(html) {
                    $lightboxBody.append(html);
                    $lightbox.find('.active img').on('load', function() {
                        $('#image-loader').hide();
                    });
                });
        };

        /* Closure to render the current photo in the lightbox */
        function getLightboxRenderer(id) {
            var currentID = id;
            return function(photos) {
                renderLightbox(currentID, photos);
                $lightbox.find('.carousel').trigger('slide.bs.carousel');
            };
        }

        // bring up the modal with spinner
        $lightbox.modal('show');

        // fetch the photo details from the Api
        Photo.objects.filter({
            page: window.page,
            album: window.album
        }).done(getLightboxRenderer(id));

    });

    $('#photo-thumbs').on('click', '[data-action="set-cover"]', function(e) {
        e.preventDefault();
        var id = $(this).closest('article').data('id');
        $('.cover').removeClass('cover');
        MyPhoto.objects.get({id: id}).then(photo => {
            return photo.setAsCover();
        }).done(photo => {
            $(this).closest('ul').siblings('a').addClass('cover');
        });
        return false;
    });

});
