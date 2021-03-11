let resource = 1000; // TODO: get resource from the server
let firstTimeDraw = true;

function display(){
    if(resource>=50){
        firstTimeDraw = true;
        resource -= 50;
        updateGold();

        /* send resource via post request */
        let xhr = new XMLHttpRequest();
        xhr.open("POST", null, true); // TODO:change null to a real url
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.send(JSON.stringify({
            "resource": resource
        }));

        let x = document.getElementById("cards");
        if(x.style.display === "none"){
            x.style.display = "block";
            x.classList.add("animate__animated", "animate__zoomIn");
        }else{
            let newone = x.cloneNode(true);
            x.parentNode.replaceChild(newone, x);
            let backs = document.getElementsByClassName("effect-on-active");
            for(let i=0;i<backs.length;i++){
                backs[i].classList.remove("active");
            }
        }
    }else{
        alert("Don't have enough gold!");
    }
    detectFlip();
}

function flipThis(){
    if((resource >= 50 && !this.classList.contains("active")) || firstTimeDraw){
        if(!firstTimeDraw) resource -= 50;
        firstTimeDraw = false;
        updateGold();
        this.classList.add("active");
    }else if(!this.classList.contains("active")){
        alert("Don't have enough gold!");
    }
}

function detectFlip(){
    let fronts = document.getElementsByClassName("effect-on-active");
    for(let i=0;i<fronts.length;i++){
        fronts[i].addEventListener('click', flipThis);
    }
}

function updateGold(){
    let x = document.getElementById("resource");
    x.innerHTML = resource;
}

updateGold();