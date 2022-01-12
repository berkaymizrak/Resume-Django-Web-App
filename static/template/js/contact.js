$(document).ready(function () {

    (function ($) {
        "use strict";


        jQuery.validator.addMethod('answercheck', function (value, element) {
            return this.optional(element) || /^\bcat\b$/.test(value)
        }, "type the correct answer -_-");

        // validate contactForm form
        $(function () {
            $('#contactForm').validate({
                rules: {
                    name: {
                        required: true,
                        minlength: 2
                    },
                    subject: {
                        required: true,
                        minlength: 4
                    },
                    // number: {
                    //     required: true,
                    //     minlength: 5
                    // },
                    email: {
                        required: true,
                        email: true
                    },
                    message: {
                        required: true,
                        minlength: 20
                    }
                },
                messages: {
                    name: {
                        required: "come on, you have a name, don't you?",
                        minlength: "your name must consist of at least 2 characters"
                    },
                    subject: {
                        required: "come on, you have a subject, don't you?",
                        minlength: "your subject must consist of at least 4 characters"
                    },
                    // number: {
                    //     required: "come on, you have a number, don't you?",
                    //     minlength: "your Number must consist of at least 5 characters"
                    // },
                    email: {
                        required: "no email, no message"
                    },
                    message: {
                        required: "um...yea, you have to write something to send this form.",
                        minlength: "thats all? really?"
                    }
                },
                submitHandler: function (form) {
                    $('#error_message').text(' Something went wrong ');
                    $('#success_message').text('Your message is successfully sent...');
                    $('#submit_btn').text('Sending, please wait...');
                    $('#submit_btn').prop('disabled', true);
                    $('#submit_btn').removeClass('submit_btn');
                    $(form).ajaxSubmit({
                        type: "POST",
                        data: $(form).serialize(),
                        url: "/",
                        success: function (response) {
                            $('#submit_btn').prop('disabled', false);
                            $('#submit_btn').text('Send Message');
                            $('#submit_btn').addClass('submit_btn');
                            if (response.success == true) {
                                $('#success_message').text(response.message);
                                $('#contactForm :input').attr('disabled', 'disabled');
                                $('#contactForm').fadeTo("slow", 1, function () {
                                    $(this).find(':input').attr('disabled', 'disabled');
                                    $(this).find('label').css('cursor', 'default');
                                    $('#success').fadeIn()
                                    $('.modal').modal('hide');
                                    $('#success').modal('show');
                                })
                            } else {
                                $('#error_message').text(response.message);
                                $('#contactForm').fadeTo("slow", 1, function () {
                                    $('#error').fadeIn();
                                    $('.modal').modal('hide');
                                    $('#error').modal('show');
                                })
                            }
                        },
                        error: function (response) {
                            $('#submit_btn').prop('disabled', false);
                            $('#submit_btn').text('Send Message');
                            $('#submit_btn').addClass('submit_btn');
                            if (response.message != null) {
                                $('#error_message').text(response.message);
                            }
                            $('#contactForm').fadeTo("slow", 1, function () {
                                $('#error').fadeIn();
                                $('.modal').modal('hide');
                                $('#error').modal('show');
                            })
                        }
                    })
                }
            })
        })

    })(jQuery)
})