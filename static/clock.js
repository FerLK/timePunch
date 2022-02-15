    var weekday = new Array(7);
        weekday[0] = "Domingo";
        weekday[1] = "Segunda";
        weekday[2] = "Terça";
        weekday[3] = "Quarta";
        weekday[4] = "Quinta";
        weekday[5] = "Sexta";
        weekday[6] = "Sábado";
    
    var month = new Array();
        month[0] = "Janeiro";
        month[1] = "Fevereiro";
        month[2] = "Março";
        month[3] = "Abril";
        month[4] = "Maio";
        month[5] = "Junho";
        month[6] = "Julho";
        month[7] = "Agosto";
        month[8] = "Setembro";
        month[9] = "Outubro";
        month[10] = "Novembro";
        month[11] = "Dezembro";

function clock(){
    var date = new Date()
    var weekDay = date.getDay()
    var monthDay = date.getDate()
    var monthNum = date.getMonth()
    var hours = date.getHours()
    var minutes = date.getMinutes()
    var seconds = date.getSeconds()
    
    if(hours < 10){
        hours = "0"+ hours
    }
    if(minutes < 10){
        minutes = "0"+ minutes
    }
    if(seconds < 10){
        seconds = "0"+ seconds
    }
 
    var clockON = document.getElementById("time").innerText = hours+":"+minutes+":"+seconds;
    var weekON = document.getElementById("weekDay").innerText = weekday[weekDay]+", "+ monthDay+" de "+ month[monthNum]
}

setInterval(clock,1000)    