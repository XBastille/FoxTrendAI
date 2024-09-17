document.querySelector(".Arrow").addEventListener('Click' , function(){
    document.querySelectorAll(".Icon-items").forEach(function(item){
          const iconName = item.querySelector('.icon-name');
          const nameText = item.getAttribute('data-name');

          if(iconName.style.display === "none" || iconName.style.display === ' ') {
            iconName.textContent = nameText;
            iconName.style.display = 'inline-block';
          }else{
            iconName.style.display = 'none';
          }
    })
    
})