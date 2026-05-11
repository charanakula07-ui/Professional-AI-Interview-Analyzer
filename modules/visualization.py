import plotly.graph_objects as go

def create_radar_chart(scores):

    categories = [
        "Confidence",
        "Communication",
        "Sentiment",
        "Overall"
    ]

    values = [
        scores["confidence"],
        scores["communication"],
        scores["sentiment"],
        scores["overall"]
    ]

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Interview Score'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        showlegend=False
    )

    return fig