from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Any

import pandas as pd
import streamlit as st

from .config import (
    DATA_PATH,
    EXACT_RESULT_POINTS,
    FINAL_TABLE_COLUMNS,
    GROUPS,
    MATCH_SIGN_POINTS,
    RANK_NUMERIC_COLUMNS,
    SPECIAL_FIELDS,
    STAGE_CONFIGS,
    TEAM_SPECIAL_FIELDS,
)


@dataclass
class MetricResult:
    participante: str
    valor: int
    total_puntos: float


@st.cache_data(show_spinner=False)
def load_dataframe(data_path: str | None = None) -> pd.DataFrame:
    path = data_path or str(DATA_PATH)
    return pd.read_csv(path)


def is_pending(value: Any) -> bool:
    if value is None:
        return True
    if pd.isna(value):
        return True
    if isinstance(value, str) and value.strip() == "":
        return True
    if str(value).strip().upper() == "PTE":
        return True
    return False


def display_value(value: Any) -> str:
    if is_pending(value):
        return "Pendiente"
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value)


def as_number(value: Any) -> float:
    if is_pending(value):
        return 0.0
    num = pd.to_numeric(pd.Series([value]), errors="coerce").iloc[0]
    if pd.isna(num):
        return 0.0
    return float(num)


def as_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if is_pending(value):
        return False
    normalized = str(value).strip().upper()
    return normalized in {"TRUE", "1", "SI", "SÍ", "YES"}


def format_number(value: Any) -> str:
    number = as_number(value)
    if float(number).is_integer():
        return str(int(number))
    return f"{number:.1f}"


def format_percent(value: float) -> str:
    if float(value).is_integer():
        return f"{int(value)}%"
    return f"{value:.1f}%"


def sort_ranking(df: pd.DataFrame) -> pd.DataFrame:
    ranked = df.copy()
    for col in RANK_NUMERIC_COLUMNS:
        ranked[col] = pd.to_numeric(ranked[col], errors="coerce").fillna(0)
    ranked = ranked.sort_values(["TOTAL_PUNTOS", "Participante"], ascending=[False, True]).reset_index(drop=True)
    ranked.insert(0, "Posicion", range(1, len(ranked) + 1))
    return ranked


def get_match_keys(df: pd.DataFrame) -> list[str]:
    return [col[:-4] for col in df.columns if col.endswith("_RTO")]


def get_group_match_map(match_keys: list[str]) -> dict[str, list[str]]:
    group_letters = list(GROUPS.keys())
    return {group: match_keys[index * 6:(index + 1) * 6] for index, group in enumerate(group_letters)}


def split_match_key(match_key: str, group_letter: str) -> tuple[str, str]:
    teams = GROUPS[group_letter]
    for team_a in teams:
        for team_b in teams:
            if team_a != team_b and f"{team_a}{team_b}" == match_key:
                return team_a, team_b
    return match_key, ""


def get_mode_with_count(values: list[Any], pending_label: str = "Pendiente") -> tuple[str, int]:
    cleaned = [display_value(value) for value in values if not is_pending(value)]
    if not cleaned:
        return pending_label, 0
    counts = Counter(cleaned)
    most_common_count = max(counts.values())
    winner = sorted([item for item, count in counts.items() if count == most_common_count])[0]
    return winner, most_common_count


def build_group_summaries(df: pd.DataFrame) -> dict[str, list[dict[str, Any]]]:
    match_keys = get_match_keys(df)
    grouped = get_group_match_map(match_keys)
    summary: dict[str, list[dict[str, Any]]] = {}
    total_participants = len(df)

    for group_letter, matches in grouped.items():
        group_rows: list[dict[str, Any]] = []
        for match_key in matches:
            result_value, result_count = get_mode_with_count(df[f"{match_key}_RTO"].tolist())
            sign_value, sign_count = get_mode_with_count(df[f"{match_key}_1X2"].tolist())
            double_count = int(df[f"{match_key}_DOB"].apply(as_bool).sum())
            team_a, team_b = split_match_key(match_key, group_letter)
            group_rows.append(
                {
                    "match_key": match_key,
                    "team_a": team_a,
                    "team_b": team_b,
                    "result": result_value,
                    "result_count": result_count,
                    "sign": sign_value,
                    "sign_count": sign_count,
                    "double_count": double_count,
                    "double_pct": (double_count / total_participants * 100) if total_participants else 0.0,
                }
            )
        summary[group_letter] = group_rows
    return summary


def build_stage_counts(df: pd.DataFrame) -> dict[str, list[dict[str, Any]]]:
    participant_count = len(df)
    results: dict[str, list[dict[str, Any]]] = {}

    for _, prefix, stage_slots in STAGE_CONFIGS:
        stage_columns = [col for col in df.columns if col.startswith(f"{prefix}_") and not col.endswith("_PTOS")]
        values = []
        for column in stage_columns:
            values.extend([display_value(value) for value in df[column].tolist() if not is_pending(value)])
        counts = Counter(values)
        stage_rows = [
            {
                "team": team,
                "count": count,
                "pct": (count / participant_count * 100) if participant_count else 0.0,
            }
            for team, count in sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:stage_slots]
        ]
        results[prefix] = stage_rows
    return results


def build_most_repeated_final(df: pd.DataFrame) -> dict[str, Any] | None:
    if "EquipoFinal_1" not in df.columns or "EquipoFinal_2" not in df.columns:
        return None
    participant_count = len(df)
    counter: Counter[tuple[str, str]] = Counter()
    for _, row in df.iterrows():
        first = row.get("EquipoFinal_1")
        second = row.get("EquipoFinal_2")
        if is_pending(first) or is_pending(second):
            continue
        pair = tuple(sorted([display_value(first), display_value(second)]))
        counter[pair] += 1
    if not counter:
        return None
    pair, count = sorted(counter.items(), key=lambda item: (-item[1], item[0]))[0]
    return {
        "pair": pair,
        "count": count,
        "pct": (count / participant_count * 100) if participant_count else 0.0,
    }


def build_top_choices(df: pd.DataFrame, column_name: str, top_n: int = 3) -> list[dict[str, Any]]:
    participant_count = len(df)
    values = [display_value(value) for value in df[column_name].tolist() if not is_pending(value)]
    counts = Counter(values)
    return [
        {
            "team": team,
            "count": count,
            "pct": (count / participant_count * 100) if participant_count else 0.0,
        }
        for team, count in sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:top_n]
    ]


def minute_range_label(value: Any) -> str:
    if is_pending(value):
        return "Pendiente"
    minute = pd.to_numeric(pd.Series([value]), errors="coerce").iloc[0]
    if pd.isna(minute):
        return display_value(value)
    minute_int = int(minute)
    start = (minute_int // 10) * 10
    end = start + 9
    return f"{start}–{end}"


def build_specials(df: pd.DataFrame) -> list[dict[str, Any]]:
    participant_count = len(df)
    specials: list[dict[str, Any]] = []

    for column_name, label in SPECIAL_FIELDS:
        raw_values = df[column_name].tolist()
        if column_name == "MinutoPrimerGol":
            transformed = [minute_range_label(value) for value in raw_values if not is_pending(value)]
        else:
            transformed = [display_value(value) for value in raw_values if not is_pending(value)]

        if transformed:
            counts = Counter(transformed)
            count = max(counts.values())
            value = sorted([item for item, current_count in counts.items() if current_count == count])[0]
        else:
            value, count = "Pendiente", 0

        specials.append(
            {
                "field": column_name,
                "label": label,
                "value": value,
                "count": count,
                "pct": (count / participant_count * 100) if participant_count else 0.0,
                "show_flag": column_name in TEAM_SPECIAL_FIELDS,
            }
        )
    return specials


def participant_exact_sequence(row: pd.Series, match_keys: list[str]) -> list[bool]:
    sequence: list[bool] = []
    for match_key in match_keys:
        value = row.get(f"{match_key}_PTOS")
        if is_pending(value):
            continue
        numeric_value = as_number(value)
        if numeric_value in EXACT_RESULT_POINTS:
            sequence.append(True)
        elif numeric_value in MATCH_SIGN_POINTS or numeric_value == 0:
            sequence.append(False)
    return sequence


def longest_run(sequence: list[bool], target: bool) -> int:
    best = 0
    current = 0
    for item in sequence:
        if item is target:
            current += 1
            best = max(best, current)
        else:
            current = 0
    return best


def build_result_metrics(ranking_df: pd.DataFrame, match_keys: list[str]) -> dict[str, MetricResult]:
    rows = []
    for _, row in ranking_df.iterrows():
        sequence = participant_exact_sequence(row, match_keys)
        exact_hits = sum(sequence)
        best_streak = longest_run(sequence, True)
        worst_streak = longest_run(sequence, False)
        rows.append(
            {
                "Participante": row["Participante"],
                "TOTAL_PUNTOS": as_number(row["TOTAL_PUNTOS"]),
                "best_streak": best_streak,
                "most_hits": exact_hits,
                "worst_streak": worst_streak,
                "least_hits": exact_hits,
            }
        )

    metrics_df = pd.DataFrame(rows)
    best_streak_row = metrics_df.sort_values(["best_streak", "TOTAL_PUNTOS", "Participante"], ascending=[False, False, True]).iloc[0]
    most_hits_row = metrics_df.sort_values(["most_hits", "TOTAL_PUNTOS", "Participante"], ascending=[False, False, True]).iloc[0]
    worst_streak_row = metrics_df.sort_values(["worst_streak", "TOTAL_PUNTOS", "Participante"], ascending=[False, True, True]).iloc[0]
    least_hits_row = metrics_df.sort_values(["least_hits", "TOTAL_PUNTOS", "Participante"], ascending=[True, True, True]).iloc[0]

    return {
        "best_streak": MetricResult(best_streak_row["Participante"], int(best_streak_row["best_streak"]), float(best_streak_row["TOTAL_PUNTOS"])),
        "most_hits": MetricResult(most_hits_row["Participante"], int(most_hits_row["most_hits"]), float(most_hits_row["TOTAL_PUNTOS"])),
        "worst_streak": MetricResult(worst_streak_row["Participante"], int(worst_streak_row["worst_streak"]), float(worst_streak_row["TOTAL_PUNTOS"])),
        "least_hits": MetricResult(least_hits_row["Participante"], int(least_hits_row["least_hits"]), float(least_hits_row["TOTAL_PUNTOS"])),
    }


def build_final_table_records(ranking_df: pd.DataFrame) -> list[dict[str, str]]:
    records: list[dict[str, str]] = []
    for _, row in ranking_df.iterrows():
        current = {}
        for display_name, column_name in FINAL_TABLE_COLUMNS:
            current[column_name] = display_value(row.get(column_name))
        records.append(current)
    return records


def build_general_view_model(df: pd.DataFrame) -> dict[str, Any]:
    ranking_df = sort_ranking(df)
    match_keys = get_match_keys(df)

    return {
        "participant_count": len(ranking_df),
        "prize_total": len(ranking_df) * 20,
        "ranking_df": ranking_df,
        "top10": ranking_df.head(10).to_dict("records"),
        "podium": ranking_df.head(3).to_dict("records"),
        "group_summaries": build_group_summaries(df),
        "stage_counts": build_stage_counts(df),
        "most_repeated_final": build_most_repeated_final(df),
        "champions": build_top_choices(df, "Campeon"),
        "subchampions": build_top_choices(df, "Subcampeon"),
        "third_places": build_top_choices(df, "TercerPuesto"),
        "specials": build_specials(df),
        "metrics": build_result_metrics(ranking_df, match_keys),
        "final_table": build_final_table_records(ranking_df),
        "match_keys": match_keys,
    }
