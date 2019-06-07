


var lists = document.querySelectorAll('.accordion ul');
/* Close lists by default (Do I want this?) */
for (var i=0; i<lists.length; i++) {
    lists[i].style.height = 0;
}
//document.getElementById('invisible').style.height=100 + 'px';

function Transform(e) {
    let clicked = e.target;
    if (clicked.tagName.toLowerCase() === 'a') {
        return;
    }
    let dropdown = this.querySelector('ul');
    let dropHeight = dropdown.scrollHeight;
    //let arrow = this.querSelector('i');
    if (dropdown.clientHeight === 0) {
        dropdown.style.height = dropHeight + 'px';
        //arrow.classList.toggle("fa-rotate-180");
    } else if (dropdown.clientHeight === dropHeight) {
        dropdown.style.height = 0;
        //arrow.classList.toggle("fa-rotate-180");
    } else {
        alert('Function Failed!');
    }
}

var items = document.getElementsByClassName('accordion');
for (var j=0; j<items.length; j++) {
    items[j].addEventListener('click', Transform);
}