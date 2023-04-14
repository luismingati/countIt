const deleteElement = document.getElementsByClassName("delete");


//IT WILL TOGGLE THE MODAL BY ADDING A CLASS TO THE MODAL
deleteElement[0].addEventListener("click", function() {
    document.getElementById("modal").classList.toggle("is-active");
})