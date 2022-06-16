window.onload = function() {
    var oInput = document.getElementById("myInput");
    var omessageBox = document.getElementById("messageBox");
    var oPostBtn = document.getElementById("doPost");

    oPostBtn.onclick = function() {
        if (oInput.value) {

            var oTime = document.createElement("div");
            oTime.className = "time";
            var myDate = new Date();
            oTime.innerHTML = myDate.toLocaleString();
            omessageBox.appendChild(oTime);


            var oMessageContent = document.createElement("div");
            oMessageContent.setAttribute("style", "border-style:dotted;background-color:papayawhip;border-width:thin;") //這行是我自己多加的
            oMessageContent.className = "message_content";
            oMessageContent.innerHTML = oInput.value;
            oInput.value = "";
            omessageBox.appendChild(oMessageContent);

        }
    }
}