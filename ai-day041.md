# AI Day 04：庄园解密



<div id="app" style="background:#fdf6e3; padding:20px; border-radius:10px; font-family:sans-serif; border:2px solid #d3af86;">
  <h2 style="text-align:center; color:#5d4037;">庄园解密：去括号与符号特训</h2>
  <div id="problems"></div>
  <button onclick="checkAnswers()" style="display:block; width:100%; padding:15px; background:#5d4037; color:white; border:none; cursor:pointer; margin-top:20px; border-radius:5px;">提交密文，查看破译结果</button>
  <p id="result" style="text-align:center; font-weight:bold; margin-top:15px;"></p>
</div>

<script>
const problems = [
  { q: "17 - (7 - 4)", a: 14 },
  { q: "-5 - 8", a: -13 },
  { q: "16 - (6 + 4)", a: 6 },
  { q: "-9 + 1", a: -8 },
  { q: "17 - (6 + 1)", a: 10 },
  { q: "-1 - 8", a: -9 },
  { q: "21 - (5 + 3)", a: 13 },
  { q: "-7 - 5", a: -12 },
  { q: "14 - (7 - 1)", a: 8 },
  { q: "-9 - 6", a: -15 }
];

function render() {
  const container = document.getElementById('problems');
  container.style.display = 'grid';
  container.style.gridTemplateColumns = '1fr 1fr';
  container.style.gap = '10px';

  problems.forEach((p, i) => {
    container.innerHTML += `<div style="padding:10px; border:1px dashed #d3af86;">${i+1}. ${p.q} = <input type="number" id="ans${i}" style="width:50px;"></div>`;
  });
}

function checkAnswers() {
  let score = 0;
  problems.forEach((p, i) => {
    const val = document.getElementById(`ans${i}`).value;
    if(parseInt(val) === p.a) score++;
  });
  document.getElementById('result').innerText = `破译完成！得分：${score * 10} / 100`;
}

render();
</script>



