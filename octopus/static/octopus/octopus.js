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
    var sPS = sPageFirst.replace(sPageSec, '');
    var sId = sPageSec.substr(0, sPageSec.indexOf('/'));
    console.log(sPageFirst,sPageSec, sPageThird, sId)
    if((sPS == "bank/")&&(sPageThird=="ticket")){
        let pickup_time = document.getElementById("pickup_time");
        let timings = document.getElementById("timings");
        fetch('/bank/'+ sId + '/json')
        .then(response => response.json())
        .then(bank =>{
            console.log(bank);
            timings.innerHTML += bank['opening_time'] + " to " + bank['closing_time'];
            pickup_time.min = bank['opening_time'];
            pickup_time.max = bank['closing_time'];
            console.log(pickup_time.min, " ,", pickup_time.max);
        });
        var date = document.getElementById('pickup_date');
        console.log(date);
        // let rep_radio = document.querySelector("#radio");
        // rep_radio.addEventListener('click', event  =>{
        //     console.log("f");
        //     if(rep_radio.value == "on"){
        //         rep_radio.style.backgroundColor = "black";
        //     }
        //     else{
        //         rep_radio.style.backgroundColor = "#CDF0D1";
        //     }
        // })
    }

})