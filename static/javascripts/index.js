// function addRemoverButton(){
//     var scripRemoverButton = document.querySelectorAll('#remove-scrip')
//     scripRemoverButton.forEach(btn=>{
//         btn.addEventListener('click',(e)=>{
//             scripValue = e.target.value
//             fetch(`/removescrip/${scripValue}`).then(res=>{
//                 if(res.status==200){
//                 e.target.parentElement.parentElement.remove()
//                 console.log("remove clicked")
//                 }
//             })

//         })
//     })

// }





async function makeRequest(){
    await fetch("/getdata").then(res=>(res).json().then(data=>{
    // console.log(data);
    createTbody(data)
    }
    )).catch(err=>{console.log(err)}).finally(err =>console.log(err))
}







var tbody = document.querySelector("table tbody")


function createTbody(data){
    console.log(data);
    data.forEach((scrip,idx)=>{
        elementIndex = idx+1
       
        var tr =  document.querySelector(`body > div.script-container > table > tbody > tr:nth-child(${elementIndex})`)
        if(scrip.Act==true){
            tr.classList.add('k')
        }
        var tdList = tr.querySelectorAll('td')
        tdList[0].innerText = scrip.name
        tdList[1].innerText = scrip.current

        
        tdList[2].innerText = scrip.open_comparision
        tdList[3].innerText = scrip.tbq_tsq
        act_idx=5
        nameID = scrip.name.replaceAll(' ','-')
        tdList[act_idx].querySelector('.ant-web-form-button').setAttribute('data-target','#'+nameID)
        tdList[act_idx].querySelector('h5').innerText = `${scrip.name}`
        tdList[act_idx].querySelector('.mody').setAttribute('id',nameID)
        tdList[act_idx].querySelectorAll(".hidden-scripcode").forEach(e=>{
            e.setAttribute('value',scrip.name)
        })
        if(scrip.bought){
            tr.classList.remove('sold')
            tr.classList.add('bought')
            tdList[4].innerText = scrip.profit_loss
        }  else if(scrip.sold){
            tr.classList.remove('bought')
            tr.classList.add('sold')
            tdList[4].innerText = scrip.profit_loss
        }


       
    }  )


        // let td = document.createElement("td")
        // let select_field = document.createElement("select")
        // select_field.setAttribute('class',"form-select form-select-sm mb-3")
        // select_field.setAttribute('aria-label',".form-select-sm example")
        // h3 = document.createElement('option')
        // h3.innerText = "hello"
        // select_field.appendChild(h3)
        // td.appendChild(select_field)
        // tr.appendChild(td)
        // tbody.appendChild(tr)
    
        
}



function checkTimeAndRequest(){
    var hour = new Date().getHours();
    if(hour<17){
        makeRequest()
    }
}
polling = setInterval(makeRequest,500)
// makeRequest()


// /html/body/div[2]/table/tbody/tr[2]
// 

