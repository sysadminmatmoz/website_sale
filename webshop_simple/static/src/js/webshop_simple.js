
// size tage event handler

function compute_sizetag (product_id){
    if(product_id == undefined){
        return;
    }
    var radios = document.getElementsByName('sizetag_' + product_id);
    for(var i = 0; i < radios.length; i++){
        if( radios[i].checked ){
            var price = document.getElementById('sizetag_price_' + product_id + '_' + radios[i].value).value
            if(price == "") {
                price = "0.00"
            }
            document.getElementById('sizetag_price_' + product_id).innerText = parseFloat(price).toFixed(2);
        }
    };
    compute_unit_total(product_id);
};

// breadtype event handler

function compute_breadtype (product_id){
    if(product_id == undefined){
        return;
    }
    var radios = document.getElementsByName('breadtype_' + product_id);
    for(var i = 0; i < radios.length; i++){
        if( radios[i].checked ){
            var price = document.getElementById('breadtype_price_' + product_id + '_' + radios[i].value).value
            if(price == "") {
                price = "0.00"
            }
            document.getElementById('breadtype_price_' + product_id).innerText = parseFloat(price).toFixed(2);
        }
    };
    compute_unit_total(product_id);
};

// sides event handler

function compute_sides(product_id){
    if(product_id == undefined){
        return;
    }
    var sides_price = 0.0;
    var my_sides = document.querySelectorAll('[id^="sides-' + product_id + '"]');
    if(my_sides.length < 1){
        return;
    }
    for( var i = 0; i < my_sides.length; i++) {
        if(my_sides[i].checked){
            var price = document.getElementById('side_price_' + product_id + '_' + my_sides[i].value).value
            if(price == "") {
                price = "0.00"
            }
            sides_price += parseFloat(price);
        }
    }
    document.getElementById('sides_price_' + product_id).innerText = parseFloat(sides_price).toFixed(2);
    // refresh total
    compute_unit_total(product_id);
};

// total price computations

function compute_unit_total(product_id){
    if(product_id == undefined){
        return;
    }
    var base_price = document.getElementById('base_price_' + product_id);
    var sizetag_price = document.getElementById('sizetag_price_' + product_id);
    var breadtype_price = document.getElementById('breadtype_price_' + product_id);
    var sides_price = document.getElementById('sides_price_' + product_id);
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
    document.getElementById('product_unit_price_' + product_id).innerText = product_unit_price.toFixed(2);
};

// run it onload to initiate tota unit price

window.onload = function(){
    var products = document.querySelectorAll('[name^="product_id"]');
    for(var i = 0; i < products.length; i++){
        var product_id = products[i].value;
        compute_sizetag(product_id);
        compute_breadtype(product_id);
        compute_sides(product_id);
        // just in case we have none of the above
        compute_unit_total(product_id);
    }
}
