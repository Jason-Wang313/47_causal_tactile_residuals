import csv
import json

from recover_paper47 import DOCS, PAPER, make_cases, metrics


GAINS = [1.0, 0.8, 0.7, 0.6, 0.5]
SHAPE_FEATURES = ["asymmetry", "onset_lag", "spatial_jump"]


def causal_score(row):
    return (
        0.35 * row["energy"]
        + 0.30 * row["asymmetry"]
        + 0.18 * row["spatial_jump"]
        + 0.12 * row["onset_lag"]
        - 0.18 * (1.0 - row["persistence"])
    )


def rescore(row):
    out = dict(row)
    out["raw_threshold"] = int(out["energy"] > 0.60)
    out["uncertainty_gate"] = int(out["energy"] + 0.35 * out["persistence"] > 0.78)
    out["causal_residual"] = int(causal_score(out) > 0.36)
    return out


def attenuate_shape_features(rows, gain):
    attenuated = []
    for row in rows:
        out = dict(row)
        for feature in SHAPE_FEATURES:
            out[feature] = round(max(0.0, min(1.0, out[feature] * gain)), 4)
        attenuated.append(rescore(out))
    return attenuated


def summarize(rows):
    out = []
    for gain in GAINS:
        m = metrics(attenuate_shape_features(rows, gain))["methods"]
        f1s = {
            "raw_threshold": m["raw_threshold"]["f1"],
            "uncertainty_gate": m["uncertainty_gate"]["f1"],
            "causal_residual": m["causal_residual"]["f1"],
        }
        winner = max(f1s, key=f1s.get)
        out.append(
            {
                "shape_feature_gain": gain,
                "raw_threshold_f1": m["raw_threshold"]["f1"],
                "uncertainty_gate_f1": m["uncertainty_gate"]["f1"],
                "causal_residual_f1": m["causal_residual"]["f1"],
                "causal_residual_accuracy": m["causal_residual"]["accuracy"],
                "winner": winner,
            }
        )
    return out


def tex_label(name):
    return {
        "raw_threshold": "Raw",
        "uncertainty_gate": "Uncertainty",
        "causal_residual": "Causal",
    }[name]


def write_outputs(rows):
    DOCS.mkdir(exist_ok=True)
    summary_path = DOCS / "v2_shape_calibration_stress.json"
    csv_path = DOCS / "v2_shape_calibration_stress.csv"
    table_path = PAPER / "v2_shape_calibration_table.tex"

    with summary_path.open("w", encoding="utf-8") as handle:
        json.dump(rows, handle, indent=2)
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        fieldnames = [
            "shape_feature_gain",
            "raw_threshold_f1",
            "uncertainty_gate_f1",
            "causal_residual_f1",
            "causal_residual_accuracy",
            "winner",
        ]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    table = (
        "\\begin{tabular}{lcccc}\n"
        "\\toprule\n"
        "Shape gain & Raw F1 & Uncertainty F1 & Causal F1 & Winner \\\\\n"
        "\\midrule\n"
        + "\n".join(
            f"{row['shape_feature_gain']:.2f} & "
            f"{row['raw_threshold_f1']:.3f} & "
            f"{row['uncertainty_gate_f1']:.3f} & "
            f"{row['causal_residual_f1']:.3f} & "
            f"{tex_label(row['winner'])} \\\\"
            for row in rows
        )
        + "\n\\bottomrule\n"
        "\\end{tabular}\n"
    )
    table_path.write_text(table, encoding="utf-8")


def main():
    rows = summarize(make_cases())
    write_outputs(rows)
    print(json.dumps(rows, indent=2))


if __name__ == "__main__":
    main()
