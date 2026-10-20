// Proves the browser simulator is the contract.
// Compiles WerracleTripodZMod9.sol, runs previewDecision() in an in-process EVM
// for the 6 calibrated seeds and 500 random seeds/risks/thresholds, and compares
// every result with the JavaScript port shipped in the web page.
//
//   npm i solc@0.8.20 @ethereumjs/vm@8 @ethereumjs/util@9 ethers@6
//   node tests/web/verify_simulator_parity.mjs [path/to/page.html]
//
import solc from 'solc'; import fs from 'fs'; import path from 'path'; import vmMod from 'vm';
import { VM } from '@ethereumjs/vm'; import { Address, hexToBytes, bytesToHex } from '@ethereumjs/util'; import { Interface, AbiCoder } from 'ethers';
const root = path.resolve(path.dirname(new URL(import.meta.url).pathname), '../..');
const page = fs.readFileSync(process.argv[2] || path.join(root, 'test/index.html'), 'utf8');
const src = page.slice(page.indexOf('const ONE = 65536'), page.indexOf('/* =========================================================\n   Shared palette'));
const ctx = {}; vmMod.createContext(ctx); vmMod.runInContext(src + '\nthis.tripodPreview = tripodPreview; this.TRIPOD = TRIPOD;', ctx);
const sources = {}; for (const f of ['WerracleTripodZMod9.sol','WerrMath.sol','IWerracle.sol','BlockchainResonanceMatrix.sol']) sources[f] = {content: fs.readFileSync(path.join(root, 'contracts', f), 'utf8')};
const out = JSON.parse(solc.compile(JSON.stringify({language:'Solidity', sources, settings:{optimizer:{enabled:true, runs:200}, outputSelection:{'*':{'*':['abi','evm.bytecode.object','storageLayout']}}}})));
const C = out.contracts['WerracleTripodZMod9.sol'].WerracleTripodZMod9, iface = new Interface(C.abi);
const slot = C.storageLayout.storage.find(x => x.label === 'seed').slot;
const vm = await VM.create(), owner = Address.fromString('0x' + '11'.repeat(20));
const dep = await vm.evm.runCall({caller: owner, data: hexToBytes('0x' + C.evm.bytecode.object + AbiCoder.defaultAbiCoder().encode(['address','uint256'], ['0x' + '22'.repeat(20), 0]).slice(2)), gasLimit: 30000000n});
const addr = dep.createdAddress, u = (v, b) => BigInt.asUintN(b, BigInt(v));
const setSeed = (cx, cy, zoom, thr) => vm.stateManager.putContractStorage(addr, hexToBytes('0x' + BigInt(slot).toString(16).padStart(64, '0')),
  hexToBytes('0x' + (u(cx,64) | (u(cy,64) << 64n) | (u(zoom,64) << 128n) | (1n << 192n) | (u(thr,16) << 224n) | (1n << 240n) | (1n << 248n)).toString(16).padStart(64, '0')));
const rnd = (a, b) => a + Math.random() * (b - a), cases = [];
for (const s of ctx.TRIPOD.SEEDS) for (const r of [-4, -1.5, -0.5, 0, 0.3, 0.6, 0.75, 1, 2.5, 4]) cases.push([s.cx, s.cy, s.zoom, Math.round(r * 65536), 5000]);
for (let i = 0; i < 500; i++) cases.push([Math.round(rnd(-2.2, 0.8) * 65536), Math.round(rnd(-1.3, 1.3) * 65536), Math.round(rnd(0.5, 120) * 65536), Math.round(rnd(-4.5, 4.5) * 65536), Math.round(rnd(100, 9900))]);
let bad = 0, gas = [];
for (const [cx, cy, zoom, risk, thr] of cases){
  await setSeed(cx, cy, zoom, thr);
  const r = await vm.evm.runCall({caller: owner, to: addr, data: hexToBytes(iface.encodeFunctionData('previewDecision', ['0x' + '00'.repeat(32), risk])), gasLimit: 30000000n});
  const [ok, conf] = iface.decodeFunctionResult('previewDecision', bytesToHex(r.execResult.returnValue)); gas.push(Number(r.execResult.executionGasUsed));
  const j = ctx.tripodPreview({cx, cy, zoom, threshold: thr}, risk);
  if (ok !== j.allowed || Number(conf) !== j.conf){ bad++; console.log('MISMATCH', {cx, cy, zoom, risk, thr}, ok, Number(conf), j.allowed, j.conf); }
}
gas.sort((a, b) => a - b);
console.log(`${cases.length} cases, ${bad} mismatches. previewDecision execution gas: min ${gas[0]}, median ${gas[gas.length >> 1]}, max ${gas.at(-1)}`);
process.exit(bad ? 1 : 0);
