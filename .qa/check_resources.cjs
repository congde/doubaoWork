const fs=require('fs');const {chromium}=require('C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
(async()=>{const b=await chromium.launch({channel:'msedge',headless:true});const p=await b.newPage({viewport:{width:1200,height:900}});const errors=[];p.on('pageerror',e=>errors.push(e.message));
const pages=['resources/思维导图与章节技能/思维导图预览.html','resources/思维导图与章节技能/章节导图预览.html','resources/章节技能_即用版/打开这里.html','resources/豆包Word整体思维导图/打开全书思维导图.html','resources/豆包工作全面思维导图/打开全面思维导图.html'];
for(const path of pages){await p.goto('http://127.0.0.1:8765/'+path);await p.waitForTimeout(200)}
await p.goto('http://127.0.0.1:8765/#chapters');await p.waitForTimeout(100);await p.locator('.concept-chip').first().click();if(!await p.locator('#drawer').isVisible())errors.push('concept drawer');await p.locator('#close-drawer').click();
for(let n=1;n<=15;n++){await p.goto('http://127.0.0.1:8765/#chapters-'+n);await p.locator('.chapter-map img').waitFor();await p.locator('.chapter-map img').evaluate(img=>img.decode());const ok=await p.locator('.chapter-map img').evaluate(img=>img.naturalWidth>=1536);if(!ok)errors.push('map '+n);}
await p.goto('http://127.0.0.1:8765/#chapters-7');await p.locator('.chapter-map img').screenshot({path:'.qa/display/map-07.png'});
fs.writeFileSync('.qa/display/resources-report.json',JSON.stringify({pages:pages.length,maps:15,errors},null,2));console.log({pages:pages.length,maps:15,errors});await b.close();process.exit(errors.length?1:0);
})().catch(e=>{console.error(e);process.exit(1)});
