document.getElementById('button').addEventListener("click", function () {
    document.querySelector('.bg-model').style.display = "flex";
    $('body').css('overflow', 'hidden');

});

document.getElementById('notesbutton').addEventListener("click", function () {
    document.querySelector('.bg-model1').style.display = "none ";
    document.querySelector('.bg-model').style.display = "flex";
});

document.getElementById('close').addEventListener("click", function () {
    document.querySelector('.bg-model').style.display = "none";
    $('body').css('overflow', 'auto');

});

document.getElementById('closebutton').addEventListener("click", function () {
    document.querySelector('.bg-model1').style.display = "none ";
});

function openPopup() {
    document.querySelector('.bg-model1').style.display = "flex";
};


var coll = document.getElementsByClassName("collapsible");
var i;

for (i = 0; i < coll.length; i++) {
    coll[i].addEventListener("click", function () {
        this.classList.toggle("active");
        var content = this.nextElementSibling;
        if (content.style.maxHeight) {
            content.style.maxHeight = null;
        } else {
            content.style.maxHeight = content.scrollHeight + "px";
        }
    });
}

function openForm() {
    document.getElementById("myForm").style.display = "block";
}

function closeForm() {
    document.getElementById("myForm").style.display = "none";
}


document.getElementById('print').addEventListener("click", function () {
    window.print();
});

document.getElementById('click').addEventListener("click", function () {
    window.print();
});

function download(file) {

    //creating an invisible element
    var element = document.createElement('a');
    element.setAttribute('href', 'download.txt');
    element.setAttribute('download', 'output');

    // Above code is equivalent to
    // <a href="path of file" download="file name">
    //onClick property
    element.click();
}

// Start file download.
document.getElementById("download")
    .addEventListener("click", function () {

        download(file);
    }, false);

$(document).ready(function () {
    $('[data-toggle="toggle"]').change(function () {
        $(this).parents().next('.hide').toggle();
    });
});

//epandaignandfafkalf

function toggle(btnID, eIDs) {
    // Feed the list of ids as a selector
    var theRows = document.querySelectorAll(eIDs);
    // Get the button that triggered this
    var theButton = document.getElementById(btnID);
    // If the button is not expanded...
    if (theButton.getAttribute("aria-expanded") == "false") {
        // Loop through the rows and show them
        for (var i = 0; i < theRows.length; i++) {
            theRows[i].classList.add("shown");
            theRows[i].classList.remove("hidden");

        }
        // Now set the button to expanded
        theButton.setAttribute("aria-expanded", "true");
        // Otherwise button is not expanded...
    } else {
        // Loop through the rows and hide them
        for (var i = 0; i < theRows.length; i++) {
            theRows[i].classList.add("hidden");
            theRows[i].classList.remove("shown");
        }
        // Now set the button to collapsed
        theButton.setAttribute("aria-expanded", "false");
    }
}


function toggle1(btnID, eIDs, subIDs) {
    var theButton = document.getElementById(btnID);
    var theRows = document.querySelectorAll(eIDs);
    var subids = document.querySelectorAll(subIDs);
    if (theButton.getAttribute("aria-expanded") == "false") {
        for (var i = 0; i < theRows.length; i++) {
            theRows[i].classList.add("shown");
            theRows[i].classList.remove("hidden");

        }
        theButton.setAttribute("aria-expanded", "true");
    } else if (theRows.querySelectorAll("aria-expanded") == "false" || theButton.getAttribute("aria-expanded") == "true") {
        for (var i = 0; i < theRows.length; i++) {
            if (i.getAttribute("aria-expanded") == "false") {
                theRows[i].classList.add("hidden");
                theRows[i].classList.remove("shown");
            }
        }
        theButton.setAttribute("aria-expanded", "false");
    } else if (theRows.querySelectorAll("aria-expanded") == "true" || theButton.getAttribute("aria-expanded") == "true") {
        for (var i = 0; i < subids.length; i++) {
            if (i.getAttribute("aria-expanded") == "false") {
                subids[i].classList.add("shown");
                subids[i].classList.remove("hidden");
            }
        }
        theRows.setAttribute("aria-expanded", "true");
    }
}



function expan(btnID, eIDs) {
    var theRows = document.querySelectorAll(eIDs);
    var theButton = document.getElementById(btnID);
    for (var i = 0; i < theRows.length; i++) {
        theRows[i].classList.add("shown");
        theRows[i].classList.remove("hidden");
    }
    theButton.setAttribute("aria-expanded", "true");
}

function collap(btnID, eIDs) {
    var theRows = document.querySelectorAll(eIDs);
    var theButton = document.getElementById(btnID);
    for (var i = 0; i < theRows.length; i++) {
        theRows[i].classList.add("hidden");
        theRows[i].classList.remove("show");
    }
    theButton.setAttribute("aria-expanded", "false");
}

window.addEventListener('scroll', nonscroll);

function nonscroll() {
    window.scroll(0, 0);
};
document.getElementById('btn1').addEventListener("scroll", function () {

});


//chaginag button to -
document.getElementById('.row1').addEventListener("click", function () {
    document.getElementById('.row1').style.transform = rotate("45deg");
});

//adding notes query
document.querySelector('#addingnoteshere').addEventListener("click", function () {
    let nh = document.querySelectorAll('texting');
    document.querySelector('#ns').innerText = nh;
});