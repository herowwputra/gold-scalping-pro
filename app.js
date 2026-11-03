const $=id=>document.getElementById(id);

async function refresh(){
  const status=$('apiStatus');
  status.textContent='Mengambil harga emas...';
  try{
    const r=await fetch('https://api.gold-api.com/price/XAU');
    if(!r.ok) throw Error('Feed gagal');
    const d=await r.json();
    $('price').textContent=Number(d.price).toFixed(2);
    $('symbol').textContent='XAU/USD SPOT';
    $('updated').textContent=new Date().toLocaleTimeString('id-ID');
    $('feedStatus').textContent='HARGA TERHUBUNG';
    $('feedNote').textContent='Harga spot publik, bukan harga broker HFM.';
    $('direction').textContent='WAIT';
    $('reason').textContent='Menunggu data candle untuk konfirmasi sinyal.';
    status.textContent='Harga berhasil diperbarui.';
  }catch(e){
    $('feedStatus').textContent='FEED TERPUTUS';
    status.textContent='Gagal mengambil harga. Coba lagi nanti.';
  }
}

$('connect').addEventListener('click',refresh);
refresh();
setInterval(refresh,60000);
