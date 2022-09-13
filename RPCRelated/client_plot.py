import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import io
from IPython.display import Image, display
import pandas as pd

def _show_img(img_bin):
    buf = io.BytesIO()
    buf.write(img_bin)
    buf.seek(0)
    plt.rcParams["figure.figsize"] = (10,10)
    image = mpimg.imread(buf)
    plt.axis('off')
    plt.imshow(image, aspect = 'equal')
    plt.show()
    buf.close()

def client_plot_countplot(client, col_label, df):
    img_bin = client.call("plot_countplot", (col_label, df))
    _show_img(img_bin)

def client_plot_hist(client, df):
    img_bin = client.call("plot_hist", df)
    _show_img(img_bin)

def client_plot_corr(client, df):
    corr_dict = client.call("plot_corr", df)
    corr_df = pd.DataFrame(data = corr_dict['data'], index = corr_dict['index'], columns = corr_dict['columns'])
    df_styled = corr_df.style.background_gradient(cmap='coolwarm',axis=None)
    display(df_styled)

def client_plot_miss(client, df):
    img_bin = client.call("plot_miss", df)
    _show_img(img_bin)