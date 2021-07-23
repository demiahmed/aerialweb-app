console.log("cart loaded");

$(".addn").hide()
$("#warning").hide()
$("#error").hide()
$("#uuidUser5").val('')

$(".more").on('click', function(){
    // console.log('clicked');
    if(!$(".addn").is(":visible")){
        $(".addn").slideDown('slow')
    }
    else {
        $(".addn").slideUp('slow')

    }
})

console.log("ajax loaded");
$("#rendercontents").hide()
$("#gifloader").hide()

$("form#find").on('submit', function(event){
 
$("#gifloader").show()






  //Data Construction

  let data = {
    name: "",
    country: "",
    lat: "",
    lon: "",
    size: "",
    num: "",
    xBound: "",
    yBound: "",
    start: "",
    end: "",
    cl: "",

  }

  //By airport Name 
    try {
      let name = $( "#airport-name option:selected" )
      if($("#airport-name").is(":visible")){
      data.name= name.text()
      }
      
    } catch (error) {
      console.log(error);
    }


  //By Country 

    try {
      let country = $( "#country-name option:selected" )
      if($("#country-name").is(":visible")){
     data.country= country.text()
      }

      
    } catch (error) {
      console.log(error);
    }

  //By Coordinates 

    try {
      let n = $( "#latitude" )
      let n2 = $( "#longitude" )
      if(n.is(":visible")&& n2.is(':visible')){
     data.lat= n.val()
     data.lon= n2.val()

      }
    } catch (error) {
      console.log(error);
    }

  //By Traffic 

    try {
      let n = $( "#batch-size" )
      let n2 = $( "#batch-number" )
      if(n.is(":visible")&& n2.is(':visible')){
     data.size= n.val()
     data.num= n2.val()

      }
    } catch (error) {
      console.log(error);
    }


    data.xBound= $("#xbnd")[0].value,
    data.yBound= $("#ybnd")[0].value,
    data.start= $("#from")[0].value,
    data.end= $("#to")[0].value,
    data.cl= $("#cloud")[0].value

  

  console.log(data);

  //send AJAX
$.post({
  // type: 'POST',
  dataType: 'JSON',
  contentType: 'application/json',
  url: window.location.pathname,
  data: JSON.stringify(data),
  success: function(data) {
    $("#error").empty()
    $("#error").hide()
    $(".folium-map").load("/map")

    // $(".folium-map").load('../../templates/folium.html')

    // $(".folium-map").empty()


    renderResults(data)
    data = {}
    console.log(`success`);


  },
  error: function(err) {
    $("#gifloader").hide()
    let message = `${err.statusText}
    - Try Broadening the Date range or increasing Cloud cover`
    $('#error')[0].innerHTML = message
    $("#error").show()
    console.log(err.statusText);
  }
  // success: function(data){ console.log(data);}
    // let html = $.parseHTML(data.data)
    // console.log(html);
    // $('html')[0] = data.data;
  
})


event.preventDefault();
})

function renderResults(toParse) {
  $("#gifloader").hide()

  let rendercontents = $('#rendercontents')
  rendercontents.empty()
  rendercontents.show()




  // console.log("Received for Processing");
  let parsed = toParse.data
  // console.log(parsed);
  let imagePath = 'static/images/'
  let extension = '.jpg'

  // let keys = Object.keys(parsed)
  // console.log(keys[0]);



  $('<div/>',{
    class: 'box'
  }).appendTo('#rendercontents');

  for (const [key, values] of Object.entries(parsed)) {

    console.log(values);


    $(".box").append(
      '<div class="elements">'+
      '<div class="text">'+
      '<p class="value">' + values.airportName + "   " + values.numofProd +  '</p>'+
      '</div>'+
      '<div class="thumbs" id="'+key+'"></div>'+
      '</div>'
    )
  //   $('<div/>',{
  //   class: 'elements'
  // }).appendTo('.box');

  //   $('<div/>',{
  //   class: 'text'
  // }).appendTo('.elements');

  // $('<p/>',{
  //   class: 'value',
  //   text: key + " - " + values.airportName + "  " + values.numofProd
  // }).appendTo('.text');

  // $('<div/>',{
  //   class: 'thumbs'
  // }).appendTo('.elements');

  for(var i=0;i<values.listofTitle.length;i++) {

    // console.log('values for ' + values + " is " + i);
  $("#" + key).append( 
    '<div class="cap">'+
      '<div class="satthumb">'+ 
        '<img src=' + imagePath + values.listofTitle[i] + extension +'>' + 
        '</div>' + 
        '<div class="overlay">&#10003;</div>' + 
        '<div class="date">' + values.dateofCapture[i] + '</div>' +
        '<div class="uuid" >' + values.listofUUID[i] + '</div>' + '</div>'
  )
}

}

//define cart js
let cart = new Array();
let image = document.getElementsByClassName("satthumb");
// console.log(image);

function addOrRemove(array, value) {
var index = array.indexOf(value);

if (index === -1) {
  console.log('adding element');
    array.push(value);
} else {
  console.log('removing element');
    array.splice(index, 1);
}
return array
}

for(var i=0;i<image.length;i++){
// console.log(2);
let uuid = $(".uuid")[i];
let overlay = $(".overlay")[i];
// console.log(overlay);
image[i].addEventListener('click',function(){
  // console.log(this);
    console.log(uuid.innerHTML);
    overlay.classList.toggle("yes");
    let str = uuid.innerHTML
    // cart.push(str);

    cart = addOrRemove(cart,str);
        },false);
};

let collect = $("#dl");
collect.on("click",function(event) {
// alert(cart)

// $("#uuidUser5").empty();
// $("#uuidUser").append(cart);
// $("#uuidUser5").val = cart;
$("#uuidUser5")[0].value = cart;

// console.log(cart);
// event.preventDefault();
const uniqueCart = [...new Set(cart)]
// alert(uniqueCart);
// uniqueCart.forEach(element => {

// })
});

}


