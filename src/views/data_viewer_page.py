import streamlit as st
import pandas as pd
import os
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
from typing import List
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from database.database import (
    create_file_data,
    get_all_file_data,
    get_file_data_by_id,
    delete_file_data,
    clear_db,
)


def data_viewer_page() -> None:
    def create_plotly_graph(
        selected_id_list: List[int],
        split_index: int,
        x_col: str,
        y_col: str,
        graph_title: str,
    ) -> go.Figure:
        """グラフを作成して返す"""
        fig: go.Figure = make_subplots(
            rows=1, cols=1, shared_xaxes=True, vertical_spacing=0.08
        )

        for selected_id in selected_id_list:
            query_result = get_file_data_by_id(selected_id)
            file_path_temp = query_result["file_path"]
            df_temp: pd.DataFrame = pd.read_csv(file_path_temp)

            # ファイル名の抽出
            temp_name: str = os.path.basename(file_path_temp)
            file_name: str = temp_name.split("_")[split_index]
            fig.add_trace(
                go.Scatter(
                    x=df_temp[x_col], y=df_temp[y_col], name=file_name, opacity=0.6
                ),
                row=1,
                col=1,
            )

        # グラフのレイアウトを更新
        fig.update_layout(height=700, width=950)
        fig.update_layout(
            title=dict(
                text=graph_title,
                font=dict(size=20, color="grey"),
                x=0.45,
                xanchor="center",
            ),
            hovermode="x",
            legend=dict(
                xanchor="right",
                yanchor="bottom",
                x=1.25,
                y=0.35,
                orientation="v",
                bgcolor="white",
                bordercolor="grey",
                borderwidth=1,
            ),
        )
        return fig

    # --------------------------------------------------
    # main-component
    # --------------------------------------------------
    st.header("Data_viewer", divider="blue")

    tab1, tab2 = st.tabs(
        [
            ":file_folder: upload-csv",
            ":chart_with_upwards_trend: Chart",
        ]
    )

    with tab1:
        uploaded_csv_file = st.file_uploader(
            "Chose an csv...", type=["csv"], accept_multiple_files=False
        )

        with st.expander("ファイルの命名ルールについて", icon=":material/info:"):
            st.write("アップロードされるファイルは、")
            st.markdown(
                "**`{ファイルダウンロード日}_{カテゴリー}_{証券コード}.csv`** を想定しています。"
            )

        if uploaded_csv_file is not None:
            if st.button(
                "ファイルを保存",
                key="save_csv_data",
                type="primary",
                icon=":material/cloud_upload:",
            ):
                try:
                    # file 保存関係
                    uploaded_csv_file_name = uploaded_csv_file.name
                    df = pd.read_csv(uploaded_csv_file, encoding="utf-8")
                    DATA_PATH = st.session_state["data_path"]
                    csv_file_path = f"{DATA_PATH}/{uploaded_csv_file_name}"
                    df.to_csv(csv_file_path, index=False)

                    # DB　書き込み関係
                    parts = uploaded_csv_file_name.split("_")
                    category = parts[1]
                    ticker_code = parts[2]

                    # 最後の doc_id を取得して新しい id を決定
                    last_doc_id = (
                        max(get_all_file_data(), key=lambda x: x.doc_id)["id"]
                        if get_all_file_data()
                        else 0
                    )
                    new_id = last_doc_id + 1

                    new_data_dict = {
                        "id": new_id,
                        "file_name": uploaded_csv_file_name,
                        "category": category,
                        "ticker_code": ticker_code,
                        "file_path": (
                            csv_file_path if uploaded_csv_file is not None else None
                        ),
                    }
                    create_file_data(new_data_dict)
                    st.success("ファイルが正常に保存されました")

                except Exception as e:
                    st.error(f"ファイルの保存中にエラーが発生しました: {e}")

    with tab2:
        file_data_list = get_all_file_data()

        if len(file_data_list) == 0:
            pass
        else:
            df = pd.DataFrame(file_data_list)

            # AgGridの設定
            grid_builder = GridOptionsBuilder.from_dataframe(
                df,
                editable=False,
                filter=True,
                resizable=True,
                sortable=True,
            )
            grid_builder.configure_selection(
                selection_mode="multiple", use_checkbox=True
            )
            grid_builder.configure_side_bar(filters_panel=True, columns_panel=False)
            grid_builder.configure_default_column(
                enablePivot=True, enableValue=True, enableRowGroup=True
            )
            grid_builder.configure_grid_options(rowHeight=50)

            grid_options = grid_builder.build()
            grid_options["columnDefs"][0]["checkboxSelection"] = True

            response = AgGrid(
                df,
                gridOptions=grid_options,
                update_mode=GridUpdateMode.MODEL_CHANGED,
                theme="alpine",
            )

            # ユーザーが選択したデータ情報を取得
            selected_df = pd.DataFrame(response["selected_rows"])
            if not selected_df.empty:
                selected_id_list = selected_df["id"].tolist()
                st.session_state.selected_id_list = selected_id_list

        # checkboxを選択していない場合は空リストをセット
        if "selected_id_list" not in st.session_state:
            st.session_state.selected_id_list = []

        left_button, right_button = st.columns(2)

        if left_button.button(
            label="グラフ作成",
            key="make_plotly",
            type="primary",
            icon=":material/search:",
            use_container_width=True,
        ):
            if len(st.session_state.selected_id_list) == 0:
                st.toast("データを選択してください", icon="🚨")
            else:
                split_index: int = 2
                x_col: str = "Date"
                y_col: str = "Close"
                graph_title: str = "株価データの時間推移"

                fig1: go.Figure = create_plotly_graph(
                    st.session_state.selected_id_list,
                    split_index,
                    x_col,
                    y_col,
                    graph_title,
                )
                st.plotly_chart(fig1, use_container_width=True)

        if right_button.button(
            label="データの削除処理",
            key="delete_file_data",
            type="primary",
            icon=":material/delete:",
            use_container_width=True,
        ):
            if len(st.session_state.selected_id_list) == 0:
                st.toast("データを選択してください", icon="🚨")
            else:
                for selected_id in selected_id_list:
                    # file
                    try:
                        query_result = get_file_data_by_id(selected_id)
                        file_path_temp = query_result["file_path"]
                        if os.path.exists(file_path_temp):
                            os.remove(file_path_temp)
                            print(f"Deleted: {file_path_temp}")
                        else:
                            print(f"File not found: {file_path_temp}")
                    except Exception as e:
                        print(f"Error deleting file: {e}")

                    # DB
                    delete_file_data(selected_id)
                st.rerun()

        if st.button(
            label="画面リセット",
            key="somthing",
            type="primary",
        ):
            st.rerun()

        # if st.button(
        #     label="ClearDB",
        #     key="clearDB",
        #     type="primary",
        # ):
        #     clear_db()
        #     st.rerun()
