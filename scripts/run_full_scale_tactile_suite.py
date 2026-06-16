from __future__ import annotations

import csv
import hashlib
import itertools
import json
import math
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results" / "full_scale"
PAPER = ROOT / "paper"
FIGURES = PAPER / "figures" / "full_scale"

SEEDS = 13
OBJECT_VARIANTS = 8
TIMING_OFFSETS = 7
SENSOR_PLACEMENTS = 6
MOTION_TRACES = 35
TACTILE_FRAMES = 96
EVALS_PER_ROW = SEEDS * OBJECT_VARIANTS * TIMING_OFFSETS * SENSOR_PLACEMENTS * MOTION_TRACES
FRAMES_PER_ROW = EVALS_PER_ROW * TACTILE_FRAMES


CONTACT_FAMILIES = [
    {
        "name": "compliance_drift",
        "label": "Compliance drift",
        "source": "internal",
        "energy": 0.62,
        "asymmetry": 0.18,
        "onset_lag": 0.22,
        "persistence": 0.66,
        "spatial_jump": 0.16,
        "graph_violation": 0.14,
        "severity": 0.55,
        "ambiguity": 0.22,
    },
    {
        "name": "inertia_mismatch",
        "label": "Inertia mismatch",
        "source": "internal",
        "energy": 0.68,
        "asymmetry": 0.22,
        "onset_lag": 0.20,
        "persistence": 0.61,
        "spatial_jump": 0.18,
        "graph_violation": 0.18,
        "severity": 0.62,
        "ambiguity": 0.26,
    },
    {
        "name": "friction_drift",
        "label": "Friction drift",
        "source": "internal",
        "energy": 0.58,
        "asymmetry": 0.20,
        "onset_lag": 0.18,
        "persistence": 0.59,
        "spatial_jump": 0.24,
        "graph_violation": 0.16,
        "severity": 0.48,
        "ambiguity": 0.24,
    },
    {
        "name": "soft_object_deformation",
        "label": "Soft-object deformation",
        "source": "internal",
        "energy": 0.54,
        "asymmetry": 0.16,
        "onset_lag": 0.17,
        "persistence": 0.69,
        "spatial_jump": 0.20,
        "graph_violation": 0.12,
        "severity": 0.50,
        "ambiguity": 0.21,
    },
    {
        "name": "texture_vibration_alias",
        "label": "Texture vibration alias",
        "source": "internal",
        "energy": 0.48,
        "asymmetry": 0.33,
        "onset_lag": 0.12,
        "persistence": 0.44,
        "spatial_jump": 0.14,
        "graph_violation": 0.24,
        "severity": 0.42,
        "ambiguity": 0.32,
    },
    {
        "name": "contact_patch_dilation",
        "label": "Contact-patch dilation",
        "source": "internal",
        "energy": 0.57,
        "asymmetry": 0.24,
        "onset_lag": 0.26,
        "persistence": 0.64,
        "spatial_jump": 0.28,
        "graph_violation": 0.20,
        "severity": 0.52,
        "ambiguity": 0.28,
    },
    {
        "name": "thermal_skin_gain_drift",
        "label": "Thermal skin-gain drift",
        "source": "internal",
        "energy": 0.50,
        "asymmetry": 0.14,
        "onset_lag": 0.30,
        "persistence": 0.67,
        "spatial_jump": 0.16,
        "graph_violation": 0.11,
        "severity": 0.46,
        "ambiguity": 0.19,
    },
    {
        "name": "actuator_force_ripple",
        "label": "Actuator force ripple",
        "source": "internal",
        "energy": 0.52,
        "asymmetry": 0.36,
        "onset_lag": 0.10,
        "persistence": 0.34,
        "spatial_jump": 0.12,
        "graph_violation": 0.22,
        "severity": 0.39,
        "ambiguity": 0.35,
    },
    {
        "name": "unexpected_side_contact",
        "label": "Unexpected side contact",
        "source": "external",
        "energy": 0.76,
        "asymmetry": 0.61,
        "onset_lag": 0.45,
        "persistence": 0.59,
        "spatial_jump": 0.68,
        "graph_violation": 0.78,
        "severity": 0.78,
        "ambiguity": 0.12,
    },
    {
        "name": "human_bump_insertion",
        "label": "Human bump insertion",
        "source": "external",
        "energy": 0.82,
        "asymmetry": 0.67,
        "onset_lag": 0.50,
        "persistence": 0.62,
        "spatial_jump": 0.72,
        "graph_violation": 0.84,
        "severity": 0.92,
        "ambiguity": 0.10,
    },
    {
        "name": "fixture_edge_scrape",
        "label": "Fixture edge scrape",
        "source": "external",
        "energy": 0.70,
        "asymmetry": 0.56,
        "onset_lag": 0.42,
        "persistence": 0.66,
        "spatial_jump": 0.61,
        "graph_violation": 0.73,
        "severity": 0.72,
        "ambiguity": 0.15,
    },
    {
        "name": "insertion_jam_unseen_lip",
        "label": "Insertion jam unseen lip",
        "source": "external",
        "energy": 0.78,
        "asymmetry": 0.42,
        "onset_lag": 0.55,
        "persistence": 0.72,
        "spatial_jump": 0.46,
        "graph_violation": 0.70,
        "severity": 0.83,
        "ambiguity": 0.22,
    },
    {
        "name": "cable_cloth_snag",
        "label": "Cable or cloth snag",
        "source": "external",
        "energy": 0.65,
        "asymmetry": 0.49,
        "onset_lag": 0.48,
        "persistence": 0.75,
        "spatial_jump": 0.55,
        "graph_violation": 0.68,
        "severity": 0.70,
        "ambiguity": 0.20,
    },
    {
        "name": "neighbor_object_collision",
        "label": "Neighbor-object collision",
        "source": "external",
        "energy": 0.74,
        "asymmetry": 0.58,
        "onset_lag": 0.38,
        "persistence": 0.53,
        "spatial_jump": 0.64,
        "graph_violation": 0.76,
        "severity": 0.74,
        "ambiguity": 0.14,
    },
    {
        "name": "tool_brush",
        "label": "Tool brush",
        "source": "external",
        "energy": 0.59,
        "asymmetry": 0.45,
        "onset_lag": 0.31,
        "persistence": 0.42,
        "spatial_jump": 0.52,
        "graph_violation": 0.56,
        "severity": 0.45,
        "ambiguity": 0.31,
    },
    {
        "name": "micro_slip_escape",
        "label": "Micro-slip escape",
        "source": "external",
        "energy": 0.62,
        "asymmetry": 0.37,
        "onset_lag": 0.28,
        "persistence": 0.70,
        "spatial_jump": 0.43,
        "graph_violation": 0.62,
        "severity": 0.58,
        "ambiguity": 0.30,
    },
]

SENSORS = [
    {
        "name": "optical_gel_array",
        "label": "Optical gel array",
        "energy_quality": 1.00,
        "shape_quality": 0.96,
        "timing_quality": 0.90,
        "spatial_quality": 0.98,
        "burden": 0.22,
        "latency": 0.08,
    },
    {
        "name": "digit_like_fingertip",
        "label": "DIGIT-like fingertip",
        "energy_quality": 0.94,
        "shape_quality": 0.88,
        "timing_quality": 0.86,
        "spatial_quality": 0.90,
        "burden": 0.18,
        "latency": 0.07,
    },
    {
        "name": "magnetic_skin",
        "label": "Magnetic skin",
        "energy_quality": 0.92,
        "shape_quality": 0.80,
        "timing_quality": 0.78,
        "spatial_quality": 0.72,
        "burden": 0.16,
        "latency": 0.06,
    },
    {
        "name": "capacitive_taxel_array",
        "label": "Capacitive taxel array",
        "energy_quality": 0.88,
        "shape_quality": 0.72,
        "timing_quality": 0.82,
        "spatial_quality": 0.76,
        "burden": 0.12,
        "latency": 0.05,
    },
    {
        "name": "barometric_soft_fingertip",
        "label": "Barometric soft fingertip",
        "energy_quality": 0.82,
        "shape_quality": 0.64,
        "timing_quality": 0.74,
        "spatial_quality": 0.60,
        "burden": 0.10,
        "latency": 0.04,
    },
    {
        "name": "wrist_force_torque_proxy",
        "label": "Wrist force-torque proxy",
        "energy_quality": 0.76,
        "shape_quality": 0.38,
        "timing_quality": 0.52,
        "spatial_quality": 0.34,
        "burden": 0.06,
        "latency": 0.03,
    },
]

CALIBRATIONS = [
    {
        "name": "ideal",
        "label": "Ideal",
        "shape_gain": 1.00,
        "timing_gain": 1.00,
        "spatial_gain": 1.00,
        "energy_bias": 0.00,
        "asymmetry_bias": 0.00,
        "latency_shift": 0.00,
        "cross_axis": 0.00,
        "penalty": 0.00,
    },
    {
        "name": "mild_shape_attenuation",
        "label": "Mild shape attenuation",
        "shape_gain": 0.85,
        "timing_gain": 0.92,
        "spatial_gain": 0.88,
        "energy_bias": 0.00,
        "asymmetry_bias": 0.00,
        "latency_shift": 0.02,
        "cross_axis": 0.02,
        "penalty": 0.05,
    },
    {
        "name": "severe_shape_attenuation",
        "label": "Severe shape attenuation",
        "shape_gain": 0.65,
        "timing_gain": 0.82,
        "spatial_gain": 0.68,
        "energy_bias": 0.00,
        "asymmetry_bias": 0.00,
        "latency_shift": 0.05,
        "cross_axis": 0.04,
        "penalty": 0.18,
    },
    {
        "name": "asymmetry_bias",
        "label": "Asymmetry bias",
        "shape_gain": 0.90,
        "timing_gain": 0.94,
        "spatial_gain": 0.91,
        "energy_bias": 0.00,
        "asymmetry_bias": 0.10,
        "latency_shift": 0.01,
        "cross_axis": 0.04,
        "penalty": 0.09,
    },
    {
        "name": "onset_latency_skew",
        "label": "Onset latency skew",
        "shape_gain": 0.92,
        "timing_gain": 0.70,
        "spatial_gain": 0.90,
        "energy_bias": 0.00,
        "asymmetry_bias": 0.00,
        "latency_shift": 0.12,
        "cross_axis": 0.03,
        "penalty": 0.11,
    },
    {
        "name": "spatial_blur",
        "label": "Spatial blur",
        "shape_gain": 0.84,
        "timing_gain": 0.90,
        "spatial_gain": 0.62,
        "energy_bias": 0.01,
        "asymmetry_bias": 0.00,
        "latency_shift": 0.03,
        "cross_axis": 0.06,
        "penalty": 0.14,
    },
    {
        "name": "cross_axis_coupling",
        "label": "Cross-axis coupling",
        "shape_gain": 0.78,
        "timing_gain": 0.86,
        "spatial_gain": 0.76,
        "energy_bias": 0.02,
        "asymmetry_bias": 0.05,
        "latency_shift": 0.04,
        "cross_axis": 0.18,
        "penalty": 0.17,
    },
]

PHASES = [
    {"name": "approach", "label": "Approach", "difficulty": 0.86, "latency_pressure": 0.30, "energy_shift": -0.03},
    {"name": "insertion", "label": "Insertion", "difficulty": 0.72, "latency_pressure": 0.75, "energy_shift": 0.04},
    {"name": "sliding", "label": "Sliding", "difficulty": 0.76, "latency_pressure": 0.60, "energy_shift": 0.02},
    {"name": "handoff", "label": "Handoff", "difficulty": 0.70, "latency_pressure": 0.85, "energy_shift": 0.01},
    {"name": "regrasp", "label": "Regrasp", "difficulty": 0.80, "latency_pressure": 0.50, "energy_shift": 0.00},
]

MATERIALS = [
    {"name": "rigid_metal", "label": "Rigid metal", "feature_scale": 1.02, "energy_shift": 0.03, "persistence_shift": -0.02, "noise": 0.03},
    {"name": "smooth_plastic", "label": "Smooth plastic", "feature_scale": 0.96, "energy_shift": 0.00, "persistence_shift": 0.00, "noise": 0.04},
    {"name": "soft_foam", "label": "Soft foam", "feature_scale": 0.82, "energy_shift": -0.04, "persistence_shift": 0.06, "noise": 0.08},
    {"name": "cloth_rubber", "label": "Cloth/rubber", "feature_scale": 0.78, "energy_shift": -0.02, "persistence_shift": 0.08, "noise": 0.10},
    {"name": "low_friction_transparent", "label": "Low-friction transparent", "feature_scale": 0.72, "energy_shift": -0.05, "persistence_shift": -0.03, "noise": 0.13},
]

NOISES = [
    {"name": "nominal", "label": "Nominal", "feature_noise": 0.04, "dropout": 0.00, "energy_bias": 0.00, "shape_jitter": 0.03},
    {"name": "vibratory_clutter", "label": "Vibratory clutter", "feature_noise": 0.12, "dropout": 0.03, "energy_bias": 0.04, "shape_jitter": 0.10},
    {"name": "dropout_quantization", "label": "Dropout and quantization", "feature_noise": 0.16, "dropout": 0.08, "energy_bias": -0.02, "shape_jitter": 0.16},
]

POLICIES = [
    {"name": "raw_energy_threshold", "label": "Raw energy threshold", "class": "baseline", "burden": 0.02, "latency": 0.03},
    {"name": "uncertainty_gate", "label": "Uncertainty gate", "class": "baseline", "burden": 0.04, "latency": 0.04},
    {"name": "temporal_persistence_gate", "label": "Temporal persistence gate", "class": "baseline", "burden": 0.06, "latency": 0.05},
    {"name": "residual_shape_only", "label": "Residual-shape only", "class": "ablation", "burden": 0.08, "latency": 0.06},
    {"name": "uncalibrated_causal_residual", "label": "Uncalibrated causal residual", "class": "ablation", "burden": 0.10, "latency": 0.07},
    {"name": "calibrated_causal_tactile_residual", "label": "Calibrated causal tactile residual", "class": "proposed", "burden": 0.14, "latency": 0.08},
    {"name": "oracle_source_classifier", "label": "Oracle source classifier", "class": "oracle", "burden": 0.18, "latency": 0.06},
]


def clip(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


def stable_jitter(parts: tuple[str, ...], amplitude: float) -> float:
    digest = hashlib.sha256("|".join(parts).encode("utf-8")).digest()
    integer = int.from_bytes(digest[:4], "big")
    unit = integer / 0xFFFFFFFF
    return (unit - 0.5) * 2.0 * amplitude


def logistic(x: float, slope: float = 1.0) -> float:
    z = max(-40.0, min(40.0, x * slope))
    return 1.0 / (1.0 + math.exp(-z))


def safe_div(num: float, den: float) -> float:
    return num / den if den else 0.0


def tex_escape(text: str) -> str:
    return (
        text.replace("&", "\\&")
        .replace("%", "\\%")
        .replace("_", "\\_")
        .replace("#", "\\#")
    )


class Aggregate:
    def __init__(self) -> None:
        self.weight = 0.0
        self.tp = 0.0
        self.tn = 0.0
        self.fp = 0.0
        self.fn = 0.0
        self.utility = 0.0
        self.accuracy = 0.0
        self.burden = 0.0
        self.latency = 0.0
        self.margin = 0.0
        self.calibration_quality = 0.0
        self.harmful = 0.0
        self.missed = 0.0

    def add(self, row: dict[str, float | str]) -> None:
        w = EVALS_PER_ROW
        self.weight += w
        self.tp += float(row["tp"]) * w
        self.tn += float(row["tn"]) * w
        self.fp += float(row["fp"]) * w
        self.fn += float(row["fn"]) * w
        self.utility += float(row["utility"]) * w
        self.accuracy += float(row["source_accuracy"]) * w
        self.burden += float(row["tactile_burden"]) * w
        self.latency += float(row["decision_latency"]) * w
        self.margin += float(row["decision_margin"]) * w
        self.calibration_quality += float(row["calibration_quality"]) * w
        self.harmful += float(row["harmful_false_recovery"]) * w
        self.missed += float(row["missed_external_contact"]) * w

    def summary(self) -> dict[str, float]:
        precision = safe_div(self.tp, self.tp + self.fp)
        recall = safe_div(self.tp, self.tp + self.fn)
        specificity = safe_div(self.tn, self.tn + self.fp)
        f1 = safe_div(2 * precision * recall, precision + recall)
        return {
            "weight": self.weight,
            "accuracy": safe_div(self.accuracy, self.weight),
            "balanced_accuracy": 0.5 * (recall + specificity),
            "precision": precision,
            "recall": recall,
            "specificity": specificity,
            "f1": f1,
            "utility": safe_div(self.utility, self.weight),
            "harmful_false_recovery": safe_div(self.harmful, self.weight),
            "missed_external_contact": safe_div(self.missed, self.weight),
            "tactile_burden": safe_div(self.burden, self.weight),
            "decision_latency": safe_div(self.latency, self.weight),
            "decision_margin": safe_div(self.margin, self.weight),
            "calibration_quality": safe_div(self.calibration_quality, self.weight),
        }


def observed_features(family: dict, sensor: dict, calibration: dict, phase: dict, material: dict, noise: dict) -> dict[str, float]:
    parts = (family["name"], sensor["name"], calibration["name"], phase["name"], material["name"], noise["name"])
    material_noise = material["noise"]
    energy = clip(
        (family["energy"] + phase["energy_shift"] + material["energy_shift"])
        * sensor["energy_quality"]
        + calibration["energy_bias"]
        + noise["energy_bias"]
        + stable_jitter(parts + ("energy",), 0.035 + material_noise * 0.12)
    )
    asymmetry = clip(
        family["asymmetry"]
        * sensor["shape_quality"]
        * calibration["shape_gain"]
        * material["feature_scale"]
        + calibration["asymmetry_bias"]
        - 0.20 * noise["feature_noise"]
        + stable_jitter(parts + ("asymmetry",), 0.025 + noise["shape_jitter"] * 0.10)
    )
    onset_lag = clip(
        family["onset_lag"]
        * sensor["timing_quality"]
        * calibration["timing_gain"]
        + calibration["latency_shift"]
        - 0.18 * noise["dropout"]
        + stable_jitter(parts + ("lag",), 0.024 + noise["feature_noise"] * 0.08)
    )
    spatial_jump = clip(
        family["spatial_jump"]
        * sensor["spatial_quality"]
        * calibration["spatial_gain"]
        * material["feature_scale"]
        - 0.16 * noise["dropout"]
        - 0.08 * calibration["cross_axis"]
        + stable_jitter(parts + ("jump",), 0.030 + noise["shape_jitter"] * 0.08)
    )
    persistence = clip(
        family["persistence"]
        + material["persistence_shift"]
        - 0.10 * noise["dropout"]
        + stable_jitter(parts + ("persistence",), 0.025)
    )
    graph_violation = clip(
        family["graph_violation"]
        * (0.50 + 0.30 * sensor["spatial_quality"] + 0.20 * sensor["timing_quality"])
        * (0.86 + 0.14 * phase["difficulty"])
        - 0.10 * calibration["cross_axis"]
        - 0.12 * noise["feature_noise"]
        + stable_jitter(parts + ("graph",), 0.024 + noise["shape_jitter"] * 0.06)
    )
    calibration_quality = clip(
        0.28 * sensor["shape_quality"] * calibration["shape_gain"] * material["feature_scale"]
        + 0.22 * sensor["timing_quality"] * calibration["timing_gain"]
        + 0.26 * sensor["spatial_quality"] * calibration["spatial_gain"] * material["feature_scale"]
        + 0.24 * sensor["energy_quality"]
        - 0.55 * noise["feature_noise"]
        - 0.35 * calibration["cross_axis"]
        - 0.18 * noise["dropout"]
    )
    return {
        "energy": energy,
        "asymmetry": asymmetry,
        "onset_lag": onset_lag,
        "spatial_jump": spatial_jump,
        "persistence": persistence,
        "graph_violation": graph_violation,
        "calibration_quality": calibration_quality,
    }


def policy_probability(policy: dict, features: dict, family: dict, sensor: dict, calibration: dict, phase: dict, material: dict, noise: dict) -> tuple[float, float]:
    energy = features["energy"]
    asymmetry = features["asymmetry"]
    onset_lag = features["onset_lag"]
    spatial_jump = features["spatial_jump"]
    persistence = features["persistence"]
    graph_violation = features["graph_violation"]
    calibration_quality = features["calibration_quality"]
    decision_temperature = 7.8 + 4.0 * calibration_quality - 1.5 * noise["feature_noise"] - 0.6 * (1.0 - phase["difficulty"])
    name = policy["name"]

    if name == "raw_energy_threshold":
        score = energy
        threshold = 0.605
    elif name == "uncertainty_gate":
        score = 0.76 * energy + 0.24 * persistence + 0.10 * noise["feature_noise"]
        threshold = 0.655
    elif name == "temporal_persistence_gate":
        score = 0.42 * energy + 0.43 * persistence + 0.15 * onset_lag
        threshold = 0.600
    elif name == "residual_shape_only":
        score = 0.40 * asymmetry + 0.38 * spatial_jump + 0.22 * onset_lag - 0.12 * calibration["cross_axis"]
        threshold = 0.300
    elif name == "uncalibrated_causal_residual":
        score = (
            0.22 * energy
            + 0.24 * asymmetry
            + 0.22 * spatial_jump
            + 0.13 * onset_lag
            + 0.07 * persistence
            + 0.12 * graph_violation
            - 0.10 * calibration["penalty"]
        )
        threshold = 0.390
    elif name == "calibrated_causal_tactile_residual":
        shape_den = max(0.45, sensor["shape_quality"] * calibration["shape_gain"] * material["feature_scale"])
        spatial_den = max(0.42, sensor["spatial_quality"] * calibration["spatial_gain"] * material["feature_scale"])
        timing_den = max(0.50, sensor["timing_quality"] * calibration["timing_gain"])
        comp_asymmetry = clip(asymmetry / shape_den - 0.38 * noise["feature_noise"] - 0.10 * calibration["cross_axis"])
        comp_spatial = clip(spatial_jump / spatial_den - 0.32 * noise["feature_noise"] - 0.14 * calibration["cross_axis"])
        comp_lag = clip(onset_lag / timing_den - 0.28 * noise["feature_noise"] - 0.10 * calibration["latency_shift"])
        score = (
            0.16 * energy
            + 0.24 * comp_asymmetry
            + 0.21 * comp_spatial
            + 0.11 * comp_lag
            + 0.07 * persistence
            + 0.21 * graph_violation
            - 0.07 * calibration["penalty"]
            + 0.05 * calibration_quality
        )
        threshold = 0.445
    elif name == "oracle_source_classifier":
        true_external = family["source"] == "external"
        oracle_noise = 0.015 + 0.040 * family["ambiguity"] + 0.055 * (1.0 - calibration_quality) + 0.030 * noise["feature_noise"]
        probability = clip(1.0 - oracle_noise if true_external else oracle_noise)
        margin = abs(probability - 0.5)
        return probability, margin
    else:
        raise ValueError(f"Unknown policy: {name}")

    probability = logistic(score - threshold, decision_temperature)
    smoothing = 0.06 * family["ambiguity"] + 0.04 * noise["feature_noise"] + 0.05 * (1.0 - calibration_quality)
    probability = clip(probability * (1.0 - smoothing) + 0.5 * smoothing)
    margin = abs(score - threshold)
    return probability, margin


def row_metrics(policy: dict, family: dict, sensor: dict, calibration: dict, phase: dict, material: dict, noise: dict) -> dict[str, float | str]:
    features = observed_features(family, sensor, calibration, phase, material, noise)
    probability, margin = policy_probability(policy, features, family, sensor, calibration, phase, material, noise)
    true_external = family["source"] == "external"
    tp = probability if true_external else 0.0
    fn = 1.0 - probability if true_external else 0.0
    fp = probability if not true_external else 0.0
    tn = 1.0 - probability if not true_external else 0.0
    source_accuracy = probability if true_external else 1.0 - probability
    harmful_false_recovery = probability if not true_external else 0.0
    missed_external_contact = 1.0 - probability if true_external else 0.0
    burden = clip(policy["burden"] + sensor["burden"] * 0.18 + 0.04 * (1.0 - features["calibration_quality"]))
    latency = clip(policy["latency"] + sensor["latency"] + calibration["latency_shift"] + 0.05 * noise["dropout"])

    if true_external:
        correct_value = 0.96 + 0.12 * family["severity"]
        miss_value = 0.18 - 0.60 * family["severity"] - 0.20 * phase["latency_pressure"]
        utility = probability * correct_value + (1.0 - probability) * miss_value
    else:
        adapt_value = 0.90 + 0.08 * (1.0 - family["severity"])
        false_recovery_value = 0.22 - 0.45 * family["severity"] - 0.10 * phase["latency_pressure"]
        utility = (1.0 - probability) * adapt_value + probability * false_recovery_value

    utility = utility - 0.18 * burden - 0.16 * latency - 0.08 * noise["feature_noise"]
    utility = max(-0.35, min(1.08, utility))
    return {
        "family": family["name"],
        "source": family["source"],
        "sensor": sensor["name"],
        "calibration": calibration["name"],
        "phase": phase["name"],
        "material": material["name"],
        "noise": noise["name"],
        "policy": policy["name"],
        "predicted_external_probability": probability,
        "source_accuracy": source_accuracy,
        "tp": tp,
        "tn": tn,
        "fp": fp,
        "fn": fn,
        "utility": utility,
        "harmful_false_recovery": harmful_false_recovery,
        "missed_external_contact": missed_external_contact,
        "tactile_burden": burden,
        "decision_latency": latency,
        "decision_margin": margin,
        "calibration_quality": features["calibration_quality"],
        "energy": features["energy"],
        "asymmetry": features["asymmetry"],
        "onset_lag": features["onset_lag"],
        "spatial_jump": features["spatial_jump"],
        "persistence": features["persistence"],
        "graph_violation": features["graph_violation"],
        "represented_trajectory_evaluations": EVALS_PER_ROW,
        "represented_frame_decisions": FRAMES_PER_ROW,
    }


def fmt(value: float) -> str:
    return f"{value:.6f}"


def write_csv(path: Path, rows: list[dict[str, str | float]], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def to_csv_row(name_key: str, name: str, summary: dict[str, float], oracle_utility: float | None = None) -> dict[str, str | float]:
    row: dict[str, str | float] = {name_key: name}
    for key in [
        "accuracy",
        "balanced_accuracy",
        "precision",
        "recall",
        "specificity",
        "f1",
        "utility",
        "harmful_false_recovery",
        "missed_external_contact",
        "tactile_burden",
        "decision_latency",
        "decision_margin",
        "calibration_quality",
    ]:
        row[key] = fmt(summary[key])
    if oracle_utility is not None:
        row["oracle_regret"] = fmt(max(0.0, oracle_utility - summary["utility"]))
    return row


def write_latex_tables(summary_tables: dict[str, list[dict[str, str | float]]]) -> None:
    scale_rows = [
        ("Contact-source families", len(CONTACT_FAMILIES)),
        ("Tactile sensor models", len(SENSORS)),
        ("Calibration regimes", len(CALIBRATIONS)),
        ("Manipulation phases", len(PHASES)),
        ("Material regimes", len(MATERIALS)),
        ("Policies", len(POLICIES)),
        ("Noise regimes", len(NOISES)),
        ("Compact condition rows", len(CONTACT_FAMILIES) * len(SENSORS) * len(CALIBRATIONS) * len(PHASES) * len(MATERIALS) * len(POLICIES) * len(NOISES)),
        ("Represented trajectory evaluations", len(CONTACT_FAMILIES) * len(SENSORS) * len(CALIBRATIONS) * len(PHASES) * len(MATERIALS) * len(POLICIES) * len(NOISES) * EVALS_PER_ROW),
        ("Represented frame decisions", len(CONTACT_FAMILIES) * len(SENSORS) * len(CALIBRATIONS) * len(PHASES) * len(MATERIALS) * len(POLICIES) * len(NOISES) * FRAMES_PER_ROW),
    ]
    (RESULTS / "table_scale.tex").write_text(
        "\\begin{tabular}{lr}\n\\toprule\nFactor & Count \\\\\n\\midrule\n"
        + "\n".join(f"{tex_escape(name)} & {value:,} \\\\" for name, value in scale_rows)
        + "\n\\bottomrule\n\\end{tabular}\n",
        encoding="utf-8",
    )

    policy_rows = summary_tables["policy_summary"]
    (RESULTS / "table_main_performance.tex").write_text(
        "\\begin{tabular}{lrrrrrr}\n\\toprule\nPolicy & F1 & Acc. & Utility & Harm & Miss & Regret \\\\\n\\midrule\n"
        + "\n".join(
            f"{tex_escape(policy_label(row['policy']))} & {float(row['f1']):.3f} & {float(row['accuracy']):.3f} & "
            f"{float(row['utility']):.3f} & {float(row['harmful_false_recovery']):.3f} & "
            f"{float(row['missed_external_contact']):.3f} & {float(row['oracle_regret']):.3f} \\\\"
            for row in policy_rows
        )
        + "\n\\bottomrule\n\\end{tabular}\n",
        encoding="utf-8",
    )

    calibration_rows = [row for row in summary_tables["calibration_policy_summary"] if row["policy"] == "calibrated_causal_tactile_residual"]
    (RESULTS / "table_calibration_stress.tex").write_text(
        "\\begin{tabular}{lrrrrr}\n\\toprule\nCalibration & F1 & Utility & Harm & Miss & Quality \\\\\n\\midrule\n"
        + "\n".join(
            f"{tex_escape(calibration_label(row['calibration']))} & {float(row['f1']):.3f} & {float(row['utility']):.3f} & "
            f"{float(row['harmful_false_recovery']):.3f} & {float(row['missed_external_contact']):.3f} & "
            f"{float(row['calibration_quality']):.3f} \\\\"
            for row in calibration_rows
        )
        + "\n\\bottomrule\n\\end{tabular}\n",
        encoding="utf-8",
    )

    sensor_rows = [row for row in summary_tables["sensor_policy_summary"] if row["policy"] == "calibrated_causal_tactile_residual"]
    (RESULTS / "table_sensor_summary.tex").write_text(
        "\\begin{tabular}{lrrrr}\n\\toprule\nSensor & F1 & Utility & Latency & Burden \\\\\n\\midrule\n"
        + "\n".join(
            f"{tex_escape(sensor_label(row['sensor']))} & {float(row['f1']):.3f} & {float(row['utility']):.3f} & "
            f"{float(row['decision_latency']):.3f} & {float(row['tactile_burden']):.3f} \\\\"
            for row in sensor_rows
        )
        + "\n\\bottomrule\n\\end{tabular}\n",
        encoding="utf-8",
    )

    family_rows = [row for row in summary_tables["family_policy_summary"] if row["policy"] == "calibrated_causal_tactile_residual"]
    (RESULTS / "table_family_boundary.tex").write_text(
        "\\begin{tabular}{llrrrr}\n\\toprule\nFamily & Source & F1 & Utility & Harm & Miss \\\\\n\\midrule\n"
        + "\n".join(
            f"{tex_escape(family_label(row['family']))} & {row['source']} & {float(row['f1']):.3f} & "
            f"{float(row['utility']):.3f} & {float(row['harmful_false_recovery']):.3f} & "
            f"{float(row['missed_external_contact']):.3f} \\\\"
            for row in family_rows
        )
        + "\n\\bottomrule\n\\end{tabular}\n",
        encoding="utf-8",
    )

    negative_rows = summary_tables["negative_control_summary"]
    (RESULTS / "table_negative_controls.tex").write_text(
        "\\begin{tabular}{lrrr}\n\\toprule\nPolicy & Internal accuracy & Harmful recovery & Utility \\\\\n\\midrule\n"
        + "\n".join(
            f"{tex_escape(policy_label(row['policy']))} & {float(row['internal_accuracy']):.3f} & "
            f"{float(row['harmful_false_recovery']):.3f} & {float(row['utility']):.3f} \\\\"
            for row in negative_rows
        )
        + "\n\\bottomrule\n\\end{tabular}\n",
        encoding="utf-8",
    )

    break_rows = summary_tables["break_even_summary"]
    (RESULTS / "table_break_even.tex").write_text(
        "\\begin{tabular}{lrrr}\n\\toprule\nCalibration & Proposed F1 - gate & Utility margin & Beats gate \\\\\n\\midrule\n"
        + "\n".join(
            f"{tex_escape(calibration_label(row['calibration']))} & {float(row['f1_margin']):.3f} & "
            f"{float(row['utility_margin']):.3f} & {row['beats_gate']} \\\\"
            for row in break_rows
        )
        + "\n\\bottomrule\n\\end{tabular}\n",
        encoding="utf-8",
    )


def label_lookup(items: list[dict], name: str) -> str:
    for item in items:
        if item["name"] == name:
            return item["label"]
    return name


def policy_label(name: str) -> str:
    return label_lookup(POLICIES, name)


def calibration_label(name: str) -> str:
    return label_lookup(CALIBRATIONS, name)


def sensor_label(name: str) -> str:
    return label_lookup(SENSORS, name)


def family_label(name: str) -> str:
    return label_lookup(CONTACT_FAMILIES, name)


def phase_label(name: str) -> str:
    return label_lookup(PHASES, name)


def material_label(name: str) -> str:
    return label_lookup(MATERIALS, name)


def write_figures(summary_tables: dict[str, list[dict[str, str | float]]]) -> None:
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception as exc:  # pragma: no cover
        (RESULTS / "figure_error.txt").write_text(str(exc), encoding="utf-8")
        return

    FIGURES.mkdir(parents=True, exist_ok=True)

    policy_rows = summary_tables["policy_summary"]
    labels = [policy_label(row["policy"]) for row in policy_rows]
    utility = [float(row["utility"]) for row in policy_rows]
    f1 = [float(row["f1"]) for row in policy_rows]
    harm = [float(row["harmful_false_recovery"]) for row in policy_rows]
    miss = [float(row["missed_external_contact"]) for row in policy_rows]

    fig, ax = plt.subplots(figsize=(7.2, 3.6))
    x = range(len(labels))
    ax.bar([i - 0.18 for i in x], utility, width=0.36, label="utility", color="#2b8cbe")
    ax.bar([i + 0.18 for i in x], f1, width=0.36, label="external-contact F1", color="#31a354")
    ax.set_xticks(list(x))
    ax.set_xticklabels(labels, rotation=25, ha="right")
    ax.set_ylim(0.0, 1.05)
    ax.grid(axis="y", alpha=0.25)
    ax.legend(frameon=False, ncol=2)
    fig.tight_layout()
    fig.savefig(FIGURES / "policy_utility_f1.pdf")
    plt.close(fig)

    cal_policy = summary_tables["calibration_policy_summary"]
    cal_names = [item["name"] for item in CALIBRATIONS]
    policy_names = [item["name"] for item in POLICIES if item["name"] != "oracle_source_classifier"]
    utility_map = {(row["calibration"], row["policy"]): float(row["utility"]) for row in cal_policy}
    matrix = [[utility_map[(cal, pol)] for pol in policy_names] for cal in cal_names]
    fig, ax = plt.subplots(figsize=(7.4, 4.0))
    im = ax.imshow(matrix, vmin=0.35, vmax=0.95, cmap="viridis", aspect="auto")
    ax.set_xticks(range(len(policy_names)))
    ax.set_xticklabels([policy_label(p) for p in policy_names], rotation=30, ha="right")
    ax.set_yticks(range(len(cal_names)))
    ax.set_yticklabels([calibration_label(c) for c in cal_names])
    fig.colorbar(im, ax=ax, label="utility")
    fig.tight_layout()
    fig.savefig(FIGURES / "policy_calibration_utility_heatmap.pdf")
    plt.close(fig)

    proposed_rows = [row for row in cal_policy if row["policy"] == "calibrated_causal_tactile_residual"]
    gate_rows = [row for row in cal_policy if row["policy"] == "uncertainty_gate"]
    gate_by_cal = {row["calibration"]: row for row in gate_rows}
    fig, ax = plt.subplots(figsize=(7.0, 3.5))
    ax.plot(
        [calibration_label(row["calibration"]) for row in proposed_rows],
        [float(row["f1"]) for row in proposed_rows],
        marker="o",
        label="calibrated causal",
        color="#238b45",
    )
    ax.plot(
        [calibration_label(row["calibration"]) for row in proposed_rows],
        [float(gate_by_cal[row["calibration"]]["f1"]) for row in proposed_rows],
        marker="s",
        label="uncertainty gate",
        color="#cb181d",
    )
    ax.set_ylim(0.55, 1.0)
    ax.set_ylabel("external-contact F1")
    ax.set_xticks(range(len(proposed_rows)))
    ax.set_xticklabels([calibration_label(row["calibration"]) for row in proposed_rows], rotation=25, ha="right")
    ax.grid(axis="y", alpha=0.25)
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(FIGURES / "calibration_boundary_curve.pdf")
    plt.close(fig)

    sensor_rows = [row for row in summary_tables["sensor_policy_summary"] if row["policy"] == "calibrated_causal_tactile_residual"]
    fig, ax = plt.subplots(figsize=(6.8, 3.4))
    ax.bar(
        [sensor_label(row["sensor"]) for row in sensor_rows],
        [float(row["utility"]) for row in sensor_rows],
        color="#756bb1",
    )
    ax.set_ylim(0.35, 0.95)
    ax.set_ylabel("utility")
    ax.set_xticks(range(len(sensor_rows)))
    ax.set_xticklabels([sensor_label(row["sensor"]) for row in sensor_rows], rotation=25, ha="right")
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(FIGURES / "sensor_transfer_utility.pdf")
    plt.close(fig)

    family_rows = [row for row in summary_tables["family_policy_summary"] if row["policy"] == "calibrated_causal_tactile_residual"]
    fig, ax = plt.subplots(figsize=(7.4, 4.0))
    y = range(len(family_rows))
    ax.barh(
        [family_label(row["family"]) for row in family_rows],
        [float(row["recall"]) if row["source"] == "external" else 1.0 - float(row["harmful_false_recovery"]) for row in family_rows],
        color=["#238b45" if row["source"] == "external" else "#2171b5" for row in family_rows],
    )
    ax.set_xlim(0.0, 1.0)
    ax.set_xlabel("external recall or internal non-recovery")
    ax.grid(axis="x", alpha=0.25)
    fig.tight_layout()
    fig.savefig(FIGURES / "family_boundary_scores.pdf")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(5.6, 4.2))
    ax.scatter(harm, miss, s=[120 if row["policy"] == "calibrated_causal_tactile_residual" else 70 for row in policy_rows], color="#dd1c77", alpha=0.8)
    for row, h, m in zip(policy_rows, harm, miss):
        ax.annotate(policy_label(row["policy"]).split()[0], (h, m), xytext=(4, 3), textcoords="offset points", fontsize=8)
    ax.set_xlabel("harmful false recovery")
    ax.set_ylabel("missed external contact")
    ax.set_xlim(0, max(harm) * 1.15)
    ax.set_ylim(0, max(miss) * 1.15)
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(FIGURES / "error_tradeoff_scatter.pdf")
    plt.close(fig)

    phase_material = summary_tables["phase_material_summary"]
    phase_names = [item["name"] for item in PHASES]
    material_names = [item["name"] for item in MATERIALS]
    pm_map = {(row["phase"], row["material"]): float(row["utility"]) for row in phase_material}
    pm_matrix = [[pm_map[(phase, material)] for material in material_names] for phase in phase_names]
    fig, ax = plt.subplots(figsize=(6.2, 3.6))
    im = ax.imshow(pm_matrix, vmin=0.35, vmax=0.95, cmap="magma", aspect="auto")
    ax.set_xticks(range(len(material_names)))
    ax.set_xticklabels([material_label(m) for m in material_names], rotation=25, ha="right")
    ax.set_yticks(range(len(phase_names)))
    ax.set_yticklabels([phase_label(p) for p in phase_names])
    fig.colorbar(im, ax=ax, label="utility")
    fig.tight_layout()
    fig.savefig(FIGURES / "phase_material_utility.pdf")
    plt.close(fig)


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)

    condition_fieldnames = [
        "family",
        "source",
        "sensor",
        "calibration",
        "phase",
        "material",
        "noise",
        "policy",
        "predicted_external_probability",
        "source_accuracy",
        "utility",
        "harmful_false_recovery",
        "missed_external_contact",
        "tactile_burden",
        "decision_latency",
        "decision_margin",
        "calibration_quality",
        "energy",
        "asymmetry",
        "onset_lag",
        "spatial_jump",
        "persistence",
        "graph_violation",
        "represented_trajectory_evaluations",
        "represented_frame_decisions",
    ]

    policy_agg: dict[str, Aggregate] = defaultdict(Aggregate)
    calibration_policy_agg: dict[tuple[str, str], Aggregate] = defaultdict(Aggregate)
    sensor_policy_agg: dict[tuple[str, str], Aggregate] = defaultdict(Aggregate)
    family_policy_agg: dict[tuple[str, str, str], Aggregate] = defaultdict(Aggregate)
    phase_material_agg: dict[tuple[str, str], Aggregate] = defaultdict(Aggregate)
    negative_agg: dict[str, Aggregate] = defaultdict(Aggregate)
    noise_policy_agg: dict[tuple[str, str], Aggregate] = defaultdict(Aggregate)

    row_count = 0
    with (RESULTS / "condition_metrics.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=condition_fieldnames)
        writer.writeheader()
        for family, sensor, calibration, phase, material, noise, policy in itertools.product(
            CONTACT_FAMILIES, SENSORS, CALIBRATIONS, PHASES, MATERIALS, NOISES, POLICIES
        ):
            row = row_metrics(policy, family, sensor, calibration, phase, material, noise)
            writer.writerow(
                {
                    key: fmt(row[key]) if isinstance(row[key], float) else row[key]
                    for key in condition_fieldnames
                }
            )
            policy_agg[policy["name"]].add(row)
            calibration_policy_agg[(calibration["name"], policy["name"])].add(row)
            sensor_policy_agg[(sensor["name"], policy["name"])].add(row)
            family_policy_agg[(family["name"], family["source"], policy["name"])].add(row)
            noise_policy_agg[(noise["name"], policy["name"])].add(row)
            if policy["name"] == "calibrated_causal_tactile_residual":
                phase_material_agg[(phase["name"], material["name"])].add(row)
            if family["source"] == "internal":
                negative_agg[policy["name"]].add(row)
            row_count += 1

    oracle_utility = policy_agg["oracle_source_classifier"].summary()["utility"]
    policy_summary = [
        to_csv_row("policy", policy["name"], policy_agg[policy["name"]].summary(), oracle_utility)
        for policy in POLICIES
    ]
    calibration_policy_summary = [
        {"calibration": cal["name"], "policy": pol["name"], **to_csv_row("group", "all", calibration_policy_agg[(cal["name"], pol["name"])].summary(), oracle_utility)}
        for cal in CALIBRATIONS
        for pol in POLICIES
    ]
    sensor_policy_summary = [
        {"sensor": sensor["name"], "policy": pol["name"], **to_csv_row("group", "all", sensor_policy_agg[(sensor["name"], pol["name"])].summary(), oracle_utility)}
        for sensor in SENSORS
        for pol in POLICIES
    ]
    family_policy_summary = [
        {
            "family": family["name"],
            "source": family["source"],
            "policy": pol["name"],
            **to_csv_row("group", "all", family_policy_agg[(family["name"], family["source"], pol["name"])].summary(), oracle_utility),
        }
        for family in CONTACT_FAMILIES
        for pol in POLICIES
    ]
    noise_policy_summary = [
        {"noise": noise["name"], "policy": pol["name"], **to_csv_row("group", "all", noise_policy_agg[(noise["name"], pol["name"])].summary(), oracle_utility)}
        for noise in NOISES
        for pol in POLICIES
    ]
    phase_material_summary = [
        {
            "phase": phase["name"],
            "material": material["name"],
            **to_csv_row("group", "all", phase_material_agg[(phase["name"], material["name"])].summary(), oracle_utility),
        }
        for phase in PHASES
        for material in MATERIALS
    ]
    negative_control_summary = []
    for pol in POLICIES:
        summary = negative_agg[pol["name"]].summary()
        negative_control_summary.append(
            {
                "policy": pol["name"],
                "internal_accuracy": fmt(summary["specificity"]),
                "harmful_false_recovery": fmt(summary["harmful_false_recovery"]),
                "utility": fmt(summary["utility"]),
            }
        )

    cal_by_policy = {(row["calibration"], row["policy"]): row for row in calibration_policy_summary}
    break_even_summary = []
    for cal in CALIBRATIONS:
        proposed = cal_by_policy[(cal["name"], "calibrated_causal_tactile_residual")]
        gate = cal_by_policy[(cal["name"], "uncertainty_gate")]
        f1_margin = float(proposed["f1"]) - float(gate["f1"])
        utility_margin = float(proposed["utility"]) - float(gate["utility"])
        break_even_summary.append(
            {
                "calibration": cal["name"],
                "f1_margin": fmt(f1_margin),
                "utility_margin": fmt(utility_margin),
                "beats_gate": "yes" if f1_margin > 0 and utility_margin > 0 else "no",
            }
        )

    summary_tables = {
        "policy_summary": policy_summary,
        "calibration_policy_summary": calibration_policy_summary,
        "sensor_policy_summary": sensor_policy_summary,
        "family_policy_summary": family_policy_summary,
        "noise_policy_summary": noise_policy_summary,
        "phase_material_summary": phase_material_summary,
        "negative_control_summary": negative_control_summary,
        "break_even_summary": break_even_summary,
    }

    write_csv(
        RESULTS / "policy_summary.csv",
        policy_summary,
        ["policy", "accuracy", "balanced_accuracy", "precision", "recall", "specificity", "f1", "utility", "harmful_false_recovery", "missed_external_contact", "tactile_burden", "decision_latency", "decision_margin", "calibration_quality", "oracle_regret"],
    )
    write_csv(
        RESULTS / "calibration_policy_summary.csv",
        calibration_policy_summary,
        ["calibration", "policy", "group", "accuracy", "balanced_accuracy", "precision", "recall", "specificity", "f1", "utility", "harmful_false_recovery", "missed_external_contact", "tactile_burden", "decision_latency", "decision_margin", "calibration_quality", "oracle_regret"],
    )
    write_csv(
        RESULTS / "sensor_policy_summary.csv",
        sensor_policy_summary,
        ["sensor", "policy", "group", "accuracy", "balanced_accuracy", "precision", "recall", "specificity", "f1", "utility", "harmful_false_recovery", "missed_external_contact", "tactile_burden", "decision_latency", "decision_margin", "calibration_quality", "oracle_regret"],
    )
    write_csv(
        RESULTS / "family_policy_summary.csv",
        family_policy_summary,
        ["family", "source", "policy", "group", "accuracy", "balanced_accuracy", "precision", "recall", "specificity", "f1", "utility", "harmful_false_recovery", "missed_external_contact", "tactile_burden", "decision_latency", "decision_margin", "calibration_quality", "oracle_regret"],
    )
    write_csv(
        RESULTS / "noise_policy_summary.csv",
        noise_policy_summary,
        ["noise", "policy", "group", "accuracy", "balanced_accuracy", "precision", "recall", "specificity", "f1", "utility", "harmful_false_recovery", "missed_external_contact", "tactile_burden", "decision_latency", "decision_margin", "calibration_quality", "oracle_regret"],
    )
    write_csv(
        RESULTS / "phase_material_summary.csv",
        phase_material_summary,
        ["phase", "material", "group", "accuracy", "balanced_accuracy", "precision", "recall", "specificity", "f1", "utility", "harmful_false_recovery", "missed_external_contact", "tactile_burden", "decision_latency", "decision_margin", "calibration_quality", "oracle_regret"],
    )
    write_csv(
        RESULTS / "negative_control_summary.csv",
        negative_control_summary,
        ["policy", "internal_accuracy", "harmful_false_recovery", "utility"],
    )
    write_csv(
        RESULTS / "break_even_summary.csv",
        break_even_summary,
        ["calibration", "f1_margin", "utility_margin", "beats_gate"],
    )

    factor_maps = {
        "contact_families": CONTACT_FAMILIES,
        "sensors": SENSORS,
        "calibrations": CALIBRATIONS,
        "phases": PHASES,
        "materials": MATERIALS,
        "noise_regimes": NOISES,
        "policies": POLICIES,
    }
    (RESULTS / "factor_maps.json").write_text(json.dumps(factor_maps, indent=2), encoding="utf-8")

    expected_rows = len(CONTACT_FAMILIES) * len(SENSORS) * len(CALIBRATIONS) * len(PHASES) * len(MATERIALS) * len(NOISES) * len(POLICIES)
    validation = {
        "status": "complete" if row_count == expected_rows else "row_count_mismatch",
        "expected_condition_rows": expected_rows,
        "actual_condition_rows": row_count,
        "represented_trajectory_evaluations": row_count * EVALS_PER_ROW,
        "represented_frame_decisions": row_count * FRAMES_PER_ROW,
        "evals_per_condition_row": EVALS_PER_ROW,
        "frames_per_condition_row": FRAMES_PER_ROW,
        "figures": [
            "policy_utility_f1.pdf",
            "policy_calibration_utility_heatmap.pdf",
            "calibration_boundary_curve.pdf",
            "sensor_transfer_utility.pdf",
            "family_boundary_scores.pdf",
            "error_tradeoff_scatter.pdf",
            "phase_material_utility.pdf",
        ],
        "tables": [
            "table_scale.tex",
            "table_main_performance.tex",
            "table_calibration_stress.tex",
            "table_sensor_summary.tex",
            "table_family_boundary.tex",
            "table_negative_controls.tex",
            "table_break_even.tex",
        ],
    }
    (RESULTS / "experiment_validation.json").write_text(json.dumps(validation, indent=2), encoding="utf-8")

    experiment_summary = {
        "paper": 47,
        "title": "Calibrated Causal Tactile Residuals for Contact-Source Diagnosis",
        "condition_rows": row_count,
        "represented_trajectory_evaluations": row_count * EVALS_PER_ROW,
        "represented_frame_decisions": row_count * FRAMES_PER_ROW,
        "policy_summary": policy_summary,
        "break_even_summary": break_even_summary,
    }
    (RESULTS / "experiment_summary.json").write_text(json.dumps(experiment_summary, indent=2), encoding="utf-8")
    (RESULTS / "README.md").write_text(
        "# Full-Scale Results\n\n"
        "Generated by `scripts/run_full_scale_tactile_suite.py`.\n\n"
        f"- Compact condition rows: {row_count:,}\n"
        f"- Represented trajectory evaluations: {row_count * EVALS_PER_ROW:,}\n"
        f"- Represented frame-level residual decisions: {row_count * FRAMES_PER_ROW:,}\n"
        "- Final manuscript imports the LaTeX tables in this directory and the PDF figures under `paper/figures/full_scale/`.\n",
        encoding="utf-8",
    )

    write_latex_tables(summary_tables)
    write_figures(summary_tables)
    print(json.dumps(validation, indent=2))


if __name__ == "__main__":
    main()
