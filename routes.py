import requests
import pandas as pd
from flask import Flask, render_template
from bokeh.plotting import figure, show
from bokeh.embed import components
app=Flask(__name__)
# Bokeh tools
TOOLS = "resize,pan,wheel_zoom,box_zoom,reset,previewsave"

# Initialize the URL for dataset location
url_path = 'https://www.quandl.com/api/v3/datasets/USCENSUS/IE_7530.json?auth_token=W_c-rhUo457bjeN2xHgy'
session = requests.Session()
r = requests.get(url_path)
new_data = r.json()

column_names = new_data['dataset']['column_names']
inp_dataset = new_data['dataset']['data']
dframe = pd.DataFrame(inp_dataset, columns=column_names)
dframe.sort_index(ascending=True, inplace=True)

def make_figure():
     plot = figure(tools=TOOLS, width=750, height=450, title='United States Import/Exports',
              x_axis_label='date', x_axis_type='datetime')

     plot.line(dframe.index, dframe.get('Exports'), color='#A6CEE3', legend='Exports')
     return plot

@app.route("/")
def index():
    greetings = 'Hello World, I am BOKEH'
    plot = make_figure()
    script, div = components(plot)
    return render_template("index.html", greetings=greetings, script=script, div=div)

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug = True)
