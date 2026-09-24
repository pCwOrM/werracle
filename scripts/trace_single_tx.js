const fs = require('fs');
const path = require('path');
const solc = require('solc');
const ganache = require('ganache');
const { ethers } = require('ethers');

async function main() {
    const contractFiles = ['IWerracle.sol', 'WerrMath.sol', 'BlockchainResonanceMatrix.sol', 'Werracle.sol', 'WerracleTripodZMod9.sol'];
    const sources = {};
    for (const relPath of contractFiles) {
        sources[relPath] = { content: fs.readFileSync(path.join(__dirname, '..', 'contracts', relPath), 'utf8') };
    }

    const input = {
        language: 'Solidity',
        sources: sources,
        settings: {
            outputSelection: { '*': { '*': ['abi', 'evm.bytecode.object'] } },
            optimizer: { enabled: true, runs: 200 }
        }
    };
    const output = JSON.parse(solc.compile(JSON.stringify(input)));
    const gp = ganache.provider({ logging: { quiet: true } });
    const provider = new ethers.BrowserProvider(gp);
    const signer = await provider.getSigner(0);
    const feeRecipient = await (await provider.getSigner(1)).getAddress();
    const fee = ethers.parseEther("0.00005");

    // Deploy Tripod
    const TripodFactory = new ethers.ContractFactory(
        output.contracts['WerracleTripodZMod9.sol'].WerracleTripodZMod9.abi,
        '0x' + output.contracts['WerracleTripodZMod9.sol'].WerracleTripodZMod9.evm.bytecode.object,
        signer
    );
    const tripod = await TripodFactory.deploy(feeRecipient, fee);
    await tripod.waitForDeployment();

    // Call decideNoul
    const stateHash = ethers.keccak256(ethers.toUtf8Bytes("trace_test"));
    const tx = await tripod.decideNoul(stateHash, 0, { value: fee });
    const receipt = await tx.wait();
    console.log("Tx Hash:", tx.hash);
    console.log("Receipt Gas Used:", Number(receipt.gasUsed));

    // Trace transaction with debug_traceTransaction
    const trace = await gp.request({
        method: 'debug_traceTransaction',
        params: [tx.hash, { disableStorage: false, disableMemory: true, disableStack: false }]
    });

    console.log("Trace structLogs length:", trace.structLogs ? trace.structLogs.length : "N/A");
    
    // Aggregate gas by opcode
    const opcodeGas = {};
    let totalOpcodeGas = 0;
    if (trace.structLogs) {
        for (let i = 0; i < trace.structLogs.length; i++) {
            const step = trace.structLogs[i];
            const op = step.op;
            const gasCost = step.gasCost;
            opcodeGas[op] = (opcodeGas[op] || 0) + gasCost;
            totalOpcodeGas += gasCost;
        }
    }
    console.log("Total Opcode Gas from trace:", totalOpcodeGas);
    console.log("Opcode breakdown (sorted by gas):");
    const sorted = Object.entries(opcodeGas).sort((a, b) => b[1] - a[1]);
    for (const [op, g] of sorted.slice(0, 15)) {
        console.log(`  ${op.padEnd(12)}: ${g.toLocaleString()} gas`);
    }
}

main().catch(console.error);
