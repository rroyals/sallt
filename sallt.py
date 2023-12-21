import flet as ft
import time
import json
from transaction import Transaction
import wallet as w

m_wallet = w.wallet()

SALLT_COLOR = "#118cf0"

POINTS_MAP = { }

POINTS = [ ]

def abbr_n(n):
    if n < 1_000:
        return str(n)
    elif n < 1_000_000:
        return f"{n / 1_000:.1f}k"
    elif n < 1_000_000_000:
        return f"{n / 1_000_000:.1f}m"
    elif n < 1_000_000_000_000:
        return f"{n // 1_000_000_000}b"
    else:
        return f"{n // 1_000_000_000_000}t"

def sample_partitions(lst, n_partitions):
        if len(lst) <= n_partitions:
            return lst
    
        step = len(lst) / n_partitions
        return [lst[int(i * step)] for i in range(n_partitions)]

class TimeChart(ft.UserControl):
    def __init__(self):
        self.data_points: list = []
        self.points: list = POINTS

        bot_labels = []
        left_labels = []
        partitioned_points = sample_partitions(POINTS, 10)
        for x, y in partitioned_points:
            cal = ft.ChartAxisLabel(
                    value=x,
                    label=ft.Container(
                        ft.Text(
                            str(POINTS_MAP.get(x)),
                            size=8,
                            color=ft.colors.with_opacity(0.75, ft.colors.WHITE),
                        ),
                        margin=ft.margin.only(top=10),
                    ),
                )
            lft = ft.ChartAxisLabel(
                    value=y,
                    label=ft.Text(
                            str(abbr_n(float(y))),
                            size=10,
                            color=ft.colors.with_opacity(0.75, ft.colors.WHITE),
                        )
                )
            bot_labels.append(cal)
            left_labels.append(lft)

        self.chart: ft.Control = ft.LineChart(
            tooltip_bgcolor=ft.colors.with_opacity(0.75, ft.colors.WHITE),
            expand=True,

            min_y=int(min(self.points, key=lambda y: y[1])[1]),
            max_y=int(max(self.points, key=lambda y: y[1])[1]),

            min_x=int(min(self.points, key=lambda x: x[0])[0]),
            max_x=int(max(self.points, key=lambda x: x[0])[0]),

            left_axis=ft.ChartAxis(labels=left_labels, labels_interval=1, labels_size=32),
            bottom_axis=ft.ChartAxis(labels=bot_labels),
        )

        self.line_chart: ft.Control = ft.LineChartData(
            color=SALLT_COLOR,
            stroke_width=2,
            curved=True,
            stroke_cap_round=True,
            below_line_gradient=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=[ft.colors.with_opacity(0.25, SALLT_COLOR),
                "transparent"],
            ),
        )

        super().__init__()

    def create_data_point(self, x, y):
        return ft.LineChartDataPoint(
            x,
            y,
            selected_below_line=ft.ChartPointLine(
                width=0.5,
                color="white54",
                dash_pattern=[2, 4],
            ),
            selected_point=ft.ChartCirclePoint(stroke_width=1),
        )

    def get_data_points(self):
        for x, y in self.points:
            self.data_points.append(self.create_data_point(x, y))
            self.chart.update()
            time.sleep(0.03)

    def build(self):
        self.line_chart.data_points = self.data_points
        self.chart.data_series = [self.line_chart]

        return ft.Column(
            horizontal_alignment="center",
            controls=[
                ft.Text(
                    f"Current Balance: {m_wallet.get_balance()} XRP",
                    size=16,
                    weight="bold",
                ),
                self.chart
            ],
        )

def main(page: ft.Page):
    page.title = "sallt"
    page.theme_mode = ft.ThemeMode.DARK

    img = ft.Image(
        src=f"https://i.ibb.co/jHyy4w6/sallt-text.png",
        width=200,
        height=100,
        fit=ft.ImageFit.COVER,
    )

    lv = ft.ListView(expand=True)
    
    txns = m_wallet.get_txn_history()

    def something_points(txns):
        partitioned_txns = sample_partitions(txns, 20)
        cur_balance = m_wallet.get_balance()
        after_balance = cur_balance
        idx = 19
        for i in range(len(partitioned_txns)):
            POINTS.append((idx, after_balance))
            POINTS_MAP[idx] = partitioned_txns[i].get_dt()[:-13]
            idx -= 1
            dir = partitioned_txns[i].get_txn_dir()
            if dir == "IN":
                after_balance -= partitioned_txns[i].get_amt()
            elif dir == "OUT":
                after_balance += partitioned_txns[i].get_amt()

    
    for i in range(len(txns)):
        if txns[i].get_txn_dir() == "OUT":
            subtitle = ft.Text(f"{txns[i].get_net_txn()} XRP", color=ft.colors.RED, size=16)
        elif txns[i].get_txn_dir() == "IN":
            subtitle = ft.Text(f"{txns[i].get_net_txn()} XRP", color=ft.colors.GREEN, size=16)
        exp = ft.ExpansionTile(
            bgcolor=SALLT_COLOR,
            title=ft.Text(f"{txns[i].get_txn_symb()} {txns[i].get_dt()}"),
            subtitle=subtitle,
            controls=[],
        )

        exp.controls.append(ft.ListTile(
            title=ft.Text(f"Info about transaction {i}\n{repr(txns[i])}"),
        ))

        lv.controls.append(exp)
        if not POINTS:
            something_points(txns)

    chart = TimeChart()
    if not txns:
        lv = ft.Text("Recent Transactions will be shown here.")
        chart = ft.Text(f"Current Balance: {m_wallet.get_balance()} XRP")#, size=16, weight="bold")


    tabs = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        tabs=[
            ft.Tab(
                text="Balance History",
                content=ft.Container(
                    padding=10,
                    content=chart, 
                    expand=True,
                    alignment=ft.alignment.center
                ),
            ),
            ft.Tab(
                text="Transaction History",
                content=ft.Container(
                    padding=5,
                    content=lv,
                    alignment=ft.alignment.center
                ),
            ),
            ft.Tab(
                text="Send",
                content=ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Container(
                                content=ft.TextField(label="Recipient Address", autofocus=True,
                                border_color=SALLT_COLOR, cursor_color=SALLT_COLOR),
                                padding=10,  # Add padding here
                            ),
                            ft.Container(
                                content=ft.TextField(label="Amount to Send",
                                border_color=SALLT_COLOR, cursor_color=SALLT_COLOR),
                                padding=10,  # Add padding here
                            ),
                            ft.ElevatedButton(
                                text="Send",
                                color=SALLT_COLOR,
                                on_click=lambda e: page.dialog(ft.Text("Transaction sent!"))
                            ),
                        ],
                        alignment=ft.alignment.center,
                        expand=1
                    ),
                    alignment=ft.alignment.center,
                    expand=1
                ),
            ),
        ],
        expand=1,
        indicator_color=SALLT_COLOR,
        label_color=SALLT_COLOR
    )

    page.add(img, tabs)
    page.update()

    if txns:
        chart.get_data_points()

ft.app(target=main)
