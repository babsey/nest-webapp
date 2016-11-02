var slider = function(ref, id, options) {
    $(ref).append('<dt>'+ options.label +'</dt><dd id="'+ id +'" class="slider"><div class="custom-handle ui-slider-handle"></div></dd>')

    var elem = $('#'+id);
    var handle = elem.find(".ui-slider-handle");
    var options = $.extend(options, {
        create: function() {
            var val = $(this).slider("value");
            handle.text(val);
            elem.attr('value', val);
        },
        slide: function(event, ui) {
            handle.text(ui.value);
            elem.attr('value', ui.value);
        },
        change: function(event, ui) {
            handle.text(ui.value);
            elem.attr('value', ui.value);
        }
    })
    return elem.slider(options);
}


var d3_slider  = function(node, param, min, max, val) {
    $('#'+node).find('.params').append('<dt id="id_'+ param+'">'+ param +': <span class="value">' + value +'</span></dt><dd id="'+ param +'"></dd>')
    nodes[node]['params'][param] = parseFloat(val);
    d3.select('#'+param).call(
        d3.slider()
        .min(min)
        .max(max)
        .value(val)
        .axis(true)
        .on("slide", function(evt, value) {
            if ($('#'+node).find('.presets').val() != 'custom') {
                $('#'+node).find('.presets').prepend('<option value="custom">custom</option>').val('custom')
            }
            if ($('#id_simulation').val() != 'custom') {
                $('#id_simulation').prepend('<option value="custom">custom</option>').val('custom');
            }
            nodes[node]['params'][param] = parseFloat(value);
            $('#id_'+param).find('.value').html(value);
        })
    );
}
