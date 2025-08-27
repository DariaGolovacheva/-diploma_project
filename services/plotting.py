# services/plotting.py
import matplotlib
matplotlib.use("Agg")   # важно для Flask + macOS
import matplotlib.pyplot as plt
import os

def plot_price(history_df, ticker: str, app_root_path: str):
    """
    Строит линейный график close price и сохраняет в static/plots/<ticker>_price.png.
    Возвращает относительный путь для вставки в HTML.
    """
    if history_df is None or history_df.empty:
        return None

    if 'Date' in history_df.columns:
        x = history_df['Date']
    else:
        x = history_df.index

    y = None
    for col in ['Close', 'close', 'Adj Close', 'adjclose']:
        if col in history_df.columns:
            y = history_df[col]
            break
    if y is None:
        return None

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(x, y)
    ax.set_title(f'{ticker} — Price')
    ax.set_xlabel('Date')
    ax.set_ylabel('Close Price')
    fig.autofmt_xdate()

    plots_dir = os.path.join(app_root_path, 'static', 'plots')
    os.makedirs(plots_dir, exist_ok=True)
    filename = f'{ticker}_price.png'
    filepath = os.path.join(plots_dir, filename)

    fig.savefig(filepath, bbox_inches='tight')
    plt.close(fig)

    return f'/static/plots/{filename}'
