"use strict";
(function ($) {
    $(document).ready(function () {
        let notificationSocket = new ReconnectingWebSocket(
            `ws://${window.location.host}/ws/notifications/`
        );
        notificationSocket.onmessage = function (e) {
            let data = JSON.parse(e.data);
            if (data.hasOwnProperty('notification_count')) {
                let countTag = $('#notification-count');
                if (data.notification_count === 0) {
                    countTag.remove();
                } else {
                    if (countTag.length === 0) {
                        let html = `<span id="notification-count">${data.notification_count}</span>`;
                        $('.ow-notifications').append(html);
                    } else {
                        countTag.html(data.notification_count);
                    }
                }
            }
            if (data.hasOwnProperty('reload_widget')) {
                if (data.reload_widget) {
                    $('.accordion').trigger('refreshNotificationWidget');
                    $('.loader').addClass('hide');
                }
            }
        };
    });
})(django.jQuery);
