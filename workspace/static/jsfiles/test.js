const filterbuttons = document.querySelectorAll(".filterbutton");
function bold(e){
    filterbuttons.forEach(element=>{
        element.classList.remove("bold");
    })
    this.classList.add("bold");
}

filterbuttons.forEach(element => {
    element.addEventListener("click",bold)
});