from __future__ import annotations

import base64
from html import escape
from pathlib import Path
from typing import Any

import streamlit as st

from .config import (
    FINAL_TABLE_COLUMNS,
    FLAG_FILES,
    GROUP_COLORS,
    LOGO_PATH,
    NEGATIVE_METRIC_LABELS,
    POSITIVE_METRIC_LABELS,
    STAGE_CONFIGS,
    TEAM_DISPLAY,
)
from .data import MetricResult, display_value, format_number, format_percent


@st.cache_data(show_spinner=False)
def image_to_base64(path_str: str) -> str:
    path = Path(path_str)
    return base64.b64encode(path.read_bytes()).decode("utf-8")


def inject_global_styles() -> None:
    st.markdown(
        """
        <style>
            :root {
                --bg: #0A0A0A;
                --panel: #121212;
                --panel-2: #171717;
                --line: #242424;
                --line-2: #2F2F2F;
                --text: #F6F6F6;
                --muted: #A4A4A4;
                --gold: #D4AF37;
                --silver: #C0C0C0;
                --bronze: #CD7F32;
            }
            .stApp {
                background: var(--bg);
            }
            [data-testid="stHeader"] {
                background: rgba(0, 0, 0, 0);
            }
            [data-testid="stSidebar"] {
                background: #0E0E0E;
                border-right: 1px solid #1A1A1A;
            }
            [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
            [data-testid="stSidebar"] label,
            [data-testid="stSidebar"] span {
                color: var(--text);
            }
            [data-testid="collapsedControl"] {
                color: var(--text);
            }
            #MainMenu, footer {
                visibility: hidden;
            }
            .block-container {
                padding-top: 1.5rem;
                padding-bottom: 2.5rem;
                max-width: 1400px;
            }
            .hero-card {
                display: flex;
                align-items: center;
                gap: 18px;
                padding: 18px 20px;
                background: linear-gradient(135deg, rgba(212, 175, 55, 0.12), rgba(18, 18, 18, 1) 40%, rgba(18, 18, 18, 1) 100%);
                border: 1px solid rgba(212, 175, 55, 0.22);
                border-radius: 24px;
                margin-bottom: 16px;
            }
            .hero-logo {
                width: 66px;
                height: 66px;
                object-fit: contain;
                flex-shrink: 0;
                border-radius: 16px;
            }
            .hero-title {
                font-size: 1.8rem;
                line-height: 1.15;
                color: var(--text);
                font-weight: 800;
                letter-spacing: 0.01em;
            }
            .section-heading {
                color: var(--text);
                font-size: 1.08rem;
                font-weight: 800;
                letter-spacing: 0.01em;
                margin: 22px 0 12px 0;
            }
            .kpi-grid,
            .ranking-grid,
            .group-grid,
            .stage-grid,
            .special-grid,
            .metric-grid,
            .podium-grid,
            .summary-grid {
                display: grid;
                gap: 14px;
            }
            .kpi-grid {
                grid-template-columns: repeat(2, minmax(0, 1fr));
                margin-bottom: 12px;
            }
            .podium-grid {
                grid-template-columns: 1fr 1.12fr 1fr;
                align-items: end;
                margin-bottom: 8px;
            }
            .ranking-grid,
            .stage-grid,
            .special-grid,
            .metric-grid,
            .summary-grid {
                grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
            }
            .group-grid {
                grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            }
            .panel,
            .kpi-card,
            .rank-card,
            .group-card,
            .choice-card,
            .special-card,
            .metric-card,
            .summary-card,
            .final-combo-card,
            .table-card,
            .mobile-record {
                background: var(--panel);
                border: 1px solid var(--line);
                border-radius: 22px;
                color: var(--text);
            }
            .kpi-card,
            .rank-card,
            .choice-card,
            .special-card,
            .metric-card,
            .summary-card,
            .final-combo-card,
            .mobile-record {
                padding: 16px;
            }
            .kpi-label,
            .rank-points,
            .group-headline,
            .choice-meta,
            .special-meta,
            .metric-value,
            .table-label,
            .table-cell-muted,
            .final-combo-meta,
            .group-col-header {
                color: var(--muted);
            }
            .kpi-value {
                font-size: 1.9rem;
                font-weight: 800;
                margin-top: 8px;
                color: var(--text);
            }
            .kpi-card {
                border-color: rgba(212, 175, 55, 0.20);
                background: linear-gradient(180deg, rgba(212, 175, 55, 0.08), rgba(18, 18, 18, 1));
            }
            .podium-card {
                position: relative;
                display: flex;
                flex-direction: column;
                justify-content: flex-end;
                border-radius: 24px;
                padding: 18px;
                min-height: 215px;
                background: linear-gradient(180deg, rgba(255,255,255,0.06), rgba(18,18,18,1));
                border: 1px solid var(--line);
            }
            .podium-card.first {
                min-height: 270px;
                border-color: rgba(212, 175, 55, 0.45);
                box-shadow: 0 0 0 1px rgba(212, 175, 55, 0.15) inset;
            }
            .podium-card.second {
                min-height: 230px;
                border-color: rgba(192, 192, 192, 0.34);
                box-shadow: 0 0 0 1px rgba(192, 192, 192, 0.12) inset;
            }
            .podium-card.third {
                min-height: 205px;
                border-color: rgba(205, 127, 50, 0.34);
                box-shadow: 0 0 0 1px rgba(205, 127, 50, 0.12) inset;
            }
            .podium-rank {
                position: absolute;
                top: 16px;
                left: 16px;
                font-size: 0.92rem;
                font-weight: 800;
                letter-spacing: 0.04em;
            }
            .podium-rank.first,
            .podium-points.first,
            .tone-gold {
                color: var(--gold);
            }
            .podium-rank.second,
            .podium-points.second,
            .tone-silver {
                color: var(--silver);
            }
            .podium-rank.third,
            .podium-points.third,
            .tone-bronze {
                color: var(--bronze);
            }
            .podium-name {
                font-size: 1.18rem;
                font-weight: 800;
                margin-top: 48px;
                color: var(--text);
                line-height: 1.2;
            }
            .podium-points {
                font-size: 2rem;
                font-weight: 900;
                margin-top: 12px;
                line-height: 1;
            }
            .podium-label,
            .rank-label {
                color: var(--muted);
                font-size: 0.8rem;
                margin-top: 6px;
            }
            .rank-card {
                display: flex;
                flex-direction: column;
                gap: 10px;
                min-height: 122px;
            }
            .rank-card.gold {
                border-color: rgba(212, 175, 55, 0.36);
                box-shadow: 0 0 0 1px rgba(212, 175, 55, 0.12) inset;
            }
            .rank-card.silver {
                border-color: rgba(192, 192, 192, 0.32);
                box-shadow: 0 0 0 1px rgba(192, 192, 192, 0.10) inset;
            }
            .rank-card.bronze {
                border-color: rgba(205, 127, 50, 0.32);
                box-shadow: 0 0 0 1px rgba(205, 127, 50, 0.10) inset;
            }
            .rank-topline {
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 12px;
            }
            .rank-position {
                display: inline-flex;
                align-items: center;
                justify-content: center;
                min-width: 38px;
                min-height: 38px;
                padding: 0 10px;
                border-radius: 999px;
                border: 1px solid var(--line-2);
                background: rgba(255,255,255,0.03);
                font-weight: 800;
                color: var(--text);
            }
            .rank-name,
            .choice-name,
            .metric-name,
            .summary-name {
                color: var(--text);
                font-weight: 800;
                line-height: 1.2;
            }
            .rank-total {
                font-size: 1.55rem;
                font-weight: 900;
                color: var(--text);
                line-height: 1;
            }
            .group-card {
                overflow: hidden;
            }
            .group-card-header {
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 12px;
                padding: 14px 16px;
                border-bottom: 1px solid rgba(255,255,255,0.06);
            }
            .group-title {
                font-size: 1rem;
                font-weight: 800;
                color: var(--text);
            }
            .group-card-body {
                padding: 10px 12px 12px 12px;
            }
            .group-grid-table {
                display: grid;
                gap: 8px;
            }
            .group-row,
            .group-row-head {
                display: grid;
                grid-template-columns: minmax(0, 1.8fr) repeat(3, minmax(56px, 0.7fr));
                gap: 10px;
                align-items: center;
            }
            .group-row-head {
                padding: 0 4px 4px 4px;
                font-size: 0.75rem;
                font-weight: 700;
                color: var(--muted);
            }
            .group-row {
                padding: 10px 10px;
                border-radius: 14px;
                background: rgba(255,255,255,0.03);
            }
            .group-match {
                color: var(--text);
                font-weight: 700;
                line-height: 1.2;
            }
            .group-cell {
                color: var(--text);
                font-weight: 800;
                text-align: center;
            }
            .choice-card,
            .special-card,
            .metric-card,
            .summary-card,
            .final-combo-card {
                display: flex;
                flex-direction: column;
                gap: 10px;
            }
            .choice-count,
            .metric-number,
            .summary-number {
                font-size: 1.55rem;
                font-weight: 900;
                line-height: 1;
                color: var(--text);
            }
            .choice-meta,
            .special-meta,
            .metric-value,
            .final-combo-meta,
            .summary-meta {
                font-size: 0.85rem;
                line-height: 1.25;
            }
            .special-label,
            .metric-label,
            .summary-label {
                color: var(--muted);
                font-size: 0.84rem;
                line-height: 1.25;
            }
            .special-main,
            .final-combo-main {
                color: var(--text);
                font-weight: 800;
                line-height: 1.2;
            }
            .flag-label {
                display: inline-flex;
                align-items: center;
                gap: 8px;
                color: var(--text);
                line-height: 1.2;
                vertical-align: middle;
            }
            .flag-label img {
                width: 22px;
                height: 15px;
                object-fit: cover;
                border-radius: 999px;
                flex-shrink: 0;
                box-shadow: 0 0 0 1px rgba(255,255,255,0.14) inset;
                background: rgba(255,255,255,0.04);
            }
            .flag-label.lg img {
                width: 26px;
                height: 18px;
            }
            .flag-pair {
                display: flex;
                flex-wrap: wrap;
                align-items: center;
                gap: 8px;
            }
            .pair-separator {
                color: var(--muted);
                font-weight: 700;
            }
            .plain-value {
                color: var(--text);
                font-weight: 800;
            }
            .summary-grid {
                margin-top: 8px;
            }
            .table-card {
                padding: 0;
                overflow: hidden;
            }
            .table-wrap {
                overflow-x: auto;
            }
            table.final-table {
                width: 100%;
                min-width: 1280px;
                border-collapse: collapse;
                color: var(--text);
            }
            table.final-table thead th {
                position: sticky;
                top: 0;
                background: #161616;
                color: var(--text);
                text-align: left;
                font-size: 0.84rem;
                font-weight: 800;
                padding: 14px 14px;
                border-bottom: 1px solid var(--line);
                white-space: nowrap;
            }
            table.final-table tbody td {
                padding: 13px 14px;
                border-bottom: 1px solid rgba(255,255,255,0.05);
                vertical-align: top;
                font-size: 0.92rem;
                line-height: 1.25;
            }
            table.final-table tbody tr:nth-child(even) {
                background: rgba(255,255,255,0.02);
            }
            .mobile-table {
                display: none;
                gap: 12px;
                padding: 14px;
            }
            .mobile-record {
                gap: 10px;
            }
            .mobile-head {
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 12px;
                padding-bottom: 10px;
                border-bottom: 1px solid rgba(255,255,255,0.06);
            }
            .mobile-title {
                color: var(--text);
                font-weight: 800;
                line-height: 1.2;
            }
            .mobile-rank {
                color: var(--gold);
                font-weight: 900;
                font-size: 1rem;
            }
            .mobile-body {
                display: grid;
                gap: 8px;
            }
            .mobile-field {
                display: grid;
                gap: 4px;
            }
            .mobile-label {
                color: var(--muted);
                font-size: 0.78rem;
            }
            .mobile-value {
                color: var(--text);
                line-height: 1.2;
            }
            @media (max-width: 900px) {
                .block-container {
                    padding-top: 1rem;
                }
                .hero-card {
                    padding: 16px;
                    border-radius: 20px;
                }
                .hero-logo {
                    width: 54px;
                    height: 54px;
                }
                .hero-title {
                    font-size: 1.35rem;
                }
                .kpi-grid,
                .podium-grid,
                .group-grid,
                .ranking-grid,
                .stage-grid,
                .special-grid,
                .metric-grid,
                .summary-grid {
                    grid-template-columns: 1fr;
                }
                .podium-card,
                .podium-card.first,
                .podium-card.second,
                .podium-card.third {
                    min-height: auto;
                }
                .group-row,
                .group-row-head {
                    grid-template-columns: minmax(0, 1.4fr) repeat(3, minmax(0, 0.65fr));
                    gap: 8px;
                }
                .table-wrap {
                    display: none;
                }
                .mobile-table {
                    display: grid;
                }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def hex_to_rgba(hex_color: str, alpha: float) -> str:
    hex_color = hex_color.lstrip("#")
    red = int(hex_color[0:2], 16)
    green = int(hex_color[2:4], 16)
    blue = int(hex_color[4:6], 16)
    return f"rgba({red}, {green}, {blue}, {alpha})"


def section_heading(title: str) -> None:
    st.markdown(f'<div class="section-heading">{escape(title)}</div>', unsafe_allow_html=True)


def team_display_name(team: str) -> str:
    return TEAM_DISPLAY.get(team, display_value(team))


def flag_label(team: str, size: str = "") -> str:
    if display_value(team) == "Pendiente":
        return '<span class="plain-value">Pendiente</span>'

    if team in FLAG_FILES and FLAG_FILES[team].exists():
        image_b64 = image_to_base64(str(FLAG_FILES[team]))
        display_name = escape(team_display_name(team))
        size_class = f" {size}" if size else ""
        return (
            f'<span class="flag-label{size_class}">' 
            f'<img src="data:image/png;base64,{image_b64}" alt="{display_name}">' 
            f'<span>{display_name}</span>'
            f'</span>'
        )
    return f'<span class="plain-value">{escape(team_display_name(team))}</span>'


def final_pair_html(pair: tuple[str, str]) -> str:
    first, second = pair
    return (
        '<div class="flag-pair">'
        f"{flag_label(first, 'lg')}"
        '<span class="pair-separator">-</span>'
        f"{flag_label(second, 'lg')}"
        '</div>'
    )


def render_header() -> None:
    logo_b64 = image_to_base64(str(LOGO_PATH))
    st.markdown(
        f"""
        <div class="hero-card">
            <img class="hero-logo" src="data:image/webp;base64,{logo_b64}" alt="Peñita FIFA World Cup 2026">
            <div class="hero-title">Peñita FIFA World Cup 2026</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_kpis(participant_count: int, prize_total: int) -> None:
    st.markdown(
        f"""
        <div class="kpi-grid">
            <div class="kpi-card">
                <div class="kpi-label">Nº de Participantes</div>
                <div class="kpi-value">{participant_count}</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Premio Total</div>
                <div class="kpi-value">{prize_total} €</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_podium(podium_rows: list[dict[str, Any]]) -> None:
    section_heading("Podio")
    ordered_positions = [
        (1, "first", podium_rows[0] if len(podium_rows) > 0 else None),
        (2, "second", podium_rows[1] if len(podium_rows) > 1 else None),
        (3, "third", podium_rows[2] if len(podium_rows) > 2 else None),
    ]
    display_order = [ordered_positions[1], ordered_positions[0], ordered_positions[2]]
    cards = []
    for position, css_class, row in display_order:
        name = escape(display_value(row["Participante"])) if row is not None else "Pendiente"
        points = format_number(row["TOTAL_PUNTOS"]) if row is not None else "Pendiente"
        cards.append(
            f"""
            <div class="podium-card {css_class}">
                <div class="podium-rank {css_class}">{position}º</div>
                <div class="podium-name">{name}</div>
                <div class="podium-points {css_class}">{points}</div>
                <div class="podium-label">TOTAL_PUNTOS</div>
            </div>
            """
        )
    st.markdown(f'<div class="podium-grid">{"".join(cards)}</div>', unsafe_allow_html=True)


def rank_card_class(position: int) -> str:
    if position == 1:
        return "gold"
    if position == 2:
        return "silver"
    if position == 3:
        return "bronze"
    return ""


def render_top10(top10_rows: list[dict[str, Any]]) -> None:
    section_heading("Top 10 del ranking total")
    cards = []
    for row in top10_rows:
        position = int(row["Posicion"])
        css_class = rank_card_class(position)
        cards.append(
            f"""
            <div class="rank-card {css_class}">
                <div class="rank-topline">
                    <div class="rank-position">{position}</div>
                    <div class="rank-total">{format_number(row['TOTAL_PUNTOS'])}</div>
                </div>
                <div class="rank-name">{escape(display_value(row['Participante']))}</div>
                <div class="rank-label">Puntos totales</div>
            </div>
            """
        )
    st.markdown(f'<div class="ranking-grid">{"".join(cards)}</div>', unsafe_allow_html=True)


def render_group_summaries(group_summaries: dict[str, list[dict[str, Any]]]) -> None:
    section_heading("Resumen por grupos: resultados más repetidos")
    group_cards = []
    for group_letter, rows in group_summaries.items():
        color = GROUP_COLORS[group_letter]
        bg_color = hex_to_rgba(color, 0.14)
        header_rows = [
            '<div class="group-row-head">'
            '<div class="group-col-header"></div>'
            '<div class="group-col-header">Resultado</div>'
            '<div class="group-col-header">1X2</div>'
            '<div class="group-col-header">DOB</div>'
            '</div>'
        ]
        body_rows = []
        for item in rows:
            match_html = (
                f"{flag_label(item['team_a'])}"
                '<span class="pair-separator">-</span>'
                f"{flag_label(item['team_b'])}"
            )
            double_value = f"{item['double_count']} · {format_percent(item['double_pct'])}"
            body_rows.append(
                f"""
                <div class="group-row">
                    <div class="group-match"><div class="flag-pair">{match_html}</div></div>
                    <div class="group-cell">{escape(display_value(item['result']))}</div>
                    <div class="group-cell">{escape(display_value(item['sign']))}</div>
                    <div class="group-cell">{double_value}</div>
                </div>
                """
            )
        group_cards.append(
            f"""
            <div class="group-card" style="border-color:{hex_to_rgba(color, 0.38)}; box-shadow: 0 0 0 1px {hex_to_rgba(color, 0.10)} inset;">
                <div class="group-card-header" style="background:{bg_color};">
                    <div class="group-title">Grupo {group_letter}</div>
                </div>
                <div class="group-card-body">
                    <div class="group-grid-table">
                        {''.join(header_rows)}
                        {''.join(body_rows)}
                    </div>
                </div>
            </div>
            """
        )
    st.markdown(f'<div class="group-grid">{"".join(group_cards)}</div>', unsafe_allow_html=True)


def render_stage_section(title: str, stage_rows: list[dict[str, Any]]) -> None:
    section_heading(title)
    cards = []
    for item in stage_rows:
        cards.append(
            f"""
            <div class="choice-card">
                <div class="choice-name">{flag_label(item['team'])}</div>
                <div class="choice-count">{item['count']}</div>
                <div class="choice-meta">{format_percent(item['pct'])}</div>
            </div>
            """
        )
    if not cards:
        cards.append('<div class="choice-card"><div class="choice-name">Pendiente</div></div>')
    st.markdown(f'<div class="stage-grid">{"".join(cards)}</div>', unsafe_allow_html=True)


def render_most_repeated_final(final_data: dict[str, Any] | None) -> None:
    section_heading("Final más repetida")
    if final_data is None:
        content = '<div class="final-combo-card"><div class="final-combo-main">Pendiente</div></div>'
    else:
        content = (
            '<div class="final-combo-card">'
            f'<div class="final-combo-main">{final_pair_html(final_data["pair"])}</div>'
            f'<div class="choice-count">{final_data["count"]}</div>'
            f'<div class="final-combo-meta">{format_percent(final_data["pct"])}'
            '</div>'
            '</div>'
        )
    st.markdown(content, unsafe_allow_html=True)


def render_summary_cards(title: str, items: list[dict[str, Any]]) -> None:
    section_heading(title)
    cards = []
    for item in items:
        cards.append(
            f"""
            <div class="summary-card">
                <div class="summary-label"></div>
                <div class="summary-name">{flag_label(item['team'])}</div>
                <div class="summary-number">{item['count']}</div>
                <div class="summary-meta">{format_percent(item['pct'])}</div>
            </div>
            """
        )
    if not cards:
        cards.append('<div class="summary-card"><div class="summary-name">Pendiente</div></div>')
    st.markdown(f'<div class="summary-grid">{"".join(cards)}</div>', unsafe_allow_html=True)


def render_specials(specials: list[dict[str, Any]]) -> None:
    section_heading("Especiales")
    cards = []
    for item in specials:
        if item["show_flag"]:
            main_value = flag_label(item["value"])
        else:
            main_value = f'<span class="plain-value">{escape(display_value(item["value"]))}</span>'
        cards.append(
            f"""
            <div class="special-card">
                <div class="special-label">{escape(item['label'])}</div>
                <div class="special-main">{main_value}</div>
                <div class="choice-count">{item['count']}</div>
                <div class="special-meta">{format_percent(item['pct'])}</div>
            </div>
            """
        )
    st.markdown(f'<div class="special-grid">{"".join(cards)}</div>', unsafe_allow_html=True)


def metric_card(label: str, metric: MetricResult) -> str:
    return (
        '<div class="metric-card">'
        f'<div class="metric-label">{escape(label)}</div>'
        f'<div class="metric-name">{escape(metric.participante)}</div>'
        f'<div class="metric-number">{metric.valor}</div>'
        '</div>'
    )


def render_metrics(metrics: dict[str, MetricResult]) -> None:
    section_heading("Tarjetas de métricas de acierto / rachas")
    html = (
        '<div class="metric-grid">'
        f'{metric_card(POSITIVE_METRIC_LABELS["best_streak"], metrics["best_streak"])}'
        f'{metric_card(POSITIVE_METRIC_LABELS["most_hits"], metrics["most_hits"])}'
        f'{metric_card(NEGATIVE_METRIC_LABELS["worst_streak"], metrics["worst_streak"])}'
        f'{metric_card(NEGATIVE_METRIC_LABELS["least_hits"], metrics["least_hits"])}'
        '</div>'
    )
    st.markdown(html, unsafe_allow_html=True)


def table_cell(value: str, column_name: str) -> str:
    if column_name in {"Campeon", "Subcampeon", "TercerPuesto"} and value != "Pendiente":
        return flag_label(value)
    return escape(value)


def render_final_table(records: list[dict[str, str]]) -> None:
    section_heading("Tabla final completa de participantes")
    header_html = "".join(f"<th>{escape(display_name)}</th>" for display_name, _ in FINAL_TABLE_COLUMNS)
    body_rows = []
    for record in records:
        cells = "".join(
            f"<td>{table_cell(record[column_name], column_name)}</td>"
            for _, column_name in FINAL_TABLE_COLUMNS
        )
        body_rows.append(f"<tr>{cells}</tr>")

    mobile_records = []
    for record in records:
        mobile_fields = []
        for display_name, column_name in FINAL_TABLE_COLUMNS[2:]:
            mobile_fields.append(
                f"""
                <div class="mobile-field">
                    <div class="mobile-label">{escape(display_name)}</div>
                    <div class="mobile-value">{table_cell(record[column_name], column_name)}</div>
                </div>
                """
            )
        mobile_records.append(
            f"""
            <div class="mobile-record">
                <div class="mobile-head">
                    <div class="mobile-rank">{escape(record['Posicion'])}</div>
                    <div class="mobile-title">{escape(record['Participante'])}</div>
                </div>
                <div class="mobile-body">
                    {''.join(mobile_fields)}
                </div>
            </div>
            """
        )

    st.markdown(
        f"""
        <div class="table-card">
            <div class="table-wrap">
                <table class="final-table">
                    <thead>
                        <tr>{header_html}</tr>
                    </thead>
                    <tbody>
                        {''.join(body_rows)}
                    </tbody>
                </table>
            </div>
            <div class="mobile-table">
                {''.join(mobile_records)}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_general_page(model: dict[str, Any]) -> None:
    render_header()
    render_kpis(model["participant_count"], model["prize_total"])
    render_podium(model["podium"])
    render_top10(model["top10"])
    render_group_summaries(model["group_summaries"])

    stage_count_lookup = model["stage_counts"]
    for title, prefix, _ in STAGE_CONFIGS:
        render_stage_section(title, stage_count_lookup.get(prefix, []))
        if prefix == "EquipoFinal":
            render_most_repeated_final(model["most_repeated_final"])

    render_summary_cards("Top 3 campeones más elegidos", model["champions"])
    render_summary_cards("Top 3 subcampeones más elegidos", model["subchampions"])
    render_summary_cards("Top 3 terceros puestos más elegidos", model["third_places"])
    render_specials(model["specials"])
    render_metrics(model["metrics"])
    render_final_table(model["final_table"])


def render_participant_shell() -> None:
    render_header()
    section_heading("Participante")
