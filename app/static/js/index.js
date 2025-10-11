function enter(x) {
    x.style.boxShadow = "0px 0px 10px 0px rgba(134, 0, 0, 1)";
};

function leave(x) {
    x.style.boxShadow = "0px 0px 0px 0px rgba(134, 0, 0, 1)";
};

   document.querySelector(`.box-shadow`).onmouseenter = function() {
    onmouseover = enter(this);    
   };

   document.querySelector(`.box-shadow`).onmouseleave = function() {
    onmouseout = leave(this);
   };
