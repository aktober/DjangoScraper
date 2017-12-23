$(document).ready(function () {

    // Mailchimp
    var updateListners = function () {
        $('.unsubscribe').each(function (index, value) {
            var id = $('.unsubscribe').eq(index).attr('value');
            $('.unsubscribe').eq(index).on('click', function (e) {
                e.preventDefault();

                $.ajax({
                    type: 'POST',
                    url: '/ajax/unsubscribe/',
                    data: {
                        'id': id,
                    },
                    success: function (data) {
                        $('.table-rows').html(genHtml(data));
                        updateListners();
                    }
                });
            });
        });
    };

    updateListners();

    $('#form-subscribe').submit(function (e) {
        e.preventDefault();
        var email = $('#new-email').val();
        $('#new-email').val('');
        $.ajax({
            type: 'POST',
            url: '/ajax/subscribe/',
            data: {
                'email': email
            },
            success: function (data) {
                $('.table-rows').html(genHtml(data));
                updateListners();
            }
        });
    });

    var genHtml = function (data) {
        var html = '';
        if (data.length > 0) {
            for (i = 0; i < data.length; i++) {
                obj = data[i];
                html += '<tr>' +
                    '<td>' + obj["email"] + '</td>' +
                    '<td>' + obj["status"] + '</td>' +
                    '<td><button class="unsubscribe btn btn-danger" value="' + obj["id"] + '">Delete</button></td>' +
                    '</tr>';
            }
        }
        return html;
    };


    // Aggregator
    $('#clear-filters').click(function (e) {
        e.preventDefault();
        $('#text-filter').val('');
        $('#category-filter').val('');
        $('#comments-filter').val('');
        $('#votes-filter').val('');
        $('#sort-select').val('');

        $.ajax({
            type: 'POST',
            url: '/ajax/filter/',
            data: {
                'text': ''
            },
            success: function (data) {
                $('#content').html(data['html']);
                updateMarkListener();
                editNewsListners();
            }
        });
    });

    $('#find-btn').click(function (e) {
        e.preventDefault();
        handleFind();
    });

    var handleFind = function () {
        var str = $('#text-filter').val();
        var cat = $('#category-filter').val();
        var comm = $('#comments-filter').val();
        var vot = $('#votes-filter').val();
        var sort = $('#sort-select').find("option:selected").attr('value');

        $.ajax({
            type: 'POST',
            url: '/ajax/filter/',
            data: {
                'text': str,
                'category': cat,
                'comments': comm,
                'votes': vot,
                'sort': sort
            },
            success: function (data) {
                $('#content').html(data['html']);
                updateMarkListener();
                editNewsListners();
            }
        });
    }

    var editNewsListners = function () {
        $('.save-btn').each(function (index, value) {
            var id = $('.save-btn').eq(index).attr('value');
            $('.save-btn').eq(index).on('click', function (e) {
                e.preventDefault();
                $.ajax({
                    type: 'GET',
                    url: '/ajax/get/',
                    data: {
                        'pk': id
                    },
                    success: function (data) {
                        $('#myModal #modal-id-input').val(data.id);
                        $('#myModal #modal-title-input').val(data.title);
                        $('#myModal #modal-category-input').val(data.category);
                        $('#myModal #modal-imageurl-input').val(data.image_url);
                        $('#myModal').modal('show');
                    }
                });

            });
        });
    };

    editNewsListners();

    $('#modal-save-btn').on('click', function (e) {
        var pk = $('#myModal #modal-id-input').val();
        var new_title = $('#myModal #modal-title-input').val();
        var category = $('#myModal #modal-category-input').val();
        var imageurl = $('#myModal #modal-imageurl-input').val();
        $.ajax({
            type: 'PATCH',
            url: '/ajax/edit-news/',
            data: {
                'id': pk,
                'title': new_title,
                'category': category,
                'image_url': imageurl
            },
            success: function (data) {
                handleFind();
            }
        });
        $('#myModal').modal('hide');
    });

    var updateMarkListener = function () {
        $('.mark-for-report').each(function (index, value) {
            var id = $('.mark-for-report').eq(index).attr('value');
            $('.mark-for-report').eq(index).on('change', function (e) {
                e.preventDefault();

                var ischecked = $('.mark-for-report').eq(index).is(':checked');

                $.ajax({
                    type: 'PATCH',
                    url: '/ajax/edit-news/',
                    data: {
                        'id': id,
                        'use_in_report': ischecked,
                    },
                    success: function (data) {
                        console.log(data);
                    }
                });

            });
        });
    };

    updateMarkListener();

    // Report
    $('#submit-report').on('click', function (e) {
        e.preventDefault();
        console.log('submit clicked');
        $.ajax({
            type: 'GET',
            url: '/ajax/submit-report/',
            success: function () {
                console.log('success');
                // $(".alert").alert('show');
            }
        });
    });

    $('#tab-report').on('click', function () {
        $.ajax({
            type: 'GET',
            url: '/ajax/report-weekly-news/',
            success: function (data) {
                console.log('success from /ajax/report-weekly-news/');
                $('#weekly-news-content').html(data);
            }
        });
    });

    $('#tab-subscribers').on('click', function () {
        $.ajax({
            type: 'GET',
            url: '/ajax/get-subscribers/',
            success: function (data) {
                console.log('success from /ajax/get-subscribers/');
                $('.table-rows').html(genHtml(data));
                updateListners();
            }
        });
    });

    $('#run-spider').on('click', function(e) {
        e.preventDefault();
        $.ajax({
            type: 'GET',
            url: '/ajax/run-crawl/',
            success: function () {
                console.log('spider started');
            }
        });
    });
});