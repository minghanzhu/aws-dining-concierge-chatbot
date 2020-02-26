var $messages = $('.messages-content');

var apigClient = apigClientFactory.newClient();

$(window).load(function () {
    $messages.mCustomScrollbar();
    // setTimeout(function () {
    //     fakeMessage();
    // }, 100);
});


function updateScrollbar() {
    $messages.mCustomScrollbar("update").mCustomScrollbar('scrollTo', 'bottom', {
        scrollInertia: 10,
        timeout: 0
    });
}

function insertMessage() {
    msg = $('.message-input').val();
    if ($.trim(msg) == '') {
        return false;
    }
    $('<div class="message message-personal">' + msg + '</div>').appendTo($('.mCSB_container')).addClass('new');
    $('.message-input').val(null);
    updateScrollbar();
    setTimeout(function () {
        newMessage(msg);
    }, 1000 + (Math.random() * 20) * 100);
}

$('.message-submit').click(function () {
    insertMessage();
});

$(window).on('keydown', function (e) {
    if (e.which == 13) {
        insertMessage();
        return false;
    }
});

function newMessage(message) {
    if ($('.message-input').val() !== '') {
        return false;
    }
    $('<div class="message loading new"><figure class="avatar"><img src="https://www.columbia.edu/content/sites/default/files/styles/cu_crop/public/content/about/icon-crown.png" /></figure><span></span></div>').appendTo($('.mCSB_container'));
    updateScrollbar();

    setTimeout(function () {
        var body = {
            messages: [
                {
                    type: "request",
                    unstructured: {
                        id: "10",
                        text: message,
                        timestamp: Date.now().toString()
                    }
                }
            ]
        };
        apigClient.chatbotPost(null, body)
            .then(function (result) {
                $('.message.loading').remove();
                console.log(result)
                var data = JSON.parse(JSON.stringify(result).replace(";", "")).data;
                console.log(data);
                console.log(data["errorMessage"])
                text = data["errorMessage"]
                $('<div class="message new"><figure class="avatar"><img src="https://www.columbia.edu/content/sites/default/files/styles/cu_crop/public/content/about/icon-crown.png" /></figure>' + text + '</div>').appendTo($('.mCSB_container')).addClass('new');
                updateScrollbar();
            }).catch(function (result) {
            console.log(result)
            $('.message.loading').remove();
            updateScrollbar();
        });
    }, 1000 + (Math.random() * 20) * 100);

}
