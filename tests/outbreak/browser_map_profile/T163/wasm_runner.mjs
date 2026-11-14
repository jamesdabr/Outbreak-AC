import fs from 'node:fs';
const data=fs.readFileSync(0);
if(data.length%96||data.length/96>1024)throw Error('request bound');
const module=await WebAssembly.compile(fs.readFileSync(process.argv[2]));
if(WebAssembly.Module.imports(module).length)throw Error('imports');
const e=(await WebAssembly.instantiate(module,{})).exports;
if(Object.keys(e).sort().join()!==['memory','request_address','response_address','request_capacity','response_capacity','run'].sort().join()||e.request_capacity()!==96||e.response_capacity()!==192)throw Error('exports/layout');
const output=Buffer.alloc(data.length/96*192);
for(let i=0;i<data.length;i+=96){
 new Uint8Array(e.memory.buffer,e.request_address(),96).set(data.subarray(i,i+96));
 if(e.run())throw Error('request');
 output.set(new Uint8Array(e.memory.buffer,e.response_address(),192),i/96*192);
}
process.stdout.write(output);
