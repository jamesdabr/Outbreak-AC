import fs from 'node:fs';
const module = new WebAssembly.Module(fs.readFileSync(process.argv[2]));
if (WebAssembly.Module.imports(module).length) throw new Error('Unexpected runtime import');
const names = WebAssembly.Module.exports(module).map(x=>x.name).sort();
if (JSON.stringify(names)!==JSON.stringify(['input_ptr','memory','output_bytes','output_ptr','run'].sort()))
  throw new Error('Unexpected test exports');
const e = new WebAssembly.Instance(module,{}).exports;
const data=fs.readFileSync(0);let offset=0,count=0;
const outputs=[];
while (offset<data.length) {
  if (++count>128 || offset+16>data.length) throw new Error('Batch/header bounds');
  const n=data.readUInt32LE(offset),declared=data.readUInt32LE(offset+4);
  const capacity=data.readUInt32LE(offset+8),nulls=data.readUInt32LE(offset+12);offset+=16;
  if (n>1048577 || offset+n>data.length) throw new Error('Input bounds');
  new Uint8Array(e.memory.buffer,e.input_ptr(),n).set(data.subarray(offset,offset+n));offset+=n;
  e.run(n,declared,capacity,nulls);
  outputs.push(Buffer.from(new Uint8Array(e.memory.buffer,e.output_ptr(),e.output_bytes())));
}
process.stdout.write(Buffer.concat(outputs));
