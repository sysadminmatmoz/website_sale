
// size tage event handler

function compute_sizetag (){
    var radios = document.getElementsByName('sizetag');
    for(var i = 0; i < radios.length; i++){
        if( radios[i].checked ){
            var price = document.getElementById('sizetag_price_' + radios[i].value).value
            if(price == "") {
                price = "0.00"
            }
            document.getElementById('sizetag_price').innerText = parseFloat(price).toFixed(2);
        }
    };
    compute_unit_total();
};

// breadtype event handler

function compute_breadtype (){
    var radios = document.getElementsByName('breadtype');
    for(var i = 0; i < radios.length; i++){
        if( radios[i].checked ){
            var price = document.getElementById('breadtype_price_' + radios[i].value).value
            if(price == "") {
                price = "0.00"
            }
            document.getElementById('breadtype_price').innerText = parseFloat(price).toFixed(2);
        }
    };
    compute_unit_total();
};

// sides event handler

function compute_sides(){
    var sides_price = 0.0;
    var my_sides = document.querySelectorAll('[id^="sides-"]');
    for( var i = 0; i < my_sides.length; i++) {
        if(my_sides[i].checked){
            console.log('checked id: ' + my_sides[i].value);
            var price = document.getElementById('side_price_' + my_sides[i].value).value
            if(price == "") {
                price = "0.00"
            }
            console.log('price:' + parseFloat(price).toFixed(2));
            sides_price += parseFloat(price);
        }
    }
    console.log('sides_price:' + parseFloat(sides_price).toFixed(2));
    document.getElementById('sides_price').innerText = parseFloat(sides_price).toFixed(2);
    // refresh total
    compute_unit_total();
};

// total price computations

function compute_unit_total(){
    var base_price = document.getElementById('base_price');
    var sizetag_price = document.getElementById('sizetag_price');
    var breadtype_price = document.getElementById('breadtype_price');
    var sides = document.getElementById('sides_price');
    var product_unit_price = 0.00;
    if(base_price){
        product_unit_price += parseFloat(base_price.innerText);
    }
    if(sizetag_price){
        product_unit_price += parseFloat(sizetag_price.innerText);
    }
    if(breadtype_price){
        product_unit_price += parseFloat(breadtype_price.innerText);
    }
    if(sides_price){
        product_unit_price += parseFloat(sides_price.innerText);
    }
    document.getElementById('product_unit_price').innerText = product_unit_price.toFixed(2);
};

