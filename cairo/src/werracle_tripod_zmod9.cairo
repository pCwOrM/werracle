// SPDX-License-Identifier: BSL-1.1
// WerracleTripodZMod9 for Starknet (Cairo 2.x / Sierra)
// Zero-Storage STARK-Native On-Chain AI Decision Oracle
// Single-Slot Seed Architecture + Sparse 12-Point Harmonic Tripod (Z mod 9)

use starknet::ContractAddress;

#[starknet::interface]
pub trait IWerracleStarknet<TContractState> {
    fn decide_noul(ref self: TContractState, state_hash: felt252, risk_score_fp: i64) -> (bool, u16);
    fn preview_decision(self: @TContractState, state_hash: felt252, risk_score_fp: i64) -> (bool, u16);
    fn decide_choice(ref self: TContractState, state_hash: felt252, num_choices: u8, context_bias_fp: i64) -> u8;
    fn decide_score(ref self: TContractState, state_hash: felt252, risk_score_fp: i64, max_score: u64) -> u64;
    fn get_seed(self: @TContractState) -> (i64, i64, u64, u32, u16, u8, u8);
    fn update_seed(ref self: TContractState, cx: i64, cy: i64, zoom: u64, threshold: u16, default_mode: u8, active_flag: u8);
    fn total_decisions_count(self: @TContractState) -> u64;
    fn owner(self: @TContractState) -> ContractAddress;
}

#[starknet::contract]
pub mod WerracleTripodZMod9 {
    use starknet::{ContractAddress, get_caller_address};
    use starknet::storage::{StoragePointerReadAccess, StoragePointerWriteAccess};
    use super::super::werr_math::WerrMath;

    #[storage]
    struct Storage {
        owner: ContractAddress,
        total_decisions_count: u64,
        // Canonical WERR 24-Byte Coordinate Seed + Governance State
        // Packed logically into a single Starknet storage structure
        seed_cx: i64,
        seed_cy: i64,
        seed_zoom: u64,
        seed_nonce: u32,
        seed_threshold: u16,
        seed_mode: u8,
        seed_active: u8,
    }

    #[event]
    #[derive(Drop, starknet::Event)]
    pub enum Event {
        DecisionEvaluated: DecisionEvaluated,
        SeedUpdated: SeedUpdated,
    }

    #[derive(Drop, starknet::Event)]
    pub struct DecisionEvaluated {
        #[key]
        pub caller: ContractAddress,
        pub state_hash: felt252,
        pub mode: u8,
        pub boundedness_bps: u16,
    }

    #[derive(Drop, starknet::Event)]
    pub struct SeedUpdated {
        pub cx: i64,
        pub cy: i64,
        pub zoom: u64,
        pub nonce: u32,
    }

    #[constructor]
    fn constructor(ref self: ContractState, initial_owner: ContractAddress) {
        self.owner.write(initial_owner);
        self.total_decisions_count.write(0);

        // Initialize with 40-Core Dual Xeon Calibrated Golden Seed (Myrberg-Feigenbaum Horizon)
        // cx = -93061 (-1.4200 in Q16.16), cy = +14417 (+0.2200 in Q16.16), zoom = 2949120 (45.0x)
        self.seed_cx.write(-93061);
        self.seed_cy.write(14417);
        self.seed_zoom.write(2949120);
        self.seed_nonce.write(1);
        self.seed_threshold.write(5000);
        self.seed_mode.write(1);
        self.seed_active.write(1);
    }

    #[abi(embed_v0)]
    impl WerracleStarknetImpl of super::IWerracleStarknet<ContractState> {
        /// 1. `noul` (Boolean Reflex Gate)
        /// Evaluates atomic True/False decision with confidence in basis points [0..10000].
        fn decide_noul(
            ref self: ContractState,
            state_hash: felt252,
            risk_score_fp: i64
        ) -> (bool, u16) {
            assert(self.seed_active.read() == 1, 'Werracle: Engine Paused');

            let cx = self.seed_cx.read();
            let cy = self.seed_cy.read();
            let zoom = self.seed_zoom.read();
            let threshold = self.seed_threshold.read();

            let boundedness_bps: u16 = WerrMath::evaluate_sparse_tripod(cx, cy, zoom);

            let bounded_i128: i128 = boundedness_bps.into();
            let fractal_bias: i128 = bounded_i128 - 5000;
            let risk_i128: i128 = risk_score_fp.into();
            let logit: i128 = -risk_i128 + ((fractal_bias * WerrMath::ONE) / 5000);

            let prob_bps: u16 = WerrMath::sigmoid_bps(logit);
            let allowed: bool = prob_bps >= threshold;
            let confidence_bps: u16 = if allowed { prob_bps } else { 10000 - prob_bps };

            let count = self.total_decisions_count.read();
            self.total_decisions_count.write(count + 1);

            self.emit(DecisionEvaluated {
                caller: get_caller_address(),
                state_hash,
                mode: 0,
                boundedness_bps,
            });

            (allowed, confidence_bps)
        }

        /// Pure / View Forward Inference Preview (Zero State Write).
        fn preview_decision(
            self: @ContractState,
            state_hash: felt252,
            risk_score_fp: i64
        ) -> (bool, u16) {
            assert(self.seed_active.read() == 1, 'Werracle: Engine Paused');

            let cx = self.seed_cx.read();
            let cy = self.seed_cy.read();
            let zoom = self.seed_zoom.read();
            let threshold = self.seed_threshold.read();

            let boundedness_bps: u16 = WerrMath::evaluate_sparse_tripod(cx, cy, zoom);

            let bounded_i128: i128 = boundedness_bps.into();
            let fractal_bias: i128 = bounded_i128 - 5000;
            let risk_i128: i128 = risk_score_fp.into();
            let logit: i128 = -risk_i128 + ((fractal_bias * WerrMath::ONE) / 5000);

            let prob_bps: u16 = WerrMath::sigmoid_bps(logit);
            let allowed: bool = prob_bps >= threshold;
            let confidence_bps: u16 = if allowed { prob_bps } else { 10000 - prob_bps };

            (allowed, confidence_bps)
        }

        /// 2. `choice` (N-Way Quadrant Route Selector)
        /// Discretely routes transactions or Dojo autonomous agent actions across optimal paths.
        fn decide_choice(
            ref self: ContractState,
            state_hash: felt252,
            num_choices: u8,
            context_bias_fp: i64
        ) -> u8 {
            assert(self.seed_active.read() == 1, 'Werracle: Engine Paused');
            assert(num_choices > 1, 'Werracle: Need >1 Choices');

            let cx = self.seed_cx.read();
            let cy = self.seed_cy.read();
            let zoom = self.seed_zoom.read();

            let boundedness_bps: u16 = WerrMath::evaluate_sparse_tripod(cx, cy, zoom);
            let bounded_i128: i128 = boundedness_bps.into();
            let bias_i128: i128 = context_bias_fp.into();

            let mut best_score: i128 = -1000000000;
            let mut best_idx: u8 = 0;
            let mut i: u8 = 0;

            while i < num_choices {
                let idx_plus_one: i128 = (i + 1).into();
                let score: i128 = bounded_i128 + ((bias_i128 * idx_plus_one) / 4);
                if score > best_score {
                    best_score = score;
                    best_idx = i;
                }
                i += 1;
            };

            let count = self.total_decisions_count.read();
            self.total_decisions_count.write(count + 1);

            self.emit(DecisionEvaluated {
                caller: get_caller_address(),
                state_hash,
                mode: 1,
                boundedness_bps,
            });

            best_idx
        }

        /// 3. `score` (Continuous Severity / Priority Rating)
        /// Computes real-time dynamic ratings (e.g. 0..3 scale) for Ekubo v2 dynamic swap fees
        /// and zkLend / Nostra collateral health factors.
        fn decide_score(
            ref self: ContractState,
            state_hash: felt252,
            risk_score_fp: i64,
            max_score: u64
        ) -> u64 {
            assert(self.seed_active.read() == 1, 'Werracle: Engine Paused');

            let risk_i128: i128 = risk_score_fp.into();
            let mut scaled_risk: i128 = (risk_i128 + (2 * WerrMath::ONE)) / 4;
            if scaled_risk < 0 {
                scaled_risk = 0;
            }
            if scaled_risk > WerrMath::ONE {
                scaled_risk = WerrMath::ONE;
            }

            let max_i128: i128 = max_score.into();
            let eval_i128: i128 = (scaled_risk * max_i128) / WerrMath::ONE;
            let evaluated_score: u64 = eval_i128.try_into().unwrap_or(0);

            let count = self.total_decisions_count.read();
            self.total_decisions_count.write(count + 1);

            self.emit(DecisionEvaluated {
                caller: get_caller_address(),
                state_hash,
                mode: 2,
                boundedness_bps: 5000,
            });

            evaluated_score
        }

        fn get_seed(self: @ContractState) -> (i64, i64, u64, u32, u16, u8, u8) {
            (
                self.seed_cx.read(),
                self.seed_cy.read(),
                self.seed_zoom.read(),
                self.seed_nonce.read(),
                self.seed_threshold.read(),
                self.seed_mode.read(),
                self.seed_active.read(),
            )
        }

        fn update_seed(
            ref self: ContractState,
            cx: i64,
            cy: i64,
            zoom: u64,
            threshold: u16,
            default_mode: u8,
            active_flag: u8
        ) {
            assert(get_caller_address() == self.owner.read(), 'Werracle: Not Owner');
            let next_nonce = self.seed_nonce.read() + 1;
            self.seed_cx.write(cx);
            self.seed_cy.write(cy);
            self.seed_zoom.write(zoom);
            self.seed_nonce.write(next_nonce);
            self.seed_threshold.write(threshold);
            self.seed_mode.write(default_mode);
            self.seed_active.write(active_flag);

            self.emit(SeedUpdated { cx, cy, zoom, nonce: next_nonce });
        }

        fn total_decisions_count(self: @ContractState) -> u64 {
            self.total_decisions_count.read()
        }

        fn owner(self: @ContractState) -> ContractAddress {
            self.owner.read()
        }
    }
}
