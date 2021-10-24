document.addEventListener('DOMContentLoaded', function() {
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    const csrftoken = getCookie('csrftoken');
    
    var sPath = window.location.pathname;
    var sPage = sPath.substring(sPath.indexOf('/') + 1);
    var sPageFirst = sPath.substring(sPath.indexOf('/') + 1);
    var sPageSec = sPageFirst.substring(sPageFirst.indexOf('/') + 1);
    var sPageThird = sPageSec.substring(sPageSec.indexOf('/') + 1);
    var sPS = sPageFirst.replace(sPageSec, '')
    console.log(sPS ,sPageFirst,sPageSec)
})