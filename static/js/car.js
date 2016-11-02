function build_car(w,h) {
    var car = svg.append('g')
        .attr("id", "car")
        .attr('w',w)
        .attr('h',h);

    // car.append('rect')
    //     .attr("class", "car")
    //     .attr("width", 2*w)
    //     .attr("height",2*h)
    //     .attr("transform", "translate(-"+w+",-"+h+")");

    car.append('rect')
        .attr("class", "car")
        .attr("width", w)
        .attr("height", h)
        .attr("transform", "translate(-"+w/2+",-"+h/2+")");

    car.append('rect')
        .attr("class", "wheel back left")
        .attr("width", w/2)
        .attr("height", w)
        .attr('x',w/2)
        .attr('y',-h/2)
        .attr("transform", "translate(-"+w/4+",-"+w/2+")");

    car.append('rect')
        .attr("class", "wheel back right")
        .attr("width", w/2)
        .attr("height", w)
        .attr('x',-w/2)
        .attr('y',-h/2)
        .attr("transform", "translate(-"+w/4+",-"+w/2+")");

    car.append('rect')
        .attr("class", "wheel front left")
        .attr("width", w/4)
        .attr("height", w)
        .attr('x',w/2)
        .attr('y',h/2)
        .attr("transform", "translate(-"+w/8+",-"+w/2+")");

    car.append('rect')
        .attr("class", "wheel front right")
        .attr("width", w/4)
        .attr("height", w)
        .attr('x',-w/2)
        .attr('y',h/2)
        .attr("transform", "translate(-"+w/8+",-"+w/2+")")
        ;

    // car.append('rect')
    //     .attr("class", "wheel")
    //     .attr("width", w/2)
    //     .attr("height", w)
    //     .attr("transform", "translate("+w/4+","+h*9/10+")");

    return car;
}

function move_car(x,y,r) {
    car.attr('x',x).attr('y',y).attr('r',r).attr("transform", "translate("+x+","+y+") rotate("+r+")");
}

function build_circle(r) {
    var circle = svg.append('circle')
        .attr('r',r);

    return circle;
}

function move_circle(x,y) {
    circle.attr("cx", x).attr("cy",y).attr("transform", "translate(0,0)");
}
