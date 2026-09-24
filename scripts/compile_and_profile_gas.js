/**
 * scripts/compile_and_profile_gas.js
 * Compiles all Werracle Solidity contracts and extracts precise gas estimates.
 */
const solc = require('solc');
const fs = require('fs');
const path = require('path');

const contracts = [
    'IWerracle.sol',
    'WerrMath.sol',
    'BlockchainResonanceMatrix.sol',
    'Werracle.sol',
    'WerracleTripodZMod9.sol'
];

console.log("=" .repeat(70));
console.log(" [COMPILER] Compiling Solidity 0.8.20 Contracts with solc...");
console.log("=" .repeat(70));

const sources = {};
for (const file of contracts) {
    const fullPath = path.join(__dirname, '..', 'contracts', file);
    sources[file] = { content: fs.readFileSync(fullPath, 'utf8') };
}

const input = {
    language: 'Solidity',
    sources: sources,
    settings: {
        outputSelection: {
            '*': {
                '*': ['abi', 'evm.bytecode', 'evm.gasEstimates', 'evm.methodIdentifiers']
            }
        },
        optimizer: {
            enabled: true,
            runs: 200
        }
    }
};

const output = JSON.parse(solc.compile(JSON.stringify(input)));

if (output.errors) {
    let hasErr = false;
    for (const err of output.errors) {
        if (err.severity === 'error') {
            console.error(err.formattedMessage);
            hasErr = true;
        } else {
            console.warn(err.formattedMessage);
        }
    }
    if (hasErr) process.exit(1);
}

console.log("\n[OK] All Contracts Compiled Successfully!");

console.log("\n" + "-".repeat(70));
console.log(" CONTRACT BYTECODE SIZES & GAS ESTIMATES");
console.log("-".repeat(70));

for (const [file, contractObj] of Object.entries(output.contracts)) {
    for (const [name, data] of Object.entries(contractObj)) {
        const binLen = data.evm.bytecode.object.length / 2;
        console.log(`\n* Contract: ${name} (${file})`);
        console.log(`  Bytecode Size: ${binLen} bytes`);
        
        const gasEstimates = data.evm.gasEstimates;
        if (gasEstimates && gasEstimates.creation) {
            console.log(`  Deployment Gas: ~${gasEstimates.creation.totalCost} gas`);
        }
        if (gasEstimates && gasEstimates.external) {
            console.log("  External Functions Gas Estimates:");
            for (const [sig, gasVal] of Object.entries(gasEstimates.external)) {
                console.log(`    - ${sig.padEnd(45)}: ${gasVal} gas`);
            }
        }
    }
}
