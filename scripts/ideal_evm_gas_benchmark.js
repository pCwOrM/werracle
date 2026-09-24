/**
 * scripts/ideal_evm_gas_benchmark.js
 * ===================================
 * Complete, High-Precision Empirical EVM Gas Profiling Suite for Werracle.
 * 
 * Executes real EVM bytecode in a live local in-memory EVM (Ganache EIP-150 / 2929 / 3860)
 * to measure exact empirical `receipt.gasUsed` and net EVM execution gas across:
 * 1. v1.0 Baseline (Werracle.sol - 16-point grid, flat 12-iteration loop)
 * 2. Phase 2 Sparse Multi-Scale Harmonic Tripod (WerracleTripodZMod9.sol - 12-point, Z mod 9 early escape, native int256 unchecked)
 * 3. Blockchain Resonance Matrix (BlockchainResonanceMatrix.sol - 0 SLOAD bytecode lookup)
 * 4. Uniswap v4 Dynamic Fee Hook (WerracleFeeHook.sol)
 * 
 * Verifies strict Phase 2 Invariant: Pure Forward Engine Gas MUST be <= 24,000 gas.
 */

const fs = require('fs');
const path = require('path');
const solc = require('solc');
const ganache = require('ganache');
const { ethers } = require('ethers');

// Helper to calculate exact calldata intrinsic gas (EIP-2028: 16 gas non-zero, 4 gas zero)
function calculateCalldataGas(hexData) {
    if (!hexData || hexData === '0x') return 0;
    const clean = hexData.startsWith('0x') ? hexData.slice(2) : hexData;
    let gas = 0;
    for (let i = 0; i < clean.length; i += 2) {
        const byte = clean.slice(i, i + 2);
        gas += (byte === '00') ? 4 : 16;
    }
    return gas;
}

// Compile all relevant contracts
function compileContracts() {
    console.log("=" .repeat(85));
    console.log(" [1/4] COMPILING SOLIDITY 0.8.20 CONTRACTS (OPTIMIZER: 200 RUNS)...");
    console.log("=" .repeat(85));

    const contractFiles = [
        'IWerracle.sol',
        'WerrMath.sol',
        'BlockchainResonanceMatrix.sol',
        'Werracle.sol',
        'WerracleTripodZMod9.sol',
        'hooks/WerracleFeeHook.sol'
    ];

    const sources = {};
    for (const relPath of contractFiles) {
        const fullPath = path.join(__dirname, '..', 'contracts', relPath);
        sources[relPath] = { content: fs.readFileSync(fullPath, 'utf8') };
    }

    const input = {
        language: 'Solidity',
        sources: sources,
        settings: {
            outputSelection: {
                '*': {
                    '*': ['abi', 'evm.bytecode.object', 'evm.deployedBytecode.object', 'evm.gasEstimates']
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
            }
        }
        if (hasErr) throw new Error("Solidity compilation failed.");
    }

    const compiled = {};
    for (const [file, contracts] of Object.entries(output.contracts)) {
        for (const [name, data] of Object.entries(contracts)) {
            compiled[name] = {
                abi: data.abi,
                bytecode: '0x' + data.evm.bytecode.object,
                deployedBytecode: '0x' + data.evm.deployedBytecode.object,
                size: data.evm.deployedBytecode.object.length / 2
            };
        }
    }

    console.log("[OK] Compilation successful!");
    return compiled;
}

async function runGasProfiling() {
    const compiled = compileContracts();

    console.log("\n" + "=" .repeat(85));
    console.log(" [2/4] INITIALIZING IN-MEMORY EVM (GANACHE CANCUN/SHANGHAI EIP-2929/3860)...");
    console.log("=" .repeat(85));

    const ganacheProvider = ganache.provider({
        logging: { quiet: true },
        wallet: {
            totalAccounts: 5,
            defaultBalance: 1000
        },
        miner: {
            blockGasLimit: 30000000
        }
    });

    const provider = new ethers.BrowserProvider(ganacheProvider);
    const signer = await provider.getSigner(0);
    const feeRecipient = await (await provider.getSigner(1)).getAddress();
    const PROTOCOL_FEE = ethers.parseEther("0.00005");

    console.log(`- Deployer Address     : ${await signer.getAddress()}`);
    console.log(`- Fee Recipient Address: ${feeRecipient}`);
    console.log(`- Protocol Fee         : 0.00005 ETH`);

    // --- DEPLOYMENT PROFILING ---
    console.log("\n" + "=" .repeat(85));
    console.log(" [3/4] DEPLOYING CONTRACTS & MEASURING DEPLOYMENT GAS...");
    console.log("=" .repeat(85));

    // 1. Deploy Werracle (Baseline)
    const WerracleFactory = new ethers.ContractFactory(
        compiled.Werracle.abi,
        compiled.Werracle.bytecode,
        signer
    );
    const deployTxV1 = await WerracleFactory.deploy(feeRecipient, PROTOCOL_FEE);
    await deployTxV1.waitForDeployment();
    const v1Receipt = await provider.getTransactionReceipt(deployTxV1.deploymentTransaction().hash);
    const v1Address = await deployTxV1.getAddress();
    const v1Contract = new ethers.Contract(v1Address, compiled.Werracle.abi, signer);

    console.log(`1. Werracle v1.0 (Baseline):`);
    console.log(`   - Address        : ${v1Address}`);
    console.log(`   - Bytecode Size  : ${compiled.Werracle.size} bytes`);
    console.log(`   - Deployment Gas : ${v1Receipt.gasUsed.toLocaleString()} gas`);

    // 2. Deploy WerracleTripodZMod9 (Phase 2)
    const TripodFactory = new ethers.ContractFactory(
        compiled.WerracleTripodZMod9.abi,
        compiled.WerracleTripodZMod9.bytecode,
        signer
    );
    const deployTxP2 = await TripodFactory.deploy(feeRecipient, PROTOCOL_FEE);
    await deployTxP2.waitForDeployment();
    const p2Receipt = await provider.getTransactionReceipt(deployTxP2.deploymentTransaction().hash);
    const p2Address = await deployTxP2.getAddress();
    const p2Contract = new ethers.Contract(p2Address, compiled.WerracleTripodZMod9.abi, signer);

    console.log(`\n2. WerracleTripodZMod9 (Phase 2):`);
    console.log(`   - Address        : ${p2Address}`);
    console.log(`   - Bytecode Size  : ${compiled.WerracleTripodZMod9.size} bytes`);
    console.log(`   - Deployment Gas : ${p2Receipt.gasUsed.toLocaleString()} gas`);

    // 3. Deploy WerracleFeeHook connected to Tripod
    const HookFactory = new ethers.ContractFactory(
        compiled.WerracleFeeHook.abi,
        compiled.WerracleFeeHook.bytecode,
        signer
    );
    const deployTxHook = await HookFactory.deploy(p2Address);
    await deployTxHook.waitForDeployment();
    const hookReceipt = await provider.getTransactionReceipt(deployTxHook.deploymentTransaction().hash);
    const hookAddress = await deployTxHook.getAddress();
    const hookContract = new ethers.Contract(hookAddress, compiled.WerracleFeeHook.abi, signer);

    console.log(`\n3. WerracleFeeHook (Uniswap v4 Dynamic Fee Hook):`);
    console.log(`   - Address        : ${hookAddress}`);
    console.log(`   - Bytecode Size  : ${compiled.WerracleFeeHook.size} bytes`);
    console.log(`   - Deployment Gas : ${hookReceipt.gasUsed.toLocaleString()} gas`);

    // Helper functions for gas measurement
    async function measureTx(description, contractCall) {
        const tx = await contractCall;
        const receipt = await tx.wait();
        const calldataGas = calculateCalldataGas(tx.data);
        const totalGas = Number(receipt.gasUsed);
        const netExecutionGas = totalGas - 21000 - calldataGas;
        return {
            description,
            totalGas,
            calldataGas,
            netExecutionGas
        };
    }

    async function measureViewGas(contract, method, ...args) {
        const gasEstimate = await contract[method].estimateGas(...args);
        // Calldata intrinsic gas
        const iface = contract.interface;
        const calldata = iface.encodeFunctionData(method, args);
        const callGas = calculateCalldataGas(calldata);
        const netForwardGas = Number(gasEstimate) - 21000 - callGas;
        return {
            totalEstimate: Number(gasEstimate),
            calldataGas: callGas,
            netForwardGas: Math.max(0, netForwardGas)
        };
    }

    const ONE_FP = 65536; // 1.0 in Q16.16

    // --- FUNCTION-BY-FUNCTION PROFILING ---
    console.log("\n" + "=" .repeat(85));
    console.log(" [4/4] EMPIRICAL MULTI-TIER EVM GAS MEASUREMENT");
    console.log("=" .repeat(85));

    // =========================================================================
    // TIER 1: PURE FORWARD INFERENCE ENGINE GAS (previewDecision)
    // Core AI Oracle computation (SLOAD + Mandelbrot Loop + Sigmoid)
    // =========================================================================
    console.log("\n--- TIER 1: PURE FORWARD INFERENCE ENGINE (previewDecision - 0 State Write) ---");

    const stateDummy = ethers.keccak256(ethers.toUtf8Bytes("state:pure_engine"));

    // 1. Stable / Interior (Normal Risk -1.5 FP)
    const riskInteriorFP = -BigInt(Math.floor(1.5 * ONE_FP));
    const v1ViewInt = await measureViewGas(v1Contract, 'previewDecision', stateDummy, riskInteriorFP);
    const p2ViewInt = await measureViewGas(p2Contract, 'previewDecision', stateDummy, riskInteriorFP);

    // 2. Shock / Exterior (Flash Attack +2.5 FP -> Fast Escape)
    const riskShockFP = BigInt(Math.floor(2.5 * ONE_FP));
    const v1ViewShock = await measureViewGas(v1Contract, 'previewDecision', stateDummy, riskShockFP);
    const p2ViewShock = await measureViewGas(p2Contract, 'previewDecision', stateDummy, riskShockFP);

    // 3. Boundary Edge of Chaos (0.0 FP)
    const v1ViewEdge = await measureViewGas(v1Contract, 'previewDecision', stateDummy, 0);
    const p2ViewEdge = await measureViewGas(p2Contract, 'previewDecision', stateDummy, 0);

    console.table([
        {
            Scenario: "Stable Market (Interior Set)",
            "v1.0 Baseline": `${v1ViewInt.netForwardGas.toLocaleString()} gas`,
            "Phase 2 Tripod Z mod 9": `${p2ViewInt.netForwardGas.toLocaleString()} gas`,
            "Engine Gas Savings": `${(v1ViewInt.netForwardGas - p2ViewInt.netForwardGas).toLocaleString()} gas`,
            "Reduction %": `${(((v1ViewInt.netForwardGas - p2ViewInt.netForwardGas) / v1ViewInt.netForwardGas) * 100).toFixed(1)}%`
        },
        {
            Scenario: "Flash Shock (Fast Escape)",
            "v1.0 Baseline": `${v1ViewShock.netForwardGas.toLocaleString()} gas`,
            "Phase 2 Tripod Z mod 9": `${p2ViewShock.netForwardGas.toLocaleString()} gas`,
            "Engine Gas Savings": `${(v1ViewShock.netForwardGas - p2ViewShock.netForwardGas).toLocaleString()} gas`,
            "Reduction %": `${(((v1ViewShock.netForwardGas - p2ViewShock.netForwardGas) / v1ViewShock.netForwardGas) * 100).toFixed(1)}%`
        },
        {
            Scenario: "Edge of Chaos Boundary (0.0 FP)",
            "v1.0 Baseline": `${v1ViewEdge.netForwardGas.toLocaleString()} gas`,
            "Phase 2 Tripod Z mod 9": `${p2ViewEdge.netForwardGas.toLocaleString()} gas`,
            "Engine Gas Savings": `${(v1ViewEdge.netForwardGas - p2ViewEdge.netForwardGas).toLocaleString()} gas`,
            "Reduction %": `${(((v1ViewEdge.netForwardGas - p2ViewEdge.netForwardGas) / v1ViewEdge.netForwardGas) * 100).toFixed(1)}%`
        }
    ]);

    // =========================================================================
    // TIER 2: FULL ON-CHAIN TRANSACTION EXECUTION (decideNoul)
    // Includes Base 21,000 tx gas, calldata, fee transfer, state counter, and events
    // =========================================================================
    console.log("\n--- TIER 2: ON-CHAIN TRANSACTION EXECUTION (decideNoul) ---");

    // Warm calls
    const hashNormal = ethers.keccak256(ethers.toUtf8Bytes("state:warm_normal"));
    const warmNormV1 = await measureTx("Warm Normal v1.0", v1Contract.decideNoul(hashNormal, riskInteriorFP, { value: PROTOCOL_FEE }));
    const warmNormP2 = await measureTx("Warm Normal Phase 2", p2Contract.decideNoul(hashNormal, riskInteriorFP, { value: PROTOCOL_FEE }));

    const hashShock = ethers.keccak256(ethers.toUtf8Bytes("state:warm_shock"));
    const warmShockV1 = await measureTx("Warm Shock v1.0", v1Contract.decideNoul(hashShock, riskShockFP, { value: PROTOCOL_FEE }));
    const warmShockP2 = await measureTx("Warm Shock Phase 2", p2Contract.decideNoul(hashShock, riskShockFP, { value: PROTOCOL_FEE }));

    console.table([
        {
            Scenario: "Warm Normal (ALLOW)",
            "v1.0 Total Tx Gas": warmNormV1.totalGas.toLocaleString(),
            "v1.0 Net Exec Gas": warmNormV1.netExecutionGas.toLocaleString(),
            "Phase 2 Total Tx Gas": warmNormP2.totalGas.toLocaleString(),
            "Phase 2 Net Exec Gas": warmNormP2.netExecutionGas.toLocaleString(),
            "Net Exec Savings": `${(warmNormV1.netExecutionGas - warmNormP2.netExecutionGas).toLocaleString()} gas`,
            "Reduction %": `${(((warmNormV1.netExecutionGas - warmNormP2.netExecutionGas) / warmNormV1.netExecutionGas) * 100).toFixed(1)}%`
        },
        {
            Scenario: "Warm Shock (DENY)",
            "v1.0 Total Tx Gas": warmShockV1.totalGas.toLocaleString(),
            "v1.0 Net Exec Gas": warmShockV1.netExecutionGas.toLocaleString(),
            "Phase 2 Total Tx Gas": warmShockP2.totalGas.toLocaleString(),
            "Phase 2 Net Exec Gas": warmShockP2.netExecutionGas.toLocaleString(),
            "Net Exec Savings": `${(warmShockV1.netExecutionGas - warmShockP2.netExecutionGas).toLocaleString()} gas`,
            "Reduction %": `${(((warmShockV1.netExecutionGas - warmShockP2.netExecutionGas) / warmShockV1.netExecutionGas) * 100).toFixed(1)}%`
        }
    ]);

    // =========================================================================
    // TIER 3: MULTI-WAY ROUTING (decideChoice) & SCORING (decideScore)
    // =========================================================================
    console.log("\n--- TIER 3: MULTI-WAY ROUTING (decideChoice) ---");
    const hashChoice = ethers.keccak256(ethers.toUtf8Bytes("state:choice_benchmark"));
    const choice2_V1 = await measureTx("2 Choices v1.0", v1Contract.decideChoice(hashChoice, 2, 0, { value: PROTOCOL_FEE }));
    const choice2_P2 = await measureTx("2 Choices Phase 2", p2Contract.decideChoice(hashChoice, 2, 0, { value: PROTOCOL_FEE }));

    const choice4_V1 = await measureTx("4 Choices v1.0", v1Contract.decideChoice(hashChoice, 4, 0, { value: PROTOCOL_FEE }));
    const choice4_P2 = await measureTx("4 Choices Phase 2", p2Contract.decideChoice(hashChoice, 4, 0, { value: PROTOCOL_FEE }));

    const choice8_V1 = await measureTx("8 Choices v1.0", v1Contract.decideChoice(hashChoice, 8, 0, { value: PROTOCOL_FEE }));
    const choice8_P2 = await measureTx("8 Choices Phase 2", p2Contract.decideChoice(hashChoice, 8, 0, { value: PROTOCOL_FEE }));

    console.table([
        {
            Route: "2 Choices (Binary Split)",
            "v1.0 Net Exec": choice2_V1.netExecutionGas.toLocaleString(),
            "Phase 2 Net Exec": choice2_P2.netExecutionGas.toLocaleString(),
            Savings: `${(choice2_V1.netExecutionGas - choice2_P2.netExecutionGas).toLocaleString()} gas`,
            "Reduction %": `${(((choice2_V1.netExecutionGas - choice2_P2.netExecutionGas) / choice2_V1.netExecutionGas) * 100).toFixed(1)}%`
        },
        {
            Route: "4 Choices (Quad Route)",
            "v1.0 Net Exec": choice4_V1.netExecutionGas.toLocaleString(),
            "Phase 2 Net Exec": choice4_P2.netExecutionGas.toLocaleString(),
            Savings: `${(choice4_V1.netExecutionGas - choice4_P2.netExecutionGas).toLocaleString()} gas`,
            "Reduction %": `${(((choice4_V1.netExecutionGas - choice4_P2.netExecutionGas) / choice4_V1.netExecutionGas) * 100).toFixed(1)}%`
        },
        {
            Route: "8 Choices (Octa Route)",
            "v1.0 Net Exec": choice8_V1.netExecutionGas.toLocaleString(),
            "Phase 2 Net Exec": choice8_P2.netExecutionGas.toLocaleString(),
            Savings: `${(choice8_V1.netExecutionGas - choice8_P2.netExecutionGas).toLocaleString()} gas`,
            "Reduction %": `${(((choice8_V1.netExecutionGas - choice8_P2.netExecutionGas) / choice8_V1.netExecutionGas) * 100).toFixed(1)}%`
        }
    ]);

    // =========================================================================
    // TIER 4: BLOCKCHAIN RESONANCE MATRIX ON-CHAIN LOOKUP
    // =========================================================================
    console.log("\n--- TIER 4: BLOCKCHAIN RESONANCE MATRIX LOOKUP (0 SLOAD) ---");
    const res1 = await p2Contract.evaluateResonanceTokens.estimateGas([0, 255, 255, 255]); // 1 valid token
    const res2 = await p2Contract.evaluateResonanceTokens.estimateGas([0, 4, 255, 255]);   // 2 valid tokens
    const res4 = await p2Contract.evaluateResonanceTokens.estimateGas([0, 4, 16, 24]);     // 4 valid tokens

    const netRes1 = Number(res1) - 21000 - 64;
    const netRes2 = Number(res2) - 21000 - 64;
    const netRes4 = Number(res4) - 21000 - 64;

    console.table([
        { Configuration: "1 Token (AMM_FLASH_SWAP)", "Total Gas": Number(res1).toLocaleString(), "Net Lookup Gas (0 SLOAD)": `${netRes1.toLocaleString()} gas` },
        { Configuration: "2 Tokens (AMM_FLASH_SWAP + MEV_SANDWICH)", "Total Gas": Number(res2).toLocaleString(), "Net Lookup Gas (0 SLOAD)": `${netRes2.toLocaleString()} gas` },
        { Configuration: "4 Tokens (4-Domain Composite Fusion)", "Total Gas": Number(res4).toLocaleString(), "Net Lookup Gas (0 SLOAD)": `${netRes4.toLocaleString()} gas` }
    ]);

    // =========================================================================
    // TIER 5: UNISWAP V4 DYNAMIC FEE HOOK (calculateDynamicFee)
    // =========================================================================
    console.log("\n--- TIER 5: UNISWAP V4 DYNAMIC FEE HOOK ---");
    const poolId = ethers.keccak256(ethers.toUtf8Bytes("pool:WETH-USDC-0.05"));
    const feeHookLow = await measureTx("Fee Hook Calm Market", hookContract.calculateDynamicFee(poolId, 0, { value: PROTOCOL_FEE }));
    const feeHookHigh = await measureTx("Fee Hook Volatility Shock", hookContract.calculateDynamicFee(poolId, BigInt(2 * ONE_FP), { value: PROTOCOL_FEE }));

    console.table([
        { Condition: "Calm Market (Low Volatility)", "Total Gas": feeHookLow.totalGas.toLocaleString(), "Net Hook + Oracle Exec Gas": `${feeHookLow.netExecutionGas.toLocaleString()} gas` },
        { Condition: "Volatility Shock (High MEV)", "Total Gas": feeHookHigh.totalGas.toLocaleString(), "Net Hook + Oracle Exec Gas": `${feeHookHigh.netExecutionGas.toLocaleString()} gas` }
    ]);

    // =========================================================================
    // TIER 6: 25-VECTOR EMPIRICAL STATISTICAL BATTERY
    // Evaluates 25 equidistant risk sweeps in [-2.5, +2.5] across EVM
    // =========================================================================
    console.log("\n" + "=" .repeat(85));
    console.log(" [STATISTICAL BATTERY] 25-VECTOR PARAMETER SWEEP IN EVM (v1.0 vs Phase 2)");
    console.log("=" .repeat(85));

    const v1EngineList = [];
    const p2EngineList = [];
    const NUM_SWEEPS = 25;

    for (let i = 0; i < NUM_SWEEPS; i++) {
        const dummyHash = ethers.keccak256(ethers.toUtf8Bytes(`sweep_${i}`));
        const riskVal = -2.5 + (i / (NUM_SWEEPS - 1.0)) * 5.0; // [-2.5, +2.5]
        const riskFP = BigInt(Math.floor(riskVal * ONE_FP));

        // 1. Pure Forward Engine Gas
        const gV1Engine = await measureViewGas(v1Contract, 'previewDecision', dummyHash, riskFP);
        const gP2Engine = await measureViewGas(p2Contract, 'previewDecision', dummyHash, riskFP);

        v1EngineList.push(gV1Engine.netForwardGas);
        p2EngineList.push(gP2Engine.netForwardGas);
        process.stdout.write(`.`);
    }
    console.log(" Done!");

    const calcStats = (arr) => {
        const sum = arr.reduce((a, b) => a + b, 0);
        const mean = sum / arr.length;
        const min = Math.min(...arr);
        const max = Math.max(...arr);
        const sorted = [...arr].sort((a, b) => a - b);
        const median = sorted[Math.floor(sorted.length / 2)];
        const variance = arr.reduce((acc, val) => acc + Math.pow(val - mean, 2), 0) / arr.length;
        const stdDev = Math.sqrt(variance);
        return { mean, median, min, max, stdDev };
    };

    const statsV1Engine = calcStats(v1EngineList);
    const statsP2Engine = calcStats(p2EngineList);

    const engineSavingsMean = statsV1Engine.mean - statsP2Engine.mean;
    const engineSavingsPct = (engineSavingsMean / statsV1Engine.mean) * 100.0;

    console.table([
        {
            Metric: "Mean Engine Gas",
            "v1.0 Baseline": `${statsV1Engine.mean.toFixed(1)} gas`,
            "Phase 2 Tripod Z mod 9": `${statsP2Engine.mean.toFixed(1)} gas`,
            "Net Reduction": `${engineSavingsMean.toFixed(1)} gas (-${engineSavingsPct.toFixed(1)}%)`
        },
        {
            Metric: "Median Engine Gas",
            "v1.0 Baseline": `${statsV1Engine.median} gas`,
            "Phase 2 Tripod Z mod 9": `${statsP2Engine.median} gas`,
            "Net Reduction": `${statsV1Engine.median - statsP2Engine.median} gas`
        },
        {
            Metric: "Min Engine Gas (Fast Escape)",
            "v1.0 Baseline": `${statsV1Engine.min} gas`,
            "Phase 2 Tripod Z mod 9": `${statsP2Engine.min} gas`,
            "Net Reduction": `${statsV1Engine.min - statsP2Engine.min} gas`
        },
        {
            Metric: "Max Engine Gas (Worst Case)",
            "v1.0 Baseline": `${statsV1Engine.max} gas`,
            "Phase 2 Tripod Z mod 9": `${statsP2Engine.max} gas`,
            "Net Reduction": `${statsV1Engine.max - statsP2Engine.max} gas`
        },
        {
            Metric: "Standard Deviation",
            "v1.0 Baseline": `${statsV1Engine.stdDev.toFixed(1)} gas`,
            "Phase 2 Tripod Z mod 9": `${statsP2Engine.stdDev.toFixed(1)} gas`,
            "Net Reduction": "N/A"
        }
    ]);

    // =========================================================================
    // FORMAL INVARIANT VERIFICATION
    // =========================================================================
    console.log("\n" + "=" .repeat(85));
    console.log(" FORMAL INVARIANT VERIFICATION: Gas <= 24,000 Gas");
    console.log("=" .repeat(85));

    const ceilingLimit = 24000;
    const isInvariantSatisfied = statsP2Engine.max <= ceilingLimit;
    const headroom = ceilingLimit - statsP2Engine.max;
    const headroomPct = ((headroom / ceilingLimit) * 100).toFixed(1);

    console.log(`- Phase 2 Max Engine Gas Ceiling : ${statsP2Engine.max.toLocaleString()} gas`);
    console.log(`- Strict Target Ceiling Limit     : ${ceilingLimit.toLocaleString()} gas`);
    console.log(`- Safety Margin Below Ceiling    : ${headroom.toLocaleString()} gas (${headroomPct}% headroom)`);
    console.log(`- Status                         : ${isInvariantSatisfied ? "[PASSED] STRICT INVARIANT FULLY SATISFIED" : "[FAILED] INVARIANT BREACHED"}`);

    if (!isInvariantSatisfied) {
        throw new Error(`INVARIANT BREACH: Phase 2 engine gas ${statsP2Engine.max} exceeds ${ceilingLimit} gas ceiling.`);
    }

    // Export comprehensive audit JSON
    const reportDir = path.join(__dirname, '..', 'tests', 'results');
    if (!fs.existsSync(reportDir)) fs.mkdirSync(reportDir, { recursive: true });

    const auditData = {
        timestamp: new Date().toISOString(),
        evmEnvironment: "Ganache In-Memory EVM (Solidity 0.8.20 / EIP-150 / EIP-2929 / EIP-3860)",
        contracts: {
            Werracle_v1: {
                address: v1Address,
                bytecodeSize: compiled.Werracle.size,
                deploymentGas: Number(v1Receipt.gasUsed)
            },
            WerracleTripodZMod9_Phase2: {
                address: p2Address,
                bytecodeSize: compiled.WerracleTripodZMod9.size,
                deploymentGas: Number(p2Receipt.gasUsed)
            },
            WerracleFeeHook: {
                address: hookAddress,
                bytecodeSize: compiled.WerracleFeeHook.size,
                deploymentGas: Number(hookReceipt.gasUsed)
            }
        },
        pureForwardEngine: {
            interior: { v1: v1ViewInt, p2: p2ViewInt },
            shock: { v1: v1ViewShock, p2: p2ViewShock },
            edgeOfChaos: { v1: v1ViewEdge, p2: p2ViewEdge }
        },
        fullTransaction: {
            warmNormal: { v1: warmNormV1, p2: warmNormP2 },
            warmShock: { v1: warmShockV1, p2: warmShockP2 },
            choices: {
                choice2: { v1: choice2_V1, p2: choice2_P2 },
                choice4: { v1: choice4_V1, p2: choice4_P2 },
                choice8: { v1: choice8_V1, p2: choice8_P2 }
            },
            resonanceMatrixLookup: { res1: netRes1, res2: netRes2, res4: netRes4 },
            dynamicFeeHook: { calm: feeHookLow, shock: feeHookHigh }
        },
        statistical100RunEngine: {
            v1: statsV1Engine,
            p2: statsP2Engine,
            savingsMean: engineSavingsMean,
            savingsPct: engineSavingsPct
        },
        invariant: {
            targetCeiling: ceilingLimit,
            phase2MaxEngineGas: statsP2Engine.max,
            headroomGas: headroom,
            headroomPct: Number(headroomPct),
            satisfied: isInvariantSatisfied
        }
    };

    const auditJsonPath = path.join(reportDir, 'evm_gas_ideal_benchmark.json');
    fs.writeFileSync(auditJsonPath, JSON.stringify(auditData, null, 2));
    console.log(`\n[OK] Complete empirical audit results saved to: ${auditJsonPath}`);

    return auditData;
}

runGasProfiling().catch(err => {
    console.error("FATAL ERROR in gas profiling:", err);
    process.exit(1);
});
