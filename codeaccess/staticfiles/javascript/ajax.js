$(function() {
            function call_ajax(f) {
             
               //var data=$('#text1').val();
                var code = editor.getValue();
                var input = `{{indata}}`;
                var output = `{{outdata}}`
                var checkbox = $('#check');
                
                if(checkbox[0].checked == true)
                {
                  input = $('#coustominput').val();
                  output = null;
                  
                }
                
              lan = $("#id_language").val();
               data={'code':code,'input':input,
               'output':output,'language':lan,'csrfmiddlewaretoken':$("input[name=csrfmiddlewaretoken]").val()};
                //console.log(data);
                $.ajax({
                    url: "/profile/execute",//'/heart/pridict/',
                    data: data,
                    dataType: 'json',
                    type: 'POST',
                    success: f,
                    error: function(error) {
                       
                    }
                });
            }

           function server_response(response) {
               
               const r = JSON.parse(response);
               if (r.result && !r.test_cases_total){
                
                z = `<div class="container">
               
                    <h3> output:</h3> 
                    <h5>${r.output} </h5> 
                </div>`;
                 const tabelBody = document.querySelector("#status_header");
         tabelBody.innerHTML = z
                var tabelbody = document.querySelector("#display_data");
             tabelbody.innerHTML ='';
             

               }
         //  else if(r.result =='COE'){
         //    z = `<div class="container">
               
         //            <h3> output:</h3> 
         //            <h5>compilation Errors</h5> 
         //        </div>`;
         //         const tabelBody = document.querySelector("#status_header");
         // tabelBody.innerHTML = z
         //        var tabelbody = document.querySelector("#display_data");
         //     tabelbody.innerHTML ='';
             

         //  }
          else
        {
         const tableData =      `<div id ="result">
        
        <div id="status_header">
        <table>
            <tr>
                <th rowspan="2"> Status </th>
                <th colspan="2"> Test Cases </th>
            </tr>
            <tr>
                <th> Total </th>
                <th> Passed </th>
            </tr>
            <tr>
                <td id = "final">${r.result} </td>
                <td id = "test_cases_total">${r.test_cases_total} </td>
                <td id = "test_cases_passed">${r.test_cases_passed}</td>
            </tr>
        </table>
        </div>`
        const tabelBody = document.querySelector("#status_header");
         tabelBody.innerHTML = tableData;
         var x = ''

        for (var i in r["display_data"])
        { var z = ''
          
             if (r["display_data"][i][1] == true)
             {
                z = `<div><div class="testcase-status success-bg">
                <div class="leftPane">
                    <h3> Testcase ${r["display_data"][i][0]} <span class="status-text-success">success</span> </h3>
                </div>`;
            }
            else{
                z = `<div class="testcase-status fail-bg">
                <div class="leftPane">
                    <h3> Testcase ${r["display_data"][i][0]} <span class="status-text-fail">fail</span> </h3>
                </div>`;
            }
            
            var y =`<div class="rightPane">
                <h2> Output: </h2>
                <p><pre>${r["display_data"][i][2]}</pre>
                <h2>expected out put </h2>
                <p><pre>${ r["display_data"][i][3] }</pre>
                
                <h2> Errors: </h2>
                <p><pre>${r["display_data"][i][4]}</pre>
            </div> </div>`;
            x = x.concat(z,y);
             var tabelbody = document.querySelector("#display_data");
             tabelbody.innerHTML =x;
             //x ="";


        }
       
               
              
            }
          }
            
            $('#form').submit(function(e) {
                e.preventDefault();
                call_ajax(server_response);
            });
        });