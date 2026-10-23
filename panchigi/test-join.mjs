import fs from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
const source=fs.readFileSync('panchigi/join/join.js','utf8');
const uuid='aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa';
for(const [search,valid] of [[`?code=${uuid}`,true],[`?code=${uuid.toUpperCase()}`,true],['',false],['?code=TEST',false],['?code=%3Cscript%3E',false],[`?code=${uuid}&code=${uuid}`,false],[`?code=${uuid}&accountId=x`,false],['?code=%zz',false],['?code=00000000-0000-0000-0000-000000000000',false]]) {
 const nodes=Object.fromEntries(['status','open-app','copy-code','invite-code'].map(k=>[k,{textContent:'',disabled:k==='copy-code',attributes:{'aria-disabled':'true'},setAttribute(k,v){this.attributes[k]=v},addEventListener(){}}]));
 const context={URLSearchParams,location:{search,hash:''},document:{getElementById:id=>nodes[id],addEventListener(){}},setTimeout(){return 1},clearTimeout(){}};
 vm.runInNewContext(source,context);
 assert.equal(nodes['copy-code'].disabled,!valid,search);
 if(valid){assert.equal(nodes['open-app'].href,'panchigi://join?code='+uuid);assert.equal(nodes['invite-code'].textContent,uuid)}else assert.equal(nodes['open-app'].href,undefined);
}
console.log('Landing URL validation: 9 fixtures PASS');
