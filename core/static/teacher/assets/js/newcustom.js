$(document).ready(function(){
        
    $(".filter-checkbox").on('click', function(){
        var filter_object={};
        $(".filter-checkbox").each(function(index,ele){
            var filter_value=$(this).val();
            var filter_key=$(this).data('filter');
            filter_object[filter_key]=Array.from(document.querySelectorAll('input[data-filter='+filter_key+']:checked')).map(function(el){
                 return el.value;
            });
        });

       
       var url = window.location.origin+filter_url
        $.ajax({
            url:url,
            data:filter_object,
            dataType:'json',
            success:function(res){
                $("#teacherData").html(res.data);
                var filter_value=$(this).val();
                var filter_key=$(this).data('filter');
            }
        });
    });
});