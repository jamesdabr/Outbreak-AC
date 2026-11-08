import fs from 'node:fs';
const module = new WebAssembly.Module(fs.readFileSync(process.argv[2]));
if (WebAssembly.Module.imports(module).length) throw new Error('Unexpected imports');
const names = WebAssembly.Module.exports(module).map(x => x.name).sort();
if (JSON.stringify(names) !== JSON.stringify(['case_buffer','execute','memory','result_buffer']))
  throw new Error('Unexpected exports');
const e = new WebAssembly.Instance(module, {}).exports;
const lines = fs.readFileSync(0, 'utf8').trim().split('\n');
if (lines.length > 256) throw new Error('Batch limit');
for (const line of lines) {
  const data = Buffer.from(line, 'hex');
  if (!data.length || data.length > 1200 || data.length * 2 !== line.length)
    throw new Error('Invalid corpus');
  new Uint8Array(e.memory.buffer, e.case_buffer(), data.length).set(data);
  const size = e.execute(data.length);
  if (!size || size > 1300) throw new Error('Invalid result');
  process.stdout.write(Buffer.from(e.memory.buffer, e.result_buffer(), size).toString('hex') + '\n');
}
