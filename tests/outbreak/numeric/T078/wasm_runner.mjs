import fs from 'node:fs';
const module = new WebAssembly.Module(fs.readFileSync(process.argv[2]));
if (WebAssembly.Module.imports(module).length) throw new Error('Unexpected runtime imports');
const expected = ['memory', 'result_x', 'result_y', 'root', 'run'].sort();
if (JSON.stringify(WebAssembly.Module.exports(module).map(x => x.name).sort()) !== JSON.stringify(expected))
  throw new Error('Unexpected exports');
const e = new WebAssembly.Instance(module, {}).exports;
const lines = fs.readFileSync(0, 'utf8').trim().split('\n');
if (lines.length > 4096) throw new Error('Batch limit');
const output = lines.map(line => {
  const parts = line.split(' ');
  if (parts[0] === '8') return `1 ${e.root(BigInt(parts[1])) >>> 0} 0`;
  const [op, a, b, c] = parts.map(Number);
  const status = e.run(op, a, b, c);
  return `${status} ${e.result_x()} ${e.result_y()}`;
});
process.stdout.write(output.join('\n') + '\n');
