const vscode=require('vscode');
const cfg=()=>vscode.workspace.getConfiguration('sovereign');
const base=()=>cfg().get('apiUrl','http://127.0.0.1:8000');
async function api(path,opt){const r=await fetch(base()+path,opt);const d=await r.json();if(!r.ok)throw new Error(d.detail||JSON.stringify(d));return d}
function activate(context){
 const status=vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left,90);status.text='$(hubot) Sovereign: checking';status.command='sovereign.health';status.show();context.subscriptions.push(status);
 async function health(){try{const hs=await api('/api/models/health');const on=hs.filter(x=>x.online).length;status.text=`$(hubot) Sovereign ${on}/${hs.length}`;vscode.window.showInformationMessage(`SovereignCodeAgent: ${on}/${hs.length} local models online`)}catch(e){status.text='$(error) Sovereign offline';vscode.window.showErrorMessage(e.message)}}
 context.subscriptions.push(vscode.commands.registerCommand('sovereign.open',()=>vscode.env.openExternal(vscode.Uri.parse(base()))));
 context.subscriptions.push(vscode.commands.registerCommand('sovereign.health',health));
 context.subscriptions.push(vscode.commands.registerCommand('sovereign.quality',async()=>{try{const d=await api('/api/quality');vscode.window.showInformationMessage(`Quality gate: ${d.ok?'PASS':'FAIL'}`)}catch(e){vscode.window.showErrorMessage(e.message)}}));
 context.subscriptions.push(vscode.commands.registerCommand('sovereign.diff',async()=>{try{const d=await api('/api/git/diff');const doc=await vscode.workspace.openTextDocument({content:d.stdout||'No diff.',language:'diff'});await vscode.window.showTextDocument(doc,{preview:true})}catch(e){vscode.window.showErrorMessage(e.message)}}));
 context.subscriptions.push(vscode.commands.registerCommand('sovereign.task',async()=>{const message=await vscode.window.showInputBox({prompt:'Describe the autonomous coding task',placeHolder:'Build, test, debug, validate and prepare the app…'});if(!message)return;try{const d=await api('/api/task/start',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message,model:cfg().get('model','gpt-oss-20b'),allow_network:cfg().get('allowNetwork',false)})});status.text=`$(sync~spin) Sovereign ${d.task_id}`;vscode.window.showInformationMessage(`Task ${d.task_id} started. Open the Sovereign workbench for live progress.`)}catch(e){vscode.window.showErrorMessage('SovereignCodeAgent: '+e.message)}}));
 health();
}
function deactivate(){}
module.exports={activate,deactivate};
