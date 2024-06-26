
let sidebar = document.querySelector(".sidebar")
let open_icon = document.querySelector("img.open")
let close_icon = document.querySelector("img.close")
let sidebar_open = true

function openSidebar(){
    if(sidebar_open){
        sidebar.style.display = "none";
        open_icon.style.display = "block";
        close_icon.style.display = "none";
        
    }else{
        sidebar.style.display = "flex";
        open_icon.style.display = "none";
        close_icon.style.display = "block";

    }
    sidebar_open = ! sidebar_open
}