const filterbuttons = document.querySelectorAll(".filterbutton");

function bold(e){
    e.classList.add("bold")
}

filterbuttons.forEach(element => {
    element.addEventListener("onclick",bold)
});
