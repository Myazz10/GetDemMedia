const eventBox = document.getElementById('event-box');
const countdownBox = document.getElementById('countdown-box');

const eventDate = Date.parse(eventBox.textContent);

const my_countdown = setInterval(()=>{
    const now = new Date().getTime();

    const diff = eventDate - now;

    const days = Math.floor(eventDate / (1000 * 60 * 60 * 24) - (now / (1000 * 60 * 60 * 24)));
    const hours = Math.floor((eventDate / (1000 * 60 * 60) - (now / (1000 * 60 * 60))) % 24);
    const minutes = Math.floor(((eventDate / (1000 * 60)) - (now / (1000 * 60))) % 60);
    const seconds = Math.floor(((eventDate / (1000)) - (now / (1000))) % 60);

    let d = " days, "
    let h = " hours, "
    let m = " minutes, "
    let s = " seconds."

    if (diff>0){
        if (days <= 1){
            d = " day, "
        }

        if (hours <= 1){
            h = " hour, "
        }

        if (minutes <= 1){
            m = " minute, "
        }

        if (seconds <= 1){
            s = " second."
        }

        countdownBox.innerHTML = days + d + hours + h + minutes + m + seconds + s;
    }
    else{
        clearInterval(my_countdown)
        countdownBox.innerHTML = "Countdown Completed - Maintenance Mode";
    }
}, 1000);
