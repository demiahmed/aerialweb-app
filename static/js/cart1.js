//Working Codeblock
console.log("cart loaded");

$(".addn").hide()

$(".more").on('click', function(){
    // console.log('clicked');
    if(!$(".addn").is(":visible")){
        $(".addn").slideDown('slow')
    }
    else {
        $(".addn").slideUp('slow')

    }
})



    let cart = [];
    let image = $(".satthumb");
    console.log(image);

function addOrRemove(array, value) {
    var index = array.indexOf(value);

    if (index === -1) {
        array.push(value);
    } else {
        array.splice(index, 1);
    }
}

for(var i=0;i<image.length;i++){
    console.log(2);
    let uuid = $(".uuid")[i];
    let overlay = $(".overlay")[i];
    // console.log(overlay);
    image[i].on('click',function(){
        console.log(uuid.innerHTML);
        overlay.toggleClass("yes");
        cart.push(uuid.innerHTML);
        addOrRemove(cart,uuid.innerHTML);
            },false);
};

let collect = $("#dl");
collect.on("click",function(event) {


    $("#uuidUser").empty();
    $("#uuidUser").append(cart);
    // $("#uuidUser5").val = cart;
    $("#uuidUser5").value = cart;

    // event.preventDefault();
    const uniqueCart = [...new Set(cart)]
    console.log(uniqueCart);
});

//end Working codeblock

