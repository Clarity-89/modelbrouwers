import "jquery";
import Handlebars from "../general/hbs-pony";
import { Photo } from "./models/photo";
import { RotateControl, Control } from "./photo-detail";
import { PhotoUpload } from "./upload";

export default class Page {
    static init() {
        this.initLightbox();
        this.initControls();
        new PhotoUpload();
    }

    static initLightbox() {
        const $lightbox = $("#modal-lightbox");
        const $lightboxBody = $lightbox.find(".modal-content");
        const photoThumbs = $("#photo-thumbs");

        const renderLightbox = (currentID, photos) => {
            const current = photos.find(e => e.id === currentID);
            current.state = { selected: true };
            const context = {
                photos: photos,
                current: current
            };
            Handlebars.render("albums::photo-lightbox", context).done(html => {
                $lightboxBody.append(html);
                $lightbox.find(".active img").on("load", function() {
                    $("#image-loader").hide();
                });
            });
        };

        /* Closure to render the current photo in the lightbox */
        const getLightboxRenderer = id => {
            const currentID = id;
            return photos => {
                renderLightbox(currentID, photos);
                $lightbox.find(".carousel").trigger("slide.bs.carousel");
            };
        };

        photoThumbs.on("click", ".album-photo", function(event) {
            event.preventDefault();

            const id = $(this).data("id");

            // remove all 'old' bits
            $lightboxBody.find(".modal-body").remove();
            $("#image-loader").show();

            // bring up the modal with spinner
            $lightbox.modal("show");

            // fetch the photo details from the Api
            Photo.objects
                .filter({
                    page: window.page,
                    album: window.album
                })
                .done(getLightboxRenderer(id));
        });

        photoThumbs.on("click", ".album-photo", event => {
            event.preventDefault();

            const id = $(event.target).data("id");

            // remove all 'old' bits
            $lightboxBody.find(".modal-body").remove();
            $("#image-loader").show();

            // bring up the modal with spinner
            $lightbox.modal("show");

            // fetch the photo details from the Api
            Photo.objects
                .filter({
                    page: window.page,
                    album: window.album
                })
                .then(getLightboxRenderer(id));
        });
    }

    static initControls() {
        const controls = {};
        const getControlClass = action => {
            switch (action) {
                case "rotate-left":
                case "rotate-right":
                    return RotateControl;
                default:
                    return Control;
            }
        };

        $(".controls").on("click", "[data-action]", function(event) {
            event.preventDefault();

            let control,
                action = $(this).data("action"),
                $figure = $(this).closest("figure");

            let cls = getControlClass(action);
            control = controls[action] || new cls($(this), $figure);
            control.toggle();
            return false;
        });
    }
}