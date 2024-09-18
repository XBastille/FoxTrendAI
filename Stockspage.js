document.querySelector(".Arrow").addEventListener('click' , function(){
    document.querySelectorAll(".Icon-items").forEach(function(item){
          const iconName = item.querySelector('.icon-name');
          const nameText = item.getAttribute('data-name');

          if(iconName.style.display === "none" || iconName.style.display === '') {
            iconName.textContent = nameText;
            iconName.style.display = 'inline-block';
            iconName.style.display = 'flex';
          }else{
            iconName.style.display = 'none';
          }
    })
})
    document.querySelector(".cha").addEventListener('click' , function(){
        const SUMMARY = document.querySelector('.sum');
        var CHART = document.querySelector('.cha');
        SUMMARY.style.backgroundColor= "black";
        CHART.style.backgroundColor = "purple";
    })
    
