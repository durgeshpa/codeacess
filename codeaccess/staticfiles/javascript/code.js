
   $('#check').prop('checked', false);
    var editor = ace.edit("editor");
    const format = ["ace/mode/c_cpp", "ace/mode/c_cpp", "ace/mode/java","ace/mode/python"]
    editor.setTheme("ace/theme/monokai");
    //var x=getElementById('language').value();
    editor.getSession().setMode('ace/mode/c_cpp');
	  editor.setOptions({
	  fontFamily: "tahoma",
	  fontSize: "15pt"
		});
    function setlanuage(){
    x = parseInt($("#id_language").val())
     var y= format[x-1];
     editor.getSession().setMode(y);
     if (x==3) {
var deafult= `import java.util.*;
class Main
{
    public static void main(String []args)
    {
    //write code here
    }
}`;
        editor.setValue(deafult);
    }
    else
    {
       editor.setValue("");
    }
    }


   function custominput() {
    var checkbox = document.getElementById('check');
   	var x = document.getElementById('input');
   	if (checkbox.checked == true) 
    {
      x.style.display = 'block';
    }
    else 
    {
     x.style.display = 'none';
    }
   	
   }

   
