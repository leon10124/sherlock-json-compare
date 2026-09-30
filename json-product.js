'use strict';
const byId=id=>document.getElementById(id);
byId('compare').onclick=async()=>{byId('compare').disabled=true;byId('output').textContent='比較中…';try{
 const response=await fetch('/venture/json-compare/api/compare',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({left:byId('left').value,right:byId('right').value,ignore_paths:byId('ignore').value.split('\n').map(s=>s.trim()).filter(Boolean),unordered:byId('unordered').checked})});
 const result=await response.json();if(!response.ok)throw Error(result.error);
 byId('output').textContent=(result.equal?'結構相同':'發現 '+result.change_count+' 個差異')+'\n'+JSON.stringify(result.changes,null,2)+(result.truncated?'\n結果已截斷，僅顯示前 200 個差異。':'');
}catch(error){byId('output').textContent='無法比較：'+error.message;}finally{byId('compare').disabled=false;}};
