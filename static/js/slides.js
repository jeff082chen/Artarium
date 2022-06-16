var myIndex_1 = 0;
var myIndex_2 = 0;
var myIndex_3 = 0;
var myIndex_4 = 0;
var myIndex_5 = 0;
carousel();

function carousel() {
    var x_1 = document.getElementsByClassName("recent");
    var x_2 = document.getElementsByClassName("dance");
    var x_3 = document.getElementsByClassName("exhibition");
    var x_4 = document.getElementsByClassName("music");
    var x_5 = document.getElementsByClassName("drama");
    for (var i = 0; i < x_1.length; i++) {
        x_1[i].style.display = "none";
    }
    for (i = 0; i < x_2.length; i++) {
        x_2[i].style.display = "none";
    }
    for (i = 0; i < x_3.length; i++) {
        x_3[i].style.display = "none";
    }
    for (i = 0; i < x_4.length; i++) {
        x_4[i].style.display = "none";
    }
    for (i = 0; i < x_5.length; i++) {
        x_5[i].style.display = "none";
    }
    myIndex_1++;
    myIndex_2++;
    myIndex_3++;
    myIndex_4++;
    myIndex_5++;
    if (myIndex_1 > x_1.length) {
        myIndex_1 = 1
    }
    x_1[myIndex_1 - 1].style.display = "block";
    if (myIndex_2 > x_2.length) {
        myIndex_2 = 1
    }
    x_2[myIndex_2 - 1].style.display = "block";
    if (myIndex_3 > x_3.length) {
        myIndex_3 = 1
    }
    x_3[myIndex_3 - 1].style.display = "block";
    if (myIndex_4 > x_4.length) {
        myIndex_4 = 1
    }
    x_4[myIndex_4 - 1].style.display = "block";
    if (myIndex_5 > x_5.length) {
        myIndex_5 = 1
    }
    x_5[myIndex_5 - 1].style.display = "block";
    setTimeout(carousel, 2000);
}
