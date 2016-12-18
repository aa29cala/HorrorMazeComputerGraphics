window.onload = function(){recalcMap();}
window.onresize = function(){recalcMap();}
    $(".percentages").hover(function(){
            $(".hide").attr("style","display:none");
            $("#"+this.id+"ID").attr("style","display:block");
        }, 

        function(){
                $(".hide").attr("style","display:none");
                $("#team").attr("style","display:block");
        });

    

    function recalcMap() {

        var width = $("#frame").width();

        var height = $("#frame").height();

        

        $("#mccoy").attr("coords",""+(width*0.13)+","+(height*0.05)+","+(width*0.256)+","+(height*0.27));

        $("#milano").attr("coords",""+(width*0.43)+","+(height*0.15)+","+(width*0.55)+","+(height*0.35));

        $("#calabrese").attr("coords",""+(width*0.73)+","+(height*0.10)+","+(width*0.87)+","+(height*0.32));

        $("#kish").attr("coords",""+(width*0.18)+","+(height*0.39)+","+(width*0.34)+","+(height*0.60));

        $("#weyna").attr("coords",""+(width*0.64)+","+(height*0.34)+","+(width*0.8)+","+(height*0.60));

    }

